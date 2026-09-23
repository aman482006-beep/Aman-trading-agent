import math

import pytest

from risk_engine import Position, evaluate, stress_test


def test_concentration_triggers_escalation():
    report = evaluate([Position("A", 0.60, 0.20), Position("CASH", 0.40, 0.0)])
    assert any(a.rule == "concentration" for a in report.alerts)
    assert report.action in {"REVIEW", "ESCALATE"}


def test_diversified_low_volatility_can_pass():
    report = evaluate([
        Position("A", 0.20, 0.20), Position("B", 0.20, 0.20),
        Position("C", 0.20, 0.20), Position("D", 0.20, 0.20),
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


def test_stress_test_excludes_cash_case_insensitively():
    positions = [Position("A", 0.60, 0.20), Position("cash", 0.40, 0.0)]
    assert stress_test(positions, {"market_selloff": -0.20})["market_selloff"] == -0.12


def test_position_rejects_invalid_weight():
    with pytest.raises(ValueError, match="weight must be"):
        Position("A", 1.10, 0.20)


def test_position_rejects_negative_volatility():
    with pytest.raises(ValueError, match="volatility must be"):
        Position("A", 0.20, -0.10)


def test_position_rejects_non_finite_inputs():
    with pytest.raises(ValueError, match="weight must be"):
        Position("A", math.nan, 0.20)
    with pytest.raises(ValueError, match="volatility must be"):
        Position("A", 0.20, math.inf)


def test_position_rejects_non_string_or_empty_ticker():
    for ticker in (123, "   "):
        with pytest.raises(ValueError, match="ticker must be a non-empty string"):
            Position(ticker, 0.20, 0.20)


def test_base_scenario_cannot_be_overridden_case_insensitively():
    positions = [Position("A", 1.0, 0.20)]
    for scenario in ("base", "BASE", " Base "):
        with pytest.raises(ValueError, match="'base' is reserved"):
            stress_test(positions, {scenario: -0.50})


def test_stress_test_rejects_non_finite_shocks():
    positions = [Position("A", 1.0, 0.20)]
    for shock in (math.nan, math.inf, -math.inf):
        with pytest.raises(ValueError, match="scenario shocks must be finite"):
            stress_test(positions, {"invalid": shock})


def test_stress_test_rejects_non_numeric_shocks():
    positions = [Position("A", 1.0, 0.20)]
    for shock in ("-0.20", None, True):
        with pytest.raises(ValueError, match="scenario shocks must be finite"):
            stress_test(positions, {"invalid": shock})


def test_stress_test_rejects_empty_scenario_names():
    positions = [Position("A", 1.0, 0.20)]
    for scenario in ("", "   "):
        with pytest.raises(ValueError, match="scenario names must be"):
            stress_test(positions, {scenario: -0.20})


def test_evaluate_rejects_invalid_concentration_threshold():
    for threshold in (0.0, 1.10, math.nan):
        with pytest.raises(ValueError, match="max_single_name must be"):
            evaluate([Position("A", 0.50, 0.20)], max_single_name=threshold)


def test_evaluate_flags_excess_total_exposure():
    report = evaluate([Position("A", 0.70, 0.20), Position("B", 0.50, 0.20)])
    assert any(a.rule == "exposure" for a in report.alerts)
    assert report.action == "ESCALATE"


def test_evaluate_rejects_duplicate_tickers_case_insensitively():
    with pytest.raises(ValueError, match="positions must contain unique tickers"):
        evaluate([Position("AAPL", 0.20, 0.20), Position("aapl", 0.20, 0.20)])


def test_evaluate_flags_high_weighted_portfolio_volatility():
    report = evaluate([
        Position("A", 0.40, 0.40),
        Position("B", 0.40, 0.35),
        Position("CASH", 0.20, 0.0),
    ])
    alert = next(a for a in report.alerts if a.rule == "portfolio_volatility")
    assert alert.severity == "MEDIUM"
    assert "38%" in alert.message
    assert report.action == "ESCALATE"


def test_cash_does_not_distort_weighted_portfolio_volatility():
    report = evaluate([
        Position("A", 0.40, 0.40),
        Position("CASH", 0.60, 0.0),
    ])
    assert not any(a.rule == "portfolio_volatility" for a in report.alerts)


def test_evaluate_flags_severe_worst_case_stress_loss():
    report = evaluate([Position("A", 1.0, 0.20)])
    alert = next(a for a in report.alerts if a.rule == "stress_loss")
    assert alert.severity == "HIGH"
    assert "30%" in alert.message
    assert "growth_shock" in alert.message


def test_empty_portfolio_is_rejected():
    with pytest.raises(ValueError, match="positions must contain at least one position"):
        evaluate([])
    with pytest.raises(ValueError, match="positions must contain at least one position"):
        stress_test([], {"market_selloff": -0.20})
