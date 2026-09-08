# Agentic Finance Lab

An original research layer built around a finance-agent workflow. The goal is not to make an LLM *sound* like an analyst; it is to make agent behaviour inspectable, bounded, and testable.

## What this demonstrates

- **Planner → specialists → skeptic → risk gate → synthesis** orchestration
- Typed state passed between agents instead of hidden prompt chains
- Evidence ledger with source, confidence, and claim ownership
- Explicit risk vetoes and escalation rules
- Run traces that make every agent decision auditable
- Deterministic portfolio stress testing without requiring an LLM or API key
- Pluggable model/tool interfaces: the orchestration layer does not depend on one provider

## Projects

### 1. Research Copilot
`agent_lab/research_copilot/`

A multi-agent equity research workflow. The planner decomposes a question, specialist agents analyse fundamentals and market context, a skeptic attacks the thesis, and a risk gate decides whether the final synthesis is allowed to pass.

### 2. Portfolio Guardian
`agent_lab/portfolio_guardian/`

A deterministic risk agent for concentration, drawdown, volatility and scenario shocks. It produces structured alerts and escalation decisions before a portfolio action can proceed.

## Design principle

> **Agents should produce decisions with provenance, not just prose.**

This lab is for research and engineering experimentation. It is not investment advice and does not place trades.
