import numpy as np
import pytest
from whittaker import whittaker_smooth


def test_second_order_penalty_preserves_linear_trend():
    y = 3.0 + 2.0 * np.arange(12)
    np.testing.assert_allclose(whittaker_smooth(y, lam=100), y, atol=1e-9)


def test_constant_sequence_is_preserved():
    np.testing.assert_allclose(whittaker_smooth(np.full(8, 4.5), lam=25), 4.5)


def test_penalty_smooths_an_impulse():
    y = np.zeros( nine := 9)
    y[4] = 10
    result = whittaker_smooth(y, lam=20)
    assert result[4] < y[4]
    assert result[4] > result[3] > result[2]
    assert np.all(result >= 0)


def test_missing_observations_are_omitted_from_data_term():
    y = np.array([1., 2., np.nan, 4., 5.])
    result = whittaker_smooth(y, lam=10)
    assert np.isfinite(result).all()
    assert result[2] == pytest.approx(3.0, abs=0.15)


def test_custom_weights_and_validation():
    y = np.array([0., 10., 0., 10., 0.])
    result = whittaker_smooth(y, lam=5, weights=[1, .1, 1, .1, 1])
    assert np.isfinite(result).all()
    with pytest.raises(ValueError, match="non-negative"):
        whittaker_smooth(y, weights=[1, 1, -1, 1, 1])
    with pytest.raises(ValueError, match="order"):
        whittaker_smooth(y, order=5)
    with pytest.raises(ValueError, match="positive"):
        whittaker_smooth([np.nan, np.nan, 1.], lam=10)
