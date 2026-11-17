"""Dense covariance-based simple, ordinary and linear universal kriging."""
from __future__ import annotations

import numpy as np

_MODELS = {"spherical", "exponential", "gaussian"}


def _points(value, name, *, minimum):
    array = np.asarray(value, dtype=float)
    if array.ndim != 2 or array.shape[1] != 2 or len(array) < minimum:
        raise ValueError(f"{name} must be an n-by-2 array with n>={minimum}")
    if not np.isfinite(array).all():
        raise ValueError(f"{name} must contain only finite coordinates")
    return array


def _covariance(distance, *, model, partial_sill, range_):
    ratio = distance / range_
    if model == "spherical":
        semivariance = np.where(
            ratio < 1.0, 1.5 * ratio - 0.5 * ratio**3, 1.0
        )
        correlation = 1.0 - semivariance
    elif model == "exponential":
        correlation = np.exp(-3.0 * ratio)
    else:
        correlation = np.exp(-3.0 * ratio**2)
    return partial_sill * correlation


def kriging_predict(
    points,
    values,
    targets,
    *,
    drift="ordinary",
    model="exponential",
    nugget=0.0,
    partial_sill=1.0,
    range_=1.0,
    observation_noise=0.0,
    known_mean=0.0,
):
    """Predict latent field values and variances at target coordinates.

    drift='simple' uses a supplied known_mean; 'ordinary' estimates an
    unknown constant mean; 'linear' uses an unknown planar drift
    beta0 + beta_x*x + beta_y*y. All unknown-drift variants enforce
    unbiasedness constraints through one block covariance solve.

    nugget and observation_noise enter the observation covariance diagonal.
    The target is the latent spatial field, so its marginal variance is
    partial_sill and the observation diagonal noise is not added to it.
    """
    xy = _points(points, "points", minimum=1)
    target = _points(targets, "targets", minimum=1)
    z = np.asarray(values, dtype=float)
    if z.shape != (len(xy),) or not np.isfinite(z).all():
        raise ValueError("values must be finite and match points")
    if drift not in {"simple", "ordinary", "linear"}:
        raise ValueError("drift must be simple, ordinary or linear")
    if model not in _MODELS:
        raise ValueError("model must be spherical, exponential or gaussian")
    try:
        nugget, sill, range_, noise, mean = map(
            float, (nugget, partial_sill, range_, observation_noise, known_mean)
        )
    except (TypeError, ValueError) as exc:
        raise ValueError("covariance parameters and known_mean must be scalar numbers") from exc
    if not np.isfinite((nugget, sill, range_, noise, mean)).all():
        raise ValueError("covariance parameters and known_mean must be finite")
    if nugget < 0 or noise < 0 or sill <= 0 or range_ <= 0:
        raise ValueError("nugget/noise must be nonnegative; sill/range must be positive")

    data_delta = xy[:, None, :] - xy[None, :, :]
    target_delta = xy[:, None, :] - target[None, :, :]
    data_distance = np.hypot(data_delta[:, :, 0], data_delta[:, :, 1])
    target_distance = np.hypot(target_delta[:, :, 0], target_delta[:, :, 1])
    covariance = _covariance(
        data_distance, model=model, partial_sill=sill, range_=range_
    )
    covariance.flat[:: len(xy) + 1] += nugget + noise
    cross = _covariance(
        target_distance, model=model, partial_sill=sill, range_=range_
    )

    try:
        if drift == "simple":
            weights = np.linalg.solve(covariance, cross)
            prediction = mean + weights.T @ (z - mean)
            variance = sill - np.sum(weights * cross, axis=0)
        else:
            if drift == "ordinary":
                design = np.ones((len(xy), 1))
                target_design = np.ones((len(target), 1))
            else:
                centre = xy.mean(axis=0)
                scale = xy.std(axis=0)
                scale[scale == 0] = 1.0
                design = np.column_stack(
                    (np.ones(len(xy)), (xy - centre) / scale)
                )
                target_design = np.column_stack(
                    (np.ones(len(target)), (target - centre) / scale)
                )
                if np.linalg.matrix_rank(design) != design.shape[1]:
                    raise ValueError("linear drift design is rank deficient")
            p = design.shape[1]
            system = np.block([
                [covariance, design],
                [design.T, np.zeros((p, p))],
            ])
            rhs = np.vstack((cross, target_design.T))
            solution = np.linalg.solve(system, rhs)
            weights = solution[: len(xy)]
            multipliers = solution[len(xy) :]
            prediction = weights.T @ z
            variance = (
                sill
                - np.sum(weights * cross, axis=0)
                - np.sum(multipliers * target_design.T, axis=0)
            )
    except np.linalg.LinAlgError as exc:
        raise ValueError(
            "kriging system is singular; inspect duplicate sites, drift rank and covariance parameters"
        ) from exc

    tolerance = 1e-9 * max(1.0, sill)
    if not np.isfinite(prediction).all() or not np.isfinite(variance).all():
        raise ValueError("kriging solution is non-finite")
    if np.any(variance < -tolerance):
        raise ValueError("kriging variance is materially negative; inspect covariance model")
    variance = np.maximum(variance, 0.0)
    return {
        "prediction": np.asarray(prediction, dtype=float),
        "variance": np.asarray(variance, dtype=float),
        "weights": np.asarray(weights.T, dtype=float),
        "drift": drift,
        "model": model,
        "observations": int(len(xy)),
        "targets": int(len(target)),
    }



