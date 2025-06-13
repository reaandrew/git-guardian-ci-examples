# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

This repository demonstrates GitGuardian integration in CI/CD workflows to prevent secrets from entering codebases. It's designed as a template/example for teams implementing robust secret detection and automated release processes.

## Development Commands

### Local Environment Setup
```bash
# Create and activate Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install pre-commit
pip install pre-commit

# Install git hook scripts
pre-commit install
pre-commit install --hook-type commit-msg
```

### Testing and Validation
```bash
# ALWAYS activate virtual environment first
source venv/bin/activate

# Install project dependencies including dev tools
pip install -e ".[dev]"

# Run all pre-commit hooks on all files
pre-commit run --all-files

# Test GitGuardian scanning specifically
ggshield secret scan pre-commit

# Run conventional commit validation
pre-commit run conventional-pre-commit --hook-stage commit-msg

# Run tests with coverage manually
python -m pytest --cov=src --cov-report=term-missing --cov-fail-under=80

# Run only the coverage test hook
pre-commit run pytest --all-files
```

### Release Process
- Releases are fully automated via semantic-release
- Push to `main` branch triggers automatic versioning and GitHub release
- No manual intervention required for releases

## Architecture

### Core Components

**Security Pipeline**: Multi-layer validation
1. **Local pre-commit**: GitGuardian ggshield scanning before commits (detects secrets in staged changes)
2. **Test coverage enforcement**: Blocks commits with <80% code coverage
3. **CI pre-commit job**: Re-runs all hooks including GitGuardian and tests
4. **CI GitGuardian full scan**: Scans entire repository to catch commits that bypassed pre-commit (e.g., --no-verify)
5. **Conventional commits**: Enforced format for automated versioning

**CI/CD Workflow**: Five sequential jobs
1. **lint-and-test**: Runs all quality checks, secret scanning, and tests with coverage
2. **gitguardian-scan**: Full repository secret scanning with ggshield (catches bypassed commits)
3. **sonarcloud**: Code quality analysis with quality gate enforcement
4. **build**: Basic validation and repository information
5. **release**: Semantic versioning and GitHub release (main branch only)

**Automated Versioning**: Uses conventional commits to determine version bumps
- `feat:` → minor version (0.1.0 → 0.2.0)
- `fix:` → patch version (0.1.0 → 0.1.1)
- `feat!:` or `BREAKING CHANGE:` → major version (0.1.0 → 1.0.0)

### Key Configuration Files

- `.pre-commit-config.yaml`: Defines all pre-commit hooks including GitGuardian and pytest
- `pytest-precommit.ini`: Pytest configuration for test execution
- `.coveragerc`: Coverage.py configuration with 80% threshold and temp file redirection
- `pyproject.toml`: Main project configuration with dependencies and test settings
- `.releaserc.json`: Semantic-release configuration for automated versioning
- `.github/workflows/ci.yml`: Complete CI/CD pipeline definition
- `sonar-project.properties`: SonarCloud analysis configuration

## Environment Requirements

**Required Environment Variables**:
- `GITGUARDIAN_API_KEY`: For local GitGuardian scanning (get from GitGuardian Dashboard)
- `GIT_GUARDIAN_API_KEY`: GitHub secret for CI/CD pipeline
- `SONAR_TOKEN`: GitHub secret for SonarCloud integration

**Python Environment**: Always activate the virtual environment (`source venv/bin/activate`) when working locally.

## Test Coverage Enforcement

This repository enforces a minimum 80% test coverage threshold at multiple levels:

### Pre-commit Coverage Validation

The pre-commit hook automatically runs tests with coverage and blocks commits that fall below 80%:

```bash
# Hook configuration uses:
python -B -m pytest -c pytest-precommit.ini -p no:cacheprovider

# Key features:
- Uses pytest-precommit.ini for clean configuration
- Generates no cache files (prevents "files modified" errors)
- Stores coverage data in /tmp to avoid working tree modifications
- Fails fast on insufficient coverage
```

### Coverage Configuration

**.coveragerc**:
- `data_file = /tmp/.coverage_precommit` (prevents repo file modifications)
- `fail_under = 80` (enforces minimum coverage threshold)
- `source = src` and `branch = true` for comprehensive coverage
- Excludes common patterns (pragma: no cover, __repr__, etc.)

