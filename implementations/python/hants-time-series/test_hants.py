import math
import numpy as np
import pytest
from hants import hants


def seasonal_series():
    t = np.arange(24, dtype=float)
    y = 5 + 2*np.sin(2*math.pi*t/12) + 0.5*np.cos(4*math.pi*t/12)
    return t, y


def test_hants_rejects_low_outlier_and_recovers_periodic_signal():
    _, y = seasonal_series()
    noisy = y.copy()
    noisy[6] = -10
    r = hants(noisy.tolist(), period=12, harmonics=2, direction="low", low_reject=3)
    assert r["rejected_indices"] == [6] and r["converged"]
    assert np.asarray(r["fitted"]) == pytest.approx(y, abs=1e-9)


def test_hants_preserves_missing_observation_mask():
    _, y = seasonal_series()
    values = y.tolist()
    values[3] = float("nan")
    r = hants(values, period=12, harmonics=2, direction="both", low_reject=.01, high_reject=.01)
    assert r["missing_indices"] == [3] and 3 not in r["valid_indices"]
    assert r["fitted"][3] == pytest.approx(y[3])


def test_hants_can_reject_high_outlier():
    _, y = seasonal_series()
    y[4] += 20
    r = hants(y.tolist(), period=12, harmonics=2, direction="high", high_reject=3)
    assert 4 in r["rejected_indices"]


def test_hants_supports_irregular_time_coordinates():
    t = np.array([0, 1, 2, 4, 5, 6, 8, 9, 10, 12], dtype=float)
    y = 3 + 2*np.sin(2*math.pi*t/12)
    r = hants(y.tolist(), period=12, harmonics=1, times=t.tolist(),
              direction="both", low_reject=.01, high_reject=.01)
    assert r["converged"] and r["fitted"] == pytest.approx(y.tolist(), abs=1e-9)


@pytest.mark.parametrize("kwargs", [
    {"period": 0}, {"period": 12, "harmonics": 0},
    {"period": 12, "direction": "up"}, {"period": 12, "low_reject": -1},
])
def test_hants_rejects_invalid_controls(kwargs):
    with pytest.raises(ValueError):
        hants([1, 2, 3, 4, 5, 6, 7], **kwargs)


def test_hants_rejects_insufficient_or_rank_deficient_observations():
    with pytest.raises(ValueError):
        hants([1, 2, 3, 4], period=12, harmonics=2)
    with pytest.raises(ValueError):
        hants([1, 2, 3, 4, 5, 6, 7], period=12, harmonics=2, times=[0]*7)


def test_hants_reports_iteration_limit_without_claiming_convergence():
    _, y = seasonal_series()
    y[3] = -100
    r = hants(y.tolist(), period=12, harmonics=2, direction="low",
              low_reject=0, max_iterations=1)
    assert r["converged"] is False
