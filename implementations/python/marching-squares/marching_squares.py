"""Marching-squares contour segment extraction for regular 2D grids."""
from __future__ import annotations
import numpy as np


def marching_squares(values, levels, x=None, y=None, valid=None):
    """Return line segments for each contour level on a rectilinear grid.

    Rows of values correspond to increasing y; columns correspond to
    increasing x. Each result maps a float contour level to an array shaped
    (n_segments, 2, 2), with each segment represented by two (x, y) points.
    Cells touching invalid/NoData vertices are skipped. Saddle cases use a
    bilinear-centre asymptotic decision (the cell-centre value).
    """
    z = np.asarray(values, dtype=float)
    if z.ndim != 2 or min(z.shape) < 2:
        raise ValueError("values must be a 2D array with at least two rows and columns")
    lev = np.asarray(levels, dtype=float)
    if lev.ndim == 0:
        lev = lev.reshape(1)
    if lev.ndim != 1 or not np.isfinite(lev).all():
        raise ValueError("levels must be a finite scalar or 1D sequence")
    xs = np.arange(z.shape[1], dtype=float) if x is None else np.asarray(x, dtype=float)
    ys = np.arange(z.shape[0], dtype=float) if y is None else np.asarray(y, dtype=float)
    if xs.shape != (z.shape[1],) or ys.shape != (z.shape[0],):
        raise ValueError("x and y must match the grid columns and rows")
    if not np.isfinite(xs).all() or not np.isfinite(ys).all():
        raise ValueError("x and y coordinates must be finite")
    if np.any(np.diff(xs) <= 0) or np.any(np.diff(ys) <= 0):
        raise ValueError("x and y coordinates must be strictly increasing")
    if valid is None:
        mask = np.isfinite(z)
    else:
        mask = np.asarray(valid, dtype=bool)
        if mask.shape != z.shape:
            raise ValueError("valid mask must match values shape")
        mask &= np.isfinite(z)
    output = {}
    for level in lev:
        segments = []
        for row in range(z.shape[0] - 1):
            for col in range(z.shape[1] - 1):
                if not (mask[row, col] and mask[row, col+1] and
                        mask[row+1, col+1] and mask[row+1, col]):
                    continue
                corners = np.array([z[row, col], z[row, col+1],
                                    z[row+1, col+1], z[row+1, col]])
                high = corners >= level
                if high.all() or not high.any():
                    continue
                coords = np.array([[xs[col], ys[row]],
                                   [xs[col+1], ys[row]],
                                   [xs[col+1], ys[row+1]],
                                   [xs[col], ys[row+1]]], dtype=float)
                edge_pairs = ((0, 1), (1, 2), (2, 3), (3, 0))
                crossings = {}
                for edge, (a, b) in enumerate(edge_pairs):
                    if high[a] != high[b]:
                        denominator = corners[b] - corners[a]
                        t = 0.5 if denominator == 0 else (level - corners[a]) / denominator
                        crossings[edge] = coords[a] + t * (coords[b] - coords[a])
                edges = sorted(crossings)
                if len(edges) == 2:
                    pairs = [(edges[0], edges[1])]
                elif len(edges) == 4:
                    centre_high = float(corners.mean()) >= level
                    # Connect around low corners when the centre is high;
                    # otherwise connect around high corners.
                    if centre_high == bool(high[0]):
                        pairs = [(0, 3), (1, 2)]
                    else:
                        pairs = [(0, 1), (2, 3)]
                else:
                    continue
                for a, b in pairs:
                    segments.append([crossings[a], crossings[b]])
        output[float(level)] = np.asarray(segments, dtype=float).reshape((-1, 2, 2))
    return output
