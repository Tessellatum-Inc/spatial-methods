# Verification record: variogram model fitting

## Implemented scope

- Spherical, exponential and Gaussian semivariogram structures.
- Nugget, partial sill and range fitted with bounded nonlinear least squares.
- Pair-count weighted residuals and optional fixed nugget.
- Directional pair filtering by azimuth and cross-track bandwidth.
- Matheron and Cressie-Hawkins empirical estimators.
- Genton (1998) Q_n-based robust semivariance using the prescribed order statistic of all pairwise increment differences within each lag class.

## Tests

Tests cover zero lag, model sill behaviour, directional filtering, robust estimator non-negativity, hand-computed Genton order-statistic values, sign/translation invariance, directional Genton pair grouping, synthetic spherical parameter recovery, fixed-nugget fitting and invalid inputs. CI status is tied to the commit containing the tests.

## Bibliography

- Genton, M. G. (1998). Highly robust variogram estimation. *Mathematical Geology*, 30(2), 213–221. https://marcgenton.github.io/1998.G.MG.1.pdf

## Limits

No geometric anisotropy fitting, nested structures, Matérn models or parameter uncertainty. Pair-count weighting is a teaching default, not a universal optimum. Genton is O(m²) in the number m of increments in a lag class and is not intended for very large bins. Its Gaussian consistency factor is fixed at 2.2191.
