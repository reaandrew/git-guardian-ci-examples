# Automated Guard Rails for Vibe Coding

There are countless warnings and horror stories about "vibe coding"—that flow state where you're cranking out features and everything feels effortless. Sure, it looks productive and the code works, but the end result is often an unmaintainable, insecure, unreliable, and untested mess. But it works, for now. Vibe coding might sound like a trendy term, but it's really just developing software without automated checks and quality gates. Traditional engineering disciplines have always relied on safety measures and quality controls, so vibe coding should be no different in my honest opinion.

![check-cycles.png](docs/images/check-cycles.png)

## Pre-commit Hooks: The First Line of Defense

![pre-commit-checks.png](docs/images/pre-commit-checks.png)

Pre-commit hooks are automated checks that run locally on your machine before code enters the repository. They're particularly crucial when working with AI coding assistants, which have transformed how we write code but can also introduce new challenges.

When AI assistants like Claude Code, GitHub Copilot, or Cursor are in "auto mode," they can rapidly generate and iterate on code. This speed is incredible for productivity, but it can also bypass human review of basic quality standards. Pre-commit hooks help with this by providing immediate, consistent feedback that both human developers and AI assistants can learn from.

Here's where it gets really powerful: when an AI coding assistant encounters a failed pre-commit check, it doesn't just ignore it—it uses that feedback to iterate and improve the code. The commit attempt blocks until all checks pass, creating a feedback loop where the AI learns to write better code that meets your standards. For example, if a commit fails because of missing test coverage, the AI can immediately add the necessary tests and try again. If code formatting is wrong, the AI learns the project's style requirements.

This creates a collaborative relationship where the AI handles the heavy lifting of code generation while the automated checks ensure quality standards are maintained. The developer gets the speed benefits of AI assistance without sacrificing code quality, security, or maintainability.

## CI Pipeline: The Second Line of Defense

![post-commit-checks.png](docs/images/post-commit-checks.png)

While pre-commit hooks catch issues locally, the CI pipeline provides comprehensive validation in a clean, controlled environment. The multi-stage approach ensures that even if something bypasses local checks, it won't reach production.

The pipeline runs progressive stages: basic linting and testing first, followed by comprehensive security scanning with GitGuardian's repository history analysis, then advanced quality analysis with SonarCloud and Semgrep security scanning. Each stage builds on the previous one, with failures stopping the pipeline immediately. This catches issues that might be missed locally due to environment differences, skipped pre-commit hooks, or complex integration problems that only surface during full builds.

For AI agents, the CI pipeline becomes even more powerful when they can query job status and receive clear failure messages. This enables the same feedback loop that works with pre-commit hooks—the agent can push code, check the CI results, and iterate based on specific failure details until all checks pass. Clear, descriptive error messages from CI jobs help the agent understand exactly what needs to be fixed.

## Automated Guardrails

Now let's examine the specific automated checks that form the backbone of a robust development workflow. The Acronym Creator project demonstrates each of these guardrails with real-world configurations that you can copy and adapt for your own projects. The repository can also be used as a repository template or as a reference to create other templates for different application types or languages.

