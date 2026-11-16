import numpy as np
import pytest
from channel_morphometry import chi_coordinate, slope_area_relationship, detect_knickpoints


def test_chi_coordinate_matches_constant_area_and_trapezoid():
    x = np.array([0., 10., 20.])
    area = np.array([100., 100., 100.])
    np.testing.assert_allclose(chi_coordinate(x, area, reference_area=100, concavity=.5), x)
    result = chi_coordinate(x, [100, 400, 400], reference_area=100, concavity=.5)
    assert result[1] == pytest.approx(7.5)
    assert result[2] > result[1]


def test_chi_rejects_nonmonotonic_distance_and_invalid_area():
    with pytest.raises(ValueError):
        chi_coordinate([0, 2, 1], [1, 2, 3], reference_area=1)
    with pytest.raises(ValueError):
        chi_coordinate([0, 1], [1, 0], reference_area=1)


def test_slope_area_fit_recovers_power_law_exponent():
    area = np.array([1., 2., 4., 8., 16., 32.])
    segment_area = 0.5 * (area[:-1] + area[1:])
    slope = 3.0 * segment_area ** -0.5
    distance = np.arange(area.size, dtype=float)
    elevation = np.concatenate(([0.], -np.cumsum(slope)))
    result = slope_area_relationship(distance, elevation, area)
    assert result["area_exponent"] == pytest.approx(-.5, abs=.03)
    assert result["r_squared"] > .99


def test_knickpoint_detection_reports_signed_chord_residual():
    x = np.arange(7, dtype=float)
    z = np.array([10, 8, 9, 7, 2, 1, 0], dtype=float)
    result = detect_knickpoints(x, z, window_size=5, min_relief=1)
    assert result["knickpoint"][2]
    assert result["kind"][2] == "convex-up"
    assert np.isnan(result["residual"][:2]).all()
    assert np.isnan(result["residual"][-2:]).all()


def test_knickpoint_contracts():
    with pytest.raises(ValueError):
        detect_knickpoints([0, 1], [1, 2])
    with pytest.raises(ValueError):
        detect_knickpoints([0, 1, 2], [1, 2, 3], window_size=4)
