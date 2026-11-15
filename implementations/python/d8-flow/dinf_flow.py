"""Tarboton-style D-infinity flow partitioning for raster elevation grids."""
from __future__ import annotations

from math import atan2, hypot, isfinite, pi
from typing import Sequence

import numpy as np

# Clockwise in raster coordinates: east, southeast, south, ... northeast.
_DIRECTIONS = (
    (0, 1), (1, 1), (1, 0), (1, -1),
    (0, -1), (-1, -1), (-1, 0), (-1, 1),
)


def _dem_and_valid(elevation, valid_mask=None, nodata=None):
    dem = np.asarray(elevation, dtype=float)
    if dem.ndim != 2 or dem.size == 0:
        raise ValueError("elevation must be a non-empty 2D array")
    valid = np.isfinite(dem)
    if nodata is not None:
        valid &= dem != nodata
    if valid_mask is not None:
        mask = np.asarray(valid_mask, dtype=bool)
        if mask.shape != dem.shape:
            raise ValueError("valid_mask must have the same shape as elevation")
        valid &= mask
    return dem, valid


def dinf_flow_weights(
    elevation: Sequence[Sequence[float]] | np.ndarray,
    *,
    cell_size: Sequence[float] = (1.0, 1.0),
    valid_mask: np.ndarray | None = None,
    nodata: float | None = None,
) -> np.ndarray:
    """Return D-infinity flow fractions for the eight neighbouring cells.

    For each cell, the eight adjacent-neighbour pairs define triangular
    facets. A planar gradient is fitted to each available facet. If its
    downslope aspect lies inside the facet, flow is split between the two
    facet neighbours in proportion to angular position. If the aspect falls
    outside, the steeper downhill facet edge is considered. Available single
    edges are also considered, allowing routing next to NoData and raster
    boundaries. The steepest candidate is selected; ties keep the first
    candidate in clockwise direction order.

    The result has shape (rows, columns, 8), ordered E, SE, S, SW, W, NW,
    N, NE. Valid sinks/flats and invalid cells have all-zero weights.
    This is a planar raster method; cell_size is (row spacing, column
    spacing) and elevation units must be compatible with horizontal units.
    """
    dem, valid = _dem_and_valid(elevation, valid_mask, nodata)
    try:
        if len(cell_size) != 2:
            raise ValueError("cell_size must contain row and column spacing")
        row_spacing, column_spacing = map(float, cell_size)
    except TypeError as exc:
        raise ValueError("cell_size must contain row and column spacing") from exc
    if not all(isfinite(v) and v > 0 for v in (row_spacing, column_spacing)):
        raise ValueError("cell_size values must be finite and positive")

    height, width = dem.shape
    weights = np.zeros((height, width, 8), dtype=float)
    ray_angles = [
        atan2(dr * row_spacing, dc * column_spacing) % (2.0 * pi)
        for dr, dc in _DIRECTIONS
    ]

    for row in range(height):
        for column in range(width):
            if not valid[row, column]:
                continue
            centre = float(dem[row, column])
            candidates: list[tuple[float, tuple[tuple[int, float], ...]]] = []

            # Evaluate the eight triangular facets around the cell centre.
            for first in range(8):
                second = (first + 1) % 8
                dr1, dc1 = _DIRECTIONS[first]
                dr2, dc2 = _DIRECTIONS[second]
                r1, c1 = row + dr1, column + dc1
                r2, c2 = row + dr2, column + dc2
                if not (0 <= r1 < height and 0 <= c1 < width
                        and 0 <= r2 < height and 0 <= c2 < width
                        and valid[r1, c1] and valid[r2, c2]):
                    continue

                x1, y1 = dc1 * column_spacing, dr1 * row_spacing
                x2, y2 = dc2 * column_spacing, dr2 * row_spacing
                dz1 = float(dem[r1, c1]) - centre
                dz2 = float(dem[r2, c2]) - centre
                determinant = x1 * y2 - x2 * y1
                gx = (dz1 * y2 - dz2 * y1) / determinant
                gy = (x1 * dz2 - x2 * dz1) / determinant
                slope = hypot(gx, gy)
                if not isfinite(slope):
                    raise ValueError("elevation range produces a non-finite facet slope")
                if slope == 0.0:
                    continue

                # Downslope aspect in coordinates where x=east and y=south.
                aspect = atan2(-gy, -gx) % (2.0 * pi)
                span = (ray_angles[second] - ray_angles[first]) % (2.0 * pi)
                offset = (aspect - ray_angles[first]) % (2.0 * pi)
                if offset <= span + 1e-12:
                    fraction = min(1.0, max(0.0, offset / span))
                    candidates.append((
                        slope,
                        ((first, 1.0 - fraction), (second, fraction)),
                    ))
                else:
                    edge1 = max(0.0, -dz1 / hypot(x1, y1))
                    edge2 = max(0.0, -dz2 / hypot(x2, y2))
                    if edge1 >= edge2 and edge1 > 0.0:
                        candidates.append((edge1, ((first, 1.0),)))
                    elif edge2 > 0.0:
                        candidates.append((edge2, ((second, 1.0),)))

            # Edge fallback is needed where a facet is incomplete at NoData
            # boundaries or the raster edge. It also handles narrow valid masks.
            for index, (dr, dc) in enumerate(_DIRECTIONS):
                nr, nc = row + dr, column + dc
                if not (0 <= nr < height and 0 <= nc < width and valid[nr, nc]):
                    continue
                drop = centre - float(dem[nr, nc])
                if drop <= 0.0:
                    continue
                distance = hypot(dr * row_spacing, dc * column_spacing)
                edge_slope = drop / distance
                if not isfinite(edge_slope):
                    raise ValueError("elevation range produces a non-finite edge slope")
                candidates.append((edge_slope, ((index, 1.0),)))

            if candidates:
                best_slope = max(item[0] for item in candidates)
                # Stable first-candidate tie handling; facet order is clockwise.
                _slope, parts = next(
                    item for item in candidates if item[0] == best_slope
                )
                for index, fraction in parts:
                    weights[row, column, index] = fraction

    return weights
