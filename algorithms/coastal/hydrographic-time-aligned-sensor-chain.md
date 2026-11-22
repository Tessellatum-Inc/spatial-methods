# Time-aligned trajectory and multi-ping hydrographic sensor-chain geometry

## Piecewise navigation trajectory

For navigation epochs \(t_k\), antenna positions \(\mathbf r_k\) and
attitudes \(\mathbf R_k\), require strictly increasing times and evaluate
each ping only inside the trajectory support. Within segment \(k\),
\[
\alpha=\frac{t-t_k}{t_{k+1}-t_k},\quad
\mathbf r(t)=(1-\alpha)\mathbf r_k+\alpha\mathbf r_{k+1},
\]
\[
\mathbf R(t)=\mathbf R_k\exp\left(
\alpha\log(\mathbf R_k^T\mathbf R_{k+1})\right).
\]
Position is piecewise linear and attitude follows the shortest SO(3)
geodesic. Segment velocity and body angular rate are constant within a
segment:
\[
\mathbf v_k=\frac{\mathbf r_{k+1}-\mathbf r_k}{t_{k+1}-t_k},
\qquad
\boldsymbol\omega_k=
\frac{\log(\mathbf R_k^T\mathbf R_{k+1})}{t_{k+1}-t_k}.
\]
No extrapolation is performed. The interpolant is continuous in pose but
its velocity and angular rate may jump at navigation knots; it is not a
dynamics model or a smoothed trajectory estimator.

## Shared multi-ping uncertainty

For ping \(i\), partition the input into ping-local parameters
\(\mathbf x_i\) and shared parameters \(\mathbf c\). The shared set can include
installation lever arms, mounting angles, common clock offset and drift.
With local Jacobian \(\mathbf J_i\) and shared Jacobian \(\mathbf K_i\),
\[
\mathbf J_{\rm all}=
\begin{bmatrix}
\mathbf J_1&0&\cdots&0&\mathbf K_1\\
0&\mathbf J_2&\cdots&0&\mathbf K_2\\
\vdots&&\ddots&&\vdots\\
0&0&\cdots&\mathbf J_N&\mathbf K_N
\end{bmatrix},
\quad
\mathbf C_p=\mathbf J_{\rm all}\mathbf C_x\mathbf J_{\rm all}^{T}.
\]
The result is a \(3N\times3N\) covariance. Its off-diagonal blocks encode
cross-ping correlation. A shared clock offset contributes
\[
\mathbf C_{p_i p_j}^{(t)}
=\sigma_{\delta t}^2\mathbf j_{t,i}\mathbf j_{t,j}^{T},
\]
whereas independent timing jitter contributes only through each ping's
local block. For a clock model
\[
\Delta t_i=\delta t_0+\dot{\delta t}(t_i-t_{\rm ref})+\epsilon_i,
\]
the common offset and drift columns are
\[
\frac{\partial\mathbf p_i}{\partial\delta t_0}=\mathbf j_{t,i},
\qquad
\frac{\partial\mathbf p_i}{\partial\dot{\delta t}}
=(t_i-t_{\rm ref})\mathbf j_{t,i}.
\]
Preserve known correlations between navigation states and shared calibration
or clock parameters. The implementation validates dimensions, finiteness
and symmetry; the covariance provider must ensure positive semidefiniteness.

## Implementation and limits

The [Python package](../../implementations/python/hydrographic-sensor-chain/README.md)
contains static and two-state time-aligned sensor-chain geometry, multi-epoch
piecewise pose interpolation, block-Jacobian assembly and full cross-ping
covariance propagation. It is a first-order model, not a clock/calibration
estimator or trajectory smoother. High-dynamic splines, clock random walks,
asynchronous filtering, vessel flexure, acoustic ray tracing and bottom
detection remain outside scope.
