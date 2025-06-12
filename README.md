# Acronym Creator

A robust Python CLI tool demonstrating comprehensive CI/CD best practices, security controls, and automated quality gates.

## Purpose

This repository serves as a template/example for teams implementing secure development workflows with:
- **Multi-layer secret detection** using GitGuardian
- **Automated test coverage enforcement** (80% minimum threshold)
- **Code quality analysis** with SonarCloud integration
- **Automated semantic versioning** and release management

The project includes a functional acronym generation CLI built with Click and comprehensive test coverage.

## Features

### 🔒 Security & Quality Controls
- **GitGuardian Secret Scanning**: Three-layer protection (local pre-commit, CI, and SonarCloud)
- **Test Coverage Enforcement**: Commits blocked if coverage drops below 80%
- **Code Quality Gates**: SonarCloud analysis with quality gate enforcement
- **Conventional Commits**: Automated commit message validation
- **Automated Dependency Scanning**: Pre-commit hooks for security validation

### 🚀 CI/CD Pipeline
- **Four-stage pipeline**: lint-and-test → sonarcloud → build → release
- **Semantic Versioning**: Automatic version bumps based on conventional commits
- **GitHub Releases**: Automated changelog generation and release publishing
- **Quality Gates**: Pipeline fails if any quality standard is not met

### 🧪 Python Package
- **Click CLI Framework**: Professional command-line interface
- **Comprehensive Testing**: Unit tests with pytest and coverage reporting
- **Package Structure**: Standard Python package with entry points
- **Development Tools**: Pre-commit hooks, linting, and type checking

## Quick Start

### 1. Local Development Setup

```bash
# Create and activate Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install the package with development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
pre-commit install --hook-type commit-msg

# Test the CLI
acronymcreator "Hello World"  # Output: HW
```

### 2. Running Tests

```bash
# ALWAYS activate virtual environment first
source venv/bin/activate

# Run tests with coverage (must maintain 80% minimum)
python -m pytest --cov=src --cov-report=term-missing --cov-fail-under=80

# Run all pre-commit hooks (includes coverage check)
pre-commit run --all-files

# Test only the coverage hook
pre-commit run pytest --all-files
```

### 3. Development Workflow

```bash
# Make your changes
git add .

# Commit with conventional format (triggers all quality checks)
git commit -m "feat: add new acronym generation feature"

# Push to trigger CI pipeline
git push
```

The pre-commit hooks will automatically:
- ✅ Run tests with coverage enforcement (80% minimum)
- ✅ Scan for secrets with GitGuardian
- ✅ Validate conventional commit format
- ✅ Fix formatting and lint issues
- ❌ Block the commit if any check fails

## Architecture Overview

### Multi-Layer Security Pipeline

```mermaid
graph LR
    A[Developer Commit] --> B[Pre-commit Hooks]
    B --> C[GitGuardian Scan]
    B --> D[Test Coverage Check]
    B --> E[Conventional Commit Check]
    B --> F[Code Formatting]
    F --> G[CI Pipeline]
    G --> H[SonarCloud Analysis]
    H --> I[Automated Release]
```

**Layer 1 - Local Pre-commit**:
- GitGuardian secret scanning
- Test coverage enforcement (80% minimum)
- Conventional commit validation
- Code formatting and linting

**Layer 2 - CI Pipeline**:
- Re-runs all pre-commit checks in clean environment
- Generates coverage reports for SonarCloud
- Validates build and package integrity

**Layer 3 - SonarCloud Quality Gate**:
- Code quality analysis
- Security vulnerability detection
- Coverage verification
- Technical debt assessment

**Layer 4 - Automated Release**:
- Semantic version calculation
- Changelog generation
- GitHub release creation
- Package publishing (when configured)

## Configuration Files

### Key Configuration Files

