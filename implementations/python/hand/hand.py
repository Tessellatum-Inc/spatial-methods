"""Height Above Nearest Drainage (HAND) from a D8 flow-direction grid."""
from __future__ import annotations

from math import isfinite
from numbers import Integral
from typing import Sequence

# ESRI D8 powers-of-two codes; rows increase southward.
_DIRECTIONS = {
    1: (0, 1), 2: (1, 1), 4: (1, 0), 8: (1, -1),
    16: (0, -1), 32: (-1, -1), 64: (-1, 0), 128: (-1, 1),
}


def height_above_nearest_drainage(
    elevation: Sequence[Sequence[float | None]],
    directions: Sequence[Sequence[int | None]],
    stream_mask: Sequence[Sequence[bool]],
) -> list[list[float | None]]:
    """Return elevation minus the first downstream stream-cell elevation.

    A valid stream cell is its own drainage target and receives HAND=0.
    A valid non-stream cell follows its D8 receiver until it reaches a stream.
    Paths ending at a sink, raster edge or NoData before reaching a stream
    return None. Cycles and uphill receiver links are rejected.

    This computes HAND for an already conditioned D8 network; it does not
    extract streams, fill depressions or resolve flats.
    """
    if len(elevation) == 0 or len(elevation[0]) == 0:
        raise ValueError("elevation must contain at least one row and column")
    rows, cols = len(elevation), len(elevation[0])
    if any(len(row) != cols for row in elevation):
        raise ValueError("elevation rows must have equal length")
    if len(directions) != rows or any(len(row) != cols for row in directions):
        raise ValueError("directions must match elevation shape")
    if len(stream_mask) != rows or any(len(row) != cols for row in stream_mask):
        raise ValueError("stream_mask must match elevation shape")

    z: list[list[float | None]] = []
    valid = [[False] * cols for _ in range(rows)]
    streams = [[False] * cols for _ in range(rows)]
    for r in range(rows):
        zr = []
        for c in range(cols):
            value = elevation[r][c]
            if value is None:
                zr.append(None)
            else:
                value = float(value)
                if not isfinite(value):
                    raise ValueError("elevations must be finite or None")
                zr.append(value)
                valid[r][c] = True
            flag = stream_mask[r][c]
            if not isinstance(flag, (bool,)):
                # Accept numpy.bool_ without importing NumPy.
                if type(flag).__name__ != "bool_":
                    raise ValueError("stream_mask values must be boolean")
            streams[r][c] = bool(flag)
            if streams[r][c] and not valid[r][c]:
                raise ValueError("stream cells must have valid elevations")
        z.append(zr)

    receiver = [[None] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if not valid[r][c]:
                if directions[r][c] is not None:
                    raise ValueError("NoData cells must have None direction codes")
                continue
            code = directions[r][c]
            if isinstance(code, bool) or not isinstance(code, Integral):
                raise ValueError("valid cells need integer D8 direction codes")
            code = int(code)
            if code not in (0, *_DIRECTIONS):
                raise ValueError("unsupported D8 direction code")
            if code == 0 or streams[r][c]:
                continue
            dr, dc = _DIRECTIONS[code]
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols and valid[nr][nc]):
                continue
            if z[nr][nc] >= z[r][c]:
                raise ValueError("D8 receiver links must be strictly downhill")
            receiver[r][c] = (nr, nc)

    # Iterative functional-graph traversal with path compression.
    state = [[0] * cols for _ in range(rows)]  # 0 unseen, 1 on current path, 2 solved
    drainage = [[None] * cols for _ in range(rows)]
    for sr in range(rows):
        for sc in range(cols):
            if not valid[sr][sc] or state[sr][sc] == 2:
                continue
            path = []
            current = (sr, sc)
            while current is not None:
                r, c = current
                if state[r][c] == 2:
                    terminal = drainage[r][c]
                    break
                if state[r][c] == 1:
                    raise ValueError("D8 flow-direction graph contains a cycle")
                state[r][c] = 1
                path.append(current)
                if streams[r][c]:
                    terminal = current
                    break
                current = receiver[r][c]
            else:
                terminal = None

            for r, c in reversed(path):
                if streams[r][c]:
                    terminal = (r, c)
                drainage[r][c] = terminal
                state[r][c] = 2

    result: list[list[float | None]] = [[None] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if not valid[r][c]:
                continue
            target = drainage[r][c]
            if target is not None:
                tr, tc = target
                result[r][c] = z[r][c] - z[tr][tc]
    return result
