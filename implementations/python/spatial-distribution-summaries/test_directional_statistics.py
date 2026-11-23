import math
import numpy as np
import pytest

from directional_statistics import (
    circular_summary, kuiper_uniformity_test, rayleigh_test,
    rose_histogram, von_mises_density, watson_u2_uniformity_test,
)


def test_circular_summary_handles_wraparound_and_returns_radians():
    result = circular_summary([math.radians(359), math.radians(1)])
    assert min(result["mean_direction"], 2*math.pi-result["mean_direction"]) < 1e-10
    assert result["mean_resultant_length"] == pytest.approx(math.cos(math.radians(1)))
    assert result["n"] == 2


def test_circular_summary_marks_mean_undefined_for_balanced_opposites():
    result = circular_summary([0, math.pi])
    assert math.isnan(result["mean_direction"])
    assert result["mean_resultant_length"] == pytest.approx(0, abs=1e-15)


def test_rayleigh_test_detects_concentrated_bearings_and_rejects_small_n():
    concentrated = rayleigh_test(np.linspace(-0.05, 0.05, 30))
    assert concentrated["statistic_z"] > 25
    assert concentrated["pvalue"] < 1e-8
    with pytest.raises(ValueError, match="three"):
        rayleigh_test([0, 1])


def test_kuiper_statistic_is_rotation_invariant():
    angles = np.array([0.1, 0.2, 0.3, 1.2, 2.4, 4.8, 5.1])
    a = kuiper_uniformity_test(angles)
    b = kuiper_uniformity_test(angles + 2.345)
    assert a["statistic_v"] == pytest.approx(b["statistic_v"], abs=1e-12)
    assert a["pvalue"] == pytest.approx(b["pvalue"], abs=1e-12)
    assert 0 <= a["pvalue"] <= 1


def test_kuiper_rejects_single_observation():
    with pytest.raises(ValueError, match="two"):
        kuiper_uniformity_test([0])


def test_von_mises_density_is_normalized_and_peaks_at_mean():
    angles = np.linspace(0, 2*math.pi, 20001)
    density = von_mises_density(angles, mean_direction=1.2, concentration=2.5)
    integral = np.trapezoid(density, angles)
    assert integral == pytest.approx(1.0, abs=2e-4)
    assert density[np.argmin(np.abs(angles-1.2))] == pytest.approx(density.max())


def test_uniform_von_mises_is_constant():
    density = von_mises_density([0, 1, 2, 3], concentration=0)
    np.testing.assert_allclose(density, 1/(2*math.pi))


def test_rose_histogram_counts_wraparound_and_weights():
    result = rose_histogram([0, 2*math.pi, math.pi/2, math.pi], bins=4,
                            weights=[1, 2, 3, 4])
    assert result["counts"].tolist() == [3, 3, 4, 0]
    assert result["total_weight"] == 10
    assert result["edges"].tolist() == pytest.approx(np.linspace(0, 2*math.pi, 5))


@pytest.mark.parametrize("angles", [[], [[0, 1]], [0, float("nan")], [float("inf")]])
def test_invalid_angle_inputs_are_rejected(angles):
    with pytest.raises(ValueError, match="angles"):
        circular_summary(angles)


def test_invalid_histogram_and_density_parameters_are_rejected():
    with pytest.raises(ValueError, match="bins"):
        rose_histogram([0, 1], bins=0)
    with pytest.raises(ValueError, match="weights"):
        rose_histogram([0, 1], weights=[1])
    with pytest.raises(ValueError, match="concentration"):
        von_mises_density([0, 1], concentration=-1)
    with pytest.raises(ValueError, match="finite"):
        von_mises_density([0, 1], mean_direction=float("nan"))


def test_watson_u2_detects_concentration_and_is_rotation_invariant():
    angles = np.linspace(-0.04, 0.04, 40)
    a = watson_u2_uniformity_test(angles)
    b = watson_u2_uniformity_test(angles + 2.17)
    assert a["statistic_u2"] == pytest.approx(b["statistic_u2"], abs=1e-12)
    assert a["pvalue"] == pytest.approx(b["pvalue"], abs=1e-12)
    assert a["pvalue"] < 1e-6


def test_watson_u2_uniform_grid_has_small_statistic_and_rejects_singleton():
    result = watson_u2_uniformity_test(2*math.pi*(np.arange(20)+0.5)/20)
    assert result["statistic_u2"] == pytest.approx(1/(12*20))
    with pytest.raises(ValueError, match="two"):
        watson_u2_uniformity_test([0])
