# Intervening-opportunities spatial interaction

The intervening-opportunities family models destination choice through opportunities encountered before a destination, rather than relying only on the destination's own attraction and travel impedance.

## Cumulative exponential formulation

For an origin i, order destination zones by increasing generalized cost. Let D_j be the opportunity mass at destination j and let C_{ij} be the total opportunity mass at destinations strictly closer than j. Under an exponential opportunity-acceptance process with rate alpha, the probability mass assigned at destination j is

\[
P_{ij}=\exp(-\alpha C_{ij})\left(1-\exp(-\alpha D_j)\right).
\]

The flow is T_{ij}=O_i P_{ij}. The remaining probability after all destinations is \(\exp(-\alpha\sum_jD_j)\), so the implementation returns unallocated origin mass explicitly.

## Equal-cost destinations

Destinations at exactly equal generalized cost are treated as one encounter group. The group's acceptance probability is computed from its combined opportunity mass and divided among its members in proportion to D_j. This avoids arbitrary dependence on column ordering when two zones have equal travel cost.

## Implementation contract

`intervening_opportunities(origins, destinations, generalized_cost, alpha=...)` returns a dictionary containing the OD flow matrix and a vector of unallocated origin mass. Inputs are nonnegative finite origin totals, opportunity masses and costs; alpha must be finite and positive. The function does not normalise away unallocated mass.

## Scope

This is one explicit cumulative exponential formulation for teaching and comparison. It is not a fitted model: alpha must be calibrated against observed interaction data. Generalized cost must represent the chosen opportunity-ordering rule. The formulation does not implement competing-destinations effects, intervening-opportunity model variants, spatial autocorrelation filtering, origin-destination regression, or network clustering.

## Verification

Tests compare outputs to the closed-form exponential survival calculation, verify tied-cost allocation is permutation invariant, check total mass accounting and exercise invalid-input and zero-opportunity cases.
