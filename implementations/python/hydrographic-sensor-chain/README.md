# Hydrographic sensor-chain trajectory and uncertainty

The package contains static GNSS/IMU/transducer geometry, two-state time
alignment, multi-epoch piecewise trajectory interpolation, multi-ping
covariance assembly and endpoint-pose covariance interpolation.

## Navigation trajectory covariance

\`trajectory_covariance.py\` propagates a joint covariance for two bracketing
navigation poses through the interpolation. The endpoint input order is
\[
[\mathbf r_0,\delta\boldsymbol\theta_0,
  \mathbf r_1,\delta\boldsymbol\theta_1],
\]
where position errors are additive in navigation coordinates and attitude
errors are left-multiplicative in navigation axes:
\[
\mathbf R_k^{\rm pert}=\exp([\delta\boldsymbol\theta_k]_\times)\mathbf R_k.
\]
The interpolated output order is position followed by a left attitude error.
The implementation computes the six-by-twelve interpolation Jacobian by
central finite differences. For attitude columns, it maps the perturbed
interpolated rotation back to a left error using
\[
\delta\boldsymbol\theta(t)
=\log(\mathbf R^{\rm pert}(t)\mathbf R(t)^T).
\]
This numerical tangent-space derivative retains the nonlinear dependence of
the SO(3) geodesic on both endpoint attitudes without assuming that endpoint
rotations commute or that the relative rotation is infinitesimal.

Given the full endpoint covariance \(\mathbf C_e\), including position,
attitude and cross-epoch correlations,
\[
\mathbf C_{\rm pose}(t)=\mathbf J_{\rm interp}\mathbf C_e
\mathbf J_{\rm interp}^{T}.
\]
At an epoch halfway between two identical poses, the position interpolation
has weights \(1/2\) and \(1/2\); correlated endpoint errors must therefore
remain correlated in the output. The same principle applies to attitude
errors through the computed tangent-space Jacobian. At either endpoint the
interpolated covariance recovers that endpoint's corresponding marginal
covariance.

The numerical derivative uses a configurable central-difference step
(default \(10^{-6}\), in the input parameter's units). It is first-order
uncertainty propagation, not a probability distribution on the rotation
manifold. The supplied joint covariance is checked for dimensions, finite
values and symmetry; positive semidefiniteness remains the caller's
responsibility.

## Multi-ping covariance

For \(N\) pings, local state blocks and one shared calibration/clock block
form a joint input vector. The assembled block Jacobian propagates the full
joint covariance into a \(3N\times3N\) sounding covariance, preserving
cross-ping correlation from common clock and calibration uncertainty.
Independent ping jitter belongs in each ping's local block.

## Trajectory interpolation

Navigation positions are piecewise linear and attitudes follow shortest-path
SO(3) geodesics. Queries outside trajectory support are rejected. Segment
rates are piecewise constant and can jump at knots; this is not a smoothed
trajectory estimator.

## Tests and limits

Run \`python -m pytest -q\` in this directory. Tests cover static/time-aligned
geometry, finite-difference timing, multi-epoch interpolation, endpoint pose
covariance, cross-ping covariance, independent jitter and invalid inputs.
The package does not yet implement a high-dynamic spline, clock random walk,
asynchronous navigation filter, vessel flexure, acoustic ray tracing,
beamforming, bottom detection or full hydrographic TPU.
