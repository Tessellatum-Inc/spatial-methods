import pytest
from theil_sen import theil_sen

def test_exact_linear_trend():
    result=theil_sen([0,1,2,3],[2,5,8,11])
    assert result["slope"]==3
    assert result["intercept"]==2
    assert result["pair_count"]==6

def test_robust_to_one_extreme_observation():
    result=theil_sen([0,1,2,3,4],[0,1,2,3,1000])
    assert result["slope"]==1
    assert result["intercept"]==0

def test_irregular_time_uses_elapsed_time():
    result=theil_sen([0,2,5],[1,5,11])
    assert result["slope"]==2
    assert result["intercept"]==1

def test_duplicate_times_are_excluded_from_slope_pairs():
    result=theil_sen([0,0,1],[1,3,5])
    assert result["pair_count"]==2
    assert result["slope"]==3

@pytest.mark.parametrize("times,values",[
    ([1],[2]),([1,1],[2,3]),([1,2],[2]),([1,float("nan")],[2,3])
])
def test_invalid_inputs(times,values):
    with pytest.raises(ValueError):theil_sen(times,values)

from theil_sen import mann_kendall_test

def test_mann_kendall_detects_monotonic_increase_and_decrease():
    increasing=mann_kendall_test([1,2,3,4,5,6,7])
    decreasing=mann_kendall_test([7,6,5,4,3,2,1])
    assert increasing["score"]>0 and increasing["p_value"]<.05
    assert decreasing["score"]<0 and decreasing["p_value"]<.05

def test_mann_kendall_tie_correction_and_constant_series():
    result=mann_kendall_test([1,1,2,2,3,3])
    assert result["variance"]>0
    constant=mann_kendall_test([4,4,4,4,4])
    assert constant["score"]==0 and constant["variance"]==0
    assert constant["p_value"]==1

def test_seasonal_mann_kendall_compares_like_seasons():
    # Each of two seasons increases over three cycles.
    result=mann_kendall_test([1,10,2,11,3,12,4,13],seasonal_period=2)
    assert result["score"]>0
    assert result["pair_count"]==12
    assert result["test"]=="seasonal Mann-Kendall"

def test_mann_kendall_validates_series_and_period():
    with pytest.raises(ValueError,match="finite"):
        mann_kendall_test([1,float("nan"),3])
    with pytest.raises(ValueError,match="seasonal_period"):
        mann_kendall_test([1,2,3],seasonal_period=3)
