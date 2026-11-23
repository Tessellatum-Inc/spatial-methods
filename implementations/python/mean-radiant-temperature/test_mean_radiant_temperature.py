import numpy as np
import pytest
from mean_radiant_temperature import mean_radiant_temperature, STEFAN_BOLTZMANN

def test_equal_temperatures():
    r = mean_radiant_temperature(25., 25., .2)
    assert r["mean_radiant_temperature_c"] == pytest.approx(25.)

def test_natural_convection_matches_heat_balance():
    tg, ta, d, eps = 35., 25., .15, .95
    h = 1.4 * (abs(tg-ta)/d)**.25
    expected = ((tg+273.15)**4 + h*(tg-ta)/(eps*STEFAN_BOLTZMANN))**.25 - 273.15
    r = mean_radiant_temperature(tg, ta, 0., globe_diameter_m=d, emissivity=eps)
    assert r["convection_regime"] == "natural"
    assert r["mean_radiant_temperature_c"] == pytest.approx(expected)

def test_forced_convection_matches_heat_balance():
    tg, ta, v, d, eps = 40., 25., 1., .15, .95
    h = 6.3*v**.6/d**.4
    expected = ((tg+273.15)**4 + h*(tg-ta)/(eps*STEFAN_BOLTZMANN))**.25 - 273.15
    r = mean_radiant_temperature(tg, ta, v, globe_diameter_m=d, emissivity=eps)
    assert r["convection_regime"] == "forced"
    assert r["convective_heat_transfer_w_m2_k"] == pytest.approx(h)
    assert r["mean_radiant_temperature_c"] == pytest.approx(expected)

def test_vector_broadcasting():
    r = mean_radiant_temperature(np.array([30.,40.]), 25., np.array([0.,1.]))
    assert r["mean_radiant_temperature_c"].shape == (2,)
    assert r["convection_regime"].tolist() == ["natural","forced"]
    assert np.all(np.isfinite(r["mean_radiant_temperature_c"]))

@pytest.mark.parametrize("args,kwargs", [
    ((-273.15,20.,.1),{}), ((20.,20.,-.1),{}),
    ((20.,20.,.1),{"globe_diameter_m":0}),
    ((20.,20.,.1),{"emissivity":0}),
    ((20.,20.,float("nan")),{}),
])
def test_invalid_inputs(args,kwargs):
    with pytest.raises(ValueError):
        mean_radiant_temperature(*args,**kwargs)
