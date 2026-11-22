# Hydrographic sensor-chain geometry, trajectory and multi-ping uncertainty

This dependency-free package models a GNSS antenna, IMU, mounted transducer
and acoustic detection point. The static geometry is
\[
\mathbf p_n=\mathbf r_{n,g}+
\mathbf R_{n\leftarrow i}(-\mathbf l_{i,g}+\mathbf l_{i,t}+
\mathbf R_{i\leftarrow t}\mathbf s_t).
\]
The static Jacobian has 18 columns; the two-state time-aligned solver appends
the derivative with respect to timing offset as column 19.

## Multi-epoch navigation trajectory

\`navigation_trajectory.py\` interpolates a sequence of navigation states at
arbitrary observation epochs. Input times must be strictly increasing, with
one GNSS antenna position and one proper rotation matrix per epoch. Position
is piecewise linear; attitude follows the shortest SO(3) geodesic separately
within each bracketing interval. Queries outside the first and last state are
rejected. At an interior knot, the segment beginning at that knot is selected;
the final trajectory epoch is evaluated at the end of the final segment.

For segment \(k\), with \(\Delta t_k=t_{k+1}-t_k\) and
\(\alpha=(t-t_k)/\Delta t_k\),
\[
\mathbf r(t)=(1-\alpha)\mathbf r_k+\alpha\mathbf r_{k+1},
\quad
\mathbf R(t)=\mathbf R_k\exp\left(\alpha\log(
\mathbf R_k^T\mathbf R_{k+1})\right).
\]
The returned segment velocity is
\[
\mathbf v_k=(\mathbf r_{k+1}-\mathbf r_k)/\Delta t_k,
\]
and the body-frame angular rate is
\[
\boldsymbol\omega_k=
\log(\mathbf R_k^T\mathbf R_{k+1})/\Delta t_k.
\]
These are piecewise-constant segment rates, not smoothed physical estimates.
At a knot the rate can be discontinuous; users requiring smooth dynamics
should use a validated spline or state estimator rather than assuming this
interpolant is differentiable across knots.

## Multi-ping covariance

For \(N\) pings, input parameters are partitioned into ping-local vectors
\(\mathbf x_i\) and one common vector \(\mathbf c\), e.g. lever arms,
mounting angles, clock offset and drift. With local Jacobians \(\mathbf J_i\)
and shared Jacobians \(\mathbf K_i\), the assembled block matrix is
\[
\mathbf J_{\rm all}=
\begin{bmatrix}
\mathbf J_1&0&\cdots&0&\mathbf K_1\\
0&\mathbf J_2&\cdots&0&\mathbf K_2\\
\vdots&&\ddots&&\vdots\\
0&0&\cdots&\mathbf J_N&\mathbf K_N
\end{bmatrix},\qquad
\mathbf C_p=\mathbf J_{\rm all}\mathbf C_x\mathbf J_{\rm all}^T.
\]
The output is a full \(3N\times3N\) covariance. Shared errors create
off-diagonal cross-ping blocks; independent ping jitter belongs in the local
blocks. The clock model
\[
\Delta t_i=\delta t_0+\dot{\delta t}(t_i-t_{\rm ref})+\epsilon_i
\]
has shared offset and drift sensitivities
\[
\frac{\partial\mathbf p_i}{\partial\delta t_0}=\mathbf j_{t,i},
\quad
\frac{\partial\mathbf p_i}{\partial\dot{\delta t}}
=(t_i-t_{\rm ref})\mathbf j_{t,i}.
\]
Retain known correlations among local navigation states and shared
calibration/clock parameters.

## Run and scope

Run \`python -m pytest -q\` in this directory. Tests cover static and
time-aligned geometry, finite-difference timing derivatives, multi-epoch
interpolation, shared-clock cross-ping covariance, independent jitter,
clock drift columns, block ordering and invalid inputs.

The trajectory interpolator does not smooth motion or estimate states.
Multi-ping covariance propagates a supplied joint covariance and validates
shape, finiteness and symmetry; the caller is responsible for positive
semidefiniteness. This package does not yet model clock random walks,
high-dynamic trajectory splines, asynchronous filtering, heave/draft/squat,
vessel flexure, acoustic ray tracing, beamforming, bottom detection or full
hydrographic TPU.
