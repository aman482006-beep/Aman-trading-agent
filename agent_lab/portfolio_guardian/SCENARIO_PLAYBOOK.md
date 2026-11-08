# Portfolio Guardian — Stress Scenario Playbook

The Portfolio Guardian uses deterministic scenario shocks to translate listed risky-position weight into an estimated portfolio-level loss.

## Built-in scenarios

| Scenario | Shock | Intended use |
| --- | ---: | --- |
| market_selloff | -20% | Broad equity sell-off |
| growth_shock | -30% | Larger downside case for growth-sensitive assets |
| rates_shock | -15% | Rate-driven repricing scenario |

The engine also reports a base scenario at 0% shock. The base name is reserved and cannot be supplied as a custom scenario.

## How the calculation works

Estimated portfolio return = sum of listed non-cash position weights × scenario shock.

Cash is excluded from invested weight. For example, a portfolio with 70% in listed risky positions and 30% in cash under a -20% shock has an estimated portfolio return of -14%.

The input should describe the complete portfolio. Any unrepresented weight is not included in stress losses, so omitted positions effectively behave like uninvested capital in this simplified calculation. Add an explicit CASH row when that is the intended assumption.

## Reading the result

The guardian identifies the scenario with the largest estimated loss. A loss worse than 25% creates a HIGH-severity stress_loss alert.

The stress loss also contributes to the overall heuristic risk score, which is capped at 100. The resulting action is:

- PASS: score below 30
- REVIEW: score from 30 through 59.9
- ESCALATE: score 60 or above

## Adding a new scenario

When extending the scenario set, keep scenarios:

1. Named clearly with a short descriptive snake_case name.
2. Deterministic, using an explicit numeric shock rather than a model-generated value.
3. Finite; reject NaN, infinity, booleans and stringified numbers.
4. Distinct from base; the zero-shock baseline is reserved.
5. Economically interpretable, with a documented description and regression test.

For example, a future sector-specific test could use tech_de_rating at -35%, provided the scenario is implemented and tested consistently with the validation rules.

## Limitations

The current model applies one shock to all listed non-cash positions. It does not model correlations, position-specific beta, options convexity, liquidity, leverage, path dependency or nonlinear payoffs. Volatility is supplied by the caller; the engine does not calculate its source or time basis. This is not a substitute for a full covariance-based risk model, factor model or historical simulation.
