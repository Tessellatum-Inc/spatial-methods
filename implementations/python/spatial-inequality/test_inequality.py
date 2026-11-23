import math
import pytest
from inequality import (
    weighted_gini, theil_t, theil_l, spatial_entropy,
    dissimilarity_index, exposure_indices,
)

def test_gini_known_two_group_and_equality_cases():
    assert weighted_gini([1,1,1]) == pytest.approx(0)
    assert weighted_gini([0,0,1,1]) == pytest.approx(0.5)
    assert weighted_gini([0,0,0]) == 0

def test_weighted_gini_and_scale_invariance():
    assert weighted_gini([0,1],[1,3]) == pytest.approx(0.25)
    assert weighted_gini([2,4,8],[1,2,3]) == pytest.approx(weighted_gini([20,40,80],[1,2,3]))

def test_theil_indices_are_zero_for_equality_and_positive_for_inequality():
    assert theil_t([5,5,5]) == pytest.approx(0)
    assert theil_l([5,5,5]) == pytest.approx(0)
    assert theil_t([1,3]) > 0
    assert theil_l([1,3]) > 0

def test_theil_t_matches_known_two_area_value():
    expected = 0.5 * 0.5 * math.log(0.5) + 0.5 * 1.5 * math.log(1.5)
    assert theil_t([1,3]) == pytest.approx(expected)

def test_theil_l_matches_known_two_area_value():
    expected = 0.5 * math.log(2/1) + 0.5 * math.log(2/3)
    assert theil_l([1,3]) == pytest.approx(expected)

def test_theil_t_supports_zero_values_but_theil_l_rejects_them():
    assert math.isfinite(theil_t([0,1,3]))
    with pytest.raises(ValueError):
        theil_l([0,1,3])

def test_spatial_entropy_is_maximum_for_equal_populations():
    result = spatial_entropy([10,10,10,10])
    assert result["entropy"] == pytest.approx(math.log(4))
    assert result["normalized_entropy"] == pytest.approx(1)

def test_spatial_entropy_is_zero_for_single_area_concentration():
    result = spatial_entropy([100,0,0])
    assert result["entropy"] == pytest.approx(0)
    assert result["normalized_entropy"] == pytest.approx(0)

def test_spatial_entropy_can_omit_normalized_value():
    result = spatial_entropy([1,3], normalize=False)
    assert result["normalized_entropy"] is None
    assert result["entropy"] == pytest.approx(-(0.25*math.log(0.25)+0.75*math.log(0.75)))

def test_dissimilarity_index_known_value_and_invariance():
    assert dissimilarity_index([80,20],[20,80]) == pytest.approx(0.6)
    assert dissimilarity_index([8,2],[2,8]) == pytest.approx(0.6)

def test_exposure_indices_sum_to_one_for_two_groups():
    result = exposure_indices([80,20],[20,80])
    assert result["isolation"] == pytest.approx(0.68)
    assert result["interaction"] == pytest.approx(0.32)
    assert result["isolation"] + result["interaction"] == pytest.approx(1)

def test_exposure_indices_when_other_group_absent():
    result = exposure_indices([4,6],[0,0])
    assert result["isolation"] == pytest.approx(1)
    assert result["interaction"] == pytest.approx(0)

@pytest.mark.parametrize("values,weights",[
    ([],None), ([-1,2],None), ([1,float("nan")],None),
    ([1,2],[1]), ([1,2],[-1,2]), ([1,2],[0,0]),
])
def test_gini_rejects_invalid_values_or_weights(values,weights):
    with pytest.raises(ValueError):
        weighted_gini(values,weights)

def test_theil_and_entropy_reject_invalid_populations():
    with pytest.raises(ValueError): theil_t([-1,2])
    with pytest.raises(ValueError): spatial_entropy([0,0])
    with pytest.raises(ValueError): spatial_entropy([1,float("inf")])

def test_dissimilarity_rejects_zero_group_total_and_length_mismatch():
    with pytest.raises(ValueError): dissimilarity_index([0,0],[1,2])
    with pytest.raises(ValueError): dissimilarity_index([1,2],[1])

def test_exposure_rejects_zero_group_a_and_length_mismatch():
    with pytest.raises(ValueError): exposure_indices([0,0],[1,2])
    with pytest.raises(ValueError): exposure_indices([1,2],[1])


def test_weighted_theil_indices_are_scale_invariant():
    values = [1, 3]
    weights = [1, 3]
    assert theil_t(values, weights) == pytest.approx(theil_t([10, 30], weights))
    assert theil_l(values, weights) == pytest.approx(theil_l([10, 30], weights))
