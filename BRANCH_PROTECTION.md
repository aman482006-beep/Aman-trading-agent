# Recommended protection rules for main

The repository contains CODEOWNERS and pull-request templates, but those files do not independently block merges. A repository administrator must configure GitHub branch rules.

## Create a branch ruleset

1. Open the repository on GitHub.
2. Go to **Settings → Rules → Rulesets → New ruleset → New branch ruleset**.
3. Name it **Protect main** and set enforcement to **Active**.
4. Set the target branch pattern to main.

## Recommended rules

Enable:

- **Require a pull request before merging.**
- **Require approvals: 1** once at least one trusted reviewer other than the pull-request author has repository access.
- **Require review from Code Owners.**
- **Dismiss stale approvals when new commits are pushed.**
- **Require conversation resolution before merging.**
- **Require status checks to pass before merging**, and select the CI job named **Python 3.11 · tests, lint and build** after it has appeared on a pull request.
- **Block force pushes** and **block branch deletion** for main.

Do not configure an approval requirement that cannot be satisfied. If the repository has only one maintainer, first add a trusted independent reviewer or maintainer with repository access; GitHub does not allow the PR author to approve their own pull request. If the only entry in CODEOWNERS is the PR author, add the second maintainer as a code owner before enabling “Require review from Code Owners”, otherwise the rule may be impossible to satisfy for maintainer-authored pull requests.

## What this repository already provides

- .github/CODEOWNERS identifies the repository maintainer for review routing.
- .github/pull_request_template.md asks contributors to describe scope, provenance, tests and safety.
- .github/ISSUE_TEMPLATE/ provides structured bug and feature reports.
- .github/workflows/ci.yml runs the complete test suite, checks the maintained code, validates the static preview JavaScript and builds the package.

A green CI result is automated evidence, not a human review. Keep both controls.
