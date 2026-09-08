from risk_engine import Position, evaluate


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
