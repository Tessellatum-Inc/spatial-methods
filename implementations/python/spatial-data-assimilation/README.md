# Low-dimensional spatial data-assimilation example

This package connects a physical spatial transition model, sensor observation
operators, sequential linear-Gaussian assimilation and a free-running forecast.
It is deliberately small enough to inspect and test, not an operational
environmental prediction system.

## Model

The state is a scalar field on a uniform periodic one-dimensional grid. Its
continuous idealisation is

\[
\frac{\partial c}{\partial t}
+u\frac{\partial c}{\partial x}
=\kappa\frac{\partial^2c}{\partial x^2}.
\]

The numerical transition uses first-order upwind advection and centred
diffusion with an explicit time step. It enforces the sufficient restriction

\[
\frac{|u|\Delta t}{\Delta x}
+2\frac{\kappa\Delta t}{\Delta x^2}\leq 1.
\]

The update matrix is periodic and non-negative under this restriction,
preserves constant fields and conserves the grid sum. Point observations are
mapped to cell-centred state values by a linear interpolation matrix \(H\).

The sequential cycle applies

\[
\mathbf{x}_k^f=F\mathbf{x}_{k-1}^a,\quad
P_k^f=FP_{k-1}^aF^\mathsf{T}+Q,
\]

\[
\mathbf{d}_k=\mathbf{y}_k-H_k\mathbf{x}_k^f,\quad
S_k=H_kP_k^fH_k^\mathsf{T}+R_k,
\]

\[
K_k=P_k^fH_k^\mathsf{T}S_k^{-1},\quad
\mathbf{x}_k^a=\mathbf{x}_k^f+K_k\mathbf{d}_k.
\]

The implementation solves the innovation system rather than explicitly
inverting \(S_k\), and uses the Joseph covariance update. Sensor locations and
observation-error covariance may vary by time. Missing observations skip the
analysis update but do not skip model propagation.

## API

- periodic_advection_diffusion_operator builds one stable model step.
- periodic_point_observation_operator builds a periodic point-sensor
  interpolation operator.
- run_linear_spatial_assimilation runs the forecast-analysis cycle and can
  propagate a free forecast beyond the last observation.

Each observation entry is None or a (y, H, R) tuple. Outputs separate forecast
priors, analysis posteriors, innovations and post-analysis forecasts.

## Reproducibility

Run python -m pip install -r requirements.txt and python -m pytest -q
from this directory.

## Scope and limitations

This is a linear-Gaussian, one-dimensional, periodic, constant-coefficient
teaching model. It does not model variable velocity/diffusivity, nonlinear
dynamics, parameter estimation, irregular grids, correlated process-observation
errors, localization, ensembles, adaptive noise estimation or real sensor
physics. Process covariance Q is supplied by the caller, not inferred from
unresolved physical processes. Forecast credibility depends on governing
equations, parameterisation, forcing and boundary assumptions.

This demonstrates a complete small forecast-analysis cycle, not an operational
forecast service. Application use requires domain-specific equations,
calibrated error models, observation operators, latency handling and
independent forecast verification.
