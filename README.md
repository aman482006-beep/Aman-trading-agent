# Agentic Finance Research Lab

[![CI](https://github.com/aman482006-beep/Aman-trading-agent/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/aman482006-beep/Aman-trading-agent/actions/workflows/ci.yml)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE)

An engineering lab exploring how financial research workflows can become more inspectable, testable and risk-aware.

**[Open the interactive GitHub Pages preview](https://aman482006-beep.github.io/Aman-trading-agent/)**

This repository contains two clearly separated components:

1. **Original experiments** in agent_lab/: a deterministic portfolio-risk engine, a research-orchestration prototype and a keyword-based earnings-document retrieval baseline.
2. **An adapted/retained upstream TradingAgents codebase** in tradingagents/ and cli/, attributed to [Tauric Research / TradingAgents](https://github.com/TauricResearch/TradingAgents).

This repository is not an official Tauric Research project and is not marked as a GitHub fork. See [UPSTREAM.md](UPSTREAM.md) for attribution and ownership boundaries.

## What is implemented

| Component | Current behaviour | Important boundary |
| --- | --- | --- |
| Portfolio Guardian | Validates long-only position inputs; flags single-name concentration, individual and weighted volatility, excess exposure and fixed scenario losses; returns PASS / REVIEW / ESCALATE. | Deterministic rules only. No price feed, covariance model, drawdown model or trade execution. |
| Research Copilot | Runs fixed planner/specialist/skeptic steps over supplied facts; records a trace and illustrative evidence; applies a deterministic risk gate. | A deterministic prototype, not an LLM-powered workflow. Sample confidence values are illustrative, not calibrated. |
| Earnings Intelligence | Ranks supplied text chunks using keyword overlap and returns evidence IDs for a claim. | A lexical baseline, not embeddings, semantic search, transcript ingestion or an LLM summariser. |
| TradingAgents framework | Retained upstream multi-agent framework and CLI, with provider integrations and its own tests. | Upstream-derived code; do not attribute upstream adoption metrics to this repository. |

## Interactive preview

The GitHub Pages site at the link above is a static, browser-only walkthrough of the Portfolio Guardian rules. It lets a reviewer edit ticker, weight and volatility inputs and see the deterministic score, alerts and fixed scenario impacts.

The page does not run Python, call an LLM, fetch live data or execute trades. The browser implementation is intended to mirror the Python risk rules; changes to either implementation should be checked together.

## Quick start

Python 3.11 is used in CI. The package metadata supports Python 3.10+.

~~~bash
git clone https://github.com/aman482006-beep/Aman-trading-agent.git
cd Aman-trading-agent

python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -e ".[dev,demo]"
~~~

### Run the local web demo

~~~bash
streamlit run app.py
~~~

The local interface demonstrates the three original agent_lab components using sample inputs. It does not connect to a broker or fetch live market information.

### Run command-line demos

~~~bash
# Portfolio Guardian
python main.py portfolio

# Research Copilot
python main.py research

# Earnings Intelligence
python main.py earnings
~~~

### Run the test suite

~~~bash
python -m pytest -q
ruff check agent_lab app.py main.py
python -m compileall -q agent_lab app.py main.py
~~~

### Use the upstream TradingAgents CLI

The upstream framework is packaged separately from the original agent_lab experiments. Install the project dependencies using the Quick start above, configure a supported provider and its credentials in your local environment, then run:

~~~bash
tradingagents
~~~

Refer to the upstream [TradingAgents documentation](https://github.com/TauricResearch/TradingAgents) for provider configuration and framework-specific workflows. Never commit API keys or local .env files.

## Portfolio Guardian assumptions

The current engine is intentionally small and deterministic:

- Position weights are long-only fractions between 0 and 1. A portfolio may have less than 100% in listed positions; the unallocated portion contributes no stress loss.
- The ticker CASH is excluded from single-name concentration and volatility calculations.
- Weighted volatility is calculated over the listed non-cash positions. The input's time basis is supplied by the caller and is not inferred.
- Built-in scenario shocks are -20% market_selloff, -30% growth_shock and -15% rates_shock.
- A worst scenario loss beyond 25% creates a HIGH stress-loss alert.
- The risk score combines fixed rule points and worst-case stress impact; it is a transparent heuristic, not a statistically calibrated risk measure.

See [the scenario playbook](agent_lab/portfolio_guardian/SCENARIO_PLAYBOOK.md) and [the risk engine](agent_lab/portfolio_guardian/risk_engine.py).

## Repository layout

~~~text
agent_lab/
  portfolio_guardian/       Original deterministic portfolio risk engine
  research_copilot/         Original deterministic workflow prototype
  earnings_intelligence/    Original keyword retrieval baseline
tradingagents/              Adapted/retained upstream framework
cli/                        Upstream framework CLI
tests/                      Upstream framework tests
app.py                      Local Streamlit interface for agent_lab demos
index.html                  Static GitHub Pages preview
UPSTREAM.md                 Attribution and ownership boundaries
AGENTS.md                   Instructions for coding agents
~~~

## Maintainer and contribution workflow

- Open issues using the structured bug and feature templates.
- Submit changes through pull requests.
- CI runs tests, lint and compile checks on pull requests and pushes to main.
- Pull requests should receive human maintainer review; green CI is not a substitute for review.
- See [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md) and the pull-request template.

## Safety and limitations

This is research and educational software. It is not investment advice, a broker, a portfolio accounting system or an automated trading system. Scenario outputs are simplified estimates from user-supplied inputs. The deterministic prototypes do not establish that a security is suitable to buy or sell. Verify all calculations and data independently before any real-world use.

## Licence

The repository is distributed under the Apache License 2.0. Upstream-derived code remains subject to the applicable upstream attribution and licence terms; see [UPSTREAM.md](UPSTREAM.md).
