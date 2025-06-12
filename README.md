# Git Guardian CI Examples

This repository demonstrates how Git Guardian can be integrated into CI/CD workflows to prevent secrets from entering the codebase - particularly important for "vibe coding" scenarios where developers might accidentally commit sensitive information.

## Purpose

Examples and configurations for integrating Git Guardian secret detection into various CI/CD pipelines to catch secrets before they reach the repository.

## Features

- **Conventional Commits**: Enforced using pre-commit hooks to ensure consistent commit message format
- **Pre-commit Hooks**: Automated code quality checks before commits
- **GitHub Actions CI**: Automated validation on push and pull requests

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

> **Note**: Always activate the virtual environment (`source venv/bin/activate`) when working with this repository to ensure you have the correct pre-commit installation.

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
