"""Forward acoustic ray tracing through a piecewise-constant water column."""
from __future__ import annotations

import math
from collections.abc import Sequence


def trace_layered_water_column(
    layer_bottom_depths_m: Sequence[float],
    sound_speeds_mps: Sequence[float],
    launch_angle_deg: float,
    two_way_travel_time_s: float,
) -> dict[str, float | int]:
    """Trace a beam through horizontal layers of constant sound speed.

    Angles are measured from downward vertical. The supplied two-way echo
    travel time is halved to trace a reciprocal one-way ray.

    Layer boundaries are positive-down depths from the transducer. There
    must be one speed per layer and the final boundary must lie below the
    ray endpoint. This is a teaching baseline, not production MBES software.
    """
    try:
        bottoms = [float(value) for value in layer_bottom_depths_m]
        speeds = [float(value) for value in sound_speeds_mps]
        angle = float(launch_angle_deg)
        two_way_time = float(two_way_travel_time_s)
    except (TypeError, ValueError):
        raise ValueError("profile, angle and travel time must be numeric") from None

    if not bottoms or len(bottoms) != len(speeds):
        raise ValueError("layer boundaries and sound speeds must be non-empty and equal length")
    if any(not math.isfinite(value) or value <= 0 for value in bottoms + speeds):
        raise ValueError("layer depths and sound speeds must be finite and positive")
    previous = 0.0
    for boundary in bottoms:
        if boundary <= previous:
            raise ValueError("layer bottom depths must be strictly increasing from zero")
        previous = boundary
    if not math.isfinite(angle) or abs(angle) >= 90.0:
        raise ValueError("launch angle must be finite and strictly between -90 and 90 degrees")
    if not math.isfinite(two_way_time) or two_way_time <= 0:
        raise ValueError("two-way travel time must be finite and positive")

    launch_rad = math.radians(angle)
    horizontal_slowness = math.sin(launch_rad) / speeds[0]
    remaining_time = two_way_time / 2.0
    depth = 0.0
    horizontal_offset = 0.0
    layers_traversed = 0

    for layer_bottom, speed in zip(bottoms, speeds):
        sine_angle = horizontal_slowness * speed
        if abs(sine_angle) >= 1.0:
            raise ValueError("ray reaches a critical/turning condition in the supplied layer")
        layer_angle = math.asin(sine_angle)
        cosine_angle = math.cos(layer_angle)
        available_depth = layer_bottom - depth
        time_to_boundary = available_depth / (speed * cosine_angle)

        if remaining_time <= time_to_boundary:
            travelled_depth = remaining_time * speed * cosine_angle
            horizontal_offset += travelled_depth * math.tan(layer_angle)
            depth += travelled_depth
            layers_traversed += 1
            return {
                "depth_m": depth,
                "horizontal_offset_m": horizontal_offset,
                "exit_angle_deg": math.degrees(layer_angle),
                "one_way_travel_time_s": two_way_time / 2.0,
                "layers_traversed": layers_traversed,
            }

        horizontal_offset += available_depth * math.tan(layer_angle)
        depth = layer_bottom
        remaining_time -= time_to_boundary
        layers_traversed += 1

    raise ValueError("supplied sound-speed profile does not extend to the ray endpoint")
