from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from math import isfinite
from typing import Dict, List


def _is_finite_number(value: object) -> bool:
    """Return whether a non-boolean int/float is finite without leaking overflow."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    try:
        return isfinite(value)
    except OverflowError:
        # math.isfinite converts large Python integers to float; that conversion
        # can overflow even though the integer itself is valid Python data.
        return False


@dataclass(frozen=True)
class Position:
    ticker: str
    weight: float
    volatility: float

    def __post_init__(self) -> None:
        if not isinstance(self.ticker, str) or not self.ticker.strip():
            raise ValueError("ticker must be a non-empty string")
        if not _is_finite_number(self.weight) or not 0.0 <= self.weight <= 1.0:
            raise ValueError("weight must be a finite value between 0 and 1 for long-only portfolios")
        if not _is_finite_number(self.volatility) or self.volatility < 0.0:
            raise ValueError("volatility must be a finite, non-negative value")


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


def _validate_positions(positions: object) -> List[Position]:
    """Validate a sequence of unique Position records before any calculation."""
    if not isinstance(positions, Sequence) or isinstance(positions, (str, bytes)):
        raise ValueError("positions must be a sequence of Position records")
    if not positions:
        raise ValueError("positions must contain at least one position")
    if any(not isinstance(position, Position) for position in positions):
        raise ValueError("positions must contain only Position records")

    validated = list(positions)
    tickers = [position.ticker.strip().upper() for position in validated]
    if len(tickers) != len(set(tickers)):
        raise ValueError("positions must contain unique tickers")
    return validated


def stress_test(positions: List[Position], shocks: Dict[str, float]) -> Dict[str, float]:
    """Estimate portfolio loss under scenario-wide price shocks.

    Each shock represents the return applied to the risky positions in that
    scenario. Portfolio impact is the weighted sum of position returns.
    """
    validated_positions = _validate_positions(positions)
    if not isinstance(shocks, Mapping):
        raise ValueError("shocks must be a mapping of scenario names to numeric returns")

    normalized_shocks: Dict[str, float] = {}
    seen_scenarios = set()
    for scenario, shock in shocks.items():
        if not isinstance(scenario, str) or not scenario.strip():
            raise ValueError("scenario names must be non-empty strings")
        clean_name = scenario.strip()
        normalized_name = clean_name.casefold()
        if normalized_name == "base":
            raise ValueError("'base' is reserved for the zero-shock baseline")
        if normalized_name in seen_scenarios:
            raise ValueError("scenario names must be unique (case-insensitive)")
        seen_scenarios.add(normalized_name)
        if not _is_finite_number(shock):
            raise ValueError("scenario shocks must be finite numbers")
        # For long-only positions, a price-return shock cannot be below -100%.
        if shock < -1.0:
            raise ValueError("scenario shocks cannot be less than -100% for long-only positions")
        normalized_shocks[clean_name] = float(shock)

    invested_weight = sum(
        position.weight
        for position in validated_positions
        if position.ticker.strip().upper() != "CASH"
    )
    scenarios = {"base": 0.0, **normalized_shocks}
    return {
        scenario: round(invested_weight * shock, 4)
        for scenario, shock in scenarios.items()
    }


def evaluate(positions: List[Position], max_single_name: float = 0.25) -> RiskReport:
    validated_positions = _validate_positions(positions)
    if not _is_finite_number(max_single_name) or not 0.0 < max_single_name <= 1.0:
        raise ValueError("max_single_name must be a finite value greater than 0 and at most 1")

    alerts: List[RiskAlert] = []
    score = 0.0

    for position in validated_positions:
        ticker = position.ticker.strip().upper()
        # Cash is not a single-name security concentration.
        if ticker != "CASH" and position.weight > max_single_name:
            alerts.append(
                RiskAlert(
                    "HIGH",
                    "concentration",
                    f"{position.ticker} is {position.weight:.0%} of the portfolio.",
                )
            )
            score += 30
        # Cash is excluded from portfolio volatility calculations, so it must
        # also be excluded from the per-position volatility alert.
        if ticker != "CASH" and position.volatility > 0.50:
            alerts.append(
                RiskAlert(
                    "MEDIUM",
                    "volatility",
                    f"{position.ticker} volatility is {position.volatility:.0%}.",
                )
            )
            score += 15

    total_weight = sum(position.weight for position in validated_positions)
    if total_weight > 1.0:
        alerts.append(
            RiskAlert("HIGH", "exposure", f"Portfolio weights sum to {total_weight:.0%}.")
        )
        score += 30

    risky_positions = [
        position for position in validated_positions
        if position.ticker.strip().upper() != "CASH"
    ]
    risky_weight = sum(position.weight for position in risky_positions)
    weighted_volatility = (
        sum(position.weight * position.volatility for position in risky_positions) / risky_weight
        if risky_weight > 0
        else 0.0
    )
    if weighted_volatility > 0.30:
        alerts.append(
            RiskAlert(
                "MEDIUM",
                "portfolio_volatility",
                f"Weighted portfolio volatility is {weighted_volatility:.0%}.",
            )
        )
        score += 20

    shocks = {
        "market_selloff": -0.20,
        "growth_shock": -0.30,
        "rates_shock": -0.15,
    }
    stress_losses = stress_test(validated_positions, shocks)
    worst_scenario, worst_loss = min(stress_losses.items(), key=lambda item: item[1])
    if worst_loss < -0.25:
        alerts.append(
            RiskAlert(
                "HIGH",
                "stress_loss",
                f"Worst stress scenario ({worst_scenario}) implies a {abs(worst_loss):.0%} portfolio loss.",
            )
        )
    score += min(40, abs(worst_loss) * 100)
    score = round(min(score, 100), 1)

    action = "ESCALATE" if score >= 60 else "REVIEW" if score >= 30 else "PASS"
    return RiskReport(score, alerts, stress_losses, action)
