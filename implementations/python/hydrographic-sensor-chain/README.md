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


## Time-aligned multi-ping covariance

`assemble_time_aligned_multiping_jacobian` appends two common clock
parameters to the shared input block: clock offset and linear clock drift.
For ping (i), its time-sensitivity vector (mathbf j_{t,i}) contributes
[
\frac{\partial\mathbf p_i}{\partial\delta t_0}=\mathbf j_{t,i},
\qquad
\frac{\partial\mathbf p_i}{\partial\dot{\delta t}}=(t_i-t_{\rm ref})\mathbf j_{t,i}.
]
`propagate_time_aligned_multiping_covariance` propagates the resulting full
joint covariance. Its input order is all ping-local blocks, the shared
calibration block, clock offset and clock drift. Cross-ping navigation
correlations and calibration/clock correlations are retained when present in
the supplied covariance. The clock model is a common offset plus linear
drift over the represented interval; it is not a stochastic clock process.


## Stochastic clock-state covariance

`clock_state_covariance.py` models clock offset and drift as a two-state
continuous-time process:
\[
\mathbf x(t)=
\begin{bmatrix}\delta t(t)\\ \dot{\delta t}(t)\end{bmatrix},
\qquad
d\delta t=\dot{\delta t}\,dt,
\qquad
d\dot{\delta t}=\sqrt q\,dW.
\]
For an interval \(\Delta t\), the exact transition and process covariance are
\[
\mathbf F(\Delta t)=
\begin{bmatrix}1&\Delta t\\0&1\end{bmatrix},
\qquad
\mathbf Q(\Delta t)=q
\begin{bmatrix}
\Delta t^3/3&\Delta t^2/2\\
\Delta t^2/2&\Delta t
\end{bmatrix}.
\]
Here \(q\) is the white frequency-rate noise spectral density under this
continuous-time model. It is not interchangeable with an arbitrary per-sample
drift variance; the physical clock-noise process and units must be selected
from calibration evidence.

`propagate_clock_state_covariance` returns every epoch's marginal state
covariance, the full cross-epoch joint state covariance, and the clock-offset
covariance. For \(i\leq j\), the state cross-covariance is
\[
\operatorname{Cov}(\mathbf x_i,\mathbf x_j)
=\mathbf P_i\mathbf F(t_j-t_i)^T.
\]
The stochastic multi-ping Jacobian adds one offset column per ping. Supply
the returned \(N\times N\) offset covariance in the clock-offset block of
the full joint input covariance to
`propagate_stochastic_clock_multiping_covariance`. That function retains
clock-to-clock and any supplied clock-to-navigation or clock-to-calibration
cross-covariances. It does not silently assume those blocks are zero.
