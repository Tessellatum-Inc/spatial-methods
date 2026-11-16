# Verification record: variogram model fitting

## Implemented scope

- Spherical, exponential and Gaussian semivariogram structures.
- Nugget, partial sill and range fitted with bounded nonlinear least squares.
- Pair-count weighted residuals and optional fixed nugget.
- Directional pair filtering by azimuth and cross-track bandwidth.
- Matheron and Cressie-Hawkins empirical estimators.

## Tests

Tests cover zero lag, model sill behaviour, directional filtering, robust estimator non-negativity, synthetic spherical parameter recovery, fixed-nugget fitting and invalid inputs. CI status is tied to the commit containing the tests.

## Limits

No geometric anisotropy fitting, nested structures, Matérn models or parameter uncertainty. Pair-count weighting is a teaching default, not a universal optimum.
