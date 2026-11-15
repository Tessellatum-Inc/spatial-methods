"""Strahler and Shreve stream ordering for a D8 channel network."""
from __future__ import annotations

from collections import deque
import numpy as np

# ESRI D8 codes: E, SE, S, SW, W, NW, N, NE.
_D8 = {
    1: (0, 1), 2: (1, 1), 4: (1, 0), 8: (1, -1),
    16: (0, -1), 32: (-1, -1), 64: (-1, 0), 128: (-1, 1),
}


def d8_stream_orders(flow_direction, stream_mask, *, nodata: int = -1):
    """Return (Strahler order, Shreve magnitude) on a D8 stream mask.

    Stream cells must form a directed acyclic network under the supplied
    D8 directions. Every stream cell either drains to another stream cell,
    terminates with code 0, or points outside the raster (an outlet).
    Directions that leave the stream mask but remain inside the raster are
    rejected: burn/derive a contiguous channel mask before ordering.

    Non-stream cells are NaN in both outputs. The algorithm is O(V+E) for
    stream cells and their single downstream links.
    """
    directions = np.asarray(flow_direction)
    streams = np.asarray(stream_mask, dtype=bool)
    if directions.ndim != 2 or directions.size == 0:
        raise ValueError("flow_direction must be a non-empty 2D array")
    if streams.shape != directions.shape:
        raise ValueError("stream_mask must match flow_direction shape")
    if not np.issubdtype(directions.dtype, np.integer):
        if not np.all(np.isfinite(directions)) or not np.all(directions == np.floor(directions)):
            raise ValueError("flow_direction must contain integer D8 codes")
        directions = directions.astype(np.int64)
    allowed = set(_D8) | {0, nodata}
    if any(int(code) not in allowed for code in np.unique(directions)):
        raise ValueError("flow_direction contains an unsupported D8 code")

    rows, cols = directions.shape
    cells = [tuple(rc) for rc in np.argwhere(streams)]
    if not cells:
        return np.full(directions.shape, np.nan), np.full(directions.shape, np.nan)

    downstream = {}
    indegree = np.zeros(directions.shape, dtype=np.int32)
    upstream_orders = {cell: [] for cell in cells}
    upstream_magnitudes = {cell: [] for cell in cells}
    for r, c in cells:
        code = int(directions[r, c])
        if code == nodata:
            raise ValueError("stream cells cannot have NoData flow direction")
        if code == 0:
            downstream[(r, c)] = None
            continue
        dr, dc = _D8[code]
        nr, nc = r + dr, c + dc
        if not (0 <= nr < rows and 0 <= nc < cols):
            downstream[(r, c)] = None
            continue
        if not streams[nr, nc]:
            raise ValueError("each in-grid downstream receiver of a stream cell must also be a stream cell")
        downstream[(r, c)] = (nr, nc)
        indegree[nr, nc] += 1

    queue = deque(cell for cell in cells if indegree[cell] == 0)
    strahler = np.full(directions.shape, np.nan)
    shreve = np.full(directions.shape, np.nan)
    processed = 0
    while queue:
        cell = queue.popleft()
        processed += 1
        orders = upstream_orders[cell]
        if not orders:
            strahler[cell] = 1
            shreve[cell] = 1
        else:
            highest = max(orders)
            strahler[cell] = highest + (1 if orders.count(highest) >= 2 else 0)
            shreve[cell] = sum(upstream_magnitudes[cell])
        receiver = downstream[cell]
        if receiver is not None:
            upstream_orders[receiver].append(strahler[cell])
            upstream_magnitudes[receiver].append(shreve[cell])
            indegree[receiver] -= 1
            if indegree[receiver] == 0:
                queue.append(receiver)

    if processed != len(cells):
        raise ValueError("stream network contains a directed cycle")
    return strahler, shreve
