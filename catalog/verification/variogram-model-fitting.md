# Verification record: variogram model fitting

## Implemented scope

- Spherical, exponential, Gaussian and Matérn semivariogram structures (fixed smoothness nu).
- Nugget, partial sill and range fitted with bounded nonlinear least squares.
- Dense Gaussian REML fitting under a constant-mean, isotropic covariance model.
- Pair-count weighted residuals and optional fixed nugget.
- Directional pair filtering by azimuth and cross-track bandwidth.
- Matheron, Cressie-Hawkins and Dowd empirical estimators.
- Fixed geometric anisotropy distance transform in directional binning and REML, plus optional joint REML estimation of azimuth and minor/major range ratio.
- Genton (1998) Q_n-based robust semivariance using the prescribed order statistic of all pairwise increment differences within each lag class.

## Tests

Tests cover zero lag, model sill behaviour, directional filtering, robust estimator non-negativity, hand-computed Genton order-statistic values, Dowd median-scale formula and outlier fixture, sign/translation invariance, directional Genton pair grouping, synthetic spherical parameter recovery, fixed-nugget fitting, seeded synthetic REML fitting, closed-form Matérn nu=0.5/1.5/2.5 covariance checks, Matérn REML fitting, bounded automatic-anisotropy fitting against the fixed-start objective, and invalid/degenerate inputs. CI status is tied to the commit containing the tests.

REML uses the restricted likelihood with the generalized least-squares estimate of the constant mean. The dense Cholesky implementation is O(n³) in time and O(n²) in memory; it is not a scalable GP method.

## Bibliography

- Genton, M. G. (1998). Highly robust variogram estimation. *Mathematical Geology*, 30(2), 213–221. https://marcgenton.github.io/1998.G.MG.1.pdf
- Mardia, K. V., & Marshall, R. J. (1984). Maximum likelihood estimation of models for residual covariance in spatial regression. *Biometrika*, 71(1), 135–146.
- Cressie, N., & Lahiri, S. N. (1996). Asymptotics for REML estimation of spatial covariance parameters. *Journal of Statistical Planning and Inference*, 50, 327–341.

## Limits

Automatic anisotropy fitting is available in dense REML, with azimuth in [0, 180) degrees and minor/major ratio in [0.1, 1]. The search is local numerical optimization, not a guarantee of a global optimum. Nested structures, Matérn smoothness estimation and parameter uncertainty are not implemented. Pair-count weighting is a teaching default, not a universal optimum. Genton is O(m²) in the number m of increments in a lag class and is not intended for very large bins. Its Gaussian consistency factor is fixed at 2.2191.
