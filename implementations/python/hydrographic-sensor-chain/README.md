# Hydrographic sensor-chain trajectory and uncertainty

This package develops the sounding coordinate from static sensor geometry
through time alignment, navigation trajectory interpolation and covariance
propagation.

## Sounding-coordinate uncertainty

\`sounding_uncertainty.py\` propagates the full sensor-chain Jacobian into a
three-dimensional sounding covariance:
\[
\mathbf C_p=\mathbf J_{\rm chain}\mathbf C_x\mathbf J_{\rm chain}^{T}.
\]
The 18-element input order is
\[
[\mathbf r_{n,g},\delta\boldsymbol\theta_n,
 \mathbf l_{i,g},\mathbf l_{i,t},
 \delta\boldsymbol\phi_i,\mathbf s_t].
\]
The corresponding Jacobian maps GNSS antenna position, navigation-frame
attitude error, both IMU-frame lever arms, IMU-frame mounting error and the
transducer-frame acoustic vector into navigation-frame sounding coordinates.
The full covariance is accepted so correlations between navigation and
calibration parameters are retained. The caller must assemble it consistently;
independence must not be assumed unless justified by the estimation process.

For trajectory-derived soundings, place the interpolated six-state pose
covariance in the leading position/attitude block of this 18-state covariance,
then include the calibration covariance and any known cross-covariance blocks.
The output is first-order covariance propagation, not a complete hydrographic
total propagated uncertainty assessment. Covariance inputs are checked for
shape, finite values and symmetry; positive semidefiniteness is the caller's
responsibility.

## Navigation trajectory covariance

\`trajectory_covariance.py\` propagates a joint covariance for two bracketing
navigation poses through the interpolation. Endpoint input order is
\[
[\mathbf r_0,\delta\boldsymbol\theta_0,
  \mathbf r_1,\delta\boldsymbol\theta_1],
\]
with additive navigation-frame position errors and left-multiplicative
navigation-frame attitude errors. The six-by-twelve interpolation Jacobian
uses central finite differences on SO(3), retaining endpoint cross-covariance.

## Multi-ping covariance

For \(N\) pings, local state blocks and one shared calibration/clock block form
a joint input vector. The full \(3N\times3N\) output covariance retains
cross-ping correlation from common clock and calibration uncertainty.
Independent ping jitter belongs in each ping's local block.

## Trajectory interpolation

Navigation positions are piecewise linear and attitudes follow shortest-path
SO(3) geodesics. Queries outside trajectory support are rejected. Segment
rates are piecewise constant and can jump at knots; this is not a smoothed
trajectory estimator.

## Tests and limits

Run \`python -m pytest -q\` in this directory. The package does not yet
implement a high-dynamic spline, clock random walk, asynchronous navigation
filter, vessel flexure, acoustic ray tracing, beamforming, bottom detection
or full hydrographic TPU.
