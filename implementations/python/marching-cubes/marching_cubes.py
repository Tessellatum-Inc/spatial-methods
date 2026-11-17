"""Validated wrapper for Lewiner marching-cubes isosurface extraction."""
from __future__ import annotations
import numpy as np
from skimage.measure import marching_cubes as _marching_cubes


def extract_isosurface(volume, level, *, spacing=(1.0, 1.0, 1.0),
                       origin=(0.0, 0.0, 0.0), step_size=1,
                       allow_degenerate=False):
    """Extract an isosurface; return vertices, faces, normals and sampled values.

    Volume axes are ordered (axis0, axis1, axis2). Vertices are transformed
    from voxel coordinates by spacing and origin in that same axis order.
    """
    data = np.asarray(volume, dtype=float)
    if data.ndim != 3 or any(n < 2 for n in data.shape) or not np.all(np.isfinite(data)):
        raise ValueError("volume must be a finite 3-D array with each dimension >= 2")
    if not np.isfinite(level) or not float(np.min(data)) < level < float(np.max(data)):
        raise ValueError("level must lie strictly inside the volume value range")
    spacing = np.asarray(spacing, dtype=float)
    origin = np.asarray(origin, dtype=float)
    if spacing.shape != (3,) or not np.all(np.isfinite(spacing)) or np.any(spacing <= 0):
        raise ValueError("spacing must contain three finite positive values")
    if origin.shape != (3,) or not np.all(np.isfinite(origin)):
        raise ValueError("origin must contain three finite values")
    if not isinstance(step_size, int) or isinstance(step_size, bool) or step_size < 1:
        raise ValueError("step_size must be a positive integer")
    if not isinstance(allow_degenerate, bool):
        raise ValueError("allow_degenerate must be Boolean")
    vertices, faces, normals, values = _marching_cubes(
        data, level=float(level), spacing=tuple(spacing),
        step_size=step_size, allow_degenerate=allow_degenerate,
        method="lewiner")
    vertices = vertices + origin
    return {"vertices": vertices, "faces": faces.astype(np.int64),
            "normals": normals, "values": values}