def sequential_gaussian_simulation(
    observation_points,
    observation_values,
    grid_points,
    *,
    model="exponential",
    partial_sill=1.0,
    range_=1.0,
    observation_noise=0.0,
    mean=0.0,
    seed=0,
):
    """Generate a sequential conditional Gaussian simulation at grid points.

    This simple-kriging simulator uses a supplied known mean and stationary
    covariance model. Grid locations are visited in seeded random order.
    Each new latent value is sampled from its Gaussian conditional
    distribution given the observations and all previously simulated cells.
    Observation noise applies only to the supplied measurements.
    """
    from numbers import Integral

    obs = _points(observation_points, "observation_points", minimum=1)
    grid = _points(grid_points, "grid_points", minimum=1)
    z = np.asarray(observation_values, dtype=float)
    if z.shape != (len(obs),) or not np.isfinite(z).all():
        raise ValueError("observation_values must be finite and match observation_points")
    if len({tuple(row) for row in obs}) != len(obs):
        raise ValueError("observation locations must be unique")
    if len({tuple(row) for row in grid}) != len(grid):
        raise ValueError("grid locations must be unique")
    if model not in _MODELS:
        raise ValueError("model must be spherical, exponential or gaussian")
    try:
        sill, range_, noise, mean = map(
            float, (partial_sill, range_, observation_noise, mean)
        )
    except (TypeError, ValueError) as exc:
        raise ValueError("simulation parameters must be scalar numbers") from exc
    if not np.isfinite((sill, range_, noise, mean)).all():
        raise ValueError("simulation parameters must be finite")
    if sill <= 0 or range_ <= 0 or noise < 0:
        raise ValueError("partial_sill and range_ must be positive; observation_noise nonnegative")
    if isinstance(seed, bool) or (seed is not None and not isinstance(seed, Integral)):
        raise ValueError("seed must be an integer or None")

    rng = np.random.default_rng(None if seed is None else int(seed))
    output = np.empty(len(grid), dtype=float)
    fixed = {}
    if noise == 0:
        lookup = {tuple(point): float(value) for point, value in zip(obs, z)}
        for index, point in enumerate(grid):
            if tuple(point) in lookup:
                fixed[index] = lookup[tuple(point)]
                output[index] = lookup[tuple(point)]
    order = rng.permutation(len(grid))
    locations = [point.copy() for point in obs]
    values = list(map(float, z))
    diagonal_noise = [noise] * len(obs)
    for raw_index in order:
        index = int(raw_index)
        if index in fixed:
            continue
        target = grid[index]
        current = np.asarray(locations, dtype=float)
        delta = current[:, None, :] - current[None, :, :]
        distances = np.hypot(delta[:, :, 0], delta[:, :, 1])
        covariance = _covariance(
            distances, model=model, partial_sill=sill, range_=range_
        )
        covariance.flat[:: len(current) + 1] += np.asarray(diagonal_noise)
        cross_distance = np.linalg.norm(current - target, axis=1)
        cross = _covariance(
            cross_distance, model=model, partial_sill=sill, range_=range_
        )
        try:
            weights = np.linalg.solve(covariance, cross)
        except np.linalg.LinAlgError as exc:
            raise ValueError("conditioning covariance is singular; inspect duplicate sites and noise") from exc
        conditional_mean = mean + float(weights @ (np.asarray(values) - mean))
        conditional_variance = sill - float(weights @ cross)
        tolerance = 1e-9 * max(1.0, sill)
        if conditional_variance < -tolerance or not np.isfinite(conditional_variance):
            raise ValueError("conditional simulation variance is invalid")
        conditional_variance = max(0.0, conditional_variance)
        draw = float(rng.normal(conditional_mean, np.sqrt(conditional_variance)))
        output[index] = draw
        locations.append(target.copy())
        values.append(draw)
        diagonal_noise.append(0.0)
    return {
        "values": output,
        "simulation_order": np.asarray(order, dtype=int),
        "fixed_grid_indices": tuple(sorted(fixed)),
        "model": model,
        "mean": mean,
        "partial_sill": sill,
        "range": range_,
    }
