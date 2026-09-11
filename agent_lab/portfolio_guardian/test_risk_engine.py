import pytest

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


def test_position_rejects_invalid_weight():
    with pytest.raises(ValueError, match="weight must be between 0 and 1"):
        Position("A", 1.10, 0.20)


def test_position_rejects_negative_volatility():
    with pytest.raises(ValueError, match="volatility must be non-negative"):
        Position("A", 0.20, -0.10)


def test_base_scenario_cannot_be_overridden():
    with pytest.raises(ValueError, match="'base' is reserved"):
        stress_test([Position("A", 1.0, 0.20)], {"base": -0.50})


def test_evaluate_rejects_invalid_concentration_threshold():
    with pytest.raises(ValueError, match="max_single_name must be greater than 0"):
        evaluate([Position("A", 0.50, 0.20)], max_single_name=0.0)

    with pytest.raises(ValueError, match="max_single_name must be greater than 0"):
        evaluate([Position("A", 0.50, 0.20)], max_single_name=1.10)
