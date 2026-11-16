import math
import pytest
from trend_tests import mann_kendall, sen_slope

def test_mann_kendall_detects_strictly_increasing_series():
    result = mann_kendall([1,2,3,4,5])
    assert result["s"] == 10
    assert result["tau_b"] == pytest.approx(1)
    assert result["z"] > 0
    assert result["p_value_two_sided"] < 0.1

def test_mann_kendall_detects_strictly_decreasing_series():
    result = mann_kendall([5,4,3,2,1])
    assert result["s"] == -10
    assert result["tau_b"] == pytest.approx(-1)
    assert result["z"] < 0

def test_mann_kendall_tie_corrected_variance():
    result = mann_kendall([1,1,2,2,3])
    assert result["variance_s"] == pytest.approx(264/18)
    assert result["s"] == 8

def test_constant_series_has_neutral_test_result():
    result = mann_kendall([3,3,3,3])
    assert result["variance_s"] == 0
    assert result["z"] == 0
    assert result["p_value_two_sided"] == 1
    assert result["tau_b"] == 0

def test_sen_slope_recovers_linear_trend_and_intercept():
    result = sen_slope([3,5,7,9])
    assert result["slope"] == pytest.approx(2)
    assert result["intercept"] == pytest.approx(3)
    assert result["pair_count"] == 6

def test_sen_slope_uses_irregular_time_spacing():
    result = sen_slope([2,6,14], times=[0,2,6])
    assert result["slope"] == pytest.approx(2)
    assert result["intercept"] == pytest.approx(2)

def test_mann_kendall_is_invariant_to_strictly_increasing_affine_transform():
    a = mann_kendall([1,4,2,8,7])
    b = mann_kendall([101,104,102,108,107])
    assert a["s"] == b["s"]
    assert a["p_value_two_sided"] == pytest.approx(b["p_value_two_sided"])

@pytest.mark.parametrize("values", [[], [1], [1,float("nan")], [True,2]])
def test_invalid_series_are_rejected(values):
    with pytest.raises(ValueError):
        mann_kendall(values)

def test_invalid_sen_time_axis_is_rejected():
    with pytest.raises(ValueError):
        sen_slope([1,2,3], times=[0,1])
    with pytest.raises(ValueError):
        sen_slope([1,2,3], times=[0,2,1])
