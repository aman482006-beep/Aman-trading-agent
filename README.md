# Aman — Agentic Finance Research Lab

> **Finance × AI × Agent Systems**

This repository is my working lab for building and evaluating agentic systems for financial research and risk analysis.

The repository also contains a forked copy of **TradingAgents**, an open-source multi-agent financial research framework by Tauric Research. The upstream framework is retained for study and experimentation; the `agent_lab/` directory contains my original engineering layer built around the same problem space.

## What I'm exploring

Financial AI is not only about asking an LLM for a stock opinion. The interesting engineering problems are around **orchestration, tool use, state, memory, evaluation, failure handling, and risk controls**.

## `agent_lab/` — original work

### 🔬 Research Copilot
A multi-agent workflow:

`Planner → Fundamentals → Market Context → Skeptic → Risk Gate → Synthesis`

It uses typed state, an evidence ledger, confidence scores, explicit veto rules, and an execution trace so a reviewer can inspect **why** a conclusion was reached rather than only seeing final prose.

### 🛡️ Portfolio Guardian
A deterministic risk agent that evaluates concentration and volatility, runs portfolio stress scenarios, and produces structured `PASS / REVIEW / ESCALATE` decisions.

No LLM or API key is required to run the risk engine, making its behaviour reproducible and testable.

## Why this repository exists

I'm interested in the intersection of **financial decision-making and software systems** — particularly what changes when traditionally sequential research workflows become agentic.

Questions I'm exploring:

- How should agents share context without losing provenance?
- How do you make multi-agent decisions auditable?
- Where should deterministic code override model judgement?
- How should memory affect future decisions?
- What happens when an agent fails halfway through a workflow?
- How do you evaluate an agent beyond whether its final answer sounds convincing?

## Run my research lab

```bash
cd agent_lab/research_copilot
python demo.py
```

```bash
cd agent_lab/portfolio_guardian
python demo.py
```

Tests:

```bash
cd agent_lab/portfolio_guardian
pytest
```

## Engineering principles

**Inspectable > magical**  
**Evidence > unsupported confidence**  
**Deterministic risk controls > unconstrained model output**  
**Reproducible experiments > cherry-picked demos**

> Research and engineering project only. Nothing here is investment advice or an automated trading recommendation.

---

### Upstream project

TradingAgents is an open-source project by Tauric Research. Their work is retained here for research, attribution, and experimentation. This repository does not claim authorship of the upstream framework.
