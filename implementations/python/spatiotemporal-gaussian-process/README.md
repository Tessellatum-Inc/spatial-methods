# Exact separable spatiotemporal Gaussian-process regression

This NumPy package provides a small-data exact Gaussian-process baseline for observations indexed by projected Euclidean coordinates and linear time.

The covariance is variance times exp(-spatial distance / spatial scale) times exp(-absolute time lag / temporal scale). It is separable: spatial and temporal dependence multiply without interaction. This differs from the companion Gneiting-class nonseparable covariance construction.

The predictor conditions a zero-mean Gaussian process on training values, an observation-noise variance, and a separate numerical Cholesky jitter. It returns posterior mean, full latent predictive covariance and marginal variance. Set include_observation_noise=True to add observation noise to the returned predictive covariance.

## Run

    python -m pip install -r requirements.txt
    python -m pytest -q

## Assumptions and limits

- Coordinates must be in one projected Euclidean coordinate system and linear unit. Times must use one consistent linear unit.
- The kernel is stationary, spatially isotropic, separable and uses fixed user-supplied hyperparameters.
- The prior mean is zero; centre the response or extend the model if a trend is required.
- Dense matrices require O(n²) memory and O(n³) factorisation time.
- Jitter is numerical stabilisation, not a fitted nugget or measurement-error estimate.
- Hyperparameter fitting, anisotropy, nonstationary means/covariances, nonseparable covariance fitting, INLA/SPDE, functional data analysis and large-data approximations are not implemented.
- Model-based uncertainty is not a distribution-free coverage guarantee.
