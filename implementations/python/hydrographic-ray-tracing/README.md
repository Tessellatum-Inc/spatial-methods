# Hydrographic layered-water-column ray tracing

A standard-library Python implementation of forward acoustic ray tracing and first-order endpoint uncertainty propagation through a horizontally stratified, piecewise-constant water column.

## Functions

- `trace_layered_water_column(layer_bottom_depths_m, sound_speeds_mps, launch_angle_deg, two_way_travel_time_s)`: trace a one-way ray for half the supplied two-way echo travel time. Snell's law preserves horizontal slowness across layer interfaces.
- `trace_layered_water_column_with_sensitivities(..., input_covariance=None)`: return the endpoint Jacobian and, when covariance is supplied, the propagated endpoint covariance.

Endpoint order is `[horizontal_offset_m, depth_m]`. Input order is `[sound_speed_layer_1_mps, ..., sound_speed_layer_N_mps, launch_angle_deg, two_way_travel_time_s]`. Angle uncertainty is therefore expressed in degrees, not radians.

## Uncertainty model

For endpoint \(\mathbf y=[x,z]^T\), input vector \(\mathbf u\), and Jacobian \(J=\partial\mathbf y/\partial\mathbf u\):

\[
C_y \approx J C_u J^T.
\]

The Jacobian is evaluated by central finite differences. Every perturbed ray must traverse the same number of layers as the nominal ray. If a perturbation changes the traversed-layer branch, the function raises an error rather than returning a misleading derivative at a discontinuity or kink. This is a local, first-order covariance approximation; it is not a nonlinear probability distribution or a complete total propagated uncertainty budget.

The input covariance must be finite, symmetric, positive semidefinite, and ordered exactly as the input vector. Off-diagonal terms are retained, so correlated sound-speed errors and cross-correlations with angle or travel time are supported.

## Example

```python
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
```

## Run tests

```bash
python -m pytest -q
```

No third-party runtime dependency is required; pytest is needed only to run the tests.

## Scope and limitations

This is a two-dimensional teaching model with constant speed inside each layer. A continuous profile must be discretised, and results depend on that representation. It assumes horizontal stratification and a stationary reciprocal path. It does not model horizontal gradients, currents, turning rays, multipath, beamforming, bottom detection, acoustic footprint, absorption, vessel motion, GNSS/INS, lever arms, water levels, vertical datum or a complete hydrographic TPU budget. Covariance propagation covers only the supplied sound-speed, launch-angle and travel-time uncertainty. It is not production MBES software or a substitute for survey calibration, field validation or independent quality control.


## Temporally correlated sound-speed profile uncertainty

The module `temporal_sound_speed_covariance.py` constructs a joint covariance
for layered profile errors observed at multiple survey epochs. For
single-epoch vertical profile covariance \(C_p\), epoch times \(t_i\), and
positive correlation time \(\tau\), it uses

\[
R_{ij}=\exp\left(-\frac{|t_i-t_j|}{\tau}\right),
\qquad
C_{(i,k),(j,\ell)}=R_{ij}(C_p)_{k\ell}.
\]

The state order is epoch-major: all layer errors at one epoch, followed by
all layers at the next. The supplied epoch order is preserved. The
single-epoch covariance must be finite, symmetric and positive
semidefinite. The exponential temporal kernel is positive semidefinite, so
the separable joint covariance is positive semidefinite as well.

For multi-ping propagation, evaluate each ping's ray Jacobian against the
profile associated with its environmental epoch, compose that profile block
through the endpoint-to-sounding sensor-chain Jacobian, and stack the
sensitivities in the same epoch-major order. Include the returned joint
profile covariance as one correlated state block in the full survey
covariance. This preserves cross-layer and cross-epoch dependence without
duplicating the same profile into independent ping blocks.

The correlation time must be estimated or justified from observations and
survey cadence; it is not a universal oceanographic constant. This model
describes anomalies around epoch-specific mean profiles. It does not
forecast or advect the mean sound-speed field, represent horizontal
gradients or currents, or replace in-situ SVP/CTD/XBT/MVP observations.



### Interpolating profiles to ping epochs

When profile observations and acoustic ping epochs do not coincide, use
`interpolate_temporal_sound_speed_profiles`. It accepts strictly increasing
observation epochs, one equal-length layer profile per epoch, target ping
epochs, and the full observation-profile covariance in epoch-major order.
Targets must lie inside the closed observation interval; extrapolation is
rejected.

For a target epoch between observations \(t_a\) and \(t_b\), define
\[
\lambda=\frac{t-t_a}{t_b-t_a},\qquad
\mathbf c(t)=(1-\lambda)\mathbf c(t_a)+\lambda\mathbf c(t_b).
\]
The function returns the linear interpolation operator \(H\), all
interpolated profiles, and
\[
C_{\mathrm{query}}=H C_{\mathrm{observed}}H^T.
\]
Because the full observation covariance is used, the result retains
cross-layer covariance, cross-observation covariance, and covariance
between different query epochs. Repeated query epochs therefore produce
identical, perfectly correlated profile blocks.

This is deterministic piecewise-linear interpolation of the supplied
profile means. The covariance is the propagated uncertainty of those
interpolated estimates under that interpolation rule; it does not include
unresolved ocean variability between observations, horizontal advection,
or model discrepancy. Those require an additional physical or stochastic
model rather than an arbitrary inflation of the covariance.
