# Instructions for coding agents

## Repository boundaries

- Original experiments maintained here are under agent_lab/.
- tradingagents/ and cli/ contain an adapted/retained upstream TradingAgents codebase. Do not claim these components as original work. Preserve upstream attribution and licence notices.
- The Streamlit app in app.py is a local interface for the original deterministic prototypes. It must not silently call brokers, execute orders, fetch live prices, or imply that sample outputs are market research.

## Required engineering standards

1. Read the relevant module README and tests before changing behaviour.
2. Add or update tests for every behavioural change.
3. Keep Portfolio Guardian deterministic. Validate untrusted inputs before calculations.
4. Label synthetic/sample inputs and heuristic confidence clearly. Do not describe the Research Copilot as an LLM-powered agent unless a real model integration is implemented and tested.
5. Describe Earnings Intelligence retrieval accurately as keyword overlap unless the implementation is replaced with a measured semantic retrieval system.
6. Never commit API keys, credentials, personal financial data or .env files.
7. Preserve the Apache-2.0 licence and upstream attribution.

## Local checks

~~~bash
python -m pip install -e ".[dev,demo]"
python -m pytest -q
ruff check agent_lab app.py main.py
python -m compileall -q agent_lab app.py main.py
~~~

## Preview

The root index.html is a static GitHub Pages preview. It demonstrates the Portfolio Guardian rules in browser JavaScript and must stay aligned with agent_lab/portfolio_guardian/risk_engine.py. It is not a Python backend or live market-data service.
