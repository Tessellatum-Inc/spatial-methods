"""Deterministic pixel-wise optical image compositing."""
from __future__ import annotations
import numpy as np


def _prepare(cube, valid_mask):
    x = np.asarray(cube, dtype=float)
    if x.ndim != 4 or min(x.shape) < 1 or not np.all(np.isfinite(x)):
        raise ValueError("cube must be finite (time, rows, cols, bands) data")
    t, rows, cols, bands = x.shape
    if valid_mask is None:
        valid = np.ones((t, rows, cols), dtype=bool)
    else:
        raw = np.asarray(valid_mask)
        if raw.shape != (t, rows, cols) or raw.dtype.kind != "b":
            raise ValueError("valid_mask must be boolean with shape (time, rows, cols)")
        valid = raw.copy()
    return x, valid


def _assemble(x, valid, selected):
    t, rows, cols, bands = x.shape
    composite = np.full((rows, cols, bands), np.nan, dtype=float)
    rr, cc = np.indices((rows, cols))
    has = selected >= 0
    composite[has] = x[selected[has], rr[has], cc[has]]
    return {
        "composite": composite,
        "selected_time_index": selected,
        "valid_observation_count": valid.sum(axis=0).astype(np.int32),
    }


def best_pixel_composite(cube, quality, *, valid_mask=None):
    """Select the highest-quality valid observation at each pixel.

    Higher quality is better. Ties select the earliest time index.
    """
    x, valid = _prepare(cube, valid_mask)
    q = np.asarray(quality, dtype=float)
    if q.shape != valid.shape or not np.all(np.isfinite(q)):
        raise ValueError("quality must be finite with shape (time, rows, cols)")
    scores = np.where(valid, q, -np.inf)
    selected = np.argmax(scores, axis=0).astype(np.int32)
    selected[~valid.any(axis=0)] = -1
    out = _assemble(x, valid, selected)
    out["selected_quality"] = np.where(selected >= 0,
        np.take_along_axis(q, np.maximum(selected, 0)[None, ...], axis=0)[0], np.nan)
    return out


def medoid_composite(cube, *, valid_mask=None):
    """Select the observed spectrum nearest the per-band temporal median.

    Euclidean distance is measured in the input band units. Bands with larger
    numeric scales therefore contribute more to the medoid distance.
    Ties select the earliest valid observation.
    """
    x, valid = _prepare(cube, valid_mask)
    t, rows, cols, bands = x.shape
    selected = np.full((rows, cols), -1, dtype=np.int32)
    for r in range(rows):
        for c in range(cols):
            times = np.flatnonzero(valid[:, r, c])
            if times.size == 0:
                continue
            spectra = x[times, r, c, :]
            target = np.median(spectra, axis=0)
            distances = np.sum((spectra - target) ** 2, axis=1)
            selected[r, c] = int(times[np.argmin(distances)])
    return _assemble(x, valid, selected)


def maximum_ndvi_composite(cube, red_band, nir_band, *, valid_mask=None, epsilon=1e-12):
    """Select the complete observed spectrum with maximum per-date NDVI."""
    x, valid = _prepare(cube, valid_mask)
    bands = x.shape[-1]
    for name, index in (("red_band", red_band), ("nir_band", nir_band)):
        if not isinstance(index, (int, np.integer)) or not 0 <= index < bands:
            raise ValueError(f"{name} must be a valid band index")
    if red_band == nir_band:
        raise ValueError("red_band and nir_band must differ")
    if not np.isfinite(epsilon) or epsilon <= 0:
        raise ValueError("epsilon must be positive and finite")
    red, nir = x[..., red_band], x[..., nir_band]
    denominator = nir + red
    ndvi = np.divide(nir - red, denominator, out=np.full_like(denominator, np.nan),
                     where=np.abs(denominator) > epsilon)
    eligible = valid & np.isfinite(ndvi)
    scores = np.where(eligible, ndvi, -np.inf)
    selected = np.argmax(scores, axis=0).astype(np.int32)
    has = eligible.any(axis=0)
    selected[~has] = -1
    out = _assemble(x, valid, selected)
    out["selected_ndvi"] = np.where(has,
        np.take_along_axis(ndvi, np.maximum(selected, 0)[None, ...], axis=0)[0], np.nan)
    return out
