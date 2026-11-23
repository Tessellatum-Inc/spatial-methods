import numpy as np
import pytest
from knox_test import knox_test


def test_detects_designed_space_time_clustering_reproducibly():
    xy = np.array([[0., 0.], [1., 0.], [10., 0.], [11., 0.], [30., 0.]])
    times = np.array([0., .1, 10., 10.1, 30.])
    a = knox_test(xy, times, spatial_threshold=1.5, temporal_threshold=1.,
                  permutations=499, random_state=9)
    b = knox_test(xy, times, spatial_threshold=1.5, temporal_threshold=1.,
                  permutations=499, random_state=9)
    assert a["observed_pairs"] == 2
    assert 0 < a["p_value"] <= 1
    assert np.array_equal(a["null_counts"], b["null_counts"])


def test_constant_times_have_no_permutation_variation():
    xy = np.array([[0., 0.], [1., 0.], [10., 0.]])
    result = knox_test(xy, [1., 1., 1.], spatial_threshold=2,
                       temporal_threshold=1, permutations=20, random_state=2)
    assert result["observed_pairs"] == 1
    assert np.all(result["null_counts"] == 1)
    assert result["p_value"] == 1
    assert np.isnan(result["z_score"])


@pytest.mark.parametrize("kwargs", [
    {"spatial_threshold": 0}, {"temporal_threshold": -1}, {"permutations": 0},
])
def test_invalid_controls_raise(kwargs):
    base = {"spatial_threshold": 1, "temporal_threshold": 1, "permutations": 5}
    base.update(kwargs)
    with pytest.raises(ValueError):
        knox_test([[0, 0], [1, 0]], [0, 1], **base)


def test_invalid_coordinate_and_time_shapes_raise():
    with pytest.raises(ValueError):
        knox_test([[0, 0]], [0], spatial_threshold=1, temporal_threshold=1)
    with pytest.raises(ValueError):
        knox_test([[0, 0], [1, 0]], [0], spatial_threshold=1, temporal_threshold=1)
