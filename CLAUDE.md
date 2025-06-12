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

# Run all pre-commit hooks on all files
pre-commit run --all-files

# Test GitGuardian scanning specifically
ggshield secret scan pre-commit

# Run conventional commit validation
pre-commit run conventional-pre-commit --hook-stage commit-msg
```

### Release Process
- Releases are fully automated via semantic-release
- Push to `main` branch triggers automatic versioning and GitHub release
- No manual intervention required for releases

## Architecture

### Core Components

**Security Pipeline**: Three-layer secret detection
1. **Local pre-commit**: GitGuardian ggshield scanning before commits
2. **CI pre-commit job**: Re-runs all hooks including GitGuardian
3. **Conventional commits**: Enforced format for automated versioning

**CI/CD Workflow**: Three sequential jobs
1. **pre-commit**: Runs all quality checks and secret scanning
2. **build**: Basic validation and repository information
3. **release**: Semantic versioning and GitHub release (main branch only)

**Automated Versioning**: Uses conventional commits to determine version bumps
- `feat:` → minor version (0.1.0 → 0.2.0)
- `fix:` → patch version (0.1.0 → 0.1.1)
- `feat!:` or `BREAKING CHANGE:` → major version (0.1.0 → 1.0.0)

### Key Configuration Files

- `.pre-commit-config.yaml`: Defines all pre-commit hooks including GitGuardian
- `.releaserc.json`: Semantic-release configuration for automated versioning
- `.github/workflows/ci.yml`: Complete CI/CD pipeline definition

## Environment Requirements

**Required Environment Variables**:
- `GITGUARDIAN_API_KEY`: For local GitGuardian scanning (get from GitGuardian Dashboard)
- `GIT_GUARDIAN_API_KEY`: GitHub secret for CI/CD pipeline

**Python Environment**: Always activate the virtual environment (`source venv/bin/activate`) when working locally.

## Commit Conventions

This repository enforces conventional commit format via pre-commit hooks:
- `feat:` `fix:` `docs:` `style:` `refactor:` `test:` `build:` `ci:` `chore:` `revert:`

Commits that don't follow this format will be rejected by the commit-msg hook.

Commit messages must only contain content which is relevant to the changes made
