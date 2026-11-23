import math
import pytest
from optical_retrieval import (
    stumpf_log_ratio, fit_stumpf_bathymetry, predict_stumpf_bathymetry,
    oc4v4_chlorophyll, OC4V4_COEFFICIENTS,
)

def test_stumpf_log_ratio_matches_definition():
    actual = stumpf_log_ratio([0.02], [0.01])
    assert actual == pytest.approx([math.log(20) / math.log(10)])

def test_stumpf_calibration_recovers_linear_depth_relation():
    blue = [0.010, 0.015, 0.020, 0.030]
    green = [0.020, 0.020, 0.020, 0.020]
    ratios = stumpf_log_ratio(blue, green)
    depths = [2.5 * x - 1.2 for x in ratios]
    model = fit_stumpf_bathymetry(blue, green, depths)
    assert model["slope"] == pytest.approx(2.5)
    assert model["intercept"] == pytest.approx(-1.2)
    assert predict_stumpf_bathymetry(blue, green, model) == pytest.approx(depths)

def test_stumpf_uses_caller_selected_log_scale_constant():
    result = stumpf_log_ratio([0.02], [0.01], n=200)
    assert result == pytest.approx([math.log(4) / math.log(2)])

def test_oc4v4_uses_maximum_blue_to_green_ratio_and_published_coefficients():
    expected_x = math.log10(0.02 / 0.005)
    expected_log_chl = sum(c * expected_x**i for i, c in enumerate(OC4V4_COEFFICIENTS))
    actual = oc4v4_chlorophyll([0.01], [0.02], [0.015], [0.005])
    assert actual == pytest.approx([10**expected_log_chl])

def test_oc4v4_output_increases_for_stronger_blue_green_ratio_in_test_range():
    low = oc4v4_chlorophyll([0.006], [0.006], [0.006], [0.006])[0]
    high = oc4v4_chlorophyll([0.02], [0.02], [0.02], [0.006])[0]
    assert high < low

def test_calibration_rejects_constant_predictor_and_mismatched_inputs():
    with pytest.raises(ValueError):
        fit_stumpf_bathymetry([0.01, 0.01], [0.02, 0.02], [1, 2])
    with pytest.raises(ValueError):
        stumpf_log_ratio([0.01], [0.01, 0.02])

@pytest.mark.parametrize("blue,green", [([0], [0.1]), ([-0.1], [0.1]), ([0.1], [0.001])])
def test_stumpf_rejects_nonpositive_or_singular_reflectance(blue, green):
    with pytest.raises(ValueError):
        stumpf_log_ratio(blue, green)

def test_oc4v4_rejects_nonpositive_or_mismatched_bands():
    with pytest.raises(ValueError):
        oc4v4_chlorophyll([0.01], [0.01], [0.01], [0])
    with pytest.raises(ValueError):
        oc4v4_chlorophyll([0.01, 0.02], [0.01], [0.01], [0.01])
