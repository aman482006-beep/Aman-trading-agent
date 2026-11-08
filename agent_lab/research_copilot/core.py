from __future__ import annotations

from dataclasses import dataclass, field
from math import isfinite
from typing import Any, Callable, Dict, List, Protocol


def _is_finite_number(value: object) -> bool:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    try:
        return isfinite(value)
    except OverflowError:
        return False


@dataclass(frozen=True)
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
    """Small synchronous agent wrapper used by the deterministic demo."""

    def __init__(self, name: str, fn: Callable[[AgentState], str]):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("agent name must be a non-empty string")
        if not callable(fn):
            raise ValueError("agent function must be callable")
        self.name = name
        self._fn = fn

    def run(self, state: AgentState) -> str:
        result = self._fn(state)
        if not isinstance(result, str):
            raise ValueError(f"agent {self.name} must return text")
        state.outputs[self.name] = result
        state.trace.append({"agent": self.name, "event": "completed", "output": result})
        return result


def add_evidence(
    state: AgentState, claim: str, source: str, confidence: float, agent: str
) -> None:
    """Attach a validated evidence record.

    Confidence is an illustrative 0..1 input for this prototype, not a calibrated
    probability and not an independently verified measure of source quality.
    """
    if not isinstance(state, AgentState):
        raise ValueError("state must be an AgentState")
    for field_name, value in (("claim", claim), ("source", source), ("agent", agent)):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} must be a non-empty string")
    if not _is_finite_number(confidence) or not 0 <= confidence <= 1:
        raise ValueError("confidence must be a finite number between 0 and 1")
    state.evidence.append(Evidence(claim.strip(), source.strip(), float(confidence), agent.strip()))


def risk_gate(state: AgentState) -> bool:
    """Apply simple deterministic research guardrails to supplied facts."""
    if not isinstance(state, AgentState) or not isinstance(state.facts, dict):
        raise ValueError("state must contain a facts dictionary")

    debt_to_equity = state.facts.get("debt_to_equity", 0.0)
    if not _is_finite_number(debt_to_equity):
        state.vetoes.append("Debt-to-equity input is missing or invalid")
    elif debt_to_equity > 2.5:
        state.vetoes.append("Leverage exceeds research policy threshold")

    free_cash_flow_positive = state.facts.get("free_cash_flow_positive")
    if free_cash_flow_positive is False:
        state.vetoes.append("Free cash flow is negative")
    elif free_cash_flow_positive not in (True, False, None):
        state.vetoes.append("Free-cash-flow input must be true, false or unknown")

    thesis_confidence = state.facts.get("thesis_confidence", 0.0)
    if not _is_finite_number(thesis_confidence):
        state.vetoes.append("Research confidence input is invalid")
    elif thesis_confidence < 0.60:
        state.vetoes.append("Research confidence is below decision threshold")

    return not state.vetoes


def run_research(state: AgentState) -> AgentState:
    """Run a fixed, deterministic prototype over caller-supplied facts.

    The specialist functions and sample evidence values are illustrative. This
    implementation does not call a language model or retrieve external data.
    """
    if not isinstance(state, AgentState):
        raise ValueError("state must be an AgentState")
    if not isinstance(state.question, str) or not state.question.strip():
        raise ValueError("question must be a non-empty string")
    if not isinstance(state.ticker, str) or not state.ticker.strip():
        raise ValueError("ticker must be a non-empty string")
    if not isinstance(state.facts, dict):
        raise ValueError("facts must be a dictionary")

    agents = [
        ResearchAgent(
            "fundamentals",
            lambda current: (
                f"Revenue growth={current.facts.get('revenue_growth_pct', 'n/a')}%; "
                f"ROIC={current.facts.get('roic_pct', 'n/a')}%; "
                f"FCF={_fcf_label(current.facts.get('free_cash_flow_positive'))}."
            ),
        ),
        ResearchAgent(
            "market_context",
            lambda current: (
                f"Momentum={current.facts.get('momentum', 'unknown')}; "
                f"volatility={current.facts.get('volatility_pct', 'n/a')}%."
            ),
        ),
        ResearchAgent(
            "skeptic",
            lambda current: (
                "Primary challenge: valuation or expectations may already price in the growth thesis. "
                "Require independent evidence before treating momentum as conviction."
            ),
        ),
    ]

    for agent in agents:
        agent.run(state)

    add_evidence(
        state, "Operating quality", "illustrative fundamentals input", 0.82, "fundamentals"
    )
    add_evidence(
        state, "Market regime", "illustrative market input", 0.68, "market_context"
    )
    add_evidence(
        state, "Expectation risk", "fixed skeptic prompt", 0.76, "skeptic"
    )

    illustrative_confidence = round(
        sum(item.confidence for item in state.evidence[-3:]) / 3,
        2,
    )
    state.facts["thesis_confidence"] = illustrative_confidence
    approved = risk_gate(state)
    state.outputs["risk_gate"] = "PASS" if approved else "VETO"
    state.outputs["synthesis"] = (
        f"{state.ticker.strip().upper()}: "
        f"{'research passes the risk gate' if approved else 'research is blocked'}; "
        f"illustrative_confidence={illustrative_confidence:.2f}."
    )
    state.trace.append(
        {
            "agent": "risk_gate",
            "event": "decision",
            "approved": approved,
            "vetoes": list(state.vetoes),
        }
    )
    return state


def _fcf_label(value: object) -> str:
    if value is True:
        return "positive"
    if value is False:
        return "negative"
    return "unknown"
