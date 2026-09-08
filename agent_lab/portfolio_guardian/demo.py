from risk_engine import Position, evaluate


if __name__ == "__main__":
    portfolio = [
        Position("NVDA", 0.32, 0.58),
        Position("MSFT", 0.20, 0.31),
        Position("JPM", 0.18, 0.27),
        Position("CASH", 0.30, 0.00),
    ]

    report = evaluate(portfolio)
    print(f"Risk score: {report.score}/100")
    print(f"Action: {report.action}")
    print("\nStress scenarios:")
    for scenario, loss in report.stress_losses.items():
        print(f"  {scenario}: {loss:.2%}")
    print("\nAlerts:")
    for alert in report.alerts:
        print(f"  [{alert.severity}] {alert.rule}: {alert.message}")
