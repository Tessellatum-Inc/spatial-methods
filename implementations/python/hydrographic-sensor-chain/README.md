# Hydrographic sensor-chain geometry and multi-ping uncertainty

The static and time-aligned geometry modules model a GNSS antenna, IMU,
mounted transducer and acoustic detection point. The static point is
\[
\mathbf p_n=\mathbf r_{n,g}+
\mathbf R_{n\leftarrow i}(-\mathbf l_{i,g}+\mathbf l_{i,t}+
\mathbf R_{i\leftarrow t}\mathbf s_t).
\]
The static Jacobian has 18 columns for antenna position, navigation attitude,
two IMU lever arms, mounting attitude and acoustic vector. The time-aligned
module appends the derivative with respect to a timing offset, giving 19
columns. It linearly interpolates antenna position and follows the shortest
SO(3) geodesic between bracketing attitudes; extrapolation is rejected.

## Multi-ping covariance

For \(N\) pings, partition the input into local states \(\mathbf x_i\) and
parameters \(\mathbf c\) shared across pings (installation lever arms,
mounting angles, clock offset and clock drift):
\[
\mathbf x=[\mathbf x_1^T,\ldots,\mathbf x_N^T,\mathbf c^T]^T.
\]
Each ping has a \(3\times L\) local Jacobian \(\mathbf J_i\) and a
\(3\times S\) shared Jacobian \(\mathbf K_i\). The block Jacobian is
\[
\mathbf J_{\rm all}=
\begin{bmatrix}
\mathbf J_1&0&\cdots&0&\mathbf K_1\\
0&\mathbf J_2&\cdots&0&\mathbf K_2\\
\vdots&&\ddots&&\vdots\\
0&0&\cdots&\mathbf J_N&\mathbf K_N
\end{bmatrix}.
\]
The propagated covariance is
\[
\mathbf C_p=\mathbf J_{\rm all}\mathbf C_x\mathbf J_{\rm all}^T.
\]
It is a full \(3N\times3N\) matrix. Its off-diagonal \(3\times3\) blocks
are cross-ping covariance. A common clock offset with variance
\(\sigma_{\delta t}^2\) contributes
\[
\mathbf C_{p_i p_j}^{(t)}
=\sigma_{\delta t}^2\mathbf j_{t,i}\mathbf j_{t,j}^T.
\]
This contribution is lost if every ping is propagated independently.

A clock model can be written
\[
\Delta t_i=\delta t_0+\dot{\delta t}(t_i-t_{\rm ref})+\epsilon_i.
\]
The shared offset and drift sensitivities are
\[
\frac{\partial\mathbf p_i}{\partial\delta t_0}=\mathbf j_{t,i},
\qquad
\frac{\partial\mathbf p_i}{\partial\dot{\delta t}}
=(t_i-t_{\rm ref})\mathbf j_{t,i}.
\]
Independent jitter \(\epsilon_i\) belongs in the ping-local input block.
Use a reference epoch near the survey midpoint to reduce offset/drift
correlation. Shared calibration parameters appear once in the common block.
Retain the complete covariance, including local-to-local and local-to-shared
cross terms when known.

The implementation assembles the block Jacobian and propagates a supplied
joint covariance. It validates dimensions, finiteness and symmetry; the
caller remains responsible for positive-semidefinite validation and for
constructing a physically meaningful joint covariance.

## Tests and scope

Run \`python -m pytest -q\` in this package. Tests cover static/time-aligned
geometry, timing finite differences, shared-clock cross-ping covariance,
independent jitter, clock drift columns, block ordering and invalid inputs.

This is first-order uncertainty propagation, not a clock or calibration
estimator. It does not yet model clock random walks, high-dynamic trajectory
splines, asynchronous filtering, heave/draft/squat, vessel flexure, acoustic
ray tracing, beamforming, bottom detection or full hydrographic TPU.
