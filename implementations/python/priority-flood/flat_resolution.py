"""Resolve drainable flats in a DEM using a deterministic BFS gradient."""
from __future__ import annotations
from collections import deque
from math import isfinite
from typing import Sequence
import numpy as np

_NEIGHBOURS = ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))


def resolve_flats(elevation: Sequence[Sequence[float]] | np.ndarray, *,
                  valid_mask: np.ndarray | None = None,
                  nodata: float | None = None,
                  epsilon: float | None = None) -> np.ndarray:
    """Raise cells away from lower outlets by BFS depth * epsilon.

    Each 8-connected equal-height component touching lower terrain is
    traversed from all outlet-adjacent cells. Every other cell has a BFS
    parent one level closer to a lower outlet, guaranteeing a descending
    path. Components without a lower outlet are unchanged. Invalid cells
    are NaN. This resolves flats only; it does not fill or breach depressions.
    """
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
    if not valid.any():
        raise ValueError("elevation must contain at least one valid cell")
    if epsilon is not None:
        epsilon = float(epsilon)
        if not isfinite(epsilon) or epsilon <= 0:
            raise ValueError("epsilon must be finite and positive")

    rows, cols = dem.shape
    out = np.full(dem.shape, np.nan, dtype=float)
    out[valid] = dem[valid]
    seen = np.zeros(dem.shape, dtype=bool)

    for sr in range(rows):
        for sc in range(cols):
            if not valid[sr, sc] or seen[sr, sc]:
                continue
            level = float(dem[sr, sc])
            component, q = [], deque([(sr, sc)])
            seen[sr, sc] = True
            while q:
                r, c = q.popleft()
                component.append((r, c))
                for dr, dc in _NEIGHBOURS:
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < rows and 0 <= nc < cols and valid[nr, nc]
                            and not seen[nr, nc] and dem[nr, nc] == level):
                        seen[nr, nc] = True
                        q.append((nr, nc))
            members = set(component)
            outlets, gaps = [], []
            for r, c in component:
                lower = False
                for dr, dc in _NEIGHBOURS:
                    nr, nc = r + dr, c + dc
                    if not (0 <= nr < rows and 0 <= nc < cols and valid[nr, nc]):
                        continue
                    value = float(dem[nr, nc])
                    if value < level:
                        lower = True
                    elif value > level:
                        gaps.append(value - level)
                if lower:
                    outlets.append((r, c))
            if not outlets:
                continue

            distances = {cell: 0 for cell in outlets}
            bfs = deque(outlets)
            while bfs:
                r, c = bfs.popleft()
                depth = distances[(r, c)] + 1
                for dr, dc in _NEIGHBOURS:
                    cell = (r + dr, c + dc)
                    if cell in members and cell not in distances:
                        distances[cell] = depth
                        bfs.append(cell)
            max_depth = max(distances.values(), default=0)
            if epsilon is None:
                step = abs(float(np.spacing(level)))
                if step == 0:
                    step = float(np.nextafter(0.0, 1.0))
                if gaps and min(gaps) / (max_depth + 1) < step:
                    raise ValueError("flat cannot be resolved without crossing higher terrain at float precision")
            else:
                step = epsilon
                if gaps and step * max_depth >= min(gaps):
                    raise ValueError("epsilon would raise flat cells to or above higher terrain")
            for r, c in component:
                out[r, c] = level + distances[(r, c)] * step
                if distances[(r, c)] and out[r, c] <= level:
                    raise ValueError("epsilon is too small to change elevation at float precision")
    return out
