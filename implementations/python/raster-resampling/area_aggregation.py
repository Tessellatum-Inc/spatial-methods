"""Exact same-extent area-weighted raster aggregation."""
from __future__ import annotations

import math
from typing import Sequence

import numpy as np


def area_weighted_resample(
    source: Sequence[Sequence[float]] | np.ndarray,
    target_shape: tuple[int, int],
    *,
    nodata_policy: str = "strict",
) -> np.ndarray:
    """Aggregate an axis-aligned grid by exact rectangular cell overlap.

    Source and target cover the same extent and orientation. Source values are
    treated as piecewise-constant cell means. Non-finite values are NoData.
    Strict mode masks a target if any positive-area overlap is missing;
    renormalize mode divides by the valid overlap area.
    """
    data = np.asarray(source, dtype=float)
    if data.ndim != 2 or data.size == 0:
        raise ValueError("source must be a non-empty 2D array")
    if len(target_shape) != 2 or any(
        not isinstance(v, (int, np.integer)) or v <= 0 for v in target_shape
    ):
        raise ValueError("target_shape must contain two positive integers")
    if nodata_policy not in ("strict", "renormalize"):
        raise ValueError("nodata_policy must be 'strict' or 'renormalize'")

    rows, cols = data.shape
    out_rows, out_cols = map(int, target_shape)
    output = np.full((out_rows, out_cols), np.nan, dtype=float)
    valid = np.isfinite(data)

    for out_r in range(out_rows):
        r0 = out_r * rows / out_rows
        r1 = (out_r + 1) * rows / out_rows
        for out_c in range(out_cols):
            c0 = out_c * cols / out_cols
            c1 = (out_c + 1) * cols / out_cols
            total = 0.0
            valid_area = 0.0
            missing = False
            for r in range(math.floor(r0), math.ceil(r1)):
                dy = max(0.0, min(r1, r + 1) - max(r0, r))
                for c in range(math.floor(c0), math.ceil(c1)):
                    dx = max(0.0, min(c1, c + 1) - max(c0, c))
                    area = dx * dy
                    if area == 0.0:
                        continue
                    if valid[r, c]:
                        total += float(data[r, c]) * area
                        valid_area += area
                    else:
                        missing = True
            if valid_area and not (nodata_policy == "strict" and missing):
                output[out_r, out_c] = total / valid_area
    return output
