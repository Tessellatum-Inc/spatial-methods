# Spatial data-assimilation examples

This package connects spatial state evolution, sensor observation operators,
sequential linear-Gaussian assimilation and independent forecast verification.
The examples are deliberately small and inspectable, not operational prediction
systems.

## 1. Uniform periodic reference model

The first model is a scalar field on a uniform periodic one-dimensional grid.
Its continuous idealisation is

\[
\frac{\partial c}{\partial t}
+u\frac{\partial c}{\partial x}
=\kappa\frac{\partial^2c}{\partial x^2}.
\]

It uses first-order upwind advection and centred diffusion with an explicit
time step, enforcing

\[
\frac{|u|\Delta t}{\Delta x}
+2\frac{\kappa\Delta t}{\Delta x^2}\leq 1.
\]

Point observations are linearly interpolated from cell centres. The sequential
filter uses forecast-analysis equations and a Joseph covariance update.
Missing observations skip analysis but not model propagation.

## 2. Nonuniform finite-volume model

For cell widths \(\Delta x_i\), the second model uses conservative face fluxes.
At face \(i+1/2\), between cells \(i\) and \(i+1\),

\[
\mathcal F_{i+1/2}
=u_{i+1/2}c^{\mathrm{upwind}}_{i+1/2}
-\kappa_{i+1/2}
\frac{c_{i+1}-c_i}{d_{i+1/2}},
\qquad
d_{i+1/2}=\frac{\Delta x_i+\Delta x_{i+1}}{2}.
\]

The cell tendency is

\[
\frac{dc_i}{dt}
=-\frac{\mathcal F_{i+1/2}-\mathcal F_{i-1/2}}{\Delta x_i}.
\]

Velocity and diffusivity vary from face to face. The explicit transition is
accepted only when it is non-negative (within round-off tolerance), a
sufficient positivity restriction for this monotone finite-volume step. It
preserves constants and conserves width-weighted mass,
\(\sum_i \Delta x_i c_i\). Sensor observations interpolate between actual
nonuniform cell centres, including across the periodic seam.

## 3. Assimilation and held-out verification

The assimilation function accepts time-varying observation tuples (y, H, R)
or None. The forecast prior and analysis posterior remain separate.
The verification function scores free forecasts against a separate sequence
of held-out (y, H) observations. It reports sample count, bias, mean absolute
error and root mean square error at each lead. It does not modify the forecast
or use verification observations in the filter.

For credible evaluation, held-out observations must be excluded from
assimilation, parameter fitting and model selection at the forecast origin.
Use chronological forecast origins, retain the forecast issue time, and report
sample counts alongside scores. A low score on a synthetic fixture is a
software test, not evidence of real-world predictive skill.

## API

- periodic_advection_diffusion_operator(...)
- periodic_point_observation_operator(...)
- periodic_nonuniform_advection_diffusion_operator(...)
- periodic_nonuniform_point_observation_operator(...)
- run_linear_spatial_assimilation(...)
- verify_spatial_forecasts(...)

Run python -m pip install -r requirements.txt followed by python -m pytest -q
from this directory.

## Scope and limitations

Both dynamics examples are one-dimensional and periodic. The nonuniform model
assumes cell-centred scalar states, time-constant face fields during each step,
explicit first-order upwind advection and two-point centred diffusion. It does
not implement non-periodic boundaries, source/sink terms, higher-order flux
limiters, nonlinear flow, parameter estimation, ensemble localisation,
correlated process-observation errors or sensor-footprint physics. Process
covariance is supplied by the caller. Real applications require physically
justified boundaries, forcing, sensor models, calibrated error covariance,
latency handling and independent out-of-sample verification.
