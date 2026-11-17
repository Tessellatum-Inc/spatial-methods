"""Small Euclidean stationary covariance models for teaching and diagnostics."""
from __future__ import annotations

from typing import Literal

import numpy as np
from numpy.typing import ArrayLike, NDArray

Model = Literal["exponential", "gaussian", "matern32", "spherical", "wendland_c2"]


def covariance_from_distance(
    distances: ArrayLike,
    *,
    model: Model = "exponential",
    variance: float = 1.0,
    range_scale: float = 1.0,
) -> NDArray[np.float64]:
    """Evaluate a normalised stationary covariance model at nonnegative distances.

    Distances and range_scale must use the same Euclidean coordinate units.
    The spherical and Wendland C2 forms are restricted here to dimensions <= 3;
    use them only with coordinates in those dimensions.
    """
    h = np.asarray(distances, dtype=np.float64)
    if not np.all(np.isfinite(h)) or np.any(h < 0):
        raise ValueError("distances must be finite and non-negative")
    if not np.isfinite(variance) or variance <= 0:
        raise ValueError("variance must be finite and positive")
    if not np.isfinite(range_scale) or range_scale <= 0:
        raise ValueError("range_scale must be finite and positive")

    r = h / float(range_scale)
    if model == "exponential":
        corr = np.exp(-r)
    elif model == "gaussian":
        corr = np.exp(-(r**2))
    elif model == "matern32":
        q = np.sqrt(3.0) * r
        corr = (1.0 + q) * np.exp(-q)
    elif model == "spherical":
        corr = np.where(r < 1.0, 1.0 - 1.5 * r + 0.5 * r**3, 0.0)
    elif model == "wendland_c2":
        corr = np.where(r < 1.0, (1.0 - r) ** 4 * (1.0 + 4.0 * r), 0.0)
    else:
        raise ValueError(f"unsupported covariance model: {model}")
    return np.asarray(float(variance) * corr, dtype=np.float64)


def covariance_matrix(
    locations: ArrayLike,
    *,
    model: Model = "exponential",
    variance: float = 1.0,
    range_scale: float = 1.0,
) -> NDArray[np.float64]:
    """Build a dense covariance matrix from finite Euclidean coordinates."""
    xy = np.asarray(locations, dtype=np.float64)
    if xy.ndim != 2 or xy.shape[0] == 0 or xy.shape[1] == 0:
        raise ValueError("locations must be a non-empty (n, dimensions) array")
    if not np.all(np.isfinite(xy)):
        raise ValueError("locations must be finite")
    if model in ("spherical", "wendland_c2") and xy.shape[1] > 3:
        raise ValueError(f"{model} is only enabled for Euclidean dimensions <= 3")
    delta = xy[:, None, :] - xy[None, :, :]
    distances = np.sqrt(np.sum(delta * delta, axis=2))
    return covariance_from_distance(
        distances, model=model, variance=variance, range_scale=range_scale
    )


def semivariogram_from_distance(
    distances: ArrayLike,
    *,
    model: Model = "exponential",
    variance: float = 1.0,
    range_scale: float = 1.0,
) -> NDArray[np.float64]:
    """Return gamma(h) = C(0) - C(h) for the selected covariance model."""
    return variance - covariance_from_distance(
        distances, model=model, variance=variance, range_scale=range_scale
    )


def covariance_matrix_diagnostics(matrix: ArrayLike, *, tolerance: float = 1e-10) -> dict[str, float | bool]:
    """Report symmetry and eigenvalue diagnostics; this is not a proof of validity."""
    cov = np.asarray(matrix, dtype=np.float64)
    if cov.ndim != 2 or cov.shape[0] == 0 or cov.shape[0] != cov.shape[1]:
        raise ValueError("matrix must be a non-empty square array")
    if not np.all(np.isfinite(cov)):
        raise ValueError("matrix must be finite")
    if not np.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and non-negative")
    symmetric = bool(np.allclose(cov, cov.T, rtol=0.0, atol=tolerance))
    eigenvalues = np.linalg.eigvalsh((cov + cov.T) / 2.0)
    minimum = float(eigenvalues[0])
    maximum = float(eigenvalues[-1])
    return {
        "symmetric": symmetric,
        "minimum_eigenvalue": minimum,
        "maximum_eigenvalue": maximum,
        "positive_semidefinite_within_tolerance": bool(symmetric and minimum >= -tolerance),
    }



