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


def hansen_hurwitz(sampled_values, draw_probabilities, *, population_size=None):
    """Estimate a finite-population total from independent with-replacement draws.

    draw_probabilities contains the per-draw selection probability of the
    sampled unit on each draw. The variance estimate is the sample variance
    of y_i/p_i divided by the number of draws; it is unavailable for one draw.
    """
    y=np.asarray(sampled_values,dtype=float)
    p=np.asarray(draw_probabilities,dtype=float)
    if y.ndim!=1 or y.size<1 or not np.isfinite(y).all():
        raise ValueError("sampled_values must be a finite non-empty 1D array")
    if p.shape!=y.shape or not np.isfinite(p).all() or np.any(p<=0) or np.any(p>1):
        raise ValueError("draw_probabilities must match values and lie in (0,1]")
    if population_size is not None:
        if isinstance(population_size,bool) or not isinstance(population_size,int) or population_size<1:
            raise ValueError("population_size must be a positive integer")
    weighted=y/p
    total=float(np.mean(weighted))
    n=len(y)
    variance=float(np.sum((weighted-total)**2)/(n*(n-1))) if n>1 else None
    result={"total":total,"variance_total":variance,
            "standard_error_total":float(np.sqrt(variance)) if variance is not None else None,
            "draw_count":n}
    if population_size is not None:
        result.update({"mean":total/population_size,
                       "variance_mean":variance/(population_size**2) if variance is not None else None,
                       "standard_error_mean":float(np.sqrt(variance))/population_size if variance is not None else None})
    return result
