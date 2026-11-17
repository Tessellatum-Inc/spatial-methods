"""Vecchia nearest-neighbour approximation to a zero-mean Gaussian process."""
from __future__ import annotations
import numpy as np


def squared_exponential_covariance(coordinates, *, variance=1.0, length_scale=1.0, nugget=0.0):
    """Build an isotropic squared-exponential covariance matrix."""
    x = np.asarray(coordinates, dtype=float)
    if x.ndim != 2 or x.shape[0] == 0 or x.shape[1] == 0 or not np.all(np.isfinite(x)):
        raise ValueError("coordinates must be a nonempty finite 2-D array")
    if not np.isfinite(variance) or variance <= 0:
        raise ValueError("variance must be finite and positive")
    if not np.isfinite(length_scale) or length_scale <= 0:
        raise ValueError("length_scale must be finite and positive")
    if not np.isfinite(nugget) or nugget < 0:
        raise ValueError("nugget must be finite and nonnegative")
    delta = x[:, None, :] - x[None, :, :]
    d2 = np.sum(delta * delta, axis=-1)
    covariance = variance * np.exp(-0.5 * d2 / (length_scale * length_scale))
    covariance.flat[::len(x) + 1] += nugget
    return covariance


def vecchia_loglikelihood(observations, coordinates, *, variance=1.0,
                          length_scale=1.0, nugget=0.0, n_neighbors=10,
                          order=None, jitter=1e-10):
    """Evaluate Vecchia's product of local Gaussian conditionals.

    At each ordered site, condition on its n_neighbors nearest predecessors.
    With all predecessors selected, the factorisation is the exact Gaussian
    likelihood (up to numerical jitter).
    """
    y = np.asarray(observations, dtype=float)
    x = np.asarray(coordinates, dtype=float)
    if y.ndim != 1 or x.ndim != 2 or x.shape[0] != y.size or y.size == 0:
        raise ValueError("observations must be 1-D and match nonempty coordinate rows")
    if not np.all(np.isfinite(y)) or not np.all(np.isfinite(x)):
        raise ValueError("observations and coordinates must be finite")
    if not isinstance(n_neighbors, int) or isinstance(n_neighbors, bool) or n_neighbors < 1:
        raise ValueError("n_neighbors must be a positive integer")
    if not np.isfinite(jitter) or jitter < 0:
        raise ValueError("jitter must be finite and nonnegative")
    if order is None:
        ordering = np.arange(y.size)
    else:
        ordering = np.asarray(order)
        if ordering.shape != (y.size,) or not np.issubdtype(ordering.dtype, np.integer) or not np.array_equal(np.sort(ordering), np.arange(y.size)):
            raise ValueError("order must be a permutation of observation indices")
    covariance = squared_exponential_covariance(
        x, variance=variance, length_scale=length_scale, nugget=nugget)
    means = np.zeros(y.size, dtype=float)
    conditional_variances = np.diag(covariance).copy()
    loglikelihood = 0.0
    for position, index in enumerate(ordering):
        previous = ordering[:position]
        if previous.size:
            distances2 = np.sum((x[previous] - x[index]) ** 2, axis=1)
            neighbours = previous[np.argsort(distances2, kind="stable")[:n_neighbors]]
            knn = covariance[np.ix_(neighbours, neighbours)].copy()
            knn.flat[::len(neighbours) + 1] += jitter
            kin = covariance[index, neighbours]
            try:
                weights = np.linalg.solve(knn, y[neighbours])
                solved_cov = np.linalg.solve(knn, kin)
            except np.linalg.LinAlgError as exc:
                raise ValueError("local covariance system is singular; increase nugget or jitter") from exc
            mean = float(kin @ weights)
            conditional_variance = float(covariance[index, index] - kin @ solved_cov)
        else:
            mean = 0.0
            conditional_variance = float(covariance[index, index])
        if not np.isfinite(conditional_variance) or conditional_variance <= 0:
            raise ValueError("non-positive conditional variance; increase nugget or jitter")
        means[index] = mean
        conditional_variances[index] = conditional_variance
        residual = y[index] - mean
        loglikelihood += -0.5 * (np.log(2*np.pi) + np.log(conditional_variance)
                                 + residual*residual/conditional_variance)
    return {"loglikelihood": float(loglikelihood), "conditional_means": means,
            "conditional_variances": conditional_variances,
            "order": ordering.copy()}
