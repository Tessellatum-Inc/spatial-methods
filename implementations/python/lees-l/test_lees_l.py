import math
import pytest

from lees_l import lees_l, row_standardize


def test_two_variable_lags_and_statistic_hand_calculation():
    w = [[0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0]]
    result = lees_l([1, 2, 3, 4], [2, 4, 6, 8], w)
    assert result["spatial_lag_x"] == pytest.approx([3, 2, 3, 2])
    assert result["spatial_lag_y"] == pytest.approx([6, 4, 6, 4])
    assert result["L"] == pytest.approx(0.2)


def test_reversing_variable_order_preserves_global_lee_l():
    w = [[0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0]]
    xy = lees_l([1, 2, 4, 3], [4, 1, 3, 2], w)["L"]
    yx = lees_l([4, 1, 3, 2], [1, 2, 4, 3], w)["L"]
    assert xy == pytest.approx(yx)


def test_positive_association_for_identical_spatial_patterns():
    w = [[0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0]]
    result = lees_l([1, 2, 4, 3], [1, 2, 4, 3], w)
    assert result["L"] > 0
    assert result["spatial_smoothing_scalar_x"] >= 0
    assert result["spatial_smoothing_scalar_y"] >= 0


def test_negative_association_when_smoothed_patterns_reverse():
    w = [[0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0]]
    result = lees_l([1, 2, 4, 3], [4, 3, 1, 2], w)
    assert result["L"] < 0


def test_row_standardization():
    assert row_standardize([[0, 2], [3, 0]]) == [[0, 1], [1, 0]]


@pytest.mark.parametrize("x,y,w", [
    ([1, 1], [1, 2], [[0, 1], [1, 0]]),
    ([1, 2], [2, 3], [[0, 0], [1, 0]]),
    ([1, 2], [2, 3], [[1, 1], [1, 0]]),
    ([1, 2], [2, 3], [[0, float("nan")], [1, 0]]),
    ([1, 2], [2, 3], [[0, -1], [1, 0]]),
    ([1, 2], [2], [[0, 1], [1, 0]]),
    ([1, 2], [2, 3], [[0, 1]]),
])
def test_invalid_inputs_raise(x, y, w):
    with pytest.raises(ValueError):
        lees_l(x, y, w)


def test_result_is_finite():
    w = [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
    result = lees_l([1, 3, 2], [4, 1, 2], w)
    assert math.isfinite(result["L"])
