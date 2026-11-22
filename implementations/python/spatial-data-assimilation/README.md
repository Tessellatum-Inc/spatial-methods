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
conserves width-weighted mass, \(\sum_i \Delta x_i c_i\), for arbitrary
periodic face velocities. A constant concentration is preserved when the
velocity field is discretely divergence-free (constant face velocity in this
one-dimensional periodic setting); spatially varying velocity can compress or
expand the concentration field. Sensor observations interpolate between actual
nonuniform cell centres, including across the periodic seam.

## 3. Nonperiodic zero-flux boundaries

A separate nonperiodic operator accepts the n-1 interior face fields on an
n-cell grid. The total advective-diffusive flux at each domain end is set to
zero. This also prevents advective mass from crossing the boundary; it is not
merely a zero diffusive gradient. The finite-volume update conserves
sum_i Delta x_i c_i. The explicit step is accepted only when its transition
matrix is non-negative. A constant concentration is preserved for pure
diffusion; with interior advection, boundary-adjacent concentrations can
change because the imposed zero total boundary flux is not the same as
extending a constant advective flux through the boundary.


## 4. Prescribed sources, sinks and boundary fluxes

The forced nonperiodic step is separate from the homogeneous transition
operator. It accepts a cell-wise source rate \(s_i\) and prescribed total
boundary fluxes \(F_L,F_R\), both oriented in the positive x direction.
Thus positive \(F_L\) is inflow and positive \(F_R\) is outflow. The
mass balance is

\[
M^{n+1}-M^n
=\Delta t\left(\sum_i\Delta x_i s_i+F_L-F_R\right),
\qquad M=\sum_i\Delta x_i c_i.
\]

Boundary fluxes are imposed values, not computed from a ghost-cell or
boundary-state closure. Source rates may be negative (sinks), but a step is
rejected if it would produce a negative concentration; values are never
clipped because clipping would break the stated mass budget. The routine
returns initial/final mass, source and boundary contributions, expected mass
change and the budget residual.

## 5. Assimilation and held-out verification

The assimilation function accepts time-varying observation tuples (y, H, R)
or None. The forecast prior and analysis posterior remain separate.
The verification function scores free forecasts against a separate sequence
of held-out (y, H) observations. It reports sample count, bias, mean absolute
error and root mean square error at each lead. It does not modify the forecast
or use verification observations in the filter.

## Analytical numerical checks

The test suite also compares the uniform periodic operators with exact Fourier
solutions. For pure advection, a sinusoid translates by \(u t\); for pure
diffusion, a mode \(\sin(kx)\) decays by \(\exp(-\kappa k^2t)\). Refinement
tests check decreasing error and expected order-of-magnitude convergence for
first-order upwind advection and centred diffusion under a time step scaled
with \(\Delta x^2\). These are discretisation checks for idealised equations,
not validation of a physical application.

For credible evaluation, held-out observations must be excluded from
assimilation, parameter fitting and model selection at the forecast origin.
Use chronological forecast origins, retain the forecast issue time, and report
sample counts alongside scores. A low score on a synthetic fixture is a
software test, not evidence of real-world predictive skill.

## API

- periodic_advection_diffusion_operator(...)
- periodic_point_observation_operator(...)
- periodic_nonuniform_advection_diffusion_operator(...)
- nonperiodic_nonuniform_advection_diffusion_operator(...)\n- nonperiodic_nonuniform_advection_diffusion_step(...)\n- nonperiodic_nonuniform_advection_diffusion_step_with_boundaries(...)
- periodic_nonuniform_point_observation_operator(...)
- run_linear_spatial_assimilation(...)
- verify_spatial_forecasts(...)

Run python -m pip install -r requirements.txt followed by python -m pytest -q
from this directory.

## Scope and limitations

The dynamics examples are one-dimensional. The periodic models use periodic closure; the nonperiodic operator implements zero total boundary flux only. The nonuniform models
assume cell-centred scalar states, time-constant face fields during each step,
explicit first-order upwind advection and two-point centred diffusion. It does
not implement non-periodic boundaries, higher-order flux
limiters, nonlinear flow, parameter estimation, ensemble localisation,
correlated process-observation errors or sensor-footprint physics. Process
covariance is supplied by the caller. Real applications require physically
justified boundaries, forcing, sensor models, calibrated error covariance,
latency handling and independent out-of-sample verification.


## Physical boundary closures

The boundary-closed step separates advective and diffusive boundary physics.
Advective inflow uses a prescribed external concentration; advective outflow
uses the adjacent interior cell as the upwind state. With positive-x
orientation, left inflow and right outflow have positive velocity, while
right inflow and left outflow have negative velocity. Diffusion independently
supports zero normal gradient or a Dirichlet concentration. For Dirichlet
values the boundary gradient uses the half-cell distance:
\[
F_{L,d}=-\kappa_L\frac{c_0-c_L}{\Delta x_0/2},\qquad
F_{R,d}=-\kappa_R\frac{c_R-c_{n-1}}{\Delta x_{n-1}/2}.
\]
The actual total boundary fluxes enter the returned mass budget. Inflow
values are required only when velocity points inward; outflow uses the
interior state. This is a first-order 1-D closure; Robin conditions and
higher-order radiation conditions are not included. The prescribed-total-
flux step remains separate for externally known fluxes.
