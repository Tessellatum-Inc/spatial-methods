"""Exact max-min p-dispersion for small finite candidate sets."""
from __future__ import annotations

from itertools import combinations
from typing import Sequence

import numpy as np


def solve_p_dispersion(
    distances: Sequence[Sequence[float]] | np.ndarray,
    p: int,
) -> tuple[tuple[int, ...], float]:
    """Select p sites maximizing their minimum pairwise distance.

    The matrix must be a symmetric, finite, non-negative pairwise distance
    matrix with a zero diagonal. Exact exhaustive enumeration is intended as
    a small-instance teaching baseline and oracle, not a large-scale solver.
    Ties are resolved lexicographically by candidate index.
    """
    matrix = np.asarray(distances, dtype=float)
    if matrix.ndim != 2 or matrix.shape[0] == 0 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("distances must be a non-empty square matrix")
    n = matrix.shape[0]
    if not isinstance(p, int) or isinstance(p, bool) or not 2 <= p <= n:
        raise ValueError("p must be an integer between 2 and the number of candidates")
    if not np.isfinite(matrix).all() or (matrix < 0).any():
        raise ValueError("distances must be finite and non-negative")
    if not np.allclose(matrix, matrix.T, rtol=1e-10, atol=1e-12):
        raise ValueError("distances must be symmetric")
    if not np.allclose(np.diag(matrix), 0.0, rtol=0.0, atol=1e-12):
        raise ValueError("distance matrix diagonal must be zero")

    best_sites: tuple[int, ...] | None = None
    best_separation = -float("inf")
    for sites in combinations(range(n), p):
        separation = min(matrix[i, j] for i, j in combinations(sites, 2))
        # Lexicographic combination order plus strict comparison fixes ties.
        if separation > best_separation:
            best_sites = sites
            best_separation = float(separation)
    assert best_sites is not None
    return best_sites, best_separation
