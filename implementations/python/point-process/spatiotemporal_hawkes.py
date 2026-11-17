"""Bounded spatiotemporal Hawkes simulation by branching clusters."""
from __future__ import annotations
import math
import numpy as np


def simulate_spatiotemporal_hawkes(
    background_rate, branching_ratio, temporal_decay, spatial_scale,
    window, horizon, *, seed=None, max_events=1_000_000,
):
    """Simulate exponential-time/Gaussian-space Hawkes clusters on a torus."""
    def finite(value, name):
        if isinstance(value, (bool, np.bool_)):
            raise ValueError(f"{name} must be finite")
        try:
            result = float(value)
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError(f"{name} must be finite") from exc
        if not math.isfinite(result):
            raise ValueError(f"{name} must be finite")
        return result

    mu = finite(background_rate, "background_rate")
    eta = finite(branching_ratio, "branching_ratio")
    beta = finite(temporal_decay, "temporal_decay")
    sigma = finite(spatial_scale, "spatial_scale")
    duration = finite(horizon, "horizon")
    try:
        if len(window) != 4:
            raise ValueError
        xmin, ymin, xmax, ymax = map(finite, window, ["window"] * 4)
    except (TypeError, ValueError) as exc:
        raise ValueError("window must be (xmin, ymin, xmax, ymax)") from exc
    if xmax <= xmin or ymax <= ymin or duration <= 0:
        raise ValueError("window and horizon must have positive extent")
    if mu < 0 or not 0 <= eta < 1 or beta <= 0 or sigma <= 0:
        raise ValueError("background rate must be nonnegative, branching ratio in [0,1), and scales positive")
    if isinstance(max_events, (bool, np.bool_)) or not isinstance(max_events, (int, np.integer)) or max_events < 1:
        raise ValueError("max_events must be a positive integer")

    width, height = xmax - xmin, ymax - ymin
    rng = np.random.default_rng(seed)
    immigrant_count = int(rng.poisson(mu * width * height * duration))
    if immigrant_count > max_events:
        raise RuntimeError("max_events exceeded by immigrant generation")
    times = list(rng.uniform(0.0, duration, size=immigrant_count))
    xs = list(rng.uniform(xmin, xmax, size=immigrant_count))
    ys = list(rng.uniform(ymin, ymax, size=immigrant_count))
    parents = [-1] * immigrant_count
    generations = [0] * immigrant_count

    cursor = 0
    while cursor < len(times):
        parent_time, parent_x, parent_y = times[cursor], xs[cursor], ys[cursor]
        child_count = int(rng.poisson(eta))
        if child_count:
            delays = rng.exponential(1.0 / beta, size=child_count)
            dx = rng.normal(0.0, sigma, size=child_count)
            dy = rng.normal(0.0, sigma, size=child_count)
            for delay, offset_x, offset_y in zip(delays, dx, dy):
                child_time = parent_time + float(delay)
                if child_time > duration:
                    continue
                if len(times) >= max_events:
                    raise RuntimeError("max_events exceeded during branching simulation")
                times.append(child_time)
                xs.append(xmin + ((parent_x + float(offset_x) - xmin) % width))
                ys.append(ymin + ((parent_y + float(offset_y) - ymin) % height))
                parents.append(cursor)
                generations.append(generations[cursor] + 1)
        cursor += 1

    if not times:
        return {"times": np.empty(0), "locations": np.empty((0, 2)),
                "parent_indices": np.empty(0, dtype=int),
                "generations": np.empty(0, dtype=int), "n_immigrants": 0,
                "n_events": 0, "branching_ratio": eta,
                "window": (xmin, ymin, xmax, ymax), "horizon": duration,
                "boundary": "periodic"}
    order = np.argsort(np.asarray(times), kind="stable")
    inverse = np.empty(len(order), dtype=int)
    inverse[order] = np.arange(len(order))
    sorted_parents = np.asarray([
        -1 if parents[int(i)] < 0 else inverse[parents[int(i)]]
        for i in order
    ], dtype=int)
    return {
        "times": np.asarray(times, dtype=float)[order],
        "locations": np.column_stack((np.asarray(xs)[order], np.asarray(ys)[order])),
        "parent_indices": sorted_parents,
        "generations": np.asarray(generations, dtype=int)[order],
        "n_immigrants": immigrant_count, "n_events": len(times),
        "branching_ratio": eta, "window": (xmin, ymin, xmax, ymax),
        "horizon": duration, "boundary": "periodic",
    }
