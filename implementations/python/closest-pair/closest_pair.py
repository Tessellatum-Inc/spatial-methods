"""O(n log n) closest pair of planar points by divide and conquer."""
from __future__ import annotations

from math import hypot, isfinite
from typing import Iterable

Point = tuple[float, float]


def closest_pair(points: Iterable[tuple[float, float]]) -> tuple[Point, Point, float]:
    """Return the closest distinct input occurrences and their Euclidean distance.

    Duplicate coordinates are valid and produce distance zero. Ties are resolved
    deterministically by the original input indices among inspected equal-distance candidates. At least two points are
    required. The implementation is planar and uses ordinary floating-point
    comparisons (not exact geometric predicates).
    """
    pts: list[Point] = []
    for point in points:
        if len(point) != 2:
            raise ValueError("Each point must contain exactly two coordinates")
        x, y = float(point[0]), float(point[1])
        if not isfinite(x) or not isfinite(y):
            raise ValueError("Coordinates must be finite")
        pts.append((x, y))
    if len(pts) < 2:
        raise ValueError("At least two points are required")

    # Keep original indices so equal coordinates remain distinct occurrences
    # and tie-breaking is stable even when the input contains duplicates.
    px = sorted(((p[0], p[1], i) for i, p in enumerate(pts)))
    py = sorted(((p[1], p[0], i) for i, p in enumerate(pts)))

    def pair_key(candidate):
        d2, i, j = candidate
        return (d2, i, j) if i < j else (d2, j, i)

    def brute(items):
        best = None
        for a in range(len(items)):
            for b in range(a + 1, len(items)):
                x1, y1, i = items[a]
                x2, y2, j = items[b]
                candidate = ((x1 - x2) ** 2 + (y1 - y2) ** 2, i, j)
                if best is None or pair_key(candidate) < pair_key(best):
                    best = candidate
        return best

    def solve(x_sorted, y_sorted):
        n = len(x_sorted)
        if n <= 3:
            return brute(x_sorted)
        middle = n // 2
        split_x = x_sorted[middle][0]
        left_x, right_x = x_sorted[:middle], x_sorted[middle:]
        left_ids = {item[2] for item in left_x}
        left_y, right_y = [], []
        for item in y_sorted:
            (left_y if item[2] in left_ids else right_y).append(item)

        best = min((solve(left_x, left_y), solve(right_x, right_y)),
                   key=pair_key)
        strip = [item for item in y_sorted
                 if (item[1] - split_x) ** 2 <= best[0]]
        for a, first in enumerate(strip):
            # In the planar packing argument, at most the next seven points
            # need inspection; retaining the y-distance guard is sufficient.
            for second in strip[a + 1:a + 8]:
                if (second[0] - first[0]) ** 2 > best[0]:
                    break
                candidate = ((first[1] - second[1]) ** 2
                             + (first[0] - second[0]) ** 2,
                             first[2], second[2])
                if pair_key(candidate) < pair_key(best):
                    best = candidate
        return best

    distance_squared, first_index, second_index = solve(px, py)
    if first_index > second_index:
        first_index, second_index = second_index, first_index
    first, second = pts[first_index], pts[second_index]
    return first, second, hypot(first[0] - second[0], first[1] - second[1])
