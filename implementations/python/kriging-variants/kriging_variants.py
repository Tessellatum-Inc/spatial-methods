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
