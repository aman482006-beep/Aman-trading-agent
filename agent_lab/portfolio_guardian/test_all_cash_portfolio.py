from agent_lab.portfolio_guardian.risk_engine import Position, evaluate


def test_fully_cash_portfolio_has_no_investment_risk_alerts():
    report = evaluate([Position("CASH", 1.0, 0.0)])

    assert report.score == 0.0
    assert report.alerts == []
    assert report.stress_losses == {
        "base": 0.0,
        "market_selloff": 0.0,
        "growth_shock": 0.0,
        "rates_shock": 0.0,
    }
    assert report.action == "PASS"
