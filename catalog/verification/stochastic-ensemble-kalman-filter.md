# Verification record: stochastic ensemble Kalman filter

## Implemented scope

- Linear observation operator and finite state-by-member ensemble.
- Sample forecast state and state/observation cross-covariances.
- Full positive-definite observation-error covariance.
- Independent Gaussian observation perturbations per ensemble member.
- Stochastic Kalman analysis update and returned sample posterior moments.

## Tests

Tests compare large-ensemble analysis means and covariances with the
conventional Kalman equations, verify seeded reproducibility and distinct
per-member perturbations, check full observation covariance, and reject
invalid dimensions and non-positive-definite observation covariance.

## Limits

Analysis step only; no forecast model, nonlinear observation operator,
localization, inflation, cycling or model-error treatment. Finite-ensemble
sampling error remains and the algorithm requires a sufficiently large
ensemble for stable covariance estimates.
