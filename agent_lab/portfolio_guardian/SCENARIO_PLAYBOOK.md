# Portfolio Guardian — Stress Scenario Playbook

The Portfolio Guardian uses deterministic scenario shocks to translate a portfolio's invested weight into an estimated portfolio-level loss.

## Built-in scenarios

| Scenario | Shock | Intended use |
| --- | ---: | --- |
| `market_selloff` | -20% | Broad equity drawdown |
| `growth_shock` | -30% | Larger downside case for growth-sensitive assets |
| `rates_shock` | -15% | Rate-driven repricing scenario |

The engine also reports a `base` scenario at 0% shock. The `base` name is reserved and cannot be supplied as a custom scenario.

## How the calculation works

`estimated loss = invested portfolio weight × scenario shock`

Cash is excluded from invested weight. For example, a portfolio with 70% invested and 30% cash under a -20% market shock has an estimated portfolio loss of 14%.

This is intentionally a simple deterministic stress test. It is **not** a substitute for a full covariance-based risk model, factor model, or historical simulation.

## Reading the result

The guardian identifies the scenario with the largest estimated loss. A loss worse than 25% creates a `HIGH`-severity `stress_loss` alert.

The stress loss also contributes to the overall risk score, which is capped at 100. The resulting action is:

- `PASS`: score below 30
- `REVIEW`: score from 30 through 59.9
- `ESCALATE`: score 60 or above

## Adding a new scenario

When extending the scenario set, keep scenarios:

1. **Named clearly** — use a short, descriptive snake_case name.
2. **Deterministic** — use an explicit numeric shock rather than a model-generated value.
3. **Finite** — avoid `NaN`, infinity, booleans, or stringified numbers.
4. **Distinct from `base`** — do not override the zero-shock baseline.
5. **Economically interpretable** — document what market condition the shock is intended to represent.

For example, a future sector-specific test could use a scenario such as `tech_de_rating: -0.35`, provided the scenario is implemented and tested consistently with the existing validation rules.

## Limitations

The current model applies one shock to all risky positions. It does not model correlations, position-specific beta, options convexity, liquidity, leverage, or nonlinear payoffs. Those are natural areas for future risk-engine improvements.