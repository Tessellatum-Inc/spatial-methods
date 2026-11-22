# Hydrographic layered-water-column ray tracing

A standard-library Python implementation of forward acoustic ray tracing and first-order endpoint uncertainty propagation through a horizontally stratified, piecewise-constant water column.

## Functions

- \`trace_layered_water_column(layer_bottom_depths_m, sound_speeds_mps, launch_angle_deg, two_way_travel_time_s)\`: trace a one-way ray for half the supplied two-way echo travel time. Snell's law preserves horizontal slowness across layer interfaces.
- \`trace_layered_water_column_with_sensitivities(..., input_covariance=None)\`: return the endpoint Jacobian and, when covariance is supplied, the propagated endpoint covariance.

Endpoint order is \`[horizontal_offset_m, depth_m]\`. Input order is \`[sound_speed_layer_1_mps, ..., sound_speed_layer_N_mps, launch_angle_deg, two_way_travel_time_s]\`. Angle uncertainty is therefore expressed in degrees, not radians.

## Uncertainty model

For endpoint \(\mathbf y=[x,z]^T\), input vector \(\mathbf u\), and Jacobian \(J=\partial\mathbf y/\partial\mathbf u\):

\[
C_y \approx J C_u J^T.
\]

The Jacobian is evaluated by central finite differences. Every perturbed ray must traverse the same number of layers as the nominal ray. If a perturbation changes the traversed-layer branch, the function raises an error rather than returning a misleading derivative at a discontinuity or kink. This is a local, first-order covariance approximation; it is not a nonlinear probability distribution or a complete total propagated uncertainty budget.

The input covariance must be finite, symmetric, positive semidefinite, and ordered exactly as the input vector. Off-diagonal terms are retained, so correlated sound-speed errors and cross-correlations with angle or travel time are supported.

## Example

\`\`\`python
from hydrographic_ray_tracing import trace_layered_water_column_with_sensitivities

result = trace_layered_water_column_with_sensitivities(
    layer_bottom_depths_m=[20.0, 80.0, 150.0],
    sound_speeds_mps=[1490.0, 1502.0, 1515.0],
    launch_angle_deg=25.0,
    two_way_travel_time_s=0.08,
    input_covariance=[
        [4.0, 1.0, 0.0, 0.0, 0.0],
        [1.0, 4.0, 0.5, 0.0, 0.0],
        [0.0, 0.5, 4.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.01, 0.0],
        [0.0, 0.0, 0.0, 0.0, 1e-8],
    ],
)
print(result["trace"])
print(result["jacobian"])
print(result["endpoint_covariance"])
\`\`\`

## Run tests

\`\`\`bash
python -m pytest -q
\`\`\`

No third-party runtime dependency is required; pytest is needed only to run the tests.

## Scope and limitations

This is a two-dimensional teaching model with constant speed inside each layer. A continuous profile must be discretised, and results depend on that representation. It assumes horizontal stratification and a stationary reciprocal path. It does not model horizontal gradients, currents, turning rays, multipath, beamforming, bottom detection, acoustic footprint, absorption, vessel motion, GNSS/INS, lever arms, water levels, vertical datum or a complete hydrographic TPU budget. Covariance propagation covers only the supplied sound-speed, launch-angle and travel-time uncertainty. It is not production MBES software or a substitute for survey calibration, field validation or independent quality control.
