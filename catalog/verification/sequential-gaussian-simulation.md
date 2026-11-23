# Verification record: sequential Gaussian simulation

## Implemented scope

- Seeded random ordering of grid locations.
- Simple-kriging conditional Gaussian draws using supplied mean and covariance model.
- Conditioning on original observations and all previous simulated cells.
- Optional independent observation noise on supplied observations.
- Exact preservation of grid locations collocated with zero-noise observations.

## Tests

Tests check reproducibility, exact-data preservation, noisy observation handling,
invalid inputs, and the single-target conditional Gaussian mean and variance
against a repeated-seed Monte Carlo oracle.

## Limits

Dense covariance reconstruction and solve at every grid cell; no variogram
fitting, local neighbourhood, large-grid acceleration, indicator simulation,
multiple-point simulation or hyperparameter uncertainty.
