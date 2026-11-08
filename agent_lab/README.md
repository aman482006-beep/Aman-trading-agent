# Agentic Finance Lab

Original research experiments exploring inspectable, bounded and testable finance workflows.

This directory contains small prototypes maintained separately from the upstream TradingAgents framework in the repository's tradingagents/ and cli/ directories.

## Projects

### 1. Portfolio Guardian

Path: agent_lab/portfolio_guardian/

A deterministic portfolio-risk rules engine. It validates position inputs, checks single-name concentration and weighted volatility, detects excess exposure, applies fixed scenario shocks and produces a score plus PASS / REVIEW / ESCALATE outcome.

It does not fetch security prices, calculate realised volatility, model correlations or drawdowns, estimate liquidity, or place trades. Its score and thresholds are transparent heuristics, not calibrated risk measures.

### 2. Research Copilot

Path: agent_lab/research_copilot/

A deterministic orchestration prototype. Fixed specialist functions populate typed state, an illustrative evidence ledger and a run trace. A rule-based gate applies simple leverage, free-cash-flow and confidence thresholds.

The current version does not call an LLM, retrieve live company data or independently verify evidence. The evidence sources and confidence values in the demo are illustrative placeholders and must not be interpreted as sourced research.

### 3. Earnings Intelligence

Path: agent_lab/earnings_intelligence/

A lexical retrieval baseline. It scores supplied chunks by keyword overlap and returns evidence IDs that a claim can reference.

The current version does not ingest earnings transcripts, use embeddings, rank semantic relevance or generate claims using an LLM. The confidence value is a simple evidence-count heuristic, not a calibrated probability.

## Run demos from the repository root

~~~bash
python main.py portfolio
python main.py research
python main.py earnings
~~~

## Tests

~~~bash
python -m pytest -q agent_lab
~~~

The top-level test suite also covers the retained upstream TradingAgents framework. See the root README and CONTRIBUTING.md for setup and complete checks.
