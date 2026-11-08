import math

import pytest

from agent_lab.research_copilot.core import AgentState, ResearchAgent, add_evidence, risk_gate, run_research


def make_state(**facts):
    return AgentState(
        question="Is this sample company worth researching?",
        ticker="DEMO",
        facts=facts,
    )


@pytest.mark.parametrize("confidence", [True, "0.7", None, math.nan, math.inf, -0.01, 1.01])
def test_add_evidence_rejects_invalid_confidence(confidence):
    with pytest.raises(ValueError, match="confidence must be"):
        add_evidence(make_state(), "claim", "source", confidence, "agent")


@pytest.mark.parametrize(
    "claim,source,agent",
    [("", "source", "agent"), ("claim", " ", "agent"), ("claim", "source", "")],
)
def test_add_evidence_rejects_empty_metadata(claim, source, agent):
    with pytest.raises(ValueError):
        add_evidence(make_state(), claim, source, 0.5, agent)


def test_research_agent_requires_callable_and_text_output():
    with pytest.raises(ValueError, match="callable"):
        ResearchAgent("example", None)
    agent = ResearchAgent("example", lambda state: 123)
    with pytest.raises(ValueError, match="return text"):
        agent.run(make_state())


def test_run_research_records_trace_and_illustrative_evidence():
    state = make_state(
        revenue_growth_pct=18.4,
        roic_pct=21.1,
        free_cash_flow_positive=True,
        debt_to_equity=0.42,
        momentum="positive",
        volatility_pct=27.0,
    )
    result = run_research(state)

    assert result.outputs["risk_gate"] == "PASS"
    assert "illustrative_confidence=0.75" in result.outputs["synthesis"]
    assert len(result.evidence) == 3
    assert len(result.trace) == 4
    assert all("illustrative" in item.source or "fixed" in item.source for item in result.evidence)


def test_risk_gate_vetoes_high_leverage_and_negative_cash_flow():
    state = make_state(
        debt_to_equity=3.0,
        free_cash_flow_positive=False,
        thesis_confidence=0.7,
    )

    assert risk_gate(state) is False
    assert "Leverage exceeds research policy threshold" in state.vetoes
    assert "Free cash flow is negative" in state.vetoes


def test_risk_gate_rejects_invalid_metrics_without_type_error():
    state = make_state(debt_to_equity="high", free_cash_flow_positive=True, thesis_confidence=0.8)

    assert risk_gate(state) is False
    assert "Debt-to-equity input is missing or invalid" in state.vetoes


def test_run_research_requires_valid_state_fields():
    with pytest.raises(ValueError, match="question"):
        run_research(AgentState("", "DEMO", {}))
    with pytest.raises(ValueError, match="ticker"):
        run_research(AgentState("Question", " ", {}))
