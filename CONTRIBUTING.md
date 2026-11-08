# Contributing

Thanks for helping improve the Agentic Finance Research Lab.

## Before opening an issue

Search existing issues and pull requests. Include the exact command, environment, expected result and actual result when reporting a defect. Never include API keys, account credentials, private financial records or other sensitive data.

## Development setup

Python 3.11 is the primary CI version. Python 3.10+ is supported by the package metadata.

~~~bash
git clone https://github.com/aman482006-beep/Aman-trading-agent.git
cd Aman-trading-agent
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev,demo]"
~~~

Run the checks before submitting:

~~~bash
python -m pytest -q
ruff check agent_lab app.py main.py
python -m compileall -q agent_lab app.py main.py
~~~

## Pull request expectations

- Keep changes focused and explain the problem they solve.
- Add regression tests for bugs and tests for new behaviour.
- Update documentation when behaviour, setup, limitations or outputs change.
- Include screenshots for meaningful user-interface changes.
- Call out whether a change touches original agent_lab/ code or the retained upstream tradingagents/ / cli/ code.
- Preserve upstream notices and licence terms.
- Explain what was actually tested. Do not report checks as passing if they were not run.

## Review process

Pull requests should receive maintainer review before merge. Reviewers should check correctness, tests, security, documentation accuracy, scope and attribution. CI provides automated checks; a green CI run is not a substitute for human review. Contributions affecting upstream code require an additional attribution/licence check.

The repository currently has a small maintainer base. External contributors should allow time for review; please do not merge your own pull request solely because CI is green.
