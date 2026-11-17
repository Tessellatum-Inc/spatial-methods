import numpy as np
import pytest
from dtw import dtw, time_weighted_dtw


def test_identical_sequences_zero():
    x = [[0., 1.], [2., 3.], [4., 5.]]
    assert dtw(x, x) == 0.0


def test_repeated_observation_warping_and_path():
    score, path = dtw([1., 2., 3.], [1., 2., 2., 3.], return_path=True)
    assert score == 0.0
    assert path[0] == (0, 0) and path[-1] == (2, 3)
    assert len(path) >= 4


def test_window_validation():
    assert dtw([0., 1.], [0., 1.], window=0) == 0.0
    with pytest.raises(ValueError):
        dtw([0.], [0., 1.], window=0)


def test_feature_dimension_validation():
    with pytest.raises(ValueError):
        dtw([[1., 2.]], [[1.]])


def test_time_penalty_increases_for_shifted_dates():
    a = [0., 1., 2.]
    plain = dtw(a, a)
    aligned = time_weighted_dtw(a, a, [0,1,2], [0,1,2])
    shifted = time_weighted_dtw(a, a, [0,1,2], [10,11,12])
    assert aligned > plain
    assert shifted > aligned


def test_twdtw_multivariate_path():
    x = [[0., 1.], [1., 2.]]
    score, path = time_weighted_dtw(x, x, [0,1], [0,1], return_path=True)
    assert score > 0 and path[0] == (0,0) and path[-1] == (1,1)


@pytest.mark.parametrize("times", [[0,2,1], [0,np.nan], [0]])
def test_bad_timestamps(times):
    with pytest.raises(ValueError):
        time_weighted_dtw([1.,2.], [1.,2.], times, [0,1])


def test_bad_penalty_parameters():
    with pytest.raises(ValueError):
        time_weighted_dtw([1.], [1.], [0], [0], alpha=0)