def _rff_features(locations, frequencies, phases, signal_variance):
    locations = np.asarray(locations, dtype=np.float64)
    return np.sqrt(2.0 * signal_variance / len(phases)) * np.cos(
        locations @ frequencies + phases
    )


def fit_random_fourier_gp(
    locations,
    values,
    *,
    range_scale=1.0,
    signal_variance=1.0,
    noise_variance=0.1,
    feature_count=256,
    mean=0.0,
    seed=0,
):
    """Fit a Gaussian-kernel GP approximation by Bayesian random features.

    The target kernel is signal_variance * exp(-(distance/range_scale)^2).
    Frequencies are sampled from N(0, 2/range_scale^2 I), the spectral
    distribution for this package's Gaussian covariance convention.
    Bayesian linear regression in the random feature basis returns a
    posterior mean and latent predictive variance.
    """
    from numbers import Integral

    xy = np.asarray(locations, dtype=np.float64)
    y = np.asarray(values, dtype=np.float64)
    if xy.ndim != 2 or xy.shape[0] < 1 or xy.shape[1] < 1:
        raise ValueError("locations must be a non-empty (n, dimensions) array")
    if not np.isfinite(xy).all():
        raise ValueError("locations must be finite")
    if y.shape != (len(xy),) or not np.isfinite(y).all():
        raise ValueError("values must be finite and match locations")
    try:
        range_scale, signal_variance, noise_variance, mean = map(
            float, (range_scale, signal_variance, noise_variance, mean)
        )
    except (TypeError, ValueError) as exc:
        raise ValueError("model parameters and mean must be finite scalars") from exc
    if not np.isfinite((range_scale, signal_variance, noise_variance, mean)).all():
        raise ValueError("model parameters and mean must be finite")
    if range_scale <= 0 or signal_variance <= 0 or noise_variance <= 0:
        raise ValueError("range_scale, signal_variance and noise_variance must be positive")
    if isinstance(feature_count, bool) or not isinstance(feature_count, Integral) or feature_count < 1:
        raise ValueError("feature_count must be a positive integer")
    if isinstance(seed, bool) or (seed is not None and not isinstance(seed, Integral)):
        raise ValueError("seed must be an integer or None")
    rng = np.random.default_rng(None if seed is None else int(seed))
    frequencies = rng.normal(
        0.0, np.sqrt(2.0) / range_scale,
        size=(xy.shape[1], int(feature_count)),
    )
    phases = rng.uniform(0.0, 2.0 * np.pi, size=int(feature_count))
    design = _rff_features(xy, frequencies, phases, signal_variance)
    precision = np.eye(int(feature_count)) + (design.T @ design) / noise_variance
    rhs = (design.T @ (y - mean)) / noise_variance
    try:
        solved = np.linalg.solve(precision, np.column_stack((rhs, np.eye(int(feature_count)))))
    except np.linalg.LinAlgError as exc:
        raise ValueError("random-feature posterior system is singular") from exc
    weight_mean = solved[:, 0]
    weight_covariance = solved[:, 1:]
    weight_covariance = 0.5 * (weight_covariance + weight_covariance.T)
    return {
        "frequencies": frequencies,
        "phases": phases,
        "weight_mean": weight_mean,
        "weight_covariance": weight_covariance,
        "mean": mean,
        "range_scale": range_scale,
        "signal_variance": signal_variance,
        "noise_variance": noise_variance,
        "feature_count": int(feature_count),
        "dimensions": int(xy.shape[1]),
        "training_observations": int(len(xy)),
    }


def predict_random_fourier_gp(model, locations):
    """Return approximate latent GP posterior means and variances."""
    xy = np.asarray(locations, dtype=np.float64)
    if xy.ndim != 2 or xy.shape[1] != model.get("dimensions") or len(xy) < 1:
        raise ValueError("locations must be a non-empty array with the fitted dimension")
    if not np.isfinite(xy).all():
        raise ValueError("locations must be finite")
    design = _rff_features(
        xy, model["frequencies"], model["phases"], model["signal_variance"]
    )
    prediction = model["mean"] + design @ model["weight_mean"]
    projected = design @ model["weight_covariance"]
    variance = np.sum(projected * design, axis=1)
    tolerance = 1e-9 * max(1.0, model["signal_variance"])
    if not np.isfinite(prediction).all() or not np.isfinite(variance).all():
        raise ValueError("random-feature prediction is non-finite")
    if np.any(variance < -tolerance):
        raise ValueError("random-feature posterior variance is materially negative")
    return {"mean": prediction, "variance": np.maximum(variance, 0.0)}
