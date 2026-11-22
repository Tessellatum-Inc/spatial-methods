# Navigation trajectory and propagated hydrographic uncertainty

## Pose interpolation and endpoint covariance

Within a bracket \([t_0,t_1]\), with
\(\alpha=(t-t_0)/(t_1-t_0)\), interpolate antenna position linearly and
attitude on the shortest SO(3) geodesic:
\[
\mathbf r(t)=(1-\alpha)\mathbf r_0+\alpha\mathbf r_1,\qquad
\mathbf R(t)=\mathbf R_0\exp\left(
\alpha\log(\mathbf R_0^T\mathbf R_1)\right).
\]
No extrapolation is permitted. The endpoint pose perturbation order is
\[
\delta\mathbf x_e=
[\delta\mathbf r_0^T,\delta\boldsymbol\theta_0^T,
 \delta\mathbf r_1^T,\delta\boldsymbol\theta_1^T]^T.
\]
Position errors are additive in navigation coordinates. Attitude errors are
left-multiplicative in navigation axes:
\[
\mathbf R_k^{\rm pert}=
\exp([\delta\boldsymbol\theta_k]_\times)\mathbf R_k.
\]
Define the interpolated output perturbation similarly. A six-by-twelve
Jacobian is evaluated by central finite differences; for attitude columns,
the output perturbation is obtained from
\[
\delta\boldsymbol\theta(t)=
\log(\mathbf R^{\rm pert}(t)\mathbf R(t)^T).
\]
This computes the local tangent-space derivative of the actual geodesic
interpolant, rather than assuming that SO(3) interpolation weights are
exactly scalar multiples of the identity.

Given the full endpoint covariance, including cross-epoch and
position-attitude terms,
\[
\mathbf C_{\rm pose}(t)=
\mathbf J_{\rm interp}\mathbf C_e\mathbf J_{\rm interp}^{T}.
\]
The full covariance matters: neighboring navigation states often share
filter history, clock errors, inertial biases or GNSS smoothing. Dropping
cross-epoch covariance can overstate or understate interpolated uncertainty.

## Multi-ping propagation

For a sequence of soundings, shared lever arms, mounting calibration and
clock parameters must appear once in the common input block. With local
Jacobian \(\mathbf J_i\), shared Jacobian \(\mathbf K_i\), and complete input
covariance \(\mathbf C_x\):
\[
\mathbf J_{\rm all}=
\begin{bmatrix}
\mathbf J_1&0&\cdots&0&\mathbf K_1\\
0&\mathbf J_2&\cdots&0&\mathbf K_2\\
\vdots&&\ddots&&\vdots\\
0&0&\cdots&\mathbf J_N&\mathbf K_N
\end{bmatrix},\qquad
\mathbf C_p=\mathbf J_{\rm all}\mathbf C_x\mathbf J_{\rm all}^{T}.
\]
The full \(3N\times3N\) output covariance retains cross-ping correlation.
Independent per-ping propagation is insufficient when navigation states,
clock or calibration parameters are shared or correlated.

## Implementation limits

The Python package implements piecewise pose interpolation, finite-difference
endpoint covariance propagation and multi-ping block covariance propagation.
Covariance inputs are checked for shape, finite values and symmetry; callers
must ensure positive semidefiniteness. The interpolation covariance is
first-order and depends on the selected finite-difference step. It is not a
navigation filter or a substitute for the filter's native covariance and
cross-covariance outputs. High-dynamic smoothing, clock random walks,
asynchronous filtering, vessel flexure, acoustic ray tracing and full
hydrographic TPU remain outside scope.
