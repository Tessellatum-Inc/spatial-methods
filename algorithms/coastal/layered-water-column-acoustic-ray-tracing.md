# Layered-water-column acoustic ray tracing

## Problem and conventions

An echo-sounder measures acoustic travel time and beam direction. Converting these observations to a seabed point requires a sound-speed model because acoustic rays refract when sound speed changes with depth.

This record defines a bounded two-dimensional ray tracer for a **piecewise-constant** sound-speed profile. Depth is positive down from the transducer; horizontal offset is positive in the launch-angle direction; launch angle is measured from downward vertical; supplied travel time is two-way and the forward ray is traced for half that time under a stationary reciprocal-path assumption.

## Snell invariant and layer propagation

For a horizontally stratified medium, Snell's law gives the invariant horizontal slowness:

\[
p=\frac{\sin\theta_i}{c_i}.
\]

Given launch angle \(\theta_0\) and first-layer speed \(c_0\):

\[
p=\frac{\sin\theta_0}{c_0},
\qquad
\theta_i=\arcsin(p c_i).
\]

A propagating ray requires \(|p c_i|<1\). Critical/turning conditions are reported rather than clipped. Within a constant-speed layer:

\[
\Delta x_i=\Delta z_i\tan\theta_i,
\qquad
\Delta t_i=\frac{\Delta z_i}{c_i\cos\theta_i}.
\]

If remaining one-way travel time \(t_r\) ends inside the current layer:

\[
\Delta z_i=t_r c_i\cos\theta_i.
\]

## Endpoint sensitivity and uncertainty

The endpoint is:

\[
\mathbf y=
\begin{bmatrix}
x\\z
\end{bmatrix},
\]

and the input vector is:

\[
\mathbf u=
\begin{bmatrix}
c_1&\cdots&c_m&\theta_0&t_{2w}
\end{bmatrix}^{T}.
\]

The endpoint Jacobian is:

\[
J=\frac{\partial\mathbf y}{\partial\mathbf u}.
\]

The implementation estimates each column with a central finite difference:

\[
J_{:,k}\approx
\frac{\mathbf y(\mathbf u+h_k\mathbf e_k)
-\mathbf y(\mathbf u-h_k\mathbf e_k)}{2h_k}.
\]

For input covariance \(C_u\), first-order endpoint covariance is:

\[
C_y\approx J C_u J^T.
\]

The covariance may contain off-diagonal terms between layer sound speeds and between sound speed, launch angle and travel time. The implementation validates its shape, finiteness, symmetry and positive semidefiniteness. It does not assume independent inputs.

Finite differences are local. The implementation requires positive and negative perturbations to remain on the same traversed-layer branch as the nominal ray. A branch change or invalid perturbed ray causes an explicit error; a derivative at a layer-transition kink is not fabricated. The result is a first-order covariance approximation, not a complete nonlinear uncertainty distribution.

## Reference implementation and validation

See [hydrographic ray tracing](../../implementations/python/hydrographic-ray-tracing/README.md). Tests cover analytic homogeneous cases, Snell-invariant behaviour, branch-stable finite-difference sensitivities, travel-time sensitivity, correlated sound-speed covariance, zero covariance and invalid covariance inputs.

## Limitations

- Piecewise-constant layers approximate continuous sound-speed profiles; discretisation affects results.
- Assumes horizontal stratification, a stationary reciprocal path and one direct forward ray.
- No horizontal gradients, current-induced refraction, turning rays, multipath, beamforming, bottom detection, acoustic footprint, absorption or vessel motion.
- Does not include navigation trajectory, GNSS/INS, transducer offsets, water level, vertical datum or other TPU terms.
- The propagated covariance covers only the supplied layer sound speeds, launch angle and two-way travel time.
- Not a production MBES beamformer, complete hydrographic processing system or field-validation result.

## Sound-speed-profile uncertainty to sounding coordinates

The ray-tracing implementation returns a two-dimensional endpoint
\(\mathbf y=[x,z]^T\) and, for supplied input covariance, its first-order
covariance \(C_{xz}\). The sensor-chain implementation can now consume that
endpoint directly through
`propagate_ray_traced_sounding_uncertainty`.

For transducer-frame beam azimuth \(\alpha\), measured from +x toward +y, the
ray endpoint is represented as
\[
\mathbf s_t=
\begin{bmatrix}
x\cos\alpha\\x\sin\alpha\\z
\end{bmatrix}.
\]
The endpoint-to-vector map is
\[
B=
\begin{bmatrix}
\cos\alpha&0\\
\sin\alpha&0\\
0&1
\end{bmatrix}.
\]
The original sensor-chain Jacobian \(J_s\) is composed with this map. The
resulting 3-by-17 Jacobian maps a joint state consisting of the 15
navigation/calibration variables followed by ray endpoint \([x,z]\) into
the three-dimensional navigation-frame sounding position. Its covariance
is
\[
C_p\approx J_{\mathrm{composed}}C_uJ_{\mathrm{composed}}^T.
\]

