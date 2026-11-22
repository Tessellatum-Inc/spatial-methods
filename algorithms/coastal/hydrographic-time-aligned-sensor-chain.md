# Navigation trajectory and propagated hydrographic uncertainty

## Sounding coordinate covariance

The sounding coordinate is computed from the GNSS antenna position, IMU
attitude, lever arms, mounting rotation and acoustic detection vector:
\[
\mathbf p_n=\mathbf r_{n,g}+
\mathbf R_{n\leftarrow i}
(-\mathbf l_{i,g}+\mathbf l_{i,t}
+\mathbf R_{i\leftarrow t}\mathbf s_t).
\]
For the parameter order
\[
\delta\mathbf x=[
\delta\mathbf r_{n,g},
\delta\boldsymbol\theta_n,
\delta\mathbf l_{i,g},
\delta\mathbf l_{i,t},
\delta\boldsymbol\phi_i,
\delta\mathbf s_t]^T,
\]
the implemented 3-by-18 Jacobian maps all first-order input errors into
navigation-frame sounding-coordinate error. Given the complete joint
covariance, including any navigation/calibration cross-covariances,
\[
\mathbf C_p=\mathbf J_{\rm chain}\mathbf C_x\mathbf J_{\rm chain}^{T}.
\]
The implementation returns the point, Jacobian, three-dimensional covariance
and marginal standard uncertainties. It does not silently construct a block
diagonal covariance: the caller supplies the full matrix and is responsible
for defensible correlations and positive semidefiniteness.

For a trajectory-derived pose, the six-by-six interpolated pose covariance
occupies the leading position/attitude block of the 18-state covariance. The
remaining blocks hold lever-arm, mounting and acoustic-vector uncertainty.
Any known covariance between pose and calibration parameters belongs in the
off-diagonal blocks. This creates a direct path from navigation interpolation
to sounding-coordinate uncertainty.

## Pose interpolation and endpoint covariance

Within a bracket \([t_0,t_1]\), with
\(\alpha=(t-t_0)/(t_1-t_0)\), interpolate antenna position linearly and
attitude on the shortest SO(3) geodesic:
\[
\mathbf r(t)=(1-\alpha)\mathbf r_0+\alpha\mathbf r_1,\qquad
\mathbf R(t)=\mathbf R_0\exp\left(
\alpha\log(\mathbf R_0^T\mathbf R_1)\right).
\]
No extrapolation is permitted. Endpoint attitude errors are left
multiplicative in navigation axes. A six-by-twelve Jacobian is evaluated by
central finite differences in the tangent space, then
\[
\mathbf C_{\rm pose}(t)=
\mathbf J_{\rm interp}\mathbf C_e\mathbf J_{\rm interp}^{T}.
\]
The full endpoint covariance retains cross-epoch and position-attitude terms.

## Multi-ping propagation

Shared lever arms, mounting calibration and clock parameters must appear once
in the common input block. The assembled block Jacobian propagates the full
joint covariance into a \(3N\times3N\) sounding covariance, preserving
cross-ping correlations. Independent per-ping propagation is insufficient
when navigation states or calibration parameters are shared.

## Implementation limits

The Python package provides first-order covariance propagation. Covariance
inputs are checked for shape, finite values and symmetry; positive
semidefiniteness remains the caller's responsibility. The interpolation
Jacobian depends on the finite-difference step. This is not a navigation
filter or a substitute for filter-native covariance outputs. High-dynamic
smoothing, clock random walks, asynchronous filtering, vessel flexure,
acoustic ray tracing and full hydrographic TPU remain outside scope.
