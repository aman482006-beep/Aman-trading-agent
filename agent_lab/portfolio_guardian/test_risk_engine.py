from risk_engine import Position, evaluate, stress_test


def test_concentration_triggers_escalation():
    report = evaluate([Position("A", 0.60, 0.20), Position("CASH", 0.40, 0.0)])
    assert any(a.rule == "concentration" for a in report.alerts)
    assert report.action in {"REVIEW", "ESCALATE"}


def test_diversified_low_volatility_can_pass():
    report = evaluate([
        Position("A", 0.20, 0.20),
        Position("B", 0.20, 0.20),
        Position("C", 0.20, 0.20),
        Position("D", 0.20, 0.20),
        Position("CASH", 0.20, 0.0),
    ])
    assert not report.alerts
    assert report.action == "PASS"


def test_stress_test_applies_scenario_shocks_to_invested_weight():
    positions = [Position("A", 0.60, 0.20), Position("B", 0.20, 0.20), Position("CASH", 0.20, 0.0)]
    losses = stress_test(positions, {"market_selloff": -0.20, "rates_shock": -0.10})

    assert losses["base"] == 0.0
    assert losses["market_selloff"] == -0.16
    assert losses["rates_shock"] == -0.08
