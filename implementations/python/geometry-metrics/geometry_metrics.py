"""Teaching implementations of point-set and polyline geometric metrics."""
from __future__ import annotations
from math import atan2, hypot, isfinite
from random import Random
from typing import Iterable, Sequence

Point = tuple[float, float]

def _points(values: Iterable[Sequence[float]], *, minimum: int = 0) -> list[Point]:
    result = []
    for p in values:
        if len(p) != 2:
            raise ValueError("each point must contain exactly two coordinates")
        x, y = float(p[0]), float(p[1])
        if not (isfinite(x) and isfinite(y)):
            raise ValueError("coordinates must be finite")
        result.append((x, y))
    if len(result) < minimum:
        raise ValueError(f"at least {minimum} point(s) are required")
    return result

def _distance(a: Point, b: Point) -> float:
    return hypot(a[0] - b[0], a[1] - b[1])

def directed_hausdorff_distance(a, b) -> float:
    """Maximum, over points in A, of distance to the nearest point in B."""
    aa, bb = _points(a, minimum=1), _points(b, minimum=1)
    return max(min(_distance(p, q) for q in bb) for p in aa)

def hausdorff_distance(a, b) -> float:
    """Symmetric Hausdorff distance between two finite point sets."""
    return max(directed_hausdorff_distance(a, b), directed_hausdorff_distance(b, a))

def discrete_frechet_distance(curve_a, curve_b) -> float:
    """Discrete Fréchet distance between ordered vertex sequences."""
    a, b = _points(curve_a, minimum=1), _points(curve_b, minimum=1)
    previous = [float("inf")] * len(b)
    for i, pa in enumerate(a):
        current = [float("inf")] * len(b)
        for j, pb in enumerate(b):
            d = _distance(pa, pb)
            if i == 0 and j == 0:
                current[j] = d
            elif i == 0:
                current[j] = max(current[j - 1], d)
            elif j == 0:
                current[j] = max(previous[j], d)
            else:
                current[j] = max(min(previous[j], previous[j - 1], current[j - 1]), d)
        previous = current
    return previous[-1]

def _circle_two(a: Point, b: Point):
    cx, cy = (a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0
    return (cx, cy, _distance(a, b) / 2.0)

def _circle_three(a: Point, b: Point, c: Point):
    ax, ay = a
    bx, by = b
    cx, cy = c
    d = 2.0 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    scale = max(1.0, abs(ax), abs(ay), abs(bx), abs(by), abs(cx), abs(cy))
    if abs(d) <= 1e-14 * scale * scale:
        pairs = [(a, b), (a, c), (b, c)]
        return max((_circle_two(p, q) for p, q in pairs), key=lambda circle: circle[2])
    aa, bb, cc = ax * ax + ay * ay, bx * bx + by * by, cx * cx + cy * cy
    ux = (aa * (by - cy) + bb * (cy - ay) + cc * (ay - by)) / d
    uy = (aa * (cx - bx) + bb * (ax - cx) + cc * (bx - ax)) / d
    return (ux, uy, hypot(ux - ax, uy - ay))

def smallest_enclosing_circle(points, *, seed: int = 0):
    """Return (center_x, center_y, radius) using randomized incremental construction.

    The shuffled incremental algorithm maintains the minimum circle for the
    prefix already processed. When a point falls outside, it is promoted to
    the boundary; nested passes then constrain one and two earlier points.
    Expected running time is linear for a random permutation in fixed
    dimension. The iterative form avoids Python recursion-depth failures.
    """
    pts = _points(points)
    if not pts:
        return None
    Random(seed).shuffle(pts)

    def contains(circle, point):
        if circle is None:
            return False
        x, y, radius = circle
        return _distance((x, y), point) <= radius + 1e-10 * max(1.0, radius)

    circle = None
    for i, point_i in enumerate(pts):
        if contains(circle, point_i):
            continue
        circle = (point_i[0], point_i[1], 0.0)
        for j in range(i):
            point_j = pts[j]
            if contains(circle, point_j):
                continue
            circle = _circle_two(point_i, point_j)
            for k in range(j):
                point_k = pts[k]
                if not contains(circle, point_k):
                    circle = _circle_three(point_i, point_j, point_k)
    return circle


def convex_hull(points):
    """Return the strict counter-clockwise monotone-chain hull."""
    pts = sorted(set(_points(points)))
    if len(pts) <= 1:
        return pts
    def cross(o, a, b):
        return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
    lower = []
    for point in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)
    upper = []
    for point in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)
    return lower[:-1] + upper[:-1]


