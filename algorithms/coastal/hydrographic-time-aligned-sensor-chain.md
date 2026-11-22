# Time-aligned hydrographic sensor-chain geometry

## Why time is part of the geometry

The sounding coordinate depends on the navigation pose at the acoustic
observation epoch, not merely on the nearest GNSS/INS record. A timing offset
during vessel motion becomes a position error. The effect includes both
translation and attitude-induced displacement of the transducer and acoustic
detection point.

## Interpolation contract

Given two navigation states at \(t_0<t_1\), evaluate at
\(t_e=t_{ping}+\Delta t\). The method requires \(t_e\in[t_0,t_1]\);
it rejects extrapolation. Antenna position is linearly interpolated:

\[
\mathbf r_{n,g}(\alpha)=(1-\alpha)\mathbf r_{n,g,0}
+\alpha\mathbf r_{n,g,1},\qquad
\alpha=\frac{t_e-t_0}{t_1-t_0}.
\]

Attitude is interpolated along the shortest SO(3) geodesic:

\[
\mathbf R_{n\leftarrow i}(\alpha)=
\mathbf R_{n\leftarrow i,0}
\exp\left(\alpha\log(
\mathbf R_{n\leftarrow i,0}^{T}
\mathbf R_{n\leftarrow i,1})\right).
\]

The rotation logarithm vector \(\boldsymbol\phi\) is expressed in the IMU
coordinates of the initial state. Within this segment, the interpolation
assumes constant translational velocity and constant body angular rate.

## Timing sensitivity

Let
\(\mathbf v_i=-\mathbf l_{i,g}+\mathbf l_{i,t}
+\mathbf R_{i\leftarrow t}\mathbf s_t\). Then

\[
\frac{\partial\mathbf p_n}{\partial\Delta t}
=\frac{\mathbf r_{n,g,1}-\mathbf r_{n,g,0}}{t_1-t_0}
+\mathbf R_{n\leftarrow i}
\left[\frac{\boldsymbol\phi}{t_1-t_0}\right]_\times\mathbf v_i.
\]

The implementation appends this three-component derivative to the static
sensor-chain Jacobian, yielding a 3 by 19 Jacobian. The final parameter is
time offset in seconds, so the derivative has coordinate-units per second.
The sign convention is explicit: positive offset evaluates the navigation
trajectory later than the ping timestamp.

A joint covariance over the 18 static geometry parameters and time offset
can be propagated as

\[
\mathbf C_p=\mathbf J_{19}\mathbf C_{19}\mathbf J_{19}^{T}.
\]

Retain covariance cross-terms when timing uncertainty is correlated with
trajectory or calibration. This formulation does not estimate latency; it
propagates a supplied offset uncertainty under the stated interpolation model.

## Implementation and tests

The [Python implementation and tests](../../implementations/python/hydrographic-sensor-chain/README.md)
provide two-state interpolation, geodesic attitude interpolation, the time
sensitivity column, finite-difference checks and strict bracket validation.

## Limits and next steps

This is a local interpolation model, not a complete navigation estimator.
It does not model asynchronous filtering, clock drift, latency estimation,
high-dynamic trajectory splines, lever-arm flexure, heave/draft/squat, acoustic
ray tracing or bottom detection. Real processing must use the acquisition
system's time tags, clock model, interpolation policy and calibration records.
A production extension should support multi-epoch trajectory interpolation,
per-sensor clock offsets, ping-to-ping shared timing covariance and dynamic
vessel motion while preserving raw time tags and provenance.
