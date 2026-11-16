"""Design-based Horvitz-Thompson total and mean estimation."""
import numpy as np


def horvitz_thompson(values, inclusion_probabilities, pairwise_inclusion,
                     *, population_size=None):
    """Estimate a population total and its design variance from a sample.

    pairwise_inclusion[i,j] is pi_ij, with diagonal pi_ii = pi_i. Positive
    second-order inclusion probabilities are required for an unbiased
    variance estimator based on the supplied sample.
    """
    y = np.asarray(values, dtype=float)
    pi = np.asarray(inclusion_probabilities, dtype=float)
    pi2 = np.asarray(pairwise_inclusion, dtype=float)
    if y.ndim != 1 or len(y) < 1 or not np.isfinite(y).all():
        raise ValueError("values must be a finite non-empty 1D array")
    n = len(y)
    if pi.shape != (n,) or not np.isfinite(pi).all() or np.any(pi <= 0) or np.any(pi > 1):
        raise ValueError("inclusion_probabilities must be finite values in (0, 1]")
    if pi2.shape != (n, n) or not np.isfinite(pi2).all():
        raise ValueError("pairwise_inclusion must be a finite n-by-n matrix")
    if np.any(pi2 <= 0) or np.any(pi2 > 1):
        raise ValueError("all pairwise inclusion probabilities must be in (0, 1]")
    if not np.allclose(pi2, pi2.T, rtol=1e-10, atol=1e-12):
        raise ValueError("pairwise inclusion matrix must be symmetric")
    if not np.allclose(np.diag(pi2), pi, rtol=1e-10, atol=1e-12):
        raise ValueError("pairwise inclusion diagonal must equal first-order probabilities")
    if np.any(pi2 - np.minimum.outer(pi, pi) > 1e-10):
        raise ValueError("pairwise probabilities cannot exceed first-order probabilities")
    if population_size is not None:
        if isinstance(population_size, bool) or not isinstance(population_size, int) or population_size < n:
            raise ValueError("population_size must be an integer at least as large as sample size")

    weighted = y / pi
    total = float(np.sum(weighted))
    delta = pi2 - np.outer(pi, pi)
    variance = float(np.sum(delta * np.outer(weighted, weighted)))
    variance = 0.0 if abs(variance) < 1e-12 else variance
    result = {"total": total, "variance_total": variance,
              "standard_error_total": float(np.sqrt(max(variance, 0.0))) if variance >= 0 else None}
    if population_size is not None:
        result.update({
            "mean": total / population_size,
            "variance_mean": variance / (population_size ** 2),
            "standard_error_mean": (float(np.sqrt(variance)) / population_size) if variance >= 0 else None,
        })
    return result