| File | Purpose |
|------|---------|
| `.pre-commit-config.yaml` | Pre-commit hooks including GitGuardian and pytest |
| `pytest-precommit.ini` | Pytest configuration for test execution |
| `.coveragerc` | Coverage.py configuration with 80% threshold |
| `pyproject.toml` | Python package configuration and dependencies |
| `.github/workflows/ci.yml` | Complete CI/CD pipeline definition |
| `.releaserc.json` | Semantic-release configuration |
| `sonar-project.properties` | SonarCloud analysis configuration |

### Environment Variables

**Local Development**:
```bash
# Required for GitGuardian secret scanning
export GITGUARDIAN_API_KEY=your_api_key_here
```

**CI/CD Secrets** (configured in GitHub repository settings):
- `GIT_GUARDIAN_API_KEY`: GitGuardian API key for CI pipeline
- `SONAR_TOKEN`: SonarCloud integration token

## Test Coverage Enforcement

This repository enforces **80% minimum test coverage** at multiple levels:

### Pre-commit Hook
- Automatically runs on every commit attempt
- Uses `python -B -m pytest -c pytest-precommit.ini -p no:cacheprovider`
- Blocks commits if coverage drops below 80%
- Generates no cache files to avoid "files modified" errors

### Configuration
- **`.coveragerc`**: Main coverage configuration with `data_file = /tmp/.coverage_precommit`
- **Branch coverage enabled**: Comprehensive testing of all code paths
- **Exclusion patterns**: Common patterns like `pragma: no cover`, `__repr__`, etc.

### Testing Commands
```bash
# Run tests with coverage manually
python -m pytest --cov=src --cov-report=term-missing --cov-fail-under=80

# Test the pre-commit hook
pre-commit run pytest --all-files
```

## Semantic Versioning & Releases

Fully automated versioning based on [Conventional Commits](https://www.conventionalcommits.org/):

| Commit Type | Version Bump | Example |
|-------------|--------------|---------|
| `feat:` | Minor | 1.0.0 → 1.1.0 |
| `fix:` | Patch | 1.0.0 → 1.0.1 |
| `feat!:` or `BREAKING CHANGE:` | Major | 1.0.0 → 2.0.0 |
| `docs:`, `style:`, `refactor:`, `test:`, `chore:` | None | No release |

**Release Process**:
1. Push to `main` branch triggers semantic-release
2. Analyzes commits since last release
3. Calculates next version number
4. Generates changelog
5. Creates GitHub release with git tag

## CLI Usage

The acronym generator CLI provides several options:

```bash
# Basic usage
acronymcreator "Hello World"                    # Output: HW

# Include articles and common words
acronymcreator "The Quick Brown Fox" --include-articles  # Output: TQBF

# Lowercase output
acronymcreator "Hello World" --lowercase         # Output: hw

# Get help
acronymcreator --help

# Check version
acronymcreator --version
```

## Troubleshooting

### Common Issues

**Coverage Below 80%**:
```bash
# Add tests for uncovered code paths
# Check coverage report for missing lines
python -m pytest --cov=src --cov-report=html
open htmlcov/index.html
```

**Pre-commit Hook Failures**:
```bash
# Re-run hooks after fixing issues
pre-commit run --all-files

# Update hook dependencies
pre-commit autoupdate
```

**GitGuardian API Issues**:
```bash
# Test GitGuardian scanning specifically
ggshield secret scan pre-commit

# Check API key is set
echo $GITGUARDIAN_API_KEY
```

### Pipeline Debugging

**SonarCloud Quality Gate Failures**:
- Check the "Check Quality Gate Status" step in CI logs
- Review detailed metrics for failed conditions
- Fix issues systematically and re-run analysis

**Semantic Release Issues**:
- Ensure commit messages follow conventional format
- Check repository URL matches in `.releaserc.json`
- Verify GitHub token permissions for releases

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/new-feature`
3. Make changes with proper test coverage (≥80%)
4. Commit using conventional format: `git commit -m "feat: add new feature"`
5. Push and create a pull request
6. All quality gates must pass before merge

## License

MIT License - see [LICENSE](LICENSE) file for details.
