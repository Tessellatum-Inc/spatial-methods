# State-estimation and data-assimilation baselines

This package contains small NumPy implementations of the extended Kalman filter (EKF) and scaled unscented Kalman filter (UKF) for discrete-time additive-noise state-space models.

## Model

`x[k+1] = f(x[k]) + w[k]`, `z[k] = h(x[k]) + v[k]`, with zero-mean process and observation noise covariances Q and R. The process model preserves state dimension; observation dimension may differ.

## Implemented

- EKF prediction/update with user-supplied analytic Jacobians and Joseph-form covariance update.
- Scaled UKF using 2n+1 state sigma points and additive Q/R.
- Single-step functions expose innovation, innovation covariance, gain and predicted moments.
- Sequence runners return filtered means, covariances and per-observation diagnostics.
- Bootstrap particle filter with stable log-weight normalisation, ESS-triggered systematic resampling, and stored weighted particle histories.
- Offline FFBSi particle smoother that samples complete trajectories backward using caller-supplied transition log densities; returns trajectories, particle indices and smoothed marginal moments.

Run tests from this directory with `python -m pytest -q --import-mode=importlib`.

## Explicit limits

These are teaching baselines, not a complete navigation filter. They omit control inputs, non-additive or correlated noise, angle-aware residuals/means, adaptive noise estimation, gating/outlier rejection, square-root UKF, augmented-noise UKF, nonlinear RTS smoothing, and manifold states. The EKF requires correct Jacobians. The UKF uses scaled unscented-transform parameters and can become numerically fragile for poor scaling or covariance choices. Neither filter is generally an exact Bayesian solution for nonlinear/non-Gaussian systems. Model and noise assumptions dominate results; covariance outputs are conditional on those assumptions.


## Ensemble transform Kalman filter

The `ensemble_square_root.py` module implements a batch linear ETKF analysis using a symmetric ensemble-space square-root transform. It updates the ensemble deterministically without perturbed observations and supports a full observation-error covariance matrix. This is a teaching implementation; localization, inflation, cycling and nonlinear observation operators remain outside scope. See the [ETKF lesson](../../../methods/ensemble-transform-kalman-filter.md) and [lab notebook](../../../notebooks/ensemble-transform-kalman-filter-lab.ipynb).



## Stochastic ensemble Kalman filter

The `enkf_analysis` function provides the perturbed-observation stochastic
EnKF for a batch linear observation operator. It computes sample forecast
and cross-covariances, forms the Kalman gain, draws an independent
observation perturbation with covariance R for each ensemble member, and
updates each member. This differs from ETKF: the stochastic EnKF uses
perturbed observations, while ETKF uses a deterministic ensemble-space
square-root transform. Both are analysis steps only; neither includes model
forecast propagation, localization or inflation.


See the separate [stochastic perturbed-observation EnKF method](../../../methods/stochastic-ensemble-kalman-filter.md) and [verification record](../../../catalog/verification/stochastic-ensemble-kalman-filter.md).