def convex_polygon_diameter(points):
    """Return (endpoint_a, endpoint_b, distance) using rotating calipers.

    The convex hull is built internally. Total time is O(n log n) for hull
    construction plus O(h) for the antipodal-pair sweep.
    """
    hull = convex_hull(points)
    n = len(hull)
    if n == 0:
        return None
    if n == 1:
        return (hull[0], hull[0], 0.0)
    if n == 2:
        return (hull[0], hull[1], _distance(hull[0], hull[1]))
    def area(i, j):
        a, b, c = hull[i], hull[(i+1) % n], hull[j]
        return abs((b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0]))
    best = (hull[0], hull[1], _distance(hull[0], hull[1]))
    j = 1
    for i in range(n):
        ni = (i+1) % n
        while area(i, (j+1) % n) > area(i, j) + 1e-14:
            j = (j+1) % n
        for a, b in ((hull[i], hull[j]), (hull[ni], hull[j])):
            d = _distance(a, b)
            if d > best[2]:
                best = (a, b, d)
        nj = (j+1) % n
        if abs(area(i, nj)-area(i, j)) <= 1e-14:
            for a, b in ((hull[i], hull[nj]), (hull[ni], hull[nj])):
                d = _distance(a, b)
                if d > best[2]:
                    best = (a, b, d)
    return best


def _ring(values):
    ring = _points(values, minimum=3)
    if ring[0] != ring[-1]:
        ring.append(ring[0])
    if len(set(ring[:-1])) < 3:
        raise ValueError("each polygon ring must contain at least three unique vertices")
    return ring


def _point_in_ring(point, ring):
    x, y = point
    inside = False
    for a, b in zip(ring, ring[1:]):
        if (a[1] > y) != (b[1] > y):
            x_cross = a[0] + (y-a[1]) * (b[0]-a[0]) / (b[1]-a[1])
            if x < x_cross:
                inside = not inside
    return inside


def _point_segment_distance(point, a, b):
    dx, dy = b[0]-a[0], b[1]-a[1]
    denom = dx*dx + dy*dy
    if denom == 0:
        return _distance(point, a)
    t = max(0.0, min(1.0, ((point[0]-a[0])*dx + (point[1]-a[1])*dy) / denom))
    return hypot(point[0]-a[0]-t*dx, point[1]-a[1]-t*dy)


