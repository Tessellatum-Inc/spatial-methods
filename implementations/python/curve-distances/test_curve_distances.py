import math
import random

import pytest

from curve_distances import (
    directed_hausdorff,
    discrete_frechet_distance,
    hausdorff_distance,
)


def test_discrete_hausdorff_known_values_and_directionality():
    a = [(0, 0), (2, 0)]
    b = [(0, 0), (1, 0), (2, 0)]
    assert directed_hausdorff(a, b) == 0
    assert directed_hausdorff(b, a) == 1
    assert hausdorff_distance(a, b) == 1


def test_hausdorff_is_symmetric_and_translation_invariant():
    a = [(-2, 1), (0, 0), (4, 3)]
    b = [(1, 2), (5, 5)]
    expected = hausdorff_distance(a, b)
    assert hausdorff_distance(b, a) == expected
    shift = (1e6, -1e6)
    moved_a = [(x + shift[0], y + shift[1]) for x, y in a]
    moved_b = [(x + shift[0], y + shift[1]) for x, y in b]
    assert hausdorff_distance(moved_a, moved_b) == pytest.approx(expected)


def test_discrete_frechet_known_alignment_and_reversal():
    line = [(0, 0), (1, 0), (2, 0)]
    assert discrete_frechet_distance(line, line) == 0
    assert discrete_frechet_distance(line, list(reversed(line))) == 2
    assert discrete_frechet_distance([(0, 0)], [(3, 4)]) == 5


def test_discrete_frechet_is_at_least_discrete_hausdorff():
    a = [(0, 0), (1, 2), (3, 1), (4, 0)]
    b = [(0, 0), (2, 1), (4, 0)]
    assert discrete_frechet_distance(a, b) >= hausdorff_distance(a, b)


def _full_matrix_frechet(a, b):
    """Independent full-matrix recurrence oracle for randomized testing."""
    table = [[0.0] * len(b) for _ in a]
    for i in range(len(a)):
        for j in range(len(b)):
            d = math.dist(a[i], b[j])
            if i == j == 0:
                table[i][j] = d
            elif i == 0:
                table[i][j] = max(table[i][j - 1], d)
            elif j == 0:
                table[i][j] = max(table[i - 1][j], d)
            else:
                table[i][j] = max(
                    min(table[i - 1][j], table[i - 1][j - 1],
                        table[i][j - 1]), d
                )
    return table[-1][-1]


def test_seeded_random_frechet_matches_full_matrix_oracle():
    rng = random.Random(20261115)
    for _ in range(250):
        a = [(rng.randrange(-8, 9), rng.randrange(-8, 9))
             for _ in range(rng.randrange(1, 9))]
        b = [(rng.randrange(-8, 9), rng.randrange(-8, 9))
             for _ in range(rng.randrange(1, 9))]
        assert discrete_frechet_distance(a, b) == pytest.approx(
            _full_matrix_frechet(a, b)
        )


@pytest.mark.parametrize("fn,args", [
    (directed_hausdorff, ([], [(0, 0)])),
    (hausdorff_distance, ([(0, 0)], [])),
    (discrete_frechet_distance, ([(0, 0)], [])),
    (discrete_frechet_distance, ([], [(0, 0)])),
])
def test_empty_curves_are_rejected(fn, args):
    with pytest.raises(ValueError, match="at least one"):
        fn(*args)


@pytest.mark.parametrize("bad", [(float("nan"), 0), (0, float("inf"))])
def test_non_finite_coordinates_are_rejected(bad):
    with pytest.raises(ValueError, match="finite"):
        hausdorff_distance([(0, 0), bad], [(1, 1)])
