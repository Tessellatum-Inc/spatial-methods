"""Positive and negative terrain openness from radial horizon angles."""
from __future__ import annotations
import numpy as np


def terrain_openness(
    elevation,
    *,
    max_distance: float,
    cell_size_x: float = 1.0,
    cell_size_y: float = 1.0,
    azimuth_count: int = 16,
    sample_spacing: float | None = None,
):
    """Calculate positive and negative openness angles in degrees.

    For each azimuth, bilinear samples are taken along a radial profile.
    Positive openness is 90 degrees minus the mean positive horizon angle;
    negative openness is 90 degrees minus the mean magnitude of the negative
    horizon angle. Both approach 90 degrees on a flat plane. Lower positive
    openness indicates enclosing terrain above the local horizon; lower
    negative openness indicates enclosing terrain below it.

    A cell is returned only when every ray is fully supported to max_distance.
    This is a radial-sampling approximation, not the exact multi-scale
    geomorphon method. Distances and elevations must use matching units.
    """
    dem = np.asarray(elevation, dtype=float)
    if dem.ndim != 2 or dem.size == 0:
        raise ValueError("elevation must be a non-empty 2D array")
    try:
        dx, dy, distance = map(float, (cell_size_x, cell_size_y, max_distance))
        step = min(dx, dy) / 2 if sample_spacing is None else float(sample_spacing)
    except (TypeError, ValueError):
        raise ValueError("cell sizes, distance and sample spacing must be finite and positive") from None
    if not np.all(np.isfinite([dx, dy, distance, step])) or min(dx, dy, distance, step) <= 0:
        raise ValueError("cell sizes, distance and sample spacing must be finite and positive")
    if isinstance(azimuth_count, (bool, np.bool_)) or not isinstance(azimuth_count, (int, np.integer)) or azimuth_count < 4:
        raise ValueError("azimuth_count must be an integer of at least four")
    radii = np.arange(step, distance, step)
    radii = np.append(radii, distance)
    rows, cols = dem.shape
    positive = np.full(dem.shape, np.nan)
    negative = np.full(dem.shape, np.nan)
    azimuths = np.arange(azimuth_count) * (2 * np.pi / azimuth_count)
    for row, col in np.ndindex(dem.shape):
        origin = dem[row, col]
        if not np.isfinite(origin):
            continue
        pos_angles, neg_angles = [], []
        supported = True
        for az in azimuths:
            angles = []
            for radius in radii:
                c = col + np.sin(az) * radius / dx
                r = row - np.cos(az) * radius / dy
                if c < 0 or c > cols - 1 or r < 0 or r > rows - 1:
                    supported = False
                    break
                c0, r0 = min(int(np.floor(c)), cols - 2), min(int(np.floor(r)), rows - 2)
                if cols < 2 or rows < 2:
                    supported = False
                    break
                fc, fr = c - c0, r - r0
                z = np.array([dem[r0,c0],dem[r0,c0+1],dem[r0+1,c0],dem[r0+1,c0+1]])
                if not np.all(np.isfinite(z)):
                    supported = False
                    break
                top = z[0] * (1-fc) + z[1] * fc
                bottom = z[2] * (1-fc) + z[3] * fc
                sample = top * (1-fr) + bottom * fr
                angles.append(np.degrees(np.arctan2(sample-origin, radius)))
            if not supported:
                break
            angles = np.asarray(angles)
            pos_angles.append(max(0.0, float(np.max(angles))))
            neg_angles.append(max(0.0, float(-np.min(angles))))
        if supported and len(pos_angles) == azimuth_count:
            positive[row,col] = 90.0 - float(np.mean(pos_angles))
            negative[row,col] = 90.0 - float(np.mean(neg_angles))
    return {"positive_openness": positive, "negative_openness": negative}