def polylabel(outer_ring, holes=(), *, precision=1.0, max_cells=1_000_000):
    """Approximate a polygon's pole of inaccessibility.

    Returns (x, y, radius, cells_examined). The radius is the distance to the
    nearest polygon boundary. Outer and hole rings must form a valid polygon.
    Precision is an absolute planar distance tolerance.
    """
    from heapq import heappop, heappush
    from math import sqrt
    outer = _ring(outer_ring)
    hole_rings = [_ring(r) for r in holes]
    if not isfinite(precision) or precision <= 0:
        raise ValueError("precision must be finite and positive")
    if not isinstance(max_cells, int) or isinstance(max_cells, bool) or max_cells < 1:
        raise ValueError("max_cells must be a positive integer")
    all_rings = [outer] + hole_rings
    min_x = min(p[0] for p in outer[:-1])
    min_y = min(p[1] for p in outer[:-1])
    max_x = max(p[0] for p in outer[:-1])
    max_y = max(p[1] for p in outer[:-1])
    width, height = max_x-min_x, max_y-min_y
    if width == 0 or height == 0:
        raise ValueError("polygon exterior must have positive area")

    def signed_distance(point):
        inside = _point_in_ring(point, outer) and not any(_point_in_ring(point, h) for h in hole_rings)
        distance = min(_point_segment_distance(point, a, b)
                       for ring in all_rings for a, b in zip(ring, ring[1:]))
        return distance if inside else -distance

    def make_cell(x, y, half):
        d = signed_distance((x, y))
        return (d + half*sqrt(2.0), x, y, half, d)

    cell_size = min(width, height)
    half = cell_size / 2.0
    heap = []
    initial_cells = 0
    x = min_x
    while x < max_x:
        y = min_y
        while y < max_y:
            initial_cells += 1
            if initial_cells > max_cells:
                raise RuntimeError("polylabel initial grid exceeded max_cells; raise the limit")
            cell = make_cell(x+half, y+half, half)
            heappush(heap, (-cell[0], cell[1], cell[2], cell[3], cell[4]))
            y += cell_size
        x += cell_size

    best = make_cell((min_x+max_x)/2.0, (min_y+max_y)/2.0, 0.0)
    cells_examined = 0
    while heap:
        neg_max, cx, cy, half, d = heappop(heap)
        upper_bound = -neg_max
        cells_examined += 1
        if cells_examined > max_cells:
            raise RuntimeError("polylabel exceeded max_cells; relax precision or raise the limit")
        if d > best[4]:
            best = (upper_bound, cx, cy, half, d)
        if upper_bound-best[4] <= precision:
            continue
        quarter = half/2.0
        for dx in (-quarter, quarter):
            for dy in (-quarter, quarter):
                child = make_cell(cx+dx, cy+dy, quarter)
                heappush(heap, (-child[0], child[1], child[2], child[3], child[4]))
    return (best[1], best[2], max(0.0, best[4]), cells_examined)


def minimum_area_bounding_rectangle(points):
    """Return the minimum-area rectangle aligned to a convex-hull edge.

    Result keys are corners (counter-clockwise), area, and edge angle in
    radians. This transparent baseline tests every hull-edge orientation and
    scans all hull vertices for each, so it is O(h^2), not linear-time calipers.
    """
    hull = convex_hull(points)
    if not hull:
        return None
    if len(hull) == 1:
        p = hull[0]
        return {"corners": (p, p, p, p), "area": 0.0, "angle_radians": 0.0}
    best = None
    edges = list(zip(hull, hull[1:] + hull[:1]))
    for a, b in edges:
        dx, dy = b[0]-a[0], b[1]-a[1]
        length = hypot(dx, dy)
        if length == 0:
            continue
        ux, uy = dx/length, dy/length
        vx, vy = -uy, ux
        along = [x*ux + y*uy for x,y in hull]
        across = [x*vx + y*vy for x,y in hull]
        s0, s1 = min(along), max(along)
        t0, t1 = min(across), max(across)
        area = (s1-s0)*(t1-t0)
        corners = (
            (s0*ux+t0*vx, s0*uy+t0*vy),
            (s1*ux+t0*vx, s1*uy+t0*vy),
            (s1*ux+t1*vx, s1*uy+t1*vy),
            (s0*ux+t1*vx, s0*uy+t1*vy),
        )
        candidate = {"corners": corners, "area": area, "angle_radians": atan2(uy,ux)}
        if best is None or area < best["area"]:
            best = candidate
    return best


