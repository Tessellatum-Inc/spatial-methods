"""Progressive morphological ground filtering for XYZ point clouds."""
from __future__ import annotations
import numpy as np
from scipy.ndimage import distance_transform_edt, maximum_filter, minimum_filter


def progressive_morphological_filter(points, cell_size=1.0, window_sizes=(3, 5, 9, 17),
                                     initial_distance=0.15, slope=0.1,
                                     max_distance=1.0, max_cells=4_000_000):
    """Return a Boolean ground mask using a rasterised progressive morphology baseline.

    Points are N x 3 (x, y, z) in a consistent projected linear unit. A minimum
    elevation surface is rasterised from candidate ground points, empty cells
    are nearest-filled, and successive grayscale openings estimate terrain.
    At each window, points exceeding the progressive height threshold are
    removed from the candidate ground set.
    """
    p = np.asarray(points, dtype=float)
    if p.ndim != 2 or p.shape[1] != 3 or p.shape[0] == 0 or not np.all(np.isfinite(p)):
        raise ValueError("points must be a nonempty finite N x 3 array")
    if not np.isfinite(cell_size) or cell_size <= 0:
        raise ValueError("cell_size must be finite and positive")
    if not np.isfinite(initial_distance) or initial_distance < 0:
        raise ValueError("initial_distance must be finite and nonnegative")
    if not np.isfinite(slope) or slope < 0:
        raise ValueError("slope must be finite and nonnegative")
    if not np.isfinite(max_distance) or max_distance < initial_distance:
        raise ValueError("max_distance must be finite and at least initial_distance")
    if not isinstance(max_cells, int) or isinstance(max_cells, bool) or max_cells < 1:
        raise ValueError("max_cells must be a positive integer")
    windows = tuple(window_sizes)
    if not windows or any(not isinstance(w, int) or isinstance(w, bool) or w < 3 or w % 2 == 0 for w in windows):
        raise ValueError("window_sizes must contain odd integers >= 3")
    if tuple(sorted(set(windows))) != windows:
        raise ValueError("window_sizes must be strictly increasing")
    xmin, ymin = np.min(p[:, :2], axis=0)
    xmax, ymax = np.max(p[:, :2], axis=0)
    cols = np.floor((p[:, 0] - xmin) / cell_size).astype(int)
    rows = np.floor((p[:, 1] - ymin) / cell_size).astype(int)
    ncols, nrows = int(cols.max()) + 1, int(rows.max()) + 1
    if nrows * ncols > max_cells:
        raise ValueError("raster grid exceeds max_cells; increase cell_size or max_cells")
    flat = rows * ncols + cols
    ground = np.ones(p.shape[0], dtype=bool)
    for window in windows:
        surface = np.full(nrows * ncols, np.inf, dtype=float)
        np.minimum.at(surface, flat[ground], p[ground, 2])
        surface = surface.reshape(nrows, ncols)
        valid = np.isfinite(surface)
        if not np.any(valid):
            raise RuntimeError("no candidate ground points remain")
        if not np.all(valid):
            nearest = distance_transform_edt(~valid, return_distances=False, return_indices=True)
            surface = surface[tuple(nearest)]
        opened = maximum_filter(minimum_filter(surface, size=window, mode="nearest"),
                                size=window, mode="nearest")
        threshold = min(max_distance, initial_distance + slope * cell_size * (window - 1))
        local_ground = opened[rows, cols]
        ground &= (p[:, 2] - local_ground) <= threshold
    return ground
