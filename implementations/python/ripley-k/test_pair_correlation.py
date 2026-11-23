import math
import random
import numpy as np
import pytest
from pair_correlation import pair_correlation


def brute_force(points, bounds, edges, correction):
    xmin, xmax, ymin, ymax = bounds
    n = len(points)
    area = (xmax - xmin) * (ymax - ymin)
    weighted = np.zeros(len(edges) - 1)
    counts = np.zeros(len(edges) - 1, dtype=int)
    for i in range(n):
        for j in range(i + 1, n):
            dx = abs(points[j][0] - points[i][0])
            dy = abs(points[j][1] - points[i][1])
            distance = math.hypot(dx, dy)
            index = np.searchsorted(edges, distance, side="right") - 1
            if distance == edges[-1]:
                index = len(edges) - 2
            if 0 <= index < len(weighted):
                counts[index] += 1
                weight = 1.0
                if correction == "translation":
                    weight = area / ((xmax - xmin - dx) * (ymax - ymin - dy))
                weighted[index] += weight
    annuli = math.pi * (np.asarray(edges[1:]) ** 2 - np.asarray(edges[:-1]) ** 2)
    return (2 * area / (n * (n - 1)) * weighted) / annuli, counts


def test_unweighted_estimator_matches_independent_oracle():
    points = [(1, 1), (2, 1), (1, 3), (4, 4), (5, 2)]
    edges = [0, 1.5, 3, 5]
    result = pair_correlation(points, bounds=(0, 6, 0, 6), bin_edges=edges,
                              edge_correction="none")
    expected, counts = brute_force(points, (0, 6, 0, 6), edges, "none")
    assert result.g_values == pytest.approx(expected)
    assert result.pair_counts.tolist() == counts.tolist()
    assert result.radii.tolist() == pytest.approx([0.75, 2.25, 4.0])


def test_translation_correction_matches_independent_oracle():
    points = [(0.5, 0.5), (1.2, 0.8), (2.5, 1.5), (3.5, 3.0), (4.5, 1.0)]
    edges = [0, 1, 2, 4, 6]
    result = pair_correlation(points, bounds=(0, 5, 0, 4), bin_edges=edges)
    expected, counts = brute_force(points, (0, 5, 0, 4), edges, "translation")
    assert result.g_values == pytest.approx(expected)
    assert result.pair_counts.tolist() == counts.tolist()


def test_translation_estimator_is_invariant_to_joint_window_translation():
    points = np.array([(1, 1), (2, 1), (1, 2), (3, 3)], dtype=float)
    shifted = points + np.array([100, -50])
    edges = [0, 1, 2, 4]
    first = pair_correlation(points, bounds=(0, 4, 0, 4), bin_edges=edges)
    second = pair_correlation(shifted, bounds=(100, 104, -50, -46), bin_edges=edges)
    assert second.g_values == pytest.approx(first.g_values)
    assert second.pair_counts.tolist() == first.pair_counts.tolist()


def test_seeded_random_patterns_match_pairwise_oracle():
    rng = random.Random(20261115)
    points = [(rng.uniform(0.1, 19.9), rng.uniform(0.1, 9.9)) for _ in range(85)]
    edges = np.linspace(0, 8, 17)
    for correction in ("none", "translation"):
        result = pair_correlation(points, bounds=(0, 20, 0, 10),
                                  bin_edges=edges, edge_correction=correction)
        expected, counts = brute_force(points, (0, 20, 0, 10), edges, correction)
        assert result.g_values == pytest.approx(expected)
        assert result.pair_counts.tolist() == counts.tolist()


def test_last_bin_includes_exact_final_edge():
    result = pair_correlation([(1, 1), (3, 1)], bounds=(0, 4, 0, 4),
                              bin_edges=[0, 1, 2], edge_correction="none")
    assert result.pair_counts.tolist() == [0, 1]


@pytest.mark.parametrize("edges", [[0], [1, 1], [2, 1], [-1, 2], [0, float("inf")]])
def test_invalid_bin_edges_rejected(edges):
    with pytest.raises(ValueError):
        pair_correlation([(1, 1), (2, 2)], bounds=(0, 4, 0, 4), bin_edges=edges)


def test_invalid_window_points_and_correction_rejected():
    with pytest.raises(ValueError):
        pair_correlation([(1, 1)], bounds=(0, 4, 0, 4), bin_edges=[0, 1])
    with pytest.raises(ValueError):
        pair_correlation([(5, 1), (1, 2)], bounds=(0, 4, 0, 4), bin_edges=[0, 1])
    with pytest.raises(ValueError):
        pair_correlation([(1, 1), (2, 2)], bounds=(0, 4, 0, 4),
                         bin_edges=[0, 1], edge_correction="isotropic")


def test_zero_overlap_translation_pair_is_rejected():
    with pytest.raises(ValueError, match="zero-overlap"):
        pair_correlation([(0, 1), (4, 3)], bounds=(0, 4, 0, 4),
                         bin_edges=[0, 6])
