"""Dense Tucker decomposition using truncated higher-order SVD (HOSVD)."""
from __future__ import annotations
import numpy as np

def _unfold(tensor, mode):
    return np.moveaxis(tensor, mode, 0).reshape(tensor.shape[mode], -1)

def _mode_product(tensor, matrix, mode):
    moved = np.moveaxis(tensor, mode, 0)
    product = matrix @ moved.reshape(moved.shape[0], -1)
    shaped = product.reshape((matrix.shape[0],) + moved.shape[1:])
    return np.moveaxis(shaped, 0, mode)

def tucker_reconstruct(core, factors):
    """Reconstruct a Tucker tensor from its core and mode factor matrices."""
    result = np.asarray(core, dtype=float)
    if result.ndim < 2 or len(factors) != result.ndim:
        raise ValueError("one factor matrix is required for every core mode")
    for mode, factor in enumerate(factors):
        factor = np.asarray(factor, dtype=float)
        if factor.ndim != 2 or factor.shape[1] != result.shape[mode]:
            raise ValueError("factor column count must match its core mode")
        result = _mode_product(result, factor, mode)
    return result

def tucker_hosvd(tensor, ranks):
    """Compute a truncated HOSVD approximation for a dense finite N-way tensor.

    Truncated HOSVD is a subspace projection, not generally the globally best
    Tucker approximation at the requested multilinear rank.
    """
    x = np.asarray(tensor, dtype=float)
    if x.ndim < 2 or any(size < 1 for size in x.shape):
        raise ValueError("tensor must have order >= 2 and nonempty modes")
    if not np.all(np.isfinite(x)):
        raise ValueError("tensor must contain only finite values")
    try:
        ranks = tuple(ranks)
    except TypeError as exc:
        raise ValueError("ranks must be a sequence with one entry per mode") from exc
    if len(ranks) != x.ndim:
        raise ValueError("ranks must contain one value per tensor mode")
    checked = []
    for rank, size in zip(ranks, x.shape):
        if not isinstance(rank, (int, np.integer)) or isinstance(rank, (bool, np.bool_)):
            raise ValueError("each multilinear rank must be an integer")
        if rank < 1 or rank > size:
            raise ValueError("each rank must be between 1 and its mode size")
        checked.append(int(rank))
    factors = []
    for mode, rank in enumerate(checked):
        u, _, _ = np.linalg.svd(_unfold(x, mode), full_matrices=False)
        factors.append(u[:, :rank])
    core = x.copy()
    for mode, factor in enumerate(factors):
        core = _mode_product(core, factor.T, mode)
    reconstruction = tucker_reconstruct(core, factors)
    norm_x = float(np.linalg.norm(x))
    error = 0.0 if norm_x == 0 else float(np.linalg.norm(x - reconstruction) / norm_x)
    return {"core": core, "factors": factors, "reconstruction": reconstruction,
            "relative_error": error, "multilinear_rank": tuple(checked)}
