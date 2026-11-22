# Hydrographic layered-water-column ray tracing

A standard-library Python implementation of a bounded acoustic ray-tracing model for a horizontally stratified water column represented by piecewise-constant sound-speed layers.

## Function

trace_layered_water_column(layer_bottom_depths_m, sound_speeds_mps, launch_angle_deg, two_way_travel_time_s)

The function traces a one-way ray for half the supplied two-way echo travel time. It uses Snell's law to preserve horizontal slowness across layer interfaces and returns depth, signed horizontal offset and exit angle.

## Example

```python
from hydrographic_ray_tracing import trace_layered_water_column

result = trace_layered_water_column(
    layer_bottom_depths_m=[20.0, 80.0, 150.0],
    sound_speeds_mps=[1490.0, 1502.0, 1515.0],
    launch_angle_deg=25.0,
    two_way_travel_time_s=0.08,
)
print(result)
```

The profile boundaries are positive-down depths from the transducer. There must be one sound speed per layer, and the final layer must extend beyond the ray endpoint. The ray angle is measured from the downward vertical.

## Run tests

```bash
python -m pytest -q
```

No third-party runtime dependency is required; pytest is needed only to run the tests.

## Scope and limitations

This is a forward, two-dimensional teaching model. Each layer has constant sound speed; a continuous profile must be discretised, and results depend on that discretisation. It assumes horizontal stratification and a stationary reciprocal path. It does not estimate sound speed, model horizontal gradients/currents, beamforming, bottom detection, transducer arrays, vessel motion, GNSS/INS, lever arms, water levels, vertical datum or uncertainty. It is not a replacement for a hydrographic acquisition/processing system or project validation.
