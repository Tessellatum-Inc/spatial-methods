# Spatial data assimilation: implementation walkthrough

## 1. Model-to-observation architecture

The package separates a spatial state, its evolution operator, measurement
operators, an uncertainty-aware analysis update and held-out forecast scoring.
The uniform-grid model is a transparent baseline; the nonuniform finite-volume
model demonstrates how conservation and observation geometry change when
cell widths and face properties vary.

## 2. Nonuniform conservative transport

Let \(\Delta x_i\) be the width of cell \(i\). The face flux is

\[
\mathcal F_{i+1/2}
=u_{i+1/2}c^{\mathrm{upwind}}_{i+1/2}
-\kappa_{i+1/2}
\frac{c_{i+1}-c_i}{(\Delta x_i+\Delta x_{i+1})/2}.
\]

The finite-volume tendency is

\[
\dot c_i=-\frac{\mathcal F_{i+1/2}-\mathcal F_{i-1/2}}{\Delta x_i}.
\]

Every internal face flux is subtracted from one cell and added to its
neighbour. Thus the semi-discrete operator conserves width-weighted mass.
Periodic closure makes the same cancellation hold at the seam. The explicit
matrix is checked for non-negative entries before return; this is a sufficient
positivity restriction, not a universal stability criterion for all schemes.

The model accepts face-by-face velocity and diffusivity. A spatially varying
velocity can change sign, so the upwind donor cell is selected independently
at each face. Diffusivity is non-negative. The periodic sensor operator uses
actual cell-centre coordinates and interpolates across the seam using
periodic copies of the first or last centre.

## 3. Nonperiodic zero-flux boundary contract

The nonperiodic operator assembles only the n-1 interior face fluxes. At both
domain ends the total flux is prescribed as zero. This means there is no
advective or diffusive mass transfer through either boundary. Each interior
face contributes equal and opposite mass changes to its adjacent cells, so

\[
\sum_i \Delta x_i c_i^{n+1}=\sum_i \Delta x_i c_i^n.
\]

Zero total flux is not interchangeable with a zero-gradient ghost cell when
the boundary velocity is nonzero. Prescribed inflow/outflow and distributed
source/sink terms require an explicit mass-budget extension and are not
folded into this homogeneous linear operator.

## 4. Filtering and validation separation

The filter returns forecast priors and analysis posteriors separately. A
held-out verification stream is supplied only to the verification function;
those observations are never passed to the assimilation update. Scores are
calculated after applying each lead's observation operator to the free
forecast state:

\[
e_{k,j}=H_{k,j}\widehat{\mathbf x}^{\,f}_k-y_{k,j}.
\]

The reported metrics are

\[
\mathrm{Bias}_k=\frac{1}{N_k}\sum_j e_{k,j},\qquad
\mathrm{MAE}_k=\frac{1}{N_k}\sum_j|e_{k,j}|,
\]

\[
\mathrm{RMSE}_k=
\sqrt{\frac{1}{N_k}\sum_j e_{k,j}^2}.
\]

Each lead's sample count is reported. If no independent observations are
available at a lead, metrics are NaN and count is zero rather than silently
substituting an analysis observation.

## 5. Analytical transport checks

For a periodic Fourier mode, pure constant-velocity advection has exact
solution \(c(x,t)=\sin(k(x-ut))\) when the initial state is \(\sin(kx)\).
Pure diffusion has exact solution
\(c(x,t)=\exp(-\kappa k^2t)\sin(kx)\). Refinement tests compare numerical
states with these solutions. Upwind advection is first order in space and
centred diffusion is second order in space; for the diffusion test, the time
step is scaled with \(\Delta x^2\) so temporal error does not dominate the
spatial convergence check.

## 6. Tests and interpretation

Tests exercise analytical convergence for periodic advection and diffusion, conservation under spatially varying face velocity,
constant-field preservation under divergence-free flow, local upwind
direction, nonuniform interpolation, periodic seam handling, positivity
restrictions and held-out score calculations. They are numerical contract
tests for this simplified model, not proof that the transport equation suits
a river, coast, atmosphere, city or other application.

Before application, replace periodic boundaries with physically defensible
boundaries; validate the transport scheme against analytical or trusted
numerical benchmarks; model actual sensor support and timing; estimate
process and observation error; and evaluate forecasts using chronological
held-out data excluded from assimilation and calibration.
