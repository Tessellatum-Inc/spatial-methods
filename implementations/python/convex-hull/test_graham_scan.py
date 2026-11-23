import random

import pytest

from graham_scan import convex_hull, jarvis_march, quickhull


@pytest.mark.parametrize("algorithm", [convex_hull, jarvis_march, quickhull])
def test_square_returns_counter_clockwise_extreme_vertices(algorithm):
    points = [(0, 0), (2, 0), (2, 2), (0, 2), (1, 1)]
    assert algorithm(points) == [
        (0.0, 0.0), (2.0, 0.0), (2.0, 2.0), (0.0, 2.0)
    ]


@pytest.mark.parametrize("algorithm", [convex_hull, jarvis_march, quickhull])
def test_degenerate_and_duplicate_inputs(algorithm):
    assert algorithm([]) == []
    assert algorithm([(3, 7)]) == [(3.0, 7.0)]
    assert algorithm([(2, 2), (0, 0)]) == [(0.0, 0.0), (2.0, 2.0)]
    assert algorithm([(3, 3), (0, 0), (1, 1), (2, 2), (4, 4)]) == [
        (0.0, 0.0), (4.0, 4.0)
    ]
    assert algorithm([(0, 0), (1, 0), (0, 1), (0, 0)]) == [
        (0.0, 0.0), (1.0, 0.0), (0.0, 1.0)
    ]


@pytest.mark.parametrize("algorithm", [convex_hull, jarvis_march, quickhull])
def test_collinear_edge_points_are_omitted(algorithm):
    points = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2),
              (1, 2), (0, 2), (0, 1), (1, 1)]
    assert algorithm(points) == [
        (0.0, 0.0), (2.0, 0.0), (2.0, 2.0), (0.0, 2.0)
    ]


@pytest.mark.parametrize("algorithm", [convex_hull, jarvis_march, quickhull])
@pytest.mark.parametrize("bad", [
    (float("nan"), 0), (0, float("inf")), (float("-inf"), 1)
])
def test_non_finite_coordinates_are_rejected(algorithm, bad):
    with pytest.raises(ValueError, match="finite"):
        algorithm([(0, 0), (1, 0), (0, 1), bad])


def _monotone_chain_reference(points):
    """Independent Andrew monotone-chain oracle used only by randomized tests."""
    pts = sorted(set(points))
    if len(pts) <= 1:
        return pts

    def cross(o, a, b):
        return ((a[0] - o[0]) * (b[1] - o[1])
                - (a[1] - o[1]) * (b[0] - o[0]))

    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


@pytest.mark.parametrize("algorithm", [convex_hull, jarvis_march, quickhull])
def test_seeded_random_clouds_match_independent_monotone_chain(algorithm):
    rng = random.Random(20261115)
    for _ in range(120):
        points = [(rng.randrange(-20, 21), rng.randrange(-20, 21))
                  for _ in range(rng.randrange(0, 45))]
        expected = _monotone_chain_reference(points)
        actual = algorithm(points)
        assert set(actual) == set(expected)
        if len(actual) >= 3:
            signed_area_twice = sum(
                actual[i][0] * actual[(i + 1) % len(actual)][1]
                - actual[(i + 1) % len(actual)][0] * actual[i][1]
                for i in range(len(actual))
            )
            assert signed_area_twice > 0