def _free_space_interval(point, start, end, epsilon):
    """Parameter interval on segment start-end within epsilon of point."""
    from math import sqrt
    dx, dy = end[0] - start[0], end[1] - start[1]
    px, py = start[0] - point[0], start[1] - point[1]
    aa = dx*dx + dy*dy
    cc = px*px + py*py - epsilon*epsilon
    if aa == 0.0:
        return (0.0, 1.0) if cc <= 0.0 else None
    bb = 2.0 * (px*dx + py*dy)
    discriminant = bb*bb - 4.0*aa*cc
    if discriminant < 0.0:
        return None
    root = sqrt(max(0.0, discriminant))
    lo = max(0.0, (-bb-root)/(2.0*aa))
    hi = min(1.0, (-bb+root)/(2.0*aa))
    return (lo, hi) if lo <= hi else None


def continuous_frechet_decision(curve_a, curve_b, epsilon):
    """Decide whether two polygonal curves have continuous Frechet distance <= epsilon.

    Uses Alt–Godau free-space reachability on the parameter-space cell grid.
    Runtime and memory are O(m*n) for m and n curve segments.
    """
    a, b = _points(curve_a, minimum=1), _points(curve_b, minimum=1)
    if not isfinite(epsilon) or epsilon < 0:
        raise ValueError("epsilon must be finite and non-negative")
    if len(a) == 1 or len(b) == 1:
        if len(a) == len(b) == 1:
            return _distance(a[0], b[0]) <= epsilon
        fixed, moving = (a[0], b) if len(a) == 1 else (b[0], a)
        return max(_distance(fixed, point) for point in moving) <= epsilon

    n, m = len(a)-1, len(b)-1
    # Reachable portions of the global bottom and left boundaries.
    bottom_boundary = [None] * n
    for i in range(n):
        interval = _free_space_interval(b[0], a[i], a[i+1], epsilon)
        if interval is not None and interval[0] <= 0.0:
            if i == 0 or (bottom_boundary[i-1] is not None and bottom_boundary[i-1][1] >= 1.0):
                bottom_boundary[i] = (0.0, interval[1])

    left_boundary = [None] * m
    for j in range(m):
        interval = _free_space_interval(a[0], b[j], b[j+1], epsilon)
        if interval is not None and interval[0] <= 0.0:
            if j == 0 or (left_boundary[j-1] is not None and left_boundary[j-1][1] >= 1.0):
                left_boundary[j] = (0.0, interval[1])

    right = [[None] * m for _ in range(n)]
    top = [[None] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            reachable_bottom = bottom_boundary[i] if j == 0 else top[i][j-1]
            reachable_left = left_boundary[j] if i == 0 else right[i-1][j]
            free_right = _free_space_interval(a[i+1], b[j], b[j+1], epsilon)
            free_top = _free_space_interval(b[j+1], a[i], a[i+1], epsilon)

            if free_right is not None:
                if reachable_bottom is not None:
                    right[i][j] = free_right
                elif reachable_left is not None:
                    lo = max(free_right[0], reachable_left[0])
                    if lo <= free_right[1]:
                        right[i][j] = (lo, free_right[1])

            if free_top is not None:
                if reachable_left is not None:
                    top[i][j] = free_top
                elif reachable_bottom is not None:
                    lo = max(free_top[0], reachable_bottom[0])
                    if lo <= free_top[1]:
                        top[i][j] = (lo, free_top[1])

    final_right = right[-1][-1]
    final_top = top[-1][-1]
    return (
        (final_right is not None and final_right[0] <= 1.0 <= final_right[1])
        or (final_top is not None and final_top[0] <= 1.0 <= final_top[1])
    )


def continuous_frechet_distance(
    curve_a, curve_b, *, tolerance=1e-6, max_iterations=80
):
    """Approximate continuous Frechet distance by bisection over the decision test.

    The returned value is an upper bound within the requested absolute
    tolerance, subject to floating-point arithmetic. Curves are polygonal
    chains in a common planar coordinate system.
    """
    a, b = _points(curve_a, minimum=1), _points(curve_b, minimum=1)
    if not isfinite(tolerance) or tolerance <= 0:
        raise ValueError("tolerance must be finite and positive")
    if not isinstance(max_iterations, int) or isinstance(max_iterations, bool) or max_iterations < 1:
        raise ValueError("max_iterations must be a positive integer")
    if len(a) == 1 or len(b) == 1:
        fixed, moving = (a[0], b) if len(a) == 1 else (b[0], a)
        return max(_distance(fixed, point) for point in moving)
    lower = max(_distance(a[0], b[0]), _distance(a[-1], b[-1]))
    upper = max(_distance(p, q) for p in a for q in b)
    if upper == lower:
        return upper
    iterations = 0
    while upper - lower > tolerance and iterations < max_iterations:
        middle = (lower + upper) / 2.0
        if continuous_frechet_decision(a, b, middle):
            upper = middle
        else:
            lower = middle
        iterations += 1
    return upper


def largest_empty_circle(points, *, precision=1.0, max_cells=1_000_000):
    """Approximate the largest empty circle with centre inside the sites' convex hull.

    Returns (center_x, center_y, radius, cells_examined). The radius is the
    distance to the nearest site. A Lipschitz branch-and-bound search gives an
    additive upper-bound gap no greater than precision, subject to floating
    point arithmetic. At least three non-collinear sites are required.
    """
    from heapq import heappop, heappush
    from math import sqrt

    sites = _points(points, minimum=3)
    hull = convex_hull(sites)
    if len(hull) < 3:
        raise ValueError("sites must have a two-dimensional convex hull")
    if not isfinite(precision) or precision <= 0:
        raise ValueError("precision must be finite and positive")
    if not isinstance(max_cells, int) or isinstance(max_cells, bool) or max_cells < 1:
        raise ValueError("max_cells must be a positive integer")

    ring = hull + [hull[0]]
    min_x = min(p[0] for p in hull)
    min_y = min(p[1] for p in hull)
    max_x = max(p[0] for p in hull)
    max_y = max(p[1] for p in hull)

    def clearance(x, y):
        return min(_distance((x, y), site) for site in sites)

    def cell(x, y, half):
        radius = clearance(x, y)
        upper = radius + half * sqrt(2.0)
        return (-upper, x, y, half, radius)

    def intersects_hull(x, y, half):
        """Conservatively test whether an axis-aligned cell meets the hull."""
        x0, x1 = x-half, x+half
        y0, y1 = y-half, y+half
        if _point_in_ring((x, y), ring):
            return True
        corners = ((x0,y0),(x1,y0),(x1,y1),(x0,y1))
        if any(_point_in_ring(point, ring) for point in corners):
            return True
        if any(x0 <= px <= x1 and y0 <= py <= y1 for px,py in hull):
            return True
        # Liang–Barsky segment/rectangle clipping catches edge crossings
        # even when neither a corner nor a hull vertex lies in the cell.
        for a, b in zip(ring, ring[1:]):
            dx, dy = b[0]-a[0], b[1]-a[1]
            p_values = (-dx, dx, -dy, dy)
            q_values = (a[0]-x0, x1-a[0], a[1]-y0, y1-a[1])
            t0, t1 = 0.0, 1.0
            hit = True
            for p_value, q_value in zip(p_values, q_values):
                if p_value == 0.0:
                    if q_value < 0.0:
                        hit = False
                        break
                else:
                    ratio = q_value / p_value
                    if p_value < 0.0:
                        t0 = max(t0, ratio)
                    else:
                        t1 = min(t1, ratio)
                    if t0 > t1:
                        hit = False
                        break
            if hit:
                return True
        return False

    # The arithmetic mean of hull vertices is inside their convex hull.
    best_x = sum(p[0] for p in hull) / len(hull)
    best_y = sum(p[1] for p in hull) / len(hull)
    best_radius = clearance(best_x, best_y)
    half = max(max_x - min_x, max_y - min_y) / 2.0
    heap = [cell((min_x + max_x) / 2.0, (min_y + max_y) / 2.0, half)]
    examined = 0

    while heap:
        neg_upper, x, y, half, radius = heappop(heap)
        upper = -neg_upper
        examined += 1
        if examined > max_cells:
            raise RuntimeError("largest-empty-circle search exceeded max_cells")
        if upper <= best_radius + precision:
            continue
        if _point_in_ring((x, y), ring) and radius > best_radius:
            best_x, best_y, best_radius = x, y, radius

        child_half = half / 2.0
        if child_half == 0.0:
            continue
        for dx in (-child_half, child_half):
            for dy in (-child_half, child_half):
                child_x, child_y = x + dx, y + dy
                if not intersects_hull(child_x, child_y, child_half):
                    continue
                child = cell(child_x, child_y, child_half)
                if -child[0] > best_radius + precision:
                    heappush(heap, child)

    return (best_x, best_y, best_radius, examined)


def minimum_area_bounding_rectangle_calipers(points):
    """Return a minimum-area oriented rectangle using four rotating supports.

    The convex hull costs O(n log n); after the hull is built, four support
    indices advance monotonically around it, giving an O(h) sweep. The result
    has the same keys as minimum_area_bounding_rectangle.
    """
    hull = convex_hull(points)
    n = len(hull)
    if n == 0:
        return None
    if n == 1:
        point = hull[0]
        return {"corners": (point, point, point, point),
                "area": 0.0, "angle_radians": 0.0}
    if n == 2:
        a, b = hull
        return {"corners": (a, b, b, a), "area": 0.0,
                "angle_radians": atan2(b[1]-a[1], b[0]-a[0])}

    def dot(point, direction):
        return point[0]*direction[0] + point[1]*direction[1]

    def initial_support(direction, maximize):
        values = [dot(point, direction) for point in hull]
        return (max if maximize else min)(range(n), key=values.__getitem__)

    def advance(index, direction, maximize):
        steps = 0
        while steps < n:
            following = (index + 1) % n
            current_value = dot(hull[index], direction)
            following_value = dot(hull[following], direction)
            improves = (
                following_value > current_value + 1e-12
                if maximize else following_value < current_value - 1e-12
            )
            if not improves:
                break
            index = following
            steps += 1
        return index

    first_dx = hull[1][0] - hull[0][0]
    first_dy = hull[1][1] - hull[0][1]
    first_length = hypot(first_dx, first_dy)
    first_u = (first_dx/first_length, first_dy/first_length)
    first_v = (-first_u[1], first_u[0])
    max_u = initial_support(first_u, True)
    min_u = initial_support(first_u, False)
    max_v = initial_support(first_v, True)
    min_v = initial_support(first_v, False)

    best = None
    for i in range(n):
        a, b = hull[i], hull[(i+1) % n]
        dx, dy = b[0]-a[0], b[1]-a[1]
        length = hypot(dx, dy)
        ux, uy = dx/length, dy/length
        u = (ux, uy)
        v = (-uy, ux)

        max_u = advance(max_u, u, True)
        min_u = advance(min_u, u, False)
        max_v = advance(max_v, v, True)
        min_v = advance(min_v, v, False)

        s0, s1 = dot(hull[min_u], u), dot(hull[max_u], u)
        t0, t1 = dot(hull[min_v], v), dot(hull[max_v], v)
        area = max(0.0, (s1-s0)*(t1-t0))
        corners = (
            (s0*ux+t0*v[0], s0*uy+t0*v[1]),
            (s1*ux+t0*v[0], s1*uy+t0*v[1]),
            (s1*ux+t1*v[0], s1*uy+t1*v[1]),
            (s0*ux+t1*v[0], s0*uy+t1*v[1]),
        )
        candidate = {
            "corners": corners,
            "area": area,
            "angle_radians": atan2(uy, ux),
        }
        if best is None or area < best["area"]:
            best = candidate
    return best
