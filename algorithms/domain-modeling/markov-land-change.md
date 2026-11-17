# Markov land-change simulation

A first-order categorical Markov model describes transitions between land-cover classes. Given aligned previous and current class rasters, estimate a row-stochastic transition matrix (P), where

\[
P_{ab}=\Pr(X_{t+1}=b\mid X_t=a).
\]

The implementation counts observed class-to-class transitions and normalizes each source-class row. A class with no observed outgoing transitions is treated as absorbing (probability one of remaining in that class); this convention is explicit and can be changed by using a positive pseudocount.

For simulation, each raster cell transitions independently according to the row of (P) corresponding to its current class. The implementation uses a seeded random stream and returns the simulated categorical raster after the requested number of steps.

## Assumptions and limitations

- Previous and current rasters must be aligned, integer-coded and free of NoData sentinels; class IDs are non-negative integers.
- The model is first-order and time-homogeneous unless a separate matrix is estimated for each period.
- Cell transitions are conditionally independent; there is no neighborhood effect, spatial interaction, patch growth or contiguity constraint.
- Transition probabilities are empirical proportions, not causal effects. Sampling design, map classification error, class aggregation and period length influence them.
- This is not a reproduction of CLUE-S, FLUS, PLUS, SLEUTH or another land-change system. Spatial allocation, driver suitability, constraints, calibration and validation remain open.

## Tests

The independent tests check a hand-calculated transition matrix, absorbing classes, row sums, seeded simulation, output shape and invalid alignment/state/matrix inputs.