### Secret Detection
**Tools Used**: GitGuardian ggshield [https://www.gitguardian.com/ggshield](https://www.gitguardian.com/ggshield)

GitGuardian automatically scans your code for accidentally committed passwords, API keys, and other sensitive information. This protection works at two levels: locally during commits and comprehensively in the CI pipeline.

**Pre-commit Hook** - Scans staged changes before they enter the repository:
```yaml
- repo: https://github.com/gitguardian/ggshield
  hooks:
    - id: ggshield
```

**CI Pipeline Stage** - Scans the complete repository history:
```yaml
- name: GitGuardian scan repository history
  env:
    GITGUARDIAN_API_KEY: ${{ secrets.GIT_GUARDIAN_API_KEY }}
  run: ggshield secret scan repo .
```

Why both? The pre-commit hook catches secrets in new changes, but the CI stage scans the entire git history. This is critical because secrets can exist in previous commits even if they've been removed from current files. Git preserves the complete history of changes, so a password committed six months ago and deleted the next day is still accessible in the repository history. The CI scan ensures comprehensive coverage and catches secrets that might have been introduced through merges, rebases, or commits made with `--no-verify`. For detailed setup instructions, see the [GitGuardian GitHub Actions integration guide](https://docs.gitguardian.com/ggshield-docs/integrations/cicd-integrations/github-actions).

### Code Quality Automation
**Tools Used**: Black (formatting) and Flake8 (linting)

Black automatically formats your code consistently, while Flake8 catches common programming errors and enforces PEP 8 compliance. This means you can focus on solving problems rather than worrying about spacing and style conventions.

```yaml
- repo: https://github.com/psf/black
  hooks:
    - id: black
- repo: https://github.com/pycqa/flake8
  hooks:
    - id: flake8
```

For convenience, we simply run the pre-commit tool again in CI, which executes all these checks once more. This is essential for numerous reasons, including catching commits made with the `--no-verify` flag that bypass local pre-commit hooks.

### Test Coverage Safety Net
**Tools Used**: pytest, coverage.py, and pytest-cov plugin

The system automatically runs your tests using pytest and calculates coverage with coverage.py through the pytest-cov plugin. Coverage is enforced at multiple levels with specific configuration files controlling the behavior.

**Pre-commit Configuration** - Uses a dedicated config for clean execution:
```ini
# pytest-precommit.ini
[pytest]
addopts = --cov=src --cov-report=term-missing --cov-fail-under=80
```

**Coverage Configuration** - Controls coverage calculation and thresholds:
```ini
# .coveragerc
[run]
branch = true
source = src
data_file = /tmp/.coverage_precommit

[report]
fail_under = 80
exclude_lines =
    pragma: no cover
    def __repr__
    if __name__ == "__main__":
```

The coverage enforcement works by requiring 80% of code lines to be tested, including branch coverage (testing both sides of if/else statements). The pre-commit hook uses a separate data file in `/tmp` to avoid modifying the working directory, and excludes common patterns like `__repr__` methods that don't need testing. If coverage drops below the threshold, the commit is blocked until more tests are added. Like the code quality checks, the CI pipeline runs the pre-commit tool again to re-validate all tests and coverage requirements.

### Security Analysis
**Tools Used**: SonarCloud and Semgrep

Security scanning tools like SonarCloud and Semgrep examine your code for common vulnerability patterns, code quality issues, and security hotspots, identifying potential problems before they reach production. These checks are only done in CI since they are not as quick, and I have focused on keeping the pre-commit tests and checks to those which are relatively fast, so you can fail fast.

```yaml
# SonarCloud integration
- name: SonarCloud Scan
  uses: SonarSource/sonarqube-scan-action@master

# Semgrep security analysis
semgrep:
  container:
    image: semgrep/semgrep
  steps:
  - run: semgrep ci
```

## Real Example: Acronym Creator

To demonstrate these concepts, I built a command-line tool that creates acronyms from phrases:

```bash
acronymcreator "Hello World"  # Returns: HW
acronymcreator "The Quick Brown Fox" --include-articles  # Returns: TQBF
```

This project includes comprehensive automated guardrails. Every time I made changes—even during rapid prototyping—the system automatically checked for secrets, formatted the code, ran tests, and verified security. This meant I could code freely without worrying about accidentally introducing problems.

![CI Pipeline Structure](docs/images/ci-pipeline.png)
*Figure 3: Multi-stage CI pipeline provides comprehensive validation*

## Automated Release Management

![Semantic Release Flow](docs/images/semantic-release.png)
*Figure 4: Conventional commits enable automated versioning and releases*

The system includes automated release management using semantic versioning. When you write commit messages using conventional formats like "feat:" for new features or "fix:" for bug fixes, the system automatically determines the appropriate version number and creates releases with generated documentation.

```json
{
  "branches": ["main"],
  "plugins": [
    "@semantic-release/commit-analyzer",
    "@semantic-release/release-notes-generator",
    "@semantic-release/changelog"
  ]
}
```

This eliminates the manual work of managing versions and release notes, while ensuring consistent documentation of changes.

## Implementation Strategy

![Implementation Timeline](docs/images/implementation-phases.png)
*Figure 5: Start with basic guardrails and gradually add more sophisticated checks*

The key to successful implementation is starting small and building gradually. Begin with basic checks like secret detection and code formatting, then add test coverage requirements once the team is comfortable. Advanced security analysis and quality gates can be introduced later as the team becomes familiar with the workflow.

The important principle is to fix issues immediately when the automated checks find them, rather than accumulating technical debt. This keeps the guardrails effective and prevents the quality standards from degrading over time.

## Benefits Beyond Safety

These automated systems don't just prevent problems—they actually enable faster development. With confidence that basic issues will be caught automatically, developers can experiment more freely and iterate more quickly. Code reviews become more focused on architecture and business logic rather than formatting and style. Teams can deploy more frequently because they trust that their quality gates will catch regressions.

![Repository Template Structure](docs/images/template-structure.png)
*Figure 6: Template repository provides instant guardrails for new projects*

## Getting Started

The Acronym Creator project serves as a template that other teams can copy and adapt for their own projects. It includes pre-configured automation for secret detection, code quality enforcement, test coverage, security scanning, and automated releases. New projects can inherit these protections immediately rather than starting from scratch.

## The Bottom Line

Automated guardrails don't slow down vibe coding—they make it sustainable. They let you maintain that productive flow state while ensuring that the code you're producing meets quality and security standards. The initial setup takes some effort, but the long-term result is faster, safer development with fewer production surprises.

The goal isn't to restrict creativity or slow down development. It's to catch the common mistakes that happen when you're focused on solving hard problems, letting you maintain both speed and quality without having to constantly worry about the details that computers can handle automatically.
