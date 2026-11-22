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
- nonperiodic_nonuniform_advection_diffusion_operator(...)\n- nonperiodic_nonuniform_advection_diffusion_step(...)\n- nonperiodic_nonuniform_advection_diffusion_step_with_boundaries(...)\n- nonperiodic_rectilinear_advection_diffusion_step_2d(...)\n- nonperiodic_rectilinear_advection_diffusion_step_2d_with_forcing(...)
- nonperiodic_rectilinear_point_observation_operator_2d(...)
- periodic_nonuniform_point_observation_operator(...)
- run_linear_spatial_assimilation(...)
- verify_spatial_forecasts(...)

Run python -m pip install -r requirements.txt followed by python -m pytest -q
from this directory.

## Scope and limitations

The 1-D and 2-D dynamics examples use rectilinear cell-centred grids. The periodic models use periodic closure; the nonperiodic operator implements zero total boundary flux only. The nonuniform models
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
supports zero normal gradient, a Dirichlet concentration, or a Robin exchange boundary. For Dirichlet
values the boundary gradient uses the half-cell distance:
\[
F_{L,d}=-\kappa_L\frac{c_0-c_L}{\Delta x_0/2},\qquad
F_{R,d}=-\kappa_R\frac{c_R-c_{n-1}}{\Delta x_{n-1}/2}.
\]
The actual total boundary fluxes enter the returned mass budget. Inflow
values are required only when velocity points inward; outflow uses the
interior state. This is a first-order 1-D closure; Robin exchange uses a non-negative transfer coefficient and ambient concentration. The half-cell diffusive resistance and boundary transfer resistance are combined in series, so the effective conductance is
\[G=\left(h^{-1}+\frac{\Delta x/2}{\kappa}\right)^{-1},\]
with zero conductance when either coefficient is zero. The positive-x diffusive flux is \(-G(c_0-c_\infty)\) at the left and \(+G(c_{n-1}-c_\infty)\) at the right. This is a linear Robin exchange closure, not a general nonlinear radiation condition. The prescribed-total-
flux step remains separate for externally known fluxes.


## 6. Two-dimensional rectilinear finite-volume transport

The 2-D step stores concentration at cell centres on a rectangular grid with
independently nonuniform x- and y-cell widths. The x-face arrays have shape
\((n_x-1,n_y)\); y-face arrays have shape \((n_x,n_y-1)\). Each internal
face uses first-order upwind advection and a two-point centred diffusive
gradient. Flux is multiplied by the physical face length before it is added
to the two adjacent cell mass tendencies with opposite signs.

For cell area \(A_{ij}=\Delta x_i\Delta y_j\), the update is
\[
c_{ij}^{n+1}=c_{ij}^{n}
+\frac{\Delta t}{A_{ij}}
\left(\sum_{f\in\partial V_{ij}} s_{if}\,\ell_f\,\mathcal F_f\right),
\]
where \(s_{if}\) is the outward-orientation sign. All four external
boundaries have zero total flux. Consequently the area-weighted mass
\(\sum_{ij}A_{ij}c_{ij}\) is conserved. The implementation uses O(nx ny)
storage rather than constructing a dense state-transition matrix.

A local outgoing-CFL condition is checked cell by cell. It is sufficient for
a non-negative explicit update with these upwind/two-point face fluxes; a
step that violates it is rejected. The returned mass-budget residual is
checked independently. This is a first-order scalar transport operator on
orthogonal rectilinear grids, not a general unstructured or curvilinear solver.

The analytical test uses a product cosine mode with homogeneous Neumann
boundaries. Its continuous decay is
\(\exp[-\pi^2(\kappa_x+\kappa_y)t]\); grid refinement checks convergence
of the numerical solution. This validates the discrete transport component,
not an environmental model.




## 7. Two-dimensional prescribed forcing and boundary exchange

The forced 2-D step extends the closed-boundary transport operator with
cell-wise source/sink rates and prescribed total boundary flux densities.
Boundary arrays are ordered left, right, bottom, top, with lengths matching
the boundary face counts. Positive left and bottom fluxes enter; positive
right and top fluxes leave. The area-weighted budget is

\[
M^{n+1}-M^n=\Delta t\left[
\sum_{ij}A_{ij}s_{ij}
+\sum_j\Delta y_j(F_{L,j}-F_{R,j})
+\sum_i\Delta x_i(F_{B,i}-F_{T,i})
\right].
\]

The routine checks the actual state change against this budget and rejects
updates that produce negative concentrations. Boundary values are prescribed
total flux densities, not ghost-cell reconstructions or physical boundary
closures; deriving them from inflow/outflow and diffusive exchange physics
remains a separate modelling decision. Corner cells receive contributions
from both intersecting boundary faces.



## 8. Two-dimensional point observation geometry

`nonperiodic_rectilinear_point_observation_operator_2d` maps a cell-centred
state with shape `(nx, ny)` to point observations by bilinear interpolation.
The caller supplies the actual, strictly increasing x- and y-cell-centre
coordinates, so nonuniform spacing is represented directly. The observation
coordinates must lie within the rectangular convex hull of those cell centres;
the operator deliberately rejects extrapolation rather than silently snapping
or extending the field beyond its represented support. State vectorisation is
NumPy C order, with flat index `i * ny + j`.

Each row has four non-negative weights that sum to one (with boundary cases
collapsing to two or one nonzero weights). Therefore constants are preserved,
and an affine field in x and y is reproduced exactly up to floating-point
round-off. This is a point-sensor interpolation operator, not an areal sensor
footprint, line integral, vertical-column measurement, or uncertainty model.
