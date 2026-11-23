"""Low-rank matrix completion by iterative singular-value thresholding."""
import math
import numpy as np


def soft_impute(matrix, *, regularization, max_rank=None,
                tolerance=1e-5, max_iterations=500):
    """Complete NaN cells with a nuclear-norm soft-thresholded SVD baseline.

    Observed cells are clamped to their original values on every iteration.
    Missing cells are initialized with the global observed mean.
    """
    data = np.asarray(matrix, dtype=float)
    if data.ndim != 2 or min(data.shape) < 1 or np.isinf(data).any():
        raise ValueError("matrix must be 2D and contain finite values or NaN")
    observed = np.isfinite(data)
    if not observed.any():
        raise ValueError("matrix must contain at least one observed value")
    if isinstance(regularization, bool) or not isinstance(regularization, (int, float)) or not math.isfinite(regularization) or regularization < 0:
        raise ValueError("regularization must be finite and nonnegative")
    if max_rank is not None and (isinstance(max_rank, bool) or not isinstance(max_rank, int) or max_rank < 1):
        raise ValueError("max_rank must be a positive integer or None")
    if isinstance(tolerance, bool) or not isinstance(tolerance, (int, float)) or not math.isfinite(tolerance) or tolerance <= 0:
        raise ValueError("tolerance must be finite and positive")
    if isinstance(max_iterations, bool) or not isinstance(max_iterations, int) or max_iterations < 1:
        raise ValueError("max_iterations must be a positive integer")
    if observed.all():
        return {"completed": data.tolist(), "iterations": 0, "converged": True,
                "relative_change": 0.0, "rank": int(np.linalg.matrix_rank(data))}
    mean_value = float(np.mean(data[observed]))
    filled = np.where(observed, data, mean_value)
    missing = ~observed
    converged = False
    relative_change = float("inf")
    singular_values = np.array([], dtype=float)
    for iteration in range(1, max_iterations + 1):
        u, singular_values, vt = np.linalg.svd(filled, full_matrices=False)
        shrunk = np.maximum(singular_values - float(regularization), 0.0)
        if max_rank is not None:
            shrunk[max_rank:] = 0.0
        reconstruction = (u * shrunk) @ vt
        old_missing = filled[missing].copy()
        filled[missing] = reconstruction[missing]
        denominator = max(float(np.linalg.norm(old_missing)), 1.0)
        relative_change = float(np.linalg.norm(filled[missing] - old_missing) / denominator)
        if relative_change <= float(tolerance):
            converged = True
            break
    final_u, final_s, final_vt = np.linalg.svd(filled, full_matrices=False)
    final_shrunk = np.maximum(final_s - float(regularization), 0.0)
    if max_rank is not None:
        final_shrunk[max_rank:] = 0.0
    final = (final_u * final_shrunk) @ final_vt
    completed = np.where(observed, data, final)
    effective_rank = int(np.count_nonzero(final_shrunk > 0))
    return {"completed": completed.tolist(), "iterations": iteration,
            "converged": converged, "relative_change": relative_change,
            "rank": effective_rank, "singular_values": final_s.tolist()}
