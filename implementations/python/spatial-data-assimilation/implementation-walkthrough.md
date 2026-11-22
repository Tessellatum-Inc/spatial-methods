# Spatial data assimilation: implementation walkthrough

## 1. What the example demonstrates

This example joins four parts that are often documented separately:

1. a spatially indexed state;
2. a model that advances that state between observation times;
3. observation operators that map the state to sensor measurements;
4. sequential uncertainty-aware updates followed by a free-running forecast.

The field is scalar and one-dimensional so every matrix can be inspected. The same architecture generalises conceptually to larger state vectors, but the computational strategy and physical model would need to change.

## 2. Build the evolution operator

The continuous model is constant-velocity advection plus diffusion:

\[
\frac{\partial c}{\partial t}
+u\frac{\partial c}{\partial x}
=\kappa\frac{\partial^2c}{\partial x^2}.
\]

For positive velocity, first-order upwind advection uses the cell to the left; for negative velocity it uses the cell to the right. Diffusion uses the centred second difference. On a periodic grid, indices wrap at the domain boundary.

Define the Courant and diffusion numbers

\[
C=\frac{|u|\Delta t}{\Delta x},\qquad
D=\frac{\kappa\Delta t}{\Delta x^2}.
\]

The explicit update is monotone under the sufficient condition

\[
C+2D\leq1.
\]

The transition matrix is row-stochastic and, because the periodic stencil is circulant, also column-stochastic. Therefore it preserves a constant field and the sum of cell values. Those invariants are tested. They are useful checks, not a proof that this coarse discretisation accurately resolves every physical regime.

## 3. Represent the sensors

A point sensor generally lies between grid-cell centres. The observation operator uses linear interpolation between the two adjacent periodic cell-centred state values. Each row sums to one, so a constant field is observed without a location-dependent bias.

This operator is a simplified measurement model. A satellite pixel, lidar footprint, acoustic path integral or areal average needs a different operator that reflects its spatial support and measurement physics.

## 4. Run the forecast-analysis cycle

At every observation time, propagate the mean and covariance:

\[
\mathbf{x}_k^f=F\mathbf{x}_{k-1}^a,\qquad
P_k^f=FP_{k-1}^aF^\mathsf{T}+Q.
\]

If an observation is present, compute the innovation and update:

\[
\mathbf{d}_k=\mathbf{y}_k-H_k\mathbf{x}_k^f,\qquad
S_k=H_kP_k^fH_k^\mathsf{T}+R_k,
\]

\[
K_k=P_k^fH_k^\mathsf{T}S_k^{-1},\qquad
\mathbf{x}_k^a=\mathbf{x}_k^f+K_k\mathbf{d}_k.
\]

The code solves the linear system involving \(S_k\) instead of explicitly inverting it. The posterior covariance uses the Joseph form,

\[
P_k^a=(I-K_kH_k)P_k^f(I-K_kH_k)^\mathsf{T}
+K_kR_kK_k^\mathsf{T}.
\]

A missing observation skips only the analysis step. The model still advances and process uncertainty still accumulates.

## 5. Continue beyond the observations

After the final analysis, the example propagates the state and covariance without further updates. This is a genuine model-based forecast from the supplied transition model, not a claim of long-range physical forecast skill. Forecast uncertainty generally grows as process noise is propagated.

The output keeps forecast priors, analysis posteriors and free forecasts separate. That separation prevents retrospective smoothed values or post-observation analyses from being mislabelled as forecasts issued earlier.

## 6. Tests and expected invariants

The tests check:
- constant-field preservation and conservation on the periodic grid;
- correct upwind direction for negative velocity;
- rejection of an unstable explicit time step;
- interpolation and periodic wrap-around at sensor locations;
- forecast and analysis array dimensions, missing-observation behaviour and free forecast horizons;
- covariance symmetry and positive-semidefinite posterior covariance;
- rejection of invalid covariance matrices and inconsistent observation dimensions.

Run the package tests with Python and NumPy installed. A successful test suite verifies these contracts for the fixtures; it does not establish application-level forecast skill.

## 7. Adapting the example responsibly

Before replacing the toy model with a real application:
- define the measurand and state variables;
- choose governing equations and boundary conditions;
- derive or validate the discretised transition and its stability;
- model the sensor footprint and temporal integration;
- estimate process and observation error from defensible evidence;
- account for missingness, latency, calibration and correlated errors;
- use chronological forecast origins and independent held-out observations;
- verify uncertainty calibration as well as point accuracy.

Do not use the periodic boundary condition for a bounded river, coastline, city or catchment merely because it is convenient. Replace it with physically justified boundary conditions and validate the numerical scheme for that problem.
