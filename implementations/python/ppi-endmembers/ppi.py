"""Pixel Purity Index (PPI) candidate scoring for hyperspectral cubes."""
from __future__ import annotations
import numpy as np

def pixel_purity_index(cube, n_projections=1000, *, top_k=None, valid_mask=None, seed=0):
    """Rank candidate pure pixels by repeated random-projection extrema.

    cube is finite (rows, columns, bands) data. Each random unit direction
    votes for the minimum and maximum projected valid pixel. Returns a
    row-major score raster (-1 for excluded pixels), ranked flat indices,
    and the corresponding original spectra.

    PPI is a candidate-screening heuristic, not a classifier or proof of
    physical purity. Rankings depend on projection count, preprocessing,
    noise and the population of valid pixels.
    """
    x = np.asarray(cube, dtype=float)
    if x.ndim != 3 or min(x.shape) < 1 or not np.all(np.isfinite(x)):
        raise ValueError("cube must be a finite non-empty (rows, cols, bands) array")
    if not isinstance(n_projections, (int, np.integer)) or n_projections < 1:
        raise ValueError("n_projections must be a positive integer")
    rows, cols, bands = x.shape
    if valid_mask is None:
        valid = np.ones((rows, cols), dtype=bool)
    else:
        raw_mask = np.asarray(valid_mask)
        if raw_mask.shape != (rows, cols) or raw_mask.dtype.kind != "b":
            raise ValueError("valid_mask must be a boolean array matching cube rows and columns")
        valid = raw_mask.copy()
    flat_valid = np.flatnonzero(valid.ravel())
    if flat_valid.size == 0:
        raise ValueError("valid_mask must select at least one pixel")
    spectra = x.reshape(-1, bands)[flat_valid]
    centered = spectra - spectra.mean(axis=0, keepdims=True)
    rng = np.random.default_rng(seed)
    scores = np.zeros(flat_valid.size, dtype=np.int64)
    for _ in range(int(n_projections)):
        direction = rng.normal(size=bands)
        norm = np.linalg.norm(direction)
        while norm == 0.0:
            direction = rng.normal(size=bands)
            norm = np.linalg.norm(direction)
        projection = centered @ (direction / norm)
        scores[int(np.argmin(projection))] += 1
        scores[int(np.argmax(projection))] += 1
    order = np.argsort(-scores, kind="stable")
    if top_k is not None:
        if not isinstance(top_k, (int, np.integer)) or top_k < 1:
            raise ValueError("top_k must be a positive integer when supplied")
        order = order[:int(top_k)]
    full_scores = np.full(rows * cols, -1, dtype=np.int64)
    full_scores[flat_valid] = scores
    candidate_indices = flat_valid[order]
    return {
        "scores": full_scores.reshape(rows, cols),
        "candidate_indices": candidate_indices,
        "candidate_spectra": x.reshape(-1, bands)[candidate_indices].copy(),
        "n_projections": int(n_projections),
    }