The full input covariance can retain ray-to-navigation and
ray-to-calibration cross-correlations. This is preferable to simply adding
an independent ray covariance to an 18-state sounding covariance when
shared error sources exist. The caller must build one consistent covariance
and must not count the same ray-input uncertainty twice.

This integration remains conditional on the two-dimensional, horizontally
stratified, piecewise-constant ray model and the supplied beam azimuth. It
does not complete all hydrographic TPU terms or validate a field survey.

## Multi-ping propagation with a shared sound-speed profile

The sensor-chain package composes the per-ping ray endpoint Jacobian with
the ray-aware sensor-chain Jacobian. For ping \(i\), the ray model input
is ordered as
\[
\mathbf u_i=[c_1,\ldots,c_m,\theta_i,t_{2w,i}]^T,
\]
where the \(m\) sound-speed parameters describe one shared profile, while
launch angle and travel time are ping-specific. The sensor-chain Jacobian
maps the first 15 navigation/calibration variables and the two-dimensional
ray endpoint into the navigation-frame sounding.

The resulting per-ping local Jacobian is
\[
J_{\mathrm{local},i}=
\begin{bmatrix}
J_{s,i}[:,1{:}15]&
J_{s,i}[:,16{:}17]J_{r,i}[:,m+1{:}m+2]
\end{bmatrix},
\]
and the shared-profile block is
\[
J_{\mathrm{profile},i}=
J_{s,i}[:,16{:}17]J_{r,i}[:,1{:}m].
\]
The joint input vector contains each local block once and the shared
sound-speed profile once. Consequently,
\[
C_{\mathrm{survey}}\approx
J_{\mathrm{joint}}C_{\mathrm{joint}}J_{\mathrm{joint}}^T
\]
retains the cross-ping covariance induced by shared profile uncertainty.
The joint covariance may additionally retain cross-ping navigation and
calibration correlations and local-to-profile correlations.

The implementation is available as
`assemble_ray_traced_multiping_jacobian` and
`propagate_ray_traced_multiping_covariance` in the hydrographic
sensor-chain package. Its local input order is 15 sensor/navigation
variables, launch angle, and two-way travel time; its shared input block
contains the sound-speed profile parameters. A clock error that affects
corrected travel time belongs in the travel-time state and its joint
cross-ping covariance, not in a second independent contribution.

This is a first-order covariance composition for the stated ray and
sensor-chain models. It does not imply a complete hydrographic TPU model
or field validation.


### Navigation-epoch timing in multi-ping covariance

The acoustic two-way travel time and the navigation evaluation epoch are
different time inputs. The ray endpoint sensitivity with respect to
two-way travel time remains ping-local. The derivative of the final
sounding with respect to a navigation epoch shift is a separate
three-component sensitivity in navigation coordinates.

The sensor-chain implementation
`assemble_time_aligned_ray_traced_multiping_jacobian` appends
one navigation-epoch clock-offset column per ping after the ping-local
ray inputs and the shared sound-speed profile. Its propagated joint
covariance can use the correlated offset covariance produced by the
stochastic clock state model. If the same clock drives acoustic travel-time
measurement, include the corresponding cross-covariance between the
navigation epoch offsets and the ping-local travel-time inputs. This
preserves shared timing effects without silently counting one clock error
twice.

The time sensitivity is supplied by the caller; this function does not
replace time-aligned trajectory interpolation or calculate the derivative
from raw navigation observations.


The trajectory-driven composition is exposed as `assemble_time_aligned_ray_traced_multiping_jacobian_from_trajectory`. It consumes the 3x19 result of the time-aligned sensor-chain interpolation, maps the acoustic endpoint coordinates into the transducer-frame acoustic vector using beam azimuth, and composes that mapping with the ray endpoint Jacobian. The final time-offset column is taken from the interpolated trajectory result itself. The corresponding propagation function is `propagate_time_aligned_ray_traced_multiping_covariance_from_trajectory`.


## Process-driven navigation epoch clock states

For a survey line, model the navigation epoch error at ping \(i\) as the
offset component of a two-state clock process,
\[
\mathbf{x}_i=
\begin{bmatrix}
\delta t_i\\
\dot{\delta t}_i
\end{bmatrix}.
\]
The sounding derivative is with respect to \(\delta t_i\), not a second
independent derivative with respect to drift. Drift affects later epoch
offsets through the clock transition and process-noise covariance. Build
the joint state covariance at the ping epochs with
\`propagate_clock_state_covariance\`; the trajectory-driven stochastic-clock
propagator checks that the final \(2N\times2N\) block of the full joint
input covariance matches this process result. This preserves cross-epoch
offset/drift correlations and allows cross-covariance with navigation,
acoustic travel-time and sound-speed inputs. It does not equate epoch-tag
uncertainty with acoustic two-way travel-time uncertainty.
