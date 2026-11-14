# Nonlinear state-estimation baselines

This package contains small NumPy implementations of the extended Kalman filter (EKF) and scaled unscented Kalman filter (UKF) for discrete-time additive-noise state-space models.

## Model

`x[k+1] = f(x[k]) + w[k]`, `z[k] = h(x[k]) + v[k]`, with zero-mean process and observation noise covariances Q and R. The process model preserves state dimension; observation dimension may differ.

## Implemented

- EKF prediction/update with user-supplied analytic Jacobians and Joseph-form covariance update.
- Scaled UKF using 2n+1 state sigma points and additive Q/R.
- Single-step functions expose innovation, innovation covariance, gain and predicted moments.
- Sequence runners return filtered means, covariances and per-observation diagnostics.

Run tests from this directory with `python -m pytest -q`.

## Explicit limits

These are teaching baselines, not a complete navigation filter. They omit control inputs, non-additive or correlated noise, angle-aware residuals/means, adaptive noise estimation, gating/outlier rejection, square-root UKF, augmented-noise UKF, smoothing, and manifold states. The EKF requires correct Jacobians. The UKF uses scaled unscented-transform parameters and can become numerically fragile for poor scaling or covariance choices. Neither filter is generally an exact Bayesian solution for nonlinear/non-Gaussian systems. Model and noise assumptions dominate results; covariance outputs are conditional on those assumptions.
