import math

import pytest

from tissot import tissot_indicatrix


R = 6_371_008.8


def spherical_mercator(lon, lat):
    phi = math.radians(lat)
    return R * math.radians(lon), R * math.log(math.tan(math.pi / 4 + phi / 2))


def equirectangular(lon, lat):
    return R * math.radians(lon), R * math.radians(lat)


def test_mercator_is_conformal_with_expected_scale():
    result = tissot_indicatrix(spherical_mercator, 12, 30)
    expected = 1 / math.cos(math.radians(30))
    assert result["major_scale"] == pytest.approx(expected, rel=1e-8)
    assert result["minor_scale"] == pytest.approx(expected, rel=1e-8)
    assert result["area_scale"] == pytest.approx(expected ** 2, rel=1e-8)
    assert result["angular_distortion_degrees"] == pytest.approx(0, abs=1e-6)


def test_equirectangular_has_known_parallel_scale():
    result = tissot_indicatrix(equirectangular, 0, 30)
    assert result["major_scale"] == pytest.approx(1 / math.cos(math.radians(30)), rel=1e-8)
    assert result["minor_scale"] == pytest.approx(1.0, rel=1e-8)
    assert result["area_scale"] == pytest.approx(1 / math.cos(math.radians(30)), rel=1e-8)
    assert result["angular_distortion_degrees"] > 0


def test_identity_local_projection_is_unit_scale():
    def identity(lon, lat):
        return R * math.radians(lon), R * math.radians(lat)
    result = tissot_indicatrix(identity, 0, 0)
    assert result["major_scale"] == pytest.approx(1)
    assert result["minor_scale"] == pytest.approx(1)
    assert result["area_scale"] == pytest.approx(1)


@pytest.mark.parametrize("kwargs", [
    {"latitude": 90},
    {"latitude": -90},
    {"latitude": float("nan")},
    {"earth_radius": 0},
    {"step_degrees": 0},
    {"step_degrees": 1},
])
def test_invalid_parameters_rejected(kwargs):
    args = {"longitude": 0, "latitude": 0, "earth_radius": R, "step_degrees": 1e-5}
    args.update(kwargs)
    with pytest.raises(ValueError):
        tissot_indicatrix(equirectangular, **args)


def test_nonfinite_projection_output_rejected():
    with pytest.raises(ValueError):
        tissot_indicatrix(lambda lon, lat: (float("nan"), lat), 0, 0)
