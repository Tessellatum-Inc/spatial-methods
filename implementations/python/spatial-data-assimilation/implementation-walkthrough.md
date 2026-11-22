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



## 9. Two-dimensional sources, sinks and prescribed boundary fluxes

The forced 2-D interface adds a source rate to each cell and four arrays of
boundary total-flux densities. Positive flux is defined inward on the left
and bottom edges and outward on the right and top edges. Since a boundary
face has a physical length, each flux density is multiplied by its edge
length before it changes cell mass. For cell areas
\(A_{ij}=\Delta x_i\Delta y_j\), summing the update yields

\[
\Delta M=\Delta t\left[
\sum_{ij}A_{ij}s_{ij}
+\sum_j\Delta y_j(F_{L,j}-F_{R,j})
+\sum_i\Delta x_i(F_{B,i}-F_{T,i})
\right].
\]

This explicit orientation convention avoids treating a flux density as
already integrated mass flow. The four edge arrays have lengths
\(n_y,n_y,n_x,n_x\); corner cells receive both adjacent edge contributions.
The routine validates shapes, finite values, non-negative resulting state
and the complete mass budget. It does not infer physical boundary fluxes
from external concentrations or implement 2-D Robin/Dirichlet boundary
closures; prescribed fluxes are the interface when those total fluxes are
known from an upstream physical model or measurement.



## 10. Two-dimensional point observation operator

The point-observation matrix is built from the actual cell-centre coordinate
vectors rather than assuming uniform cell spacing. For an observation inside
one centre-to-centre rectangle, let its local fractions be
[
\alpha=\frac{x-x_i}{x_{i+1}-x_i},\qquad
\beta=\frac{y-y_j}{y_{j+1}-y_j}.
]
Its four bilinear weights are
[
(1-\alpha)(1-\beta),\quad
\alpha(1-\beta),\quad
(1-\alpha)\beta,\quad
\alpha\beta.
]
They are non-negative and sum to one, so the operator preserves a constant
field. Bilinear interpolation also reproduces any field of the form
(a+bx+cy+dxy) exactly within each rectangle; the tests include the affine
subset. The state is flattened in C order, with x index first and
(k=i n_y+j). Observations outside the convex hull of cell centres are
rejected: extrapolation would require a separate, explicit boundary model.
The operator describes point samples only; finite sensor footprints and
correlated measurement errors require their own observation models.


## 11. Two-dimensional ensemble assimilation

The integrated path first advances each prior member with the 2-D conservative
finite-volume step, preserving the member-wise area-weighted mass budget under
closed boundaries. It then flattens each forecast field in NumPy C order and
applies the point-sensor matrix. This ordering must match the operator's flat
index k=i*n_y+j; otherwise the observation geometry is permuted.

For m ensemble members, let A=X^f-xbar^f and Y=HA. With R=LL^T, whitening
gives Y_w=L^{-1}Y and d_w=L^{-1}(y-H*xbar^f). The ETKF solves
\[
Cw=Y_w^T d_w,\qquad C=(m-1)I_m+Y_w^T Y_w,
\]
then updates xbar^a=xbar^f+Aw. If C=V Lambda V^T, the symmetric anomaly
transform is
\[
T=V\operatorname{diag}\left(\sqrt{(m-1)/\lambda_i}\right)V^T,
\qquad A^a=AT.
\]
The implementation uses Cholesky whitening, a linear solve for weights and
a symmetric eigendecomposition. It avoids both an n_state-by-n_state
covariance and a dense n_state-by-n_state transport matrix.

The forecast ensemble is stored as (nx, ny, m); each member is advanced
separately, with common face fields and optional common sources/boundary
fluxes. The observation matrix is (n_obs, nx*ny), using C-order flattening.
Member mass budgets are returned. The analysis is an unconstrained Gaussian
update and may contain negative values even though forecast inputs must be
non-negative. No clipping is applied; a positivity-preserving analysis,
localisation and inflation are not yet implemented.
