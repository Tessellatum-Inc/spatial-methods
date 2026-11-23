"""Power-law multiple-flow-direction routing and accumulation on a raster DEM."""
from __future__ import annotations

from math import hypot, isfinite
from typing import Sequence

import numpy as np

# Flow-fraction channel order: E, SE, S, SW, W, NW, N, NE.
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


def mfd_flow_weights(
    elevation: Sequence[Sequence[float]] | np.ndarray,
    *,
    exponent: float = 1.1,
    cell_size: Sequence[float] = (1.0, 1.0),
    valid_mask: np.ndarray | None = None,
    nodata: float | None = None,
) -> np.ndarray:
    """Return eight downhill flow fractions per cell using power-law MFD.

    For each strictly lower neighbour j, slope_ij is the elevation drop
    divided by centre-to-centre distance. Its unnormalised weight is
    slope_ij ** exponent. Fractions are normalised over all lower neighbours.
    A valid sink/flat and an invalid cell have eight zero weights.
    """
    dem, valid = _dem_and_valid(elevation, valid_mask, nodata)
    try:
        exponent = float(exponent)
    except (TypeError, ValueError) as exc:
        raise ValueError("exponent must be finite and positive") from exc
    if not isfinite(exponent) or exponent <= 0:
        raise ValueError("exponent must be finite and positive")
    try:
        if len(cell_size) != 2:
            raise ValueError("cell_size must contain row and column spacing")
        row_spacing, column_spacing = map(float, cell_size)
    except TypeError as exc:
        raise ValueError("cell_size must contain row and column spacing") from exc
    if not all(isfinite(v) and v > 0 for v in (row_spacing, column_spacing)):
        raise ValueError("cell_size values must be finite and positive")

    height, width = dem.shape
    fractions = np.zeros((height, width, 8), dtype=float)
    for row in range(height):
        for column in range(width):
            if not valid[row, column]:
                continue
            candidates = []
            for direction_index, (dr, dc) in enumerate(_DIRECTIONS):
                nr, nc = row + dr, column + dc
                if not (0 <= nr < height and 0 <= nc < width and valid[nr, nc]):
                    continue
                drop = float(dem[row, column] - dem[nr, nc])
                if not isfinite(drop):
                    raise ValueError("elevation range produces a non-finite drop")
                if drop <= 0:
                    continue
                distance = hypot(dr * row_spacing, dc * column_spacing)
                slope = drop / distance
                if not isfinite(slope):
                    raise ValueError("elevation range produces a non-finite slope")
                candidates.append((direction_index, slope))

            if candidates:
                log_weights = np.array(
                    [exponent * np.log(slope) for _, slope in candidates],
                    dtype=float,
                )
                if not np.all(np.isfinite(log_weights)):
                    raise ValueError("exponent and slope magnitudes produce non-finite weights")
                scaled = np.exp(log_weights - np.max(log_weights))
                fractions[row, column, [i for i, _ in candidates]] = scaled / scaled.sum()
    return fractions


def mfd_flow_accumulation(
    elevation: Sequence[Sequence[float]] | np.ndarray,
    flow_weights: np.ndarray,
    *,
    initial_contribution: float | np.ndarray = 1.0,
    valid_mask: np.ndarray | None = None,
    nodata: float | None = None,
) -> np.ndarray:
    """Accumulate contributions through a strictly downhill MFD graph.

    Every valid cell starts with initial_contribution (a scalar or raster).
    A sink retains its accumulated total. Invalid cells are returned as NaN.
    A Kahn topological traversal processes the acyclic downhill graph in O(N)
    time for a fixed eight-neighbour grid.
    """
    dem, valid = _dem_and_valid(elevation, valid_mask, nodata)
    if not valid.any():
        raise ValueError("elevation must contain at least one valid cell")
    weights = np.asarray(flow_weights, dtype=float)
    if weights.shape != dem.shape + (8,):
        raise ValueError("flow_weights must have shape (rows, columns, 8)")
    if not np.all(np.isfinite(weights)) or np.any(weights < 0):
        raise ValueError("flow_weights must be finite and nonnegative")
    if np.any(weights[~valid] != 0):
        raise ValueError("invalid cells must have zero outgoing flow weights")

    sums = weights.sum(axis=2)
    valid_sums = np.isclose(sums, 0.0, atol=1e-10) | np.isclose(
        sums, 1.0, rtol=1e-7, atol=1e-9
    )
    if np.any(valid & ~valid_sums):
        raise ValueError("each valid cell must have zero or unit-sum outgoing flow weights")

    height, width = dem.shape
    for row, column in np.argwhere(valid):
        for index, (dr, dc) in enumerate(_DIRECTIONS):
            if weights[row, column, index] <= 0:
                continue
            nr, nc = row + dr, column + dc
            if not (0 <= nr < height and 0 <= nc < width and valid[nr, nc]):
                raise ValueError("positive flow weights must point to valid in-grid neighbours")
            if dem[nr, nc] >= dem[row, column]:
                raise ValueError("positive flow weights must point strictly downhill")

    contribution = np.asarray(initial_contribution, dtype=float)
    accumulation = np.full(dem.shape, np.nan, dtype=float)
    if contribution.ndim == 0:
        value = float(contribution)
        if not isfinite(value) or value < 0:
            raise ValueError("initial_contribution must be finite and nonnegative")
        accumulation[valid] = value
    else:
        if (
            contribution.shape != dem.shape
            or not np.all(np.isfinite(contribution[valid]))
            or np.any(contribution[valid] < 0)
        ):
            raise ValueError(
                "initial_contribution raster must match elevation and be finite nonnegative on valid cells"
            )
        accumulation[valid] = contribution[valid]

    indegree = np.zeros(dem.shape, dtype=np.int16)
    for row, column in np.argwhere(valid):
        for index, (dr, dc) in enumerate(_DIRECTIONS):
            if weights[row, column, index] > 0:
                indegree[row + dr, column + dc] += 1

    queue = [
        tuple(index) for index in np.argwhere(valid & (indegree == 0))
    ]
    head = 0
    processed = 0
    while head < len(queue):
        row, column = queue[head]
        head += 1
        processed += 1
        amount = accumulation[row, column]
        for index, (dr, dc) in enumerate(_DIRECTIONS):
            fraction = weights[row, column, index]
            if fraction > 0:
                nr, nc = row + dr, column + dc
                accumulation[nr, nc] += amount * fraction
                indegree[nr, nc] -= 1
                if indegree[nr, nc] == 0:
                    queue.append((nr, nc))

    if processed != int(valid.sum()):
        raise ValueError("flow graph contains a cycle")
    return accumulation
