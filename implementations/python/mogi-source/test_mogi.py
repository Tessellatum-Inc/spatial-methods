import numpy as np
import pytest
from mogi import mogi_displacement


def test_vertical_displacement_directly_above_source_matches_analytic_value():
    depth, volume, nu = 3000.0, 2.5e6, 0.25
    result = mogi_displacement(0.0, 0.0, source_depth=depth,
                              volume_change=volume, poisson_ratio=nu)
    expected = (1-nu) * volume / (np.pi * depth**2)
    assert result["east"] == 0.0
    assert result["north"] == 0.0
    assert result["vertical"] == pytest.approx(expected)
    assert result["magnitude"] == pytest.approx(expected)


def test_mogi_horizontal_radial_symmetry_and_vertical_symmetry():
    east = mogi_displacement(1000., 0., source_depth=2500.,
                             volume_change=1e6)
    north = mogi_displacement(0., 1000., source_depth=2500.,
                              volume_change=1e6)
    assert east["east"] == pytest.approx(north["north"])
    assert east["north"] == pytest.approx(0.)
    assert east["vertical"] == pytest.approx(north["vertical"])
    west = mogi_displacement(-1000., 0., source_depth=2500.,
                             volume_change=1e6)
    assert west["east"] == pytest.approx(-east["east"])
    assert west["vertical"] == pytest.approx(east["vertical"])


def test_mogi_displacement_is_linear_in_volume_change_and_broadcasts():
    a = mogi_displacement(np.array([0., 1000.]), 0., source_depth=2000.,
                          volume_change=1e6)
    b = mogi_displacement(np.array([0., 1000.]), 0., source_depth=2000.,
                          volume_change=3e6)
    np.testing.assert_allclose(b["east"], 3*a["east"])
    np.testing.assert_allclose(b["vertical"], 3*a["vertical"])
    assert a["vertical"].shape == (2,)


def test_mogi_matches_independent_cartesian_equation():
    x = np.array([-2000., 0., 1500.])
    y = np.array([500., -1000., 2500.])
    depth, volume, nu = 4000., -8e6, .3
    result = mogi_displacement(x, y, source_depth=depth,
                               volume_change=volume, poisson_ratio=nu)
    r2 = x*x + y*y + depth*depth
    coefficient = (1-nu)*volume/np.pi/r2**1.5
    np.testing.assert_allclose(result["east"], coefficient*x, rtol=1e-13)
    np.testing.assert_allclose(result["north"], coefficient*y, rtol=1e-13)
    np.testing.assert_allclose(result["vertical"], coefficient*depth, rtol=1e-13)


@pytest.mark.parametrize("kwargs", [
    {"source_depth": 0.0, "volume_change": 1.0},
    {"source_depth": -1.0, "volume_change": 1.0},
    {"source_depth": 1.0, "volume_change": 1.0, "poisson_ratio": .5},
    {"source_depth": 1.0, "volume_change": 1.0, "poisson_ratio": 0.0},
    {"source_depth": np.nan, "volume_change": 1.0},
])
def test_mogi_rejects_invalid_source_parameters(kwargs):
    with pytest.raises(ValueError):
        mogi_displacement(0., 0., **kwargs)


def test_mogi_rejects_nonfinite_observation_coordinates():
    with pytest.raises(ValueError, match="coordinates"):
        mogi_displacement(np.nan, 0., source_depth=1., volume_change=1.)
