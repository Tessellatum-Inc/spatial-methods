import pytest
from kalman import kalman_local_level, rts_local_level


def test_filter_tracks_level_and_returns_nonnegative_variance():
    means, variances = kalman_local_level([1, 1.2, 0.9, 1.1],
                                          process_variance=0.01,
                                          observation_variance=0.1)
    assert len(means) == len(variances) == 4
    assert all(v >= 0 for v in variances)
    assert means[-1] == pytest.approx(1.0, abs=0.2)


def test_missing_observation_only_performs_prediction():
    means, variances = kalman_local_level([None], process_variance=0.2,
                                          observation_variance=0.1,
                                          initial_mean=0, initial_variance=0)
    assert means == [0]
    assert variances == [0.2]


def test_rts_smoother_revises_earlier_estimates():
    filtered, _ = kalman_local_level([0, 0, 5], process_variance=0.1,
                                     observation_variance=0.2)
    smoothed, variances = rts_local_level([0, 0, 5], process_variance=0.1,
                                          observation_variance=0.2)
    assert smoothed[0] > filtered[0]
    assert all(v >= 0 for v in variances)


def test_invalid_variances_rejected():
    with pytest.raises(ValueError):
        kalman_local_level([1, 2], process_variance=-1,
                           observation_variance=1)
    with pytest.raises(ValueError):
        rts_local_level([1, 2], process_variance=1,
                        observation_variance=0)
