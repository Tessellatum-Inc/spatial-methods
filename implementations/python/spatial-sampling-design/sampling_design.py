"""Space-filling sampling designs for bounded continuous parameter spaces."""
from __future__ import annotations

import math
import random
from collections.abc import Iterable, Sequence


def _validate_bounds(bounds: Sequence[tuple[float, float]]) -> list[tuple[float, float]]:
    if isinstance(bounds, (str, bytes)) or not bounds:
        raise ValueError("bounds must contain at least one (lower, upper) pair")
    checked = []
    for pair in bounds:
        if isinstance(pair, (str, bytes)) or len(pair) != 2:
            raise ValueError("each bound must be a (lower, upper) pair")
        lower, upper = pair
        if (isinstance(lower, bool) or isinstance(upper, bool)
                or not isinstance(lower, (int, float))
                or not isinstance(upper, (int, float))
                or not math.isfinite(lower) or not math.isfinite(upper)
                or lower >= upper):
            raise ValueError("bounds must be finite numeric pairs with lower < upper")
        checked.append((float(lower), float(upper)))
    return checked


def _validate_size(n: int) -> None:
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise ValueError("sample size must be a positive integer")


def _distance2(a: Sequence[float], b: Sequence[float]) -> float:
    return math.fsum((x - y) ** 2 for x, y in zip(a, b))


def latin_hypercube(
    n: int,
    bounds: Sequence[tuple[float, float]],
    *,
    seed: int | None = None,
    centered: bool = False,
) -> list[tuple[float, ...]]:
    """Generate an n-point Latin hypercube over a rectangular domain.

    Every dimension is divided into n equal-width strata, and exactly one
    sample is placed in each stratum. Random jitter is uniform within each
    stratum; centered=True uses stratum midpoints. A local RNG makes seeded
    calls reproducible without changing global random state.
    """
    _validate_size(n)
    domain = _validate_bounds(bounds)
    if not isinstance(centered, bool):
        raise ValueError("centered must be boolean")
    rng = random.Random(seed)
    columns: list[list[float]] = []
    for lower, upper in domain:
        width = (upper - lower) / n
        order = list(range(n))
        rng.shuffle(order)
        if centered:
            values = [lower + (stratum + 0.5) * width for stratum in order]
        else:
            values = [lower + (stratum + rng.random()) * width for stratum in order]
        columns.append(values)
    return [tuple(columns[d][i] for d in range(len(domain))) for i in range(n)]


def minimum_pair_distance(points: Sequence[Sequence[float]]) -> float:
    """Return the minimum Euclidean distance between distinct sample rows."""
    if len(points) < 2:
        raise ValueError("at least two points are required")
    dimension = len(points[0])
    if dimension < 1 or any(len(point) != dimension for point in points):
        raise ValueError("points must have one consistent positive dimension")
    if any(not math.isfinite(value) for point in points for value in point):
        raise ValueError("point coordinates must be finite")
    return math.sqrt(min(
        _distance2(points[i], points[j])
        for i in range(len(points)) for j in range(i + 1, len(points))
    ))


def maximin_latin_hypercube(
    n: int,
    bounds: Sequence[tuple[float, float]],
    *,
    candidates: int = 32,
    seed: int | None = None,
    centered: bool = False,
) -> list[tuple[float, ...]]:
    """Choose the best of several randomized Latin hypercubes by maximin score.

    Distances are measured after independently scaling each domain dimension
    to [0, 1], so units and ranges do not dominate the criterion. This is a
    multi-start heuristic, not a proof of globally optimal maximin design.
    """
    _validate_size(n)
    domain = _validate_bounds(bounds)
    if isinstance(candidates, bool) or not isinstance(candidates, int) or candidates < 1:
        raise ValueError("candidates must be a positive integer")
    if n < 2:
        raise ValueError("maximin design requires at least two points")
    rng = random.Random(seed)
    best: list[tuple[float, ...]] | None = None
    best_score = -1.0
    for _ in range(candidates):
        design = latin_hypercube(n, domain, seed=rng.getrandbits(64), centered=centered)
        normalized = [
            tuple((point[d] - domain[d][0]) / (domain[d][1] - domain[d][0])
                  for d in range(len(domain)))
            for point in design
        ]
        score = minimum_pair_distance(normalized)
        if score > best_score:
            best, best_score = design, score
    assert best is not None
    return best


def kmeans_coverage(
    points: Sequence[Sequence[float]],
    k: int,
    *,
    max_iterations: int = 100,
    tolerance: float = 1e-9,
) -> list[tuple[float, ...]]:
    """Return k centroid sites summarizing supplied spatial sample points.

    Initialization uses deterministic farthest-first selection. Lloyd updates
    then assign each observation to its nearest centroid and recompute means.
    Empty clusters retain their previous centroid. This is a local heuristic;
    it does not guarantee a globally optimal k-means objective.
    """
    if isinstance(k, bool) or not isinstance(k, int) or k < 1:
        raise ValueError("k must be a positive integer")
    if isinstance(max_iterations, bool) or not isinstance(max_iterations, int) or max_iterations < 1:
        raise ValueError("max_iterations must be a positive integer")
    if (isinstance(tolerance, bool) or not isinstance(tolerance, (int, float))
            or not math.isfinite(tolerance) or tolerance < 0):
        raise ValueError("tolerance must be a finite non-negative number")
    if isinstance(points, (str, bytes)) or len(points) < k:
        raise ValueError("points must contain at least k observations")
    dimension = len(points[0])
    if dimension < 1 or any(len(point) != dimension for point in points):
        raise ValueError("points must have one consistent positive dimension")
    data = [tuple(float(x) for x in point) for point in points]
    if any(not math.isfinite(x) for point in data for x in point):
        raise ValueError("point coordinates must be finite")

    centroids = [data[0]]
    while len(centroids) < k:
        candidate = max(
            data,
            key=lambda point: min(_distance2(point, center) for center in centroids),
        )
        centroids.append(candidate)

    for _ in range(max_iterations):
        groups: list[list[tuple[float, ...]]] = [[] for _ in range(k)]
        for point in data:
            index = min(range(k), key=lambda i: _distance2(point, centroids[i]))
            groups[index].append(point)
        updated = []
        for index, group in enumerate(groups):
            if not group:
                updated.append(centroids[index])
            else:
                updated.append(tuple(
                    math.fsum(point[d] for point in group) / len(group)
                    for d in range(dimension)
                ))
        movement = max(math.sqrt(_distance2(a, b)) for a, b in zip(centroids, updated))
        centroids = updated
        if movement <= tolerance:
            break
    return centroids
