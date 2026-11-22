# Hydrographic sensor-chain trajectory and uncertainty

This package develops sounding coordinates from sensor geometry through
time alignment, navigation trajectory interpolation, acoustic ray tracing
and covariance propagation.

## Sounding-coordinate uncertainty

\`sounding_uncertainty.py\` provides two complementary paths:

- \`propagate_sounding_uncertainty\` accepts the established 18-state
  covariance, including a three-component acoustic vector.
- \`propagate_ray_traced_sounding_uncertainty\` accepts a 17-state covariance
  in which the acoustic vector is replaced by the ray endpoint
  \([x,z]\). It maps the endpoint into the transducer frame using beam
  azimuth, composes the ray-to-vector map with the sensor-chain Jacobian,
  and propagates the joint covariance into navigation coordinates.

For the ray-aware function, input order is
\[
[\mathbf r_{n,g},\delta\boldsymbol\theta_n,
 \mathbf l_{i,g},\mathbf l_{i,t},\delta\boldsymbol\phi_i,x,z].
\]
The endpoint mapping for transducer-frame azimuth \(\alpha\), measured from
+x toward +y, is
\[
\mathbf s_t=
\begin{bmatrix}
x\cos\alpha\\x\sin\alpha\\z
\end{bmatrix},
\qquad
B=\frac{\partial\mathbf s_t}{\partial[x,z]}=
\begin{bmatrix}
\cos\alpha&0\\
\sin\alpha&0\\
0&1
\end{bmatrix}.
\]
If \(J_s\) is the original sensor-chain Jacobian, the composed Jacobian is
\[
J_{\rm composed}=
\begin{bmatrix}
J_s[:,1{:}15]&J_s[:,16{:}18]B
\end{bmatrix},
\qquad
C_p\approx J_{\rm composed}C_uJ_{\rm composed}^{T}.
\]
(The Python slices are zero-based: the first block contains 15 columns and
the second block the three acoustic-vector columns.)

The full 17-by-17 covariance can retain cross-correlations between the ray
endpoint and navigation/calibration states. This avoids adding the ray
covariance as an independent acoustic-vector term when those correlations
are known. Supply one consistent joint covariance; do not count the same
sound-speed, angle or travel-time uncertainty again in another input block.

The existing 18-state route remains available when the acoustic vector and
its covariance have already been assembled upstream. Covariance inputs are
checked for shape, finite values and symmetry; positive semidefiniteness
remains the caller's responsibility in this sensor-chain module.

## Navigation trajectory covariance

\`trajectory_covariance.py\` propagates a joint covariance for two bracketing
navigation poses through interpolation. Endpoint input order is
\[
[\mathbf r_0,\delta\boldsymbol\theta_0,
  \mathbf r_1,\delta\boldsymbol\theta_1].
\]
It retains endpoint cross-covariance.

## Multi-ping covariance

For \(N\) pings, local state blocks and one shared calibration/clock block
form a joint input vector. The full \(3N\times3N\) output covariance retains
cross-ping correlation from common clock and calibration uncertainty.
Stochastic clock offset covariance can be propagated across ping epochs.

## Trajectory interpolation

Navigation positions are piecewise linear and attitudes follow shortest-path
SO(3) geodesics. Queries outside trajectory support are rejected.

## Tests and limits

Run \`python -m pytest -q\` in this directory. The package remains a bounded
teaching implementation: it is not a production hydrographic processing
system or a complete total propagated uncertainty (TPU) solution.
