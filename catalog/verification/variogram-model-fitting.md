# Verification record: variogram model fitting

## Implemented scope

- Spherical, exponential and Gaussian semivariogram structures.
- Nugget, partial sill and range fitted with bounded nonlinear least squares.
- Dense Gaussian REML fitting under a constant-mean, isotropic covariance model.
- Pair-count weighted residuals and optional fixed nugget.
- Directional pair filtering by azimuth and cross-track bandwidth.
- Matheron, Cressie-Hawkins and Dowd empirical estimators.
- Fixed geometric anisotropy distance transform with major-axis azimuth and minor/major range ratio in directional binning and REML.
- Genton (1998) Q_n-based robust semivariance using the prescribed order statistic of all pairwise increment differences within each lag class.

## Tests

Tests cover zero lag, model sill behaviour, directional filtering, robust estimator non-negativity, hand-computed Genton order-statistic values, Dowd median-scale formula and outlier fixture, sign/translation invariance, directional Genton pair grouping, synthetic spherical parameter recovery, fixed-nugget fitting, seeded synthetic REML fitting, and invalid/degenerate inputs. CI status is tied to the commit containing the tests.

REML uses the restricted likelihood with the generalized least-squares estimate of the constant mean. The dense Cholesky implementation is O(n³) in time and O(n²) in memory; it is not a scalable GP method.

## Bibliography

- Genton, M. G. (1998). Highly robust variogram estimation. *Mathematical Geology*, 30(2), 213–221. https://marcgenton.github.io/1998.G.MG.1.pdf
- Mardia, K. V., & Marshall, R. J. (1984). Maximum likelihood estimation of models for residual covariance in spatial regression. *Biometrika*, 71(1), 135–146.
- Cressie, N., & Lahiri, S. N. (1996). Asymptotics for REML estimation of spatial covariance parameters. *Journal of Statistical Planning and Inference*, 50, 327–341.

## Limits

Automatic anisotropy parameter fitting, nested structures, Matérn models or parameter uncertainty are not implemented. Anisotropy orientation and ratio are supplied by the analyst. Pair-count weighting is a teaching default, not a universal optimum. Genton is O(m²) in the number m of increments in a lag class and is not intended for very large bins. Its Gaussian consistency factor is fixed at 2.2191.