**pytest-precommit.ini**:
- `[pytest]` section header (required for .ini files)
- `addopts = --cov=src --cov-report=term-missing --cov-fail-under=80`
- Simplified since coverage.py reads configuration from .coveragerc

**pyproject.toml**:
- Main project dependencies and test settings
- Alternative location for coverage config (uses `[tool.coverage.run]` section)

### Testing Commands

```bash
# Run tests with coverage (local development)
python -m pytest --cov=src --cov-report=term-missing --cov-fail-under=80

# Test the pre-commit hook specifically
pre-commit run pytest --all-files

# Run all pre-commit hooks (includes coverage check)
pre-commit run --all-files
```

### Coverage Troubleshooting

**Common Issues**:
- **Low coverage**: Add tests for uncovered code paths
- **"Files modified" error**: Coverage.py only reads config from .coveragerc, setup.cfg, or pyproject.toml
- **CI vs local differences**: Ensure .coveragerc data_file redirects to /tmp to avoid repo modifications

**Coverage Requirements**:
- Minimum 80% total coverage required for commits
- Branch coverage enabled for comprehensive testing
- Both local pre-commit and CI enforce the same threshold

## SonarCloud Quality Gate Troubleshooting

When the SonarCloud stage fails, the CI pipeline includes a detailed quality gate status check that shows:

### Checking Quality Gate Failures

The CI workflow automatically polls the SonarCloud API and displays detailed failure information:

```bash
# Example output when quality gate fails:
Quality Gate Status: ERROR
Quality Gate failed for the following reasons:
- coverage: 45.2 is less than 80
- duplicated_lines_density: 15.3 is greater than 3
- code_smells: 12 is greater than 0
```

### Common Quality Gate Conditions

**Coverage Requirements**:
- New code coverage must be ≥ 80%
- Overall coverage should meet project standards

**Code Quality Metrics**:
- Duplicated lines density should be < 3%
- Code smells should be minimized
- Security hotspots must be reviewed
- Maintainability rating should be A

**Debugging SonarCloud Issues**:
1. **Check CI logs**: Look for the "Check Quality Gate Status" step output
2. **Review metrics**: Each failed condition shows actual vs expected values
3. **Fix systematically**: Address each condition individually
4. **Re-run analysis**: Push changes to trigger new SonarCloud scan

### Manual SonarCloud API Check

If needed, you can manually check quality gate status:

```bash
# Get project status
curl -s -u "$SONAR_TOKEN:" \
  "https://sonarcloud.io/api/qualitygates/project_status?projectKey=reaandrew_acronymcreator"
```

## GitGuardian Secret Detection

This repository implements comprehensive secret detection at multiple levels to prevent credentials from entering the codebase.

### Pre-commit Secret Scanning

**Local Protection**: GitGuardian ggshield runs on every commit attempt
- Scans **staged changes only** (files being committed)
- Detects API keys, tokens, passwords, certificates, and other secrets
- Blocks commit if secrets are found
- Part of the pre-commit hook chain that also includes linting and tests

### CI Full Repository Scanning

**Comprehensive Protection**: Dedicated GitGuardian stage in CI pipeline
- Scans **entire repository** using `ggshield secret scan path . --recursive`
- Catches commits that bypassed pre-commit hooks (e.g., using `--no-verify`)
- Runs on all branches and pull requests for comprehensive coverage
- Excludes `.git/**` directory to avoid false positives from temporary CI credentials

### Two-Layer Security Model

1. **Prevention**: Pre-commit hooks stop secrets at commit time
2. **Detection**: CI scanning catches any secrets that slip through

This dual approach ensures secrets cannot enter the repository through normal development workflows or emergency bypasses.

### GitGuardian Configuration

**Pre-commit Hook**:
```yaml
- repo: https://github.com/gitguardian/ggshield
  hooks:
    - id: ggshield
      name: GitGuardian Shield
```

**CI Stage**:
```yaml
gitguardian-scan:
  name: GitGuardian Full Repository Scan
  steps:
    - name: Install ggshield
      run: pip install ggshield
    - name: GitGuardian scan all files
      run: ggshield secret scan path . --recursive --yes --exclude ".git/**"
```

## Commit Conventions

This repository enforces conventional commit format via pre-commit hooks:
- `feat:` `fix:` `docs:` `style:` `refactor:` `test:` `build:` `ci:` `chore:` `revert:`

Commits that don't follow this format will be rejected by the commit-msg hook.

Commit messages must only contain content which is relevant to the changes made
