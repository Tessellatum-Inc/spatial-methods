"""Teaching implementations of point-set and polyline geometric metrics."""
from __future__ import annotations
from math import atan2, hypot, isclose, isfinite, ulp
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
    # The distance is symmetric; keep the shorter sequence in the DP columns.
    if len(b) > len(a):
        a, b = b, a
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
    dx, dy = b[0] - a[0], b[1] - a[1]
    cx, cy = a[0] + dx / 2.0, a[1] + dy / 2.0
    return (cx, cy, hypot(dx, dy) / 2.0)


def _circle_three(a: Point, b: Point, c: Point):
    """Circumcircle computed in a local frame to avoid translation scaling."""
    ux, uy = b[0] - a[0], b[1] - a[1]
    vx, vy = c[0] - a[0], c[1] - a[1]
    determinant = 2.0 * (ux * vy - uy * vx)
    edge_scale = max(hypot(ux, uy), hypot(vx, vy),
                     hypot(c[0] - b[0], c[1] - b[1]))
    if edge_scale == 0.0 or abs(determinant) <= 1e-14 * edge_scale * edge_scale:
        pairs = [(a, b), (a, c), (b, c)]
        return max((_circle_two(p, q) for p, q in pairs), key=lambda circle: circle[2])
    u2, v2 = ux * ux + uy * uy, vx * vx + vy * vy
    offset_x = (u2 * vy - v2 * uy) / determinant
    offset_y = (ux * v2 - vx * u2) / determinant
    center_x, center_y = a[0] + offset_x, a[1] + offset_y
    return (center_x, center_y, hypot(offset_x, offset_y))


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
        tolerance = 8.0 * max(ulp(x), ulp(y), ulp(point[0]), ulp(point[1]), ulp(radius))
        return _distance((x, y), point) <= radius + tolerance

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
        while area(i, (j+1) % n) > area(i, j):
            j = (j+1) % n
        for a, b in ((hull[i], hull[j]), (hull[ni], hull[j])):
            d = _distance(a, b)
            if d > best[2]:
                best = (a, b, d)
        nj = (j+1) % n
        if isclose(area(i, nj), area(i, j), rel_tol=1e-14, abs_tol=0.0):
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
    Runtime is O(m*n); auxiliary memory is O(min(m, n)) after orienting
    the shorter curve as the column dimension.
    """
    a, b = _points(curve_a, minimum=1), _points(curve_b, minimum=1)
    if not isfinite(epsilon) or epsilon < 0:
        raise ValueError("epsilon must be finite and non-negative")
    if len(a) == 1 or len(b) == 1:
        if len(a) == len(b) == 1:
            return _distance(a[0], b[0]) <= epsilon
        fixed, moving = (a[0], b) if len(a) == 1 else (b[0], a)
        return max(_distance(fixed, point) for point in moving) <= epsilon

    # The recurrence only needs the preceding row and the preceding cell
    # within the current row. Put the shorter curve on the column axis.
    if len(b) > len(a):
        a, b = b, a
    n, m = len(a)-1, len(b)-1
    right_previous = [None] * m
    final_top = [None] * m
    bottom_previous = None

    for i in range(n):
        bottom_interval = _free_space_interval(b[0], a[i], a[i+1], epsilon)
        if (bottom_interval is not None and bottom_interval[0] <= 0.0
                and (i == 0 or (bottom_previous is not None
                                and bottom_previous[1] >= 1.0))):
            bottom_current = (0.0, bottom_interval[1])
        else:
            bottom_current = None
        bottom_previous = bottom_current

        right_current = [None] * m
        top_current = [None] * m
        left_previous = None

        for j in range(m):
            if i == 0:
                left_interval = _free_space_interval(a[0], b[j], b[j+1], epsilon)
                if (left_interval is not None and left_interval[0] <= 0.0
                        and (j == 0 or (left_previous is not None
                                        and left_previous[1] >= 1.0))):
                    reachable_left = (0.0, left_interval[1])
                else:
                    reachable_left = None
                left_previous = reachable_left
            else:
                reachable_left = right_previous[j]

            reachable_bottom = bottom_current if j == 0 else top_current[j-1]
            free_right = _free_space_interval(a[i+1], b[j], b[j+1], epsilon)
            free_top = _free_space_interval(b[j+1], a[i], a[i+1], epsilon)

            if free_right is not None:
                if reachable_bottom is not None:
                    right_current[j] = free_right
                elif reachable_left is not None:
                    lo = max(free_right[0], reachable_left[0])
                    if lo <= free_right[1]:
                        right_current[j] = (lo, free_right[1])

            if free_top is not None:
                if reachable_left is not None:
                    top_current[j] = free_top
                elif reachable_bottom is not None:
                    lo = max(free_top[0], reachable_bottom[0])
                    if lo <= free_top[1]:
                        top_current[j] = (lo, free_top[1])

        right_previous = right_current
        final_top = top_current

    final_right = right_previous[-1]
    last_top = final_top[-1]
    return (
        (final_right is not None and final_right[0] <= 1.0 <= final_right[1])
        or (last_top is not None and last_top[0] <= 1.0 <= last_top[1])
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

    origin_x, origin_y = hull[0]

    def dot(point, direction):
        return ((point[0]-origin_x)*direction[0]
                + (point[1]-origin_y)*direction[1])

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
                following_value > current_value
                if maximize else following_value < current_value
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
            (origin_x+s0*ux+t0*v[0], origin_y+s0*uy+t0*v[1]),
            (origin_x+s1*ux+t0*v[0], origin_y+s1*uy+t0*v[1]),
            (origin_x+s1*ux+t1*v[0], origin_y+s1*uy+t1*v[1]),
            (origin_x+s0*ux+t1*v[0], origin_y+s0*uy+t1*v[1]),
        )
        candidate = {
            "corners": corners,
            "area": area,
            "angle_radians": atan2(uy, ux),
        }
        if best is None or area < best["area"]:
            best = candidate
    return best


def convex_polygon_minimum_width(points):
    """Return the minimum support-line width of a planar point set.

    The strict convex hull is built internally. For each hull edge, the
    maximum perpendicular distance to its parallel support line is found
    with a monotone antipodal pointer. The total is O(n log n) for hull
    construction plus O(h) for the rotating-calipers sweep, with O(h)
    hull storage. Width is zero for fewer than three non-collinear hull
    vertices (including empty, singleton and collinear inputs).
    """
    hull = convex_hull(points)
    n = len(hull)
    if n < 3:
        return 0.0

    def cross_edge(i, j):
        a = hull[i]
        b = hull[(i + 1) % n]
        p = hull[j]
        return ((b[0] - a[0]) * (p[1] - a[1])
                - (b[1] - a[1]) * (p[0] - a[0]))

    opposite = 1
    best = float("inf")
    for i in range(n):
        next_i = (i + 1) % n
        edge_length = _distance(hull[i], hull[next_i])
        if edge_length == 0.0:
            continue
        current_area = cross_edge(i, opposite)
        advances = 0
        while advances < n:
            next_opposite = (opposite + 1) % n
            next_area = cross_edge(i, next_opposite)
            if next_area > current_area:
                opposite = next_opposite
                current_area = next_area
                advances += 1
            else:
                break
        best = min(best, current_area / edge_length)
    return 0.0 if best == float("inf") else best


def _advance_caliper(hull, index, dx, dy):
    """Advance a support vertex while the next vertex improves its projection."""
    n = len(hull)
    for _ in range(n):
        current = hull[index][0] * dx + hull[index][1] * dy
        nxt_index = (index + 1) % n
        nxt = hull[nxt_index][0] * dx + hull[nxt_index][1] * dy
        tolerance = 8.0 * max(ulp(current), ulp(nxt))
        if nxt > current + tolerance:
            index = nxt_index
        else:
            break
    return index


def _rotating_caliper_bounds(hull, ux, uy, supports):
    """Return four support indices for u, -u, v and -v."""
    vx, vy = -uy, ux
    directions = ((ux, uy), (-ux, -uy), (vx, vy), (-vx, -vy))
    return tuple(_advance_caliper(hull, i, dx, dy)
                 for i, (dx, dy) in zip(supports, directions))


def minimum_area_bounding_rectangle_calipers(points):
    """Minimum-area enclosing rectangle in O(n log n) including hull creation.

    The hull is counter-clockwise. Four monotone support pointers track the
    maximum/minimum projections on the edge direction and its normal while
    hull-edge orientations rotate. Returns corners, area, width, height and
    edge angle. Degenerate point and line inputs are handled explicitly.
    """
    hull = convex_hull(points)
    n = len(hull)
    if n == 0:
        return None
    if n == 1:
        p = hull[0]
        return {"corners": (p, p, p, p), "area": 0.0,
                "width": 0.0, "height": 0.0, "angle_radians": 0.0}
    if n == 2:
        a, b = hull
        return {"corners": (a, b, b, a), "area": 0.0,
                "width": _distance(a, b), "height": 0.0,
                "angle_radians": atan2(b[1]-a[1], b[0]-a[0])}

    edges = list(zip(hull, hull[1:] + hull[:1]))
    a0, b0 = edges[0]
    length = hypot(b0[0]-a0[0], b0[1]-a0[1])
    ux0, uy0 = (b0[0]-a0[0])/length, (b0[1]-a0[1])/length
    vx0, vy0 = -uy0, ux0
    directions = ((ux0, uy0), (-ux0, -uy0), (vx0, vy0), (-vx0, -vy0))
    supports = tuple(max(range(n), key=lambda i, d=d: hull[i][0]*d[0]+hull[i][1]*d[1])
                     for d in directions)
    best = None
    min_width = float("inf")
    min_width_edge = None

    for a, b in edges:
        dx, dy = b[0]-a[0], b[1]-a[1]
        edge_length = hypot(dx, dy)
        if edge_length == 0.0:
            continue
        ux, uy = dx/edge_length, dy/edge_length
        vx, vy = -uy, ux
        supports = _rotating_caliper_bounds(hull, ux, uy, supports)
        i_max_u, i_min_u, i_max_v, i_min_v = supports
        max_u = hull[i_max_u][0]*ux + hull[i_max_u][1]*uy
        min_u = -(hull[i_min_u][0]*(-ux) + hull[i_min_u][1]*(-uy))
        max_v = hull[i_max_v][0]*vx + hull[i_max_v][1]*vy
        min_v = -(hull[i_min_v][0]*(-vx) + hull[i_min_v][1]*(-vy))
        width, height = max_u-min_u, max_v-min_v
        if height < min_width:
            min_width, min_width_edge = height, ((a, b), (vx, vy))
        area = width*height
        if best is None or area < best["area"]:
            corners = (
                (min_u*ux+min_v*vx, min_u*uy+min_v*vy),
                (max_u*ux+min_v*vx, max_u*uy+min_v*vy),
                (max_u*ux+max_v*vx, max_u*uy+max_v*vy),
                (min_u*ux+max_v*vx, min_u*uy+max_v*vy),
            )
            best = {"corners": corners, "area": area, "width": width,
                    "height": height, "angle_radians": atan2(uy, ux)}

    best["minimum_width"] = min_width
    best["minimum_width_edge"] = min_width_edge[0]
    best["minimum_width_normal"] = min_width_edge[1]
    return best
