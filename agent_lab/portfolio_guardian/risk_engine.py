from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class Position:
    ticker: str
    weight: float
    volatility: float

    def __post_init__(self) -> None:
        if not self.ticker.strip():
            raise ValueError("ticker must not be empty")
        if not 0.0 <= self.weight <= 1.0:
            raise ValueError("weight must be between 0 and 1 for long-only portfolios")
        if self.volatility < 0.0:
            raise ValueError("volatility must be non-negative")


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
    """Estimate portfolio loss under scenario-wide price shocks.

    Each shock represents the return applied to the risky positions in that
    scenario. Portfolio impact is the weighted sum of position returns.
    """
    if "base" in shocks:
        raise ValueError("'base' is reserved for the zero-shock baseline")

    invested_weight = sum(p.weight for p in positions if p.ticker != "CASH")
    return {
        scenario: round(invested_weight * shock, 4)
        for scenario, shock in {"base": 0.0, **shocks}.items()
    }


def evaluate(positions: List[Position], max_single_name: float = 0.25) -> RiskReport:
    if not 0.0 < max_single_name <= 1.0:
        raise ValueError("max_single_name must be greater than 0 and at most 1")

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
