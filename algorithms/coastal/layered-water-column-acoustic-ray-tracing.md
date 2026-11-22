# Layered-water-column acoustic ray tracing

## Problem and conventions

An echo-sounder measures acoustic travel time and beam direction. Converting these observations to a seabed point requires a sound-speed model because acoustic rays refract when sound speed changes with depth.

This record defines a bounded two-dimensional ray tracer for a **piecewise-constant** sound-speed profile. It propagates a ray from a transducer into successively deeper horizontal layers. It is a computational teaching baseline for understanding refraction, not a production MBES beamformer or complete hydrographic processing suite.

Conventions: depth is positive down from the transducer; horizontal offset is positive in the launch-angle direction; launch angle is measured from downward vertical; input travel time is two-way and the forward ray is traced for half that time, assuming a stationary reciprocal path. Each layer is homogeneous with one constant sound speed. Layer-bottom depths are strictly increasing and the final boundary must extend beyond the ray endpoint.

## Snell invariant

For a horizontally stratified medium, Snell's law gives the invariant horizontal slowness:

\[
p=\frac{\sin\theta_i}{c_i}
\]

where \(\theta_i\) is the ray angle from vertical and \(c_i\) is sound speed in layer \(i\). Given launch angle \(\theta_0\) and first-layer speed \(c_0\):

\[
p=\frac{\sin\theta_0}{c_0},
\qquad
\theta_i=\arcsin(p c_i)
\]

A propagating ray requires \(|p c_i|<1\). If the value reaches or exceeds one, the implementation reports a critical/turning condition rather than silently clipping the angle.

Within a constant-speed layer, a vertical increment \(\Delta z_i\) produces:

\[
\Delta x_i=\Delta z_i\tan\theta_i,
\qquad
\Delta t_i=\frac{\Delta z_i}{c_i\cos\theta_i}
\]

If remaining one-way travel time \(t_r\) ends inside the current layer:

\[
\Delta z_i=t_r c_i\cos\theta_i
\]

The horizontal offset and depth are accumulated layer by layer. At a speed discontinuity, ray direction changes according to Snell's law while horizontal slowness is conserved.

## Inputs and outputs

The reference function accepts strictly increasing layer-bottom depths in metres from the transducer, one positive sound speed in metres per second per layer, launch angle in degrees from vertical, and positive two-way travel time in seconds. It returns depth, signed horizontal offset, exit angle, one-way travel time and number of traversed layers.

## Numerical and physical limitations

- The profile is piecewise constant. A continuous profile must be discretised; results depend on layer thickness and representation.
- The model is two-dimensional and assumes horizontally stratified water, no horizontal sound-speed gradients, no current-induced refraction and a stationary reciprocal path.
- It does not estimate sound speed, surface sound speed, beamforming direction, bottom detection, acoustic footprint, absorption, multipath, vessel motion, GNSS/INS trajectory, transducer offsets or vertical datum.
- It does not model uncertainty or covariance.
- It traces a forward ray for a supplied launch angle and measured travel time. It does not solve the inverse problem of estimating launch angle from a detected bottom position.

## Reference implementation and validation

See [hydrographic ray tracing](../../implementations/python/hydrographic-ray-tracing/README.md). Tests cover vertical and oblique analytic cases, signed offsets, Snell-invariant behaviour across a speed interface, exact layer-boundary termination, invalid inputs, insufficient profile depth and critical-angle conditions.

A successful synthetic test demonstrates the implementation under its stated layered-medium assumptions only. It does not establish sonar calibration, hydrographic survey accuracy or field performance.
