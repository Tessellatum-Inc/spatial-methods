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


def _jacobi_eigenvalues(matrix: list[list[float]]) -> list[float]:
    """Eigenvalues of a real symmetric matrix using Jacobi rotations."""
    a = [row[:] for row in matrix]
    n = len(a)
    for _ in range(max(1, 50 * n * n)):
        p, q, largest = 0, 0, 0.0
        for i in range(n):
            for j in range(i + 1, n):
                if abs(a[i][j]) > largest:
                    p, q, largest = i, j, abs(a[i][j])
        if largest <= 1e-12 * max(1.0, max(abs(a[i][i]) for i in range(n))):
            break
        tau = (a[q][q] - a[p][p]) / (2.0 * a[p][q])
        t = math.copysign(1.0, tau) / (abs(tau) + math.sqrt(1.0 + tau * tau))
        c = 1.0 / math.sqrt(1.0 + t * t)
        s = t * c
        app, aqq, apq = a[p][p], a[q][q], a[p][q]
        a[p][p] = app - t * apq
        a[q][q] = aqq + t * apq
        a[p][q] = a[q][p] = 0.0
        for k in range(n):
            if k in (p, q):
                continue
            akp, akq = a[k][p], a[k][q]
            a[k][p] = a[p][k] = c * akp - s * akq
            a[k][q] = a[q][k] = s * akp + c * akq
    return [a[i][i] for i in range(n)]


def trace_layered_water_column_with_sensitivities(
    layer_bottom_depths_m: Sequence[float],
    sound_speeds_mps: Sequence[float],
    launch_angle_deg: float,
    two_way_travel_time_s: float,
    input_covariance: Sequence[Sequence[float]] | None = None,
) -> dict[str, object]:
    """Return endpoint Jacobian and optional covariance propagation.

    Endpoint order is [horizontal_offset_m, depth_m]. Input order is
    [sound_speed_layer_1, ..., sound_speed_layer_m, launch_angle_deg,
    two_way_travel_time_s]. Derivatives are central finite differences.

    A perturbation that changes the traversed-layer branch is rejected:
    derivatives at a layer-transition kink are not silently reported.
    If supplied, input_covariance must be a symmetric positive-semidefinite
    covariance in exactly the stated input order.
    """
    bottoms = list(layer_bottom_depths_m)
    speeds = [float(value) for value in sound_speeds_mps]
    angle = float(launch_angle_deg)
    travel_time = float(two_way_travel_time_s)
    base = trace_layered_water_column(bottoms, speeds, angle, travel_time)
    parameters = speeds + [angle, travel_time]
    steps = [max(abs(value) * 1e-5, 1e-3) for value in speeds]
    steps += [1e-5, max(abs(travel_time) * 1e-5, 1e-8)]
    jacobian = [[], []]
    endpoint_keys = ("horizontal_offset_m", "depth_m")

    for column, step in enumerate(steps):
        plus = parameters[:]
        minus = parameters[:]
        plus[column] += step
        minus[column] -= step
        if column < len(speeds) and minus[column] <= 0:
            raise ValueError("finite-difference step would make sound speed non-positive")
        try:
            high = trace_layered_water_column(bottoms, plus[:-2], plus[-2], plus[-1])
            low = trace_layered_water_column(bottoms, minus[:-2], minus[-2], minus[-1])
        except ValueError as exc:
            raise ValueError("cannot compute a stable sensitivity at this ray/profile configuration") from exc
        if high["layers_traversed"] != base["layers_traversed"] or low["layers_traversed"] != base["layers_traversed"]:
            raise ValueError("sensitivity is undefined at a layer-transition branch change")
        for row, key in enumerate(endpoint_keys):
            jacobian[row].append((float(high[key]) - float(low[key])) / (2.0 * step))

    result: dict[str, object] = {
        "trace": base,
        "endpoint_order": list(endpoint_keys),
        "input_order": [f"sound_speed_layer_{i + 1}_mps" for i in range(len(speeds))]
        + ["launch_angle_deg", "two_way_travel_time_s"],
        "jacobian": jacobian,
        "differentiation": "central finite differences; branch-stability checked",
    }

    if input_covariance is not None:
        n = len(parameters)
        try:
            covariance = [[float(value) for value in row] for row in input_covariance]
        except (TypeError, ValueError):
            raise ValueError("input covariance must be a finite numeric square matrix") from None
        if len(covariance) != n or any(len(row) != n for row in covariance):
            raise ValueError(f"input covariance must have shape {n} by {n}")
        if any(not math.isfinite(value) for row in covariance for value in row):
            raise ValueError("input covariance must contain only finite values")
        scale = max(1.0, max(abs(value) for row in covariance for value in row))
        if any(abs(covariance[i][j] - covariance[j][i]) > 1e-10 * scale for i in range(n) for j in range(n)):
            raise ValueError("input covariance must be symmetric")
        covariance = [[0.5 * (covariance[i][j] + covariance[j][i]) for j in range(n)] for i in range(n)]
        if min(_jacobi_eigenvalues(covariance)) < -1e-10 * scale:
            raise ValueError("input covariance must be positive semidefinite")
        propagated = []
        for r in range(2):
            output_row = []
            for s in range(2):
                value = sum(jacobian[r][i] * covariance[i][j] * jacobian[s][j]
                            for i in range(n) for j in range(n))
                output_row.append(value)
            propagated.append(output_row)
        result["input_covariance"] = covariance
        result["endpoint_covariance"] = propagated
    return result
