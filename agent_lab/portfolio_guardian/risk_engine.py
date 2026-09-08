from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class Position:
    ticker: str
    weight: float
    volatility: float


@dataclass(frozen=True)
class RiskAlert:
    severity: str
    rule: str
    message: str


@dataclass
class RiskReport:
    score: float
    alerts: List[RiskAlert]
    stress_losses: Dict[str, float]
    action: str


def stress_test(positions: List[Position], shocks: Dict[str, float]) -> Dict[str, float]:
    """Estimate portfolio loss under simple single-scenario price shocks."""
    return {
        scenario: round(sum(p.weight * shocks.get(p.ticker, 0.0) for p in positions), 4)
        for scenario in {"base", *shocks.keys()}
    }


def evaluate(positions: List[Position], max_single_name: float = 0.25) -> RiskReport:
    alerts: List[RiskAlert] = []
    score = 0.0

    for p in positions:
        if p.weight > max_single_name:
            alerts.append(RiskAlert("HIGH", "concentration", f"{p.ticker} is {p.weight:.0%} of the portfolio."))
            score += 30
        if p.volatility > 0.50:
            alerts.append(RiskAlert("MEDIUM", "volatility", f"{p.ticker} volatility is {p.volatility:.0%}."))
            score += 15

    shocks = {
        "market_selloff": -0.20,
        "growth_shock": -0.30,
        "rates_shock": -0.15,
    }
    stress_losses = stress_test(positions, shocks)
    score += min(40, abs(min(stress_losses.values())) * 100)
    score = round(min(score, 100), 1)

    action = "ESCALATE" if score >= 60 else "REVIEW" if score >= 30 else "PASS"
    return RiskReport(score, alerts, stress_losses, action)
