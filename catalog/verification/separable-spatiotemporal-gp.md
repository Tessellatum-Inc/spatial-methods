# Verification — separable spatiotemporal Gaussian process

**Status:** Partial implementation of the separable spatiotemporal GP subset.

## Implemented

- Product exponential covariance on projected Euclidean space crossed with linear time.
- Dense exact zero-mean GP conditioning using Cholesky factorisation.
- Separate observation-noise variance and numerical jitter.
- Posterior mean, full latent predictive covariance and marginal variance.
- Optional observation-noise contribution to predictive covariance.

## Independent checks

- Hand-computed one-training-observation posterior moments.
- Exact product-kernel arithmetic for known spatial and temporal lags.
- Irregular-design covariance symmetry and eigenvalue checks.
- Posterior covariance symmetry and positive-semidefinite check.
- Observation-noise effect on posterior mean and latent versus observed variance.
- Shape, finiteness, parameter and coordinate-dimension validation.

Run from this package directory: python -m pytest -q.

## Not covered

Kernel hyperparameter estimation, nonzero/trend mean models, anisotropic or nonstationary covariance, nonseparable fitting, INLA/SPDE, functional data analysis, Bayesian model comparison and scalable GP approximations.
