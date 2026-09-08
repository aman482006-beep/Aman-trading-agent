from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Protocol


@dataclass
class Evidence:
    claim: str
    source: str
    confidence: float
    agent: str


@dataclass
class AgentState:
    question: str
    ticker: str
    facts: Dict[str, Any]
    evidence: List[Evidence] = field(default_factory=list)
    outputs: Dict[str, str] = field(default_factory=dict)
    trace: List[Dict[str, Any]] = field(default_factory=list)
    vetoes: List[str] = field(default_factory=list)


class Agent(Protocol):
    name: str

    def run(self, state: AgentState) -> str: ...


class ResearchAgent:
    def __init__(self, name: str, fn: Callable[[AgentState], str]):
        self.name = name
        self._fn = fn

    def run(self, state: AgentState) -> str:
        result = self._fn(state)
        state.outputs[self.name] = result
        state.trace.append({"agent": self.name, "event": "completed", "output": result})
        return result


def add_evidence(state: AgentState, claim: str, source: str, confidence: float, agent: str) -> None:
    if not 0 <= confidence <= 1:
        raise ValueError("confidence must be between 0 and 1")
    state.evidence.append(Evidence(claim, source, confidence, agent))


def risk_gate(state: AgentState) -> bool:
    facts = state.facts
    if facts.get("debt_to_equity", 0) > 2.5:
        state.vetoes.append("Leverage exceeds research policy threshold")
    if facts.get("free_cash_flow_positive") is False:
        state.vetoes.append("Free cash flow is negative")
    if facts.get("thesis_confidence", 0) < 0.60:
        state.vetoes.append("Research confidence is below decision threshold")
    return not state.vetoes


def run_research(state: AgentState) -> AgentState:
    agents = [
        ResearchAgent("fundamentals", lambda s: (
            f"Revenue growth={s.facts.get('revenue_growth_pct', 'n/a')}%; "
            f"ROIC={s.facts.get('roic_pct', 'n/a')}%; "
            f"FCF={'positive' if s.facts.get('free_cash_flow_positive') else 'negative'}."
        )),
        ResearchAgent("market_context", lambda s: (
            f"Momentum={s.facts.get('momentum', 'unknown')}; "
            f"volatility={s.facts.get('volatility_pct', 'n/a')}%."
        )),
        ResearchAgent("skeptic", lambda s: (
            "Primary challenge: valuation or expectations may already price in the growth thesis. "
            "Require independent evidence before treating momentum as conviction."
        )),
    ]

    for agent in agents:
        agent.run(state)

    add_evidence(state, "Operating quality", "fundamentals snapshot", 0.82, "fundamentals")
    add_evidence(state, "Market regime", "market snapshot", 0.68, "market_context")
    add_evidence(state, "Expectation risk", "skeptic review", 0.76, "skeptic")

    state.facts["thesis_confidence"] = round(sum(e.confidence for e in state.evidence) / len(state.evidence), 2)
    approved = risk_gate(state)
    state.outputs["risk_gate"] = "PASS" if approved else "VETO"
    state.outputs["synthesis"] = (
        f"{state.ticker}: {'research passes the risk gate' if approved else 'research is blocked'}; "
        f"confidence={state.facts['thesis_confidence']:.2f}."
    )
    state.trace.append({"agent": "risk_gate", "event": "decision", "approved": approved, "vetoes": state.vetoes})
    return state
