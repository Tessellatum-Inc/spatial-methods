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
the boundary velocity is nonzero. Prescribed inflow/outflow and distributed source/sink terms are handled by a separate forced step, not folded into this homogeneous linear operator.


## 4. Prescribed forcing and boundary mass budget

The forced step leaves the homogeneous transport matrix intact and applies
cell source/sink rates and boundary fluxes explicitly. Both boundary fluxes
are oriented in positive x: positive left flux enters, positive right flux
leaves. Summing the finite-volume equations over cells cancels every interior
face contribution and gives

\[
M^{n+1}-M^n
=\Delta t\left(\sum_i\Delta x_i s_i+F_L-F_R\right).
\]

The API checks this identity against the actual updated state and returns the
budget terms and residual. Prescribed boundary fluxes are not inferred from
boundary concentrations; a physical inflow/outflow closure remains an
application-specific responsibility. A sink or boundary outflow that drives
any cell negative causes rejection rather than clipping.

## 5. Filtering and validation separation

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

## 6. Analytical transport checks

For a periodic Fourier mode, pure constant-velocity advection has exact
solution \(c(x,t)=\sin(k(x-ut))\) when the initial state is \(\sin(kx)\).
Pure diffusion has exact solution
\(c(x,t)=\exp(-\kappa k^2t)\sin(kx)\). Refinement tests compare numerical
states with these solutions. Upwind advection is first order in space and
centred diffusion is second order in space; for the diffusion test, the time
step is scaled with \(\Delta x^2\) so temporal error does not dominate the
spatial convergence check.

## 7. Tests and interpretation

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


## Physical boundary closures

At advective inflow, the external concentration supplies the upwind state;
at outflow, the adjacent interior concentration is used. Diffusion is
independently set to zero normal gradient or Dirichlet concentration. The
Dirichlet gradient is evaluated over the boundary half-cell. The resulting
total boundary fluxes obey
\[
M^{n+1}-M^n=\Delta t\left(\sum_i\Delta x_i s_i+F_L-F_R\right).
\]
The implementation checks this budget. The prescribed-flux interface remains
separate and is appropriate when the total boundary flux is known directly.


## 8. Two-dimensional rectilinear transport

The 2-D implementation generalises the same conservative face-flux
construction to cell areas \(A_{ij}=\Delta x_i\Delta y_j\). An x-normal
face has length \(\Delta y_j\), and a y-normal face has length
\(\Delta x_i\). For every interior face, its integrated flux is subtracted
from one adjacent cell's mass tendency and added to the other's. The four
outer boundaries are closed with zero total flux, so summing over all cells
cancels every internal contribution and preserves area-weighted mass.

The update is evaluated directly on arrays rather than assembling a dense
transition matrix. Its local positivity condition is
\[
\Delta t\,\frac{\sum_{f\,\mathrm{outgoing}} a_f\ell_f}{A_{ij}}
\leq 1,
\]
where \(a_f\) is the non-negative coefficient multiplying the cell's own
concentration in its outward flux. This condition keeps the explicit
self-weight non-negative; the routine rejects a violating time step. A
homogeneous-Neumann product cosine benchmark checks convergence to the
analytical two-dimensional diffusion decay. The current operator is
orthogonal/rectilinear, scalar, first order in advection, and closed at all
outer boundaries; it does not yet represent open boundaries, sources,
unstructured meshes, or multidimensional data-assimilation coupling.
