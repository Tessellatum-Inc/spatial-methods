import numpy as np
import pytest
from coastal_processes import stockdon_runup, cerc_longshore_transport, shoreline_change_rates


def test_stockdon_runup_known_shape_and_percentile_order():
    r2 = stockdon_runup(2.0, 10.0, 0.05)
    assert np.ndim(r2) == 0 and r2 > 0
    assert stockdon_runup(2.0, 10.0, 0.05, percentile=1) == pytest.approx(.75*r2)
    assert stockdon_runup(2.0, 10.0, 0.05, percentile=50) == pytest.approx(.5*r2)
    assert stockdon_runup(2.0, 10.0, 0.05, percentile=0) == 0


def test_stockdon_broadcasting_and_invalid_inputs():
    got = stockdon_runup([1, 2], 8, .04)
    assert got.shape == (2,) and got[1] > got[0]
    with pytest.raises(ValueError): stockdon_runup(-1, 8, .04)
    with pytest.raises(ValueError): stockdon_runup(1, 8, .04, percentile=95)


def test_cerc_zero_normal_and_oblique_wave_angles():
    assert cerc_longshore_transport(2, 0) == pytest.approx(0)
    assert cerc_longshore_transport(2, 20) > 0
    assert cerc_longshore_transport(2, -20) < 0
    assert cerc_longshore_transport(2, 20) == pytest.approx(
        -cerc_longshore_transport(2, -20))


def test_cerc_validation():
    with pytest.raises(ValueError): cerc_longshore_transport(-1, 10)
    with pytest.raises(ValueError): cerc_longshore_transport(1, 10, porosity=1)
    with pytest.raises(ValueError): cerc_longshore_transport(1, 10, rho_sediment=1000)


def test_shoreline_rates_exact_linear_trend_and_sorting():
    r = shoreline_change_rates([2020, 2000, 2010], [2, 0, 1])
    assert r["epr"] == pytest.approx(.1)
    assert r["ols_rate"] == pytest.approx(.1)
    assert r["ols_r_squared"] == pytest.approx(1)


def test_shoreline_weighted_regression_and_validation():
    r = shoreline_change_rates([2000, 2010, 2020], [0, 1, 2.2],
                               uncertainties=[.1, .1, .5])
    assert r["wlr_rate"] != pytest.approx(r["ols_rate"])
    with pytest.raises(ValueError): shoreline_change_rates([1, 1], [2, 3])
    with pytest.raises(ValueError): shoreline_change_rates([1, 2], [2, np.nan])
    with pytest.raises(ValueError): shoreline_change_rates([1, 2], [2, 3], uncertainties=[0, 1])
