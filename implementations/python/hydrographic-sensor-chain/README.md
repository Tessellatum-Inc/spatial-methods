# Hydrographic sensor-chain trajectory and uncertainty

This package develops sounding coordinates from sensor geometry through
time alignment, navigation trajectory interpolation, acoustic ray tracing
and covariance propagation.

## Sounding-coordinate uncertainty

`sounding_uncertainty.py` provides two complementary paths:

- `propagate_sounding_uncertainty` accepts the established 18-state
  covariance, including a three-component acoustic vector.
- `propagate_ray_traced_sounding_uncertainty` accepts a 17-state covariance
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

`trajectory_covariance.py` propagates a joint covariance for two bracketing
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

Run `python -m pytest -q` in this directory. The package remains a bounded
teaching implementation: it is not a production hydrographic processing
system or a complete total propagated uncertainty (TPU) solution.

## Ray-traced multi-ping covariance

`multiping_covariance.py` now composes ray endpoint sensitivities with each
ping's 3-by-17 sensor-chain Jacobian through
`assemble_ray_traced_multiping_jacobian` and
`propagate_ray_traced_multiping_covariance`.

For ping \(i\), let \(J_{s,i}\) map the 15 sensor/navigation states and
ray endpoint \([x_i,z_i]\) into the sounding, and let
\(J_{r,i}\) map the shared sound-speed profile plus that ping's launch angle
and two-way travel time into the ray endpoint. The composed per-ping blocks
are
\[
J_{\mathrm{local},i}
=
\begin{bmatrix}
J_{s,i}[:,1{:}15] &
J_{s,i}[:,16{:}17]J_{r,i}[:,m+1{:}m+2]
\end{bmatrix},
\]
\[
J_{\mathrm{profile},i}
=
J_{s,i}[:,16{:}17]J_{r,i}[:,1{:}m].
\]
The assembled joint Jacobian places every per-ping local block first and
the \(m\)-parameter sound-speed profile exactly once at the end. Its
first-order output covariance is
\[
C_{\mathrm{survey}}\approx J_{\mathrm{joint}}C_{\mathrm{joint}}J_{\mathrm{joint}}^T.
\]

The joint input covariance can retain cross-ping correlations among local
states, correlations between local states and the shared profile, and
correlations within the profile. A shared profile perturbation therefore
creates off-diagonal covariance between soundings even when ping-local
measurement errors are independent.

The local block order is 15 sensor/navigation variables, launch angle in
degrees, and two-way travel time in seconds. If clock error contributes to
the corrected travel time, represent it in that travel-time state and its
cross-ping covariance in the same joint covariance. Do not add the same
clock contribution again as an independent clock term. This interface
propagates supplied first-order covariance; it does not claim complete
survey TPU or replace the need to model datum, water level, vessel motion,
beamforming, sound-speed profile estimation and other error sources.


## Time-aligned ray-traced multi-ping covariance

`assemble_time_aligned_ray_traced_multiping_jacobian` and
`propagate_time_aligned_ray_traced_multiping_covariance` extend
the ray-traced multi-ping model with one navigation-epoch clock-offset
variable per ping.

There are two distinct time sensitivities:

1. The ray endpoint depends on the ping's acoustic two-way travel time.
   This remains in the per-ping ray input block alongside launch angle.
2. The interpolated vessel pose depends on the navigation evaluation epoch.
   Its sounding-coordinate derivative is supplied as one 3-vector per ping,
   in navigation-coordinate units per second. A separate clock-offset
   column is appended for each ping.

The input covariance order is
\[
[\text{ping-local sensor, angle and travel-time blocks};
 \text{shared sound-speed profile};
 \text{navigation epoch offsets by ping}].
\]
The final \(N\times N\) block may be populated from the offset covariance
returned by `propagate_clock_state_covariance` in
`clock_state_covariance.py`. The full joint covariance can
also retain correlations between navigation epoch offsets, acoustic
travel-time errors, navigation states and the shared profile.

If one physical clock contributes to both navigation epoch tagging and
acoustic travel-time measurement, its cross-covariance must be represented
in the joint input covariance. Do not assume the two effects are
independent, and do not add the same clock contribution again as a separate
variance term. The function propagates the supplied first-order model; it
does not itself estimate clock states or derive navigation time
sensitivities from a trajectory.


The trajectory-driven variant, `assemble_time_aligned_ray_traced_multiping_jacobian_from_trajectory`, accepts one result per ping from `time_aligned_sensor_chain_sounding_point_and_jacobian`, plus each ping's beam azimuth and ray endpoint Jacobian. It composes the 3x19 interpolated sensor-chain Jacobian with the endpoint-to-vector azimuth mapping and the ray Jacobian, then carries the returned navigation-epoch sensitivity into the per-ping clock columns. The companion `propagate_time_aligned_ray_traced_multiping_covariance_from_trajectory` performs the joint covariance propagation. This removes the need for the caller to manually copy the navigation-epoch sensitivity into a separate argument. It does not remove the need to supply the correct beam azimuth, ray sensitivities or joint covariance.


### Trajectory-driven stochastic clock offset and drift

The stochastic-clock trajectory variant,
\`assemble_time_aligned_ray_traced_stochastic_clock_multiping_jacobian_from_trajectory\`
and its covariance propagation companion, use a two-state clock at each ping:
\[
\mathbf{x}_i=[\delta t_i,\dot{\delta t}_i]^T.
\]
Generate the joint state covariance at the ping epochs with
\`propagate_clock_state_covariance\`. The final covariance block supplied to
the trajectory propagation function must match that generated process
covariance; the function checks this rather than silently accepting an
unrelated offset/drift block.

The direct sounding derivative is with respect to epoch offset. There is no
separate direct derivative with respect to drift: drift changes the
cross-epoch offset/state covariance through the clock transition model.
This distinction prevents drift from being counted twice. The full joint
input covariance still permits cross-correlations between clock states,
navigation/sensor states, acoustic travel-time inputs and the shared sound-
speed profile.


### Shared-clock effect on acoustic interval measurement

The process-driven trajectory propagator also accepts one measured two-way
travel time per ping. Under the local constant-rate approximation, a clock
with reading \(C(t)=t+\delta t(t)\) reports
\[
T_m=C(t_r)-C(t_t)
\approx T+\dot{\delta t}\,T,
\]
because the constant offset cancels in an elapsed-time difference. To
first order, the corrected interval is
\[
T\approx T_m(1-\dot{\delta t}),\qquad
\frac{\partial T}{\partial\dot{\delta t}}\approx -T_m.
\]
The propagated sounding Jacobian therefore has two distinct sensitivities
to each ping's same clock state: epoch offset acts through the navigation
trajectory, while fractional drift acts through the ray endpoint's
two-way-travel-time derivative. Their covariance and cross-correlation are
handled once in the shared clock-state covariance block.

This is a short-interval, locally constant fractional-rate approximation.
It does not yet integrate clock process noise over the transmit-to-receive
interval or model separate transmit and receive clock observations. For
those cases, use a clock-state model evaluated at both event epochs and
derive the interval as the difference of their clock readings.
