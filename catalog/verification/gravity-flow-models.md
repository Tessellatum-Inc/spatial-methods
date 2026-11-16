# Verification record: constrained gravity-flow models

## Implemented

Unconstrained, production-constrained, attraction-constrained and doubly constrained gravity-flow allocation. Doubly constrained flows use iterative proportional fitting (RAS). A Wilson-style wrapper constructs exponential generalized-cost impedance and applies the doubly constrained solver.

## Tests

Tests cover unconstrained seed flows, origin and destination margin constraints, simultaneous balancing, exponential cost deterrence, zero margins, structural zeros, infeasible support, invalid values and non-convergence diagnostics.

## Limits

No parameter calibration, negative-binomial regression, high-dimensional fixed effects, competing-destination model, intervening-opportunities model or OD network clustering is implemented. The exponential impedance beta is supplied by the caller and is not estimated.
