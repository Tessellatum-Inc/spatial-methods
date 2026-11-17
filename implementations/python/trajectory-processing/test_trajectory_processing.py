import numpy as np
import pytest

from trajectory_processing import (
    detect_stay_points,
    douglas_peucker,
    douglas_peucker_indices,
    dtw_distance,
    lcss_similarity,
)


def test_stay_point_detects_duration_and_reports_centroid_and_indices():
    points = [(0, 0), (1, 0), (0, 1), (10, 0), (11, 0)]
    times = [0, 10, 20, 30, 40]
    stays = detect_stay_points(points, times, max_distance=2, min_duration=15)
    assert len(stays) == 1
    assert stays[0]["start_index"] == 0
    assert stays[0]["end_index"] == 2
    assert stays[0]["duration"] == 20
    np.testing.assert_allclose(stays[0]["location"], [1 / 3, 1 / 3])


def test_stay_point_requires_both_spatial_and_temporal_thresholds():
    points = [(0, 0), (1, 0), (4, 0), (8, 0)]
    stays = detect_stay_points(points, [0, 5, 10, 15],
                               max_distance=1.5, min_duration=20)
    assert stays == []


def test_douglas_peucker_preserves_endpoints_and_removes_collinear_points():
    points = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
    indices = douglas_peucker_indices(points, tolerance=0)
    np.testing.assert_array_equal(indices, [0, 4])
    np.testing.assert_allclose(douglas_peucker(points, tolerance=0), [[0, 0], [4, 0]])


def test_douglas_peucker_retains_corner_when_deviation_exceeds_tolerance():
    points = [(0, 0), (1, 0), (2, 2), (3, 0), (4, 0)]
    simplified = douglas_peucker_indices(points, tolerance=0.5)
    assert 2 in simplified
    assert simplified[0] == 0 and simplified[-1] == 4


def test_dtw_identity_and_known_alignment_cost():
    a = [(0, 0), (1, 0), (2, 0)]
    assert dtw_distance(a, a) == pytest.approx(0)
    assert dtw_distance([(0, 0), (2, 0)], [(0, 0), (1, 0), (2, 0)]) == pytest.approx(0)


def test_dtw_window_matches_unconstrained_when_window_is_wide():
    a = [(0, 0), (1, 1), (2, 0)]
    b = [(0, 0), (1, 0), (2, 0)]
    assert dtw_distance(a, b, window=3) == pytest.approx(dtw_distance(a, b))


def test_lcss_similarity_is_exact_for_matching_and_nonmatching_sequences():
    a = [(0, 0), (1, 0), (2, 0), (3, 0)]
    b = [(0, 0), (1, 0), (9, 9), (3, 0)]
    assert lcss_similarity(a, a, epsilon=0) == pytest.approx(1)
    assert lcss_similarity(a, b, epsilon=0) == pytest.approx(0.75)


def test_lcss_delta_limits_temporal_warping():
    a = [(0, 0), (1, 0), (2, 0), (3, 0)]
    b = [(9, 9), (0, 0), (1, 0), (2, 0), (3, 0)]
    assert lcss_similarity(a, b, epsilon=0, delta=0) < 1
    assert lcss_similarity(a, b, epsilon=0, delta=1) == pytest.approx(1)


@pytest.mark.parametrize("points,times", [
    ([], []), ([(0, 0), (1, 1)], [0]), ([(0, 0), (float("nan"), 1)], [0, 1]),
    ([(0, 0), (1, 1)], [1, 0]),
])
def test_stay_point_rejects_invalid_inputs(points, times):
    with pytest.raises(ValueError):
        detect_stay_points(points, times, max_distance=1, min_duration=1)


def test_douglas_peucker_rejects_invalid_tolerance():
    with pytest.raises(ValueError):
        douglas_peucker([(0, 0), (1, 1)], tolerance=-1)


def test_dtw_and_lcss_reject_invalid_controls():
    with pytest.raises(ValueError):
        dtw_distance([(0, 0)], [(0, 0), (1, 1)], window=0)
    with pytest.raises(ValueError):
        lcss_similarity([(0, 0)], [(0, 0)], epsilon=-1)
    with pytest.raises(ValueError):
        lcss_similarity([(0, 0)], [(0, 0)], epsilon=1, delta=-1)
