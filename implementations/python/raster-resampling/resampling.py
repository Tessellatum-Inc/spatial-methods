"""Nearest, bilinear, cubic-convolution and Lanczos raster resampling."""
from __future__ import annotations

import math
from typing import Sequence

import numpy as np


def _cubic_weight(distance: float, a: float = -0.5) -> float:
    """Keys cubic-convolution kernel (Catmull-Rom when a=-0.5)."""
    x = abs(distance)
    if x < 1.0:
        return (a + 2.0) * x**3 - (a + 3.0) * x**2 + 1.0
    if x < 2.0:
        return a * x**3 - 5.0 * a * x**2 + 8.0 * a * x - 4.0 * a
    return 0.0


def _lanczos_weight(distance: float, radius: int = 3) -> float:
    """Windowed-sinc interpolation kernel with finite support."""
    x = abs(distance)
    if x == 0.0:
        return 1.0
    if x >= radius:
        return 0.0
    return (math.sin(math.pi * x) / (math.pi * x)) * (
        math.sin(math.pi * x / radius) / (math.pi * x / radius)
    )


def resample_to_shape(
    source: Sequence[Sequence[float]] | np.ndarray,
    target_shape: tuple[int, int],
    *,
    method: str = "bilinear",
    nodata_policy: str = "strict",
) -> np.ndarray:
    """Resample a 2D array to a new shape over the same extent and orientation.

    Target pixel centres map linearly to source pixel-centre coordinates.
    Non-finite source values are NoData. Supported methods are nearest,
    bilinear, cubic (Keys/Catmull-Rom, a=-0.5) and Lanczos-3. For interpolating
    methods, NoData policy is 'strict' (any nonzero-weight missing sample
    invalidates the result) or 'renormalize' (use valid samples only). The
    latter is useful near data gaps but can change the effective kernel,
    especially for negative-lobed cubic and Lanczos filters.
    """
    data = np.asarray(source, dtype=float)
    if data.ndim != 2 or data.size == 0:
        raise ValueError("source must be a non-empty 2D array")
    if (
        len(target_shape) != 2
        or any(not isinstance(v, (int, np.integer)) or v <= 0 for v in target_shape)
    ):
        raise ValueError("target_shape must contain two positive integers")
    if method not in ("nearest", "bilinear", "cubic", "lanczos"):
        raise ValueError("method must be 'nearest', 'bilinear', 'cubic' or 'lanczos'")
    if nodata_policy not in ("strict", "renormalize"):
        raise ValueError("nodata_policy must be 'strict' or 'renormalize'")

    in_rows, in_cols = data.shape
    out_rows, out_cols = map(int, target_shape)
    output = np.full((out_rows, out_cols), np.nan, dtype=float)
    valid = np.isfinite(data)

    for r in range(out_rows):
        sr = (r + 0.5) * in_rows / out_rows - 0.5
        for c in range(out_cols):
            sc = (c + 0.5) * in_cols / out_cols - 0.5
            if method == "nearest":
                rr = min(in_rows - 1, max(0, math.floor(sr + 0.5)))
                cc = min(in_cols - 1, max(0, math.floor(sc + 0.5)))
                if valid[rr, cc]:
                    output[r, c] = data[rr, cc]
                continue

            if method == "bilinear":
                r0, c0 = math.floor(sr), math.floor(sc)
                fr, fc = sr - r0, sc - c0
                samples = [
                    (r0, c0, (1 - fr) * (1 - fc)),
                    (r0, c0 + 1, (1 - fr) * fc),
                    (r0 + 1, c0, fr * (1 - fc)),
                    (r0 + 1, c0 + 1, fr * fc),
                ]
            else:
                radius = 2 if method == "cubic" else 3
                kernel = _cubic_weight if method == "cubic" else _lanczos_weight
                row_start = math.floor(sr) - radius + 1
                col_start = math.floor(sc) - radius + 1
                samples = []
                for source_row in range(row_start, math.floor(sr) + radius + 1):
                    wr = kernel(sr - source_row)
                    if wr == 0.0:
                        continue
                    for source_col in range(col_start, math.floor(sc) + radius + 1):
                        wc = kernel(sc - source_col)
                        weight = wr * wc
                        if weight != 0.0:
                            samples.append((source_row, source_col, weight))

            weighted: list[tuple[float, float]] = []
            missing_nonzero_weight = False
            for rr, cc, weight in samples:
                # Edge extension: clamp to the nearest edge cell. Repeated
                # clamped indices are intentional and their weights add.
                rr = min(in_rows - 1, max(0, rr))
                cc = min(in_cols - 1, max(0, cc))
                if valid[rr, cc]:
                    weighted.append((float(data[rr, cc]), weight))
                elif weight != 0.0:
                    missing_nonzero_weight = True

            if not weighted or (nodata_policy == "strict" and missing_nonzero_weight):
                continue
            total_weight = sum(weight for _, weight in weighted)
            # Negative-lobed kernels can have near-zero remaining weight after
            # NoData removal. Do not amplify noise by dividing by it.
            if abs(total_weight) <= 1e-12:
                continue
            output[r, c] = sum(value * weight for value, weight in weighted) / total_weight

    return output
