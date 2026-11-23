"""Raster line-of-sight viewshed reference algorithms."""
from __future__ import annotations

import math
import numpy as np


def _bresenham_cells(r0: int, c0: int, r1: int, c1: int):
    """Yield integer grid cells from start to end, excluding the start."""
    dc, dr = abs(c1 - c0), abs(r1 - r0)
    sc = 1 if c0 < c1 else -1
    sr = 1 if r0 < r1 else -1
    err = dc - dr
    r, c = r0, c0
    while (r, c) != (r1, c1):
        e2 = 2 * err
        if e2 > -dr:
            err -= dr
            c += sc
        if e2 < dc:
            err += dc
            r += sr
        yield r, c


def viewshed(
    elevation,
    observer,
    *,
    observer_height: float = 1.7,
    target_height: float = 0.0,
    cell_size_x: float = 1.0,
    cell_size_y: float = 1.0,
    earth_radius: float | None = None,
    refraction_coefficient: float = 0.0,
) -> np.ndarray:
    """Return a Boolean raster of cells visible from one grid-cell observer.

    observer is (row, column). Heights and cell dimensions must use the same
    linear unit. If earth_radius is supplied, apparent terrain/target heights
    are corrected by d²(1-k)/(2R), where k is the refraction coefficient.
    Rays use a centre-to-centre Bresenham path; this is a transparent discrete
    LOS baseline, not an exact continuous-surface or R3/R2/XDraw viewshed.
    Any NoData cell on a ray makes that target indeterminate (False).
    """
    dem = np.asarray(elevation, dtype=float)
    if dem.ndim != 2 or dem.size == 0:
        raise ValueError("elevation must be a non-empty 2D array")
    if len(observer) != 2 or any(int(v) != v for v in observer):
        raise ValueError("observer must be an integer (row, column) pair")
    r0, c0 = map(int, observer)
    if not (0 <= r0 < dem.shape[0] and 0 <= c0 < dem.shape[1]):
        raise ValueError("observer is outside the elevation grid")
    if not np.isfinite(dem[r0, c0]):
        raise ValueError("observer cell must contain a finite elevation")
    try:
        oh, th, dx, dy, refr = map(float, (
            observer_height, target_height, cell_size_x, cell_size_y,
            refraction_coefficient,
        ))
    except (TypeError, ValueError):
        raise ValueError("heights, cell sizes and refraction coefficient must be finite") from None
    if not all(map(math.isfinite, (oh, th, dx, dy, refr))) or dx <= 0 or dy <= 0:
        raise ValueError("heights/refraction must be finite and cell sizes positive")
    radius = None
    if earth_radius is not None:
        try:
            radius = float(earth_radius)
        except (TypeError, ValueError):
            raise ValueError("earth_radius must be finite and positive") from None
        if not math.isfinite(radius) or radius <= 0:
            raise ValueError("earth_radius must be finite and positive")
    observer_z = dem[r0, c0] + oh
    result = np.zeros(dem.shape, dtype=bool)
    result[r0, c0] = True
    for rt in range(dem.shape[0]):
        for ct in range(dem.shape[1]):
            if (rt, ct) == (r0, c0) or not np.isfinite(dem[rt, ct]):
                continue
            distance = math.hypot((ct - c0) * dx, (rt - r0) * dy)
            target_z = dem[rt, ct] + th
            drop = 0.0 if radius is None else distance * distance * (1.0 - refr) / (2.0 * radius)
            target_slope = (target_z - drop - observer_z) / distance
            visible = True
            for ri, ci in _bresenham_cells(r0, c0, rt, ct):
                if (ri, ci) == (rt, ct):
                    break
                if not np.isfinite(dem[ri, ci]):
                    visible = False
                    break
                d = math.hypot((ci - c0) * dx, (ri - r0) * dy)
                curvature_drop = 0.0 if radius is None else d * d * (1.0 - refr) / (2.0 * radius)
                terrain_slope = (dem[ri, ci] - curvature_drop - observer_z) / d
                if terrain_slope >= target_slope - 1e-12:
                    visible = False
                    break
            result[rt, ct] = visible
    return result


def cumulative_viewshed(elevation, observers, **kwargs) -> np.ndarray:
    """Count how many observer locations can see each cell.

    Each observer is (row, column). All observer options are shared. A target
    is counted only when its line of sight is determinate and visible.
    """
    dem = np.asarray(elevation, dtype=float)
    if dem.ndim != 2 or dem.size == 0:
        raise ValueError("elevation must be a non-empty 2D array")
    locations = list(observers)
    if not locations:
        raise ValueError("at least one observer is required")
    total = np.zeros(dem.shape, dtype=np.int32)
    for observer in locations:
        total += viewshed(dem, observer, **kwargs).astype(np.int32)
    return total
