"""Tarboton-style D-infinity flow routing and accumulation."""
from math import atan2, hypot, isfinite, pi
from typing import Sequence

# Counter-clockwise: E, NE, N, NW, W, SW, S, SE.
# Raster rows increase southward; map y increases northward.
_NEIGHBOURS = ((0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1),(1,0),(1,1))
_TWO_PI = 2.0 * pi


def _read_dem(dem):
    if not dem or not dem[0]:
        raise ValueError("DEM must contain at least one row and column")
    ncols = len(dem[0])
    if any(len(row) != ncols for row in dem):
        raise ValueError("DEM rows must have equal length")
    out = []
    for row in dem:
        clean = []
        for value in row:
            if value is None:
                clean.append(None)
            else:
                value = float(value)
                if not isfinite(value):
                    raise ValueError("elevations must be finite or None")
                clean.append(value)
        out.append(clean)
    return out


def d_infinity_flow_fractions(dem: Sequence[Sequence[float | None]], *,
                              cell_width: float = 1.0,
                              cell_height: float = 1.0):
    """Return a grid of zero, one or two (row, col, fraction) links per cell.

    NoData cells are None; valid sinks are empty tuples. Each triangular facet
    fits a plane through the centre and two adjacent neighbours. The steepest
    feasible downslope direction is selected and split between its bracketing
    neighbours by angular proportion. No depression or flat conditioning is
    performed.
    """
    z = _read_dem(dem)
    dx, dy = float(cell_width), float(cell_height)
    if not isfinite(dx) or dx <= 0 or not isfinite(dy) or dy <= 0:
        raise ValueError("cell dimensions must be finite and positive")
    nr, nc = len(z), len(z[0])
    vectors = [(dc * dx, -dr * dy) for dr, dc in _NEIGHBOURS]
    angles = [atan2(y, x) % _TWO_PI for x, y in vectors]
    result = [[None if z[r][c] is None else tuple() for c in range(nc)]
              for r in range(nr)]

    for r in range(nr):
        for c in range(nc):
            centre = z[r][c]
            if centre is None:
                continue
            neighbours = []
            for dr, dc in _NEIGHBOURS:
                rr, cc = r + dr, c + dc
                value = z[rr][cc] if 0 <= rr < nr and 0 <= cc < nc else None
                neighbours.append((rr, cc, value))

            best_slope, best_links = 0.0, tuple()
            # Valid single-edge descent is the fallback for sector clipping
            # and for facets interrupted by NoData or the raster boundary.
            for i, (rr, cc, value) in enumerate(neighbours):
                if value is not None and value < centre:
                    slope = (centre - value) / hypot(*vectors[i])
                    if slope > best_slope:
                        best_slope = slope
                        best_links = ((rr, cc, 1.0),)

            for i in range(8):
                j = (i + 1) % 8
                r1, c1, z1 = neighbours[i]
                r2, c2, z2 = neighbours[j]
                if z1 is None or z2 is None:
                    continue
                x1, y1 = vectors[i]
                x2, y2 = vectors[j]
                d1, d2 = z1 - centre, z2 - centre
                det = x1 * y2 - x2 * y1
                if det == 0:
                    continue
                gx = (d1 * y2 - d2 * y1) / det
                gy = (x1 * d2 - x2 * d1) / det
                slope = hypot(gx, gy)
                if slope <= best_slope or slope == 0:
                    continue
                down_x, down_y = -gx, -gy
                a1, a2 = angles[i], angles[j]
                if a2 <= a1:
                    a2 += _TWO_PI
                theta = atan2(down_y, down_x) % _TWO_PI
                if theta < a1:
                    theta += _TWO_PI
                if a1 - 1e-12 <= theta <= a2 + 1e-12:
                    span = a2 - a1
                    if span <= 0:
                        continue
                    w1 = max(0.0, min(1.0, (a2 - theta) / span))
                    w2 = max(0.0, min(1.0, (theta - a1) / span))
                    links = []
                    if w1 > 1e-12:
                        links.append((r1, c1, w1))
                    if w2 > 1e-12:
                        links.append((r2, c2, w2))
                    total = sum(link[2] for link in links)
                    if total:
                        best_slope = slope
                        best_links = tuple((rr, cc, w / total) for rr, cc, w in links)
            result[r][c] = best_links
    return result


def d_infinity_flow_accumulation(dem, flow_fractions, *, initial=None):
    """Accumulate contributions using a topological traversal of D-infinity links."""
    z = _read_dem(dem)
    nr, nc = len(z), len(z[0])
    if len(flow_fractions) != nr or any(len(row) != nc for row in flow_fractions):
        raise ValueError("flow_fractions must match DEM shape")
    if initial is None:
        contribution = [[None if z[r][c] is None else 1.0 for c in range(nc)]
                        for r in range(nr)]
    else:
        if len(initial) != nr or any(len(row) != nc for row in initial):
            raise ValueError("initial contributions must match DEM shape")
        contribution = []
        for r in range(nr):
            row = []
            for c in range(nc):
                value = initial[r][c]
                if z[r][c] is None:
                    if value is not None:
                        raise ValueError("NoData contribution must be None")
                    row.append(None)
                else:
                    value = float(value)
                    if not isfinite(value) or value < 0:
                        raise ValueError("contributions must be finite and non-negative")
                    row.append(value)
            contribution.append(row)

    indegree = [[0] * nc for _ in range(nr)]
    outgoing = [[tuple() for _ in range(nc)] for _ in range(nr)]
    valid_count = 0
    for r in range(nr):
        for c in range(nc):
            links = flow_fractions[r][c]
            if z[r][c] is None:
                if links is not None:
                    raise ValueError("NoData flow links must be None")
                continue
            valid_count += 1
            if links is None or len(links) > 2:
                raise ValueError("valid cells need zero, one or two flow links")
            total, clean = 0.0, []
            for rr, cc, weight in links:
                if not isinstance(rr, int) or isinstance(rr, bool) or not isinstance(cc, int) or isinstance(cc, bool) or not (0 <= rr < nr and 0 <= cc < nc):
                    raise ValueError("flow target outside DEM")
                weight = float(weight)
                if z[rr][cc] is None or z[rr][cc] >= z[r][c]:
                    raise ValueError("flow links must point to strictly lower valid cells")
                if not isfinite(weight) or weight <= 0:
                    raise ValueError("flow weights must be finite and positive")
                clean.append((rr, cc, weight))
                total += weight
                indegree[rr][cc] += 1
            if clean and abs(total - 1.0) > 1e-9:
                raise ValueError("outgoing flow fractions must sum to one")
            outgoing[r][c] = tuple(clean)

    queue = [(r, c) for r in range(nr) for c in range(nc)
             if z[r][c] is not None and indegree[r][c] == 0]
    accumulation = [[None if z[r][c] is None else contribution[r][c]
                     for c in range(nc)] for r in range(nr)]
    cursor = processed = 0
    while cursor < len(queue):
        r, c = queue[cursor]
        cursor += 1
        processed += 1
        for rr, cc, weight in outgoing[r][c]:
            accumulation[rr][cc] += accumulation[r][c] * weight
            indegree[rr][cc] -= 1
            if indegree[rr][cc] == 0:
                queue.append((rr, cc))
    if processed != valid_count:
        raise ValueError("flow graph contains a cycle")
    return accumulation
