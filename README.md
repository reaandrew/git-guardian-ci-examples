# Git Guardian CI Examples

This repository demonstrates how Git Guardian can be integrated into CI/CD workflows to prevent secrets from entering the codebase - particularly important for "vibe coding" scenarios where developers might accidentally commit sensitive information.

## Purpose

Examples and configurations for integrating Git Guardian secret detection into various CI/CD pipelines to catch secrets before they reach the repository.

## Features

- **Git Guardian Secret Scanning**: Prevents secrets from being committed using ggshield pre-commit hooks
- **Conventional Commits**: Enforced using pre-commit hooks to ensure consistent commit message format
- **Pre-commit Hooks**: Automated code quality checks before commits
- **GitHub Actions CI**: Automated validation on push and pull requests
- **Semantic Versioning**: Automatic version tagging and changelog generation based on conventional commits

## Setup

To set up the pre-commit hooks locally:

```bash
# Create and activate a Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install pre-commit
pip install pre-commit

# Install the git hook scripts
pre-commit install

# Install the commit-msg hook for conventional commits
pre-commit install --hook-type commit-msg
```

### Git Guardian Setup

For Git Guardian secret scanning to work locally, you need to:

1. **Get a Git Guardian API key** from [GitGuardian Dashboard](https://dashboard.gitguardian.com/)
2. **Set the environment variable**:
   ```bash
   export GITGUARDIAN_API_KEY=your_api_key_here
   ```
3. **Add to your shell profile** (optional, for persistence):
   ```bash
   echo 'export GITGUARDIAN_API_KEY=your_api_key_here' >> ~/.bashrc
   # or ~/.zshrc if using zsh
   ```

> **Note**:
> - Always activate the virtual environment (`source venv/bin/activate`) when working with this repository
> - The Git Guardian API key is automatically available in CI/CD through the `GIT_GUARDIAN_API_KEY` repository secret
> - Local commits will be blocked if secrets are detected, even without the API key, but with reduced detection capabilities

## Conventional Commits

This repository enforces conventional commit format:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `style:` for formatting changes
- `refactor:` for code refactoring
- `test:` for adding tests
- `build:` for build system changes
- `ci:` for CI configuration changes
- `chore:` for maintenance tasks
- `revert:` for reverting changes

## Versioning and Releases

This repository uses [semantic-release](https://semantic-release.gitbook.io/) for automatic versioning and releases:

- **Version Bumps**: Based on conventional commit types:
  - `feat:` → Minor version bump (0.1.0 → 0.2.0)
  - `fix:` → Patch version bump (0.1.0 → 0.1.1)
  - `feat!:` or `BREAKING CHANGE:` → Major version bump (0.1.0 → 1.0.0)
  - `docs:`, `style:`, `refactor:`, `test:`, `build:`, `ci:`, `chore:` → No version bump

- **Automatic Release**: Every push to `main` triggers semantic-release which:
  - Analyzes commits since the last release
  - Determines the next version number
  - Generates a changelog
  - Creates a GitHub release with git tag
  - Updates the version in `package.json`

- **Starting Version**: The first release will be `v0.1.0`

## Demonstrating Guard Rails    

This line has trailing whitespace to demonstrate lint failures in CI.
