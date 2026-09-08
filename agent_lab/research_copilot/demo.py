from core import AgentState, run_research


if __name__ == "__main__":
    state = AgentState(
        question="Is this company worth researching further?",
        ticker="DEMO",
        facts={
            "revenue_growth_pct": 18.4,
            "roic_pct": 21.1,
            "free_cash_flow_positive": True,
            "debt_to_equity": 0.42,
            "momentum": "positive",
            "volatility_pct": 27.0,
        },
    )

    result = run_research(state)
    print("\n=== AGENT DECISION ===")
    print(result.outputs["synthesis"])
    print("\n=== TRACE ===")
    for event in result.trace:
        print(event)
    print("\n=== EVIDENCE LEDGER ===")
    for item in result.evidence:
        print(f"[{item.confidence:.2f}] {item.agent}: {item.claim} <- {item.source}")
    if result.vetoes:
        print("\n=== VETOES ===")
        for veto in result.vetoes:
            print("-", veto)
