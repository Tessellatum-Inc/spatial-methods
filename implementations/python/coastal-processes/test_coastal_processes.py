import numpy as np
import pytest
from coastal_processes import stockdon_runup, cerc_longshore_transport, shoreline_change_rates


def test_stockdon_runup_known_shape_and_percentile_order():
    r2 = stockdon_runup(2.0, 10.0, 0.05)
    assert np.ndim(r2) == 0 and r2 > 0
    assert stockdon_runup(2.0, 10.0, 0.05, percentile=1) == pytest.approx(.75*r2)
    assert stockdon_runup(2.0, 10.0, 0.05, percentile=50) == pytest.approx(.5*r2)
    low = stockdon_runup(2.0, 10.0, 0.05, percentile=0)
    assert low < stockdon_runup(2.0, 10.0, 0.05, percentile=50)
    assert low != 0


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


def test_bruun_rule_recession_scales_with_rise_and_width():
    from coastal_processes import bruun_rule_recession
    assert bruun_rule_recession(1, 100, 2, 8) == pytest.approx(10)
    assert bruun_rule_recession(2, 100, 2, 8) == pytest.approx(20)
    np.testing.assert_allclose(bruun_rule_recession([1, 2], 100, 2, 8), [10, 20])


def test_bruun_rule_rejects_invalid_geometry():
    from coastal_processes import bruun_rule_recession
    with pytest.raises(ValueError): bruun_rule_recession(-1, 100, 2, 8)
    with pytest.raises(ValueError): bruun_rule_recession(1, 0, 2, 8)
    with pytest.raises(ValueError): bruun_rule_recession(1, 100, 2, 0)


def test_dean_profile_and_integral_match_analytic_values():
    from coastal_processes import dean_equilibrium_profile, dean_profile_volume
    x = np.array([0., 1., 8., 27.])
    np.testing.assert_allclose(dean_equilibrium_profile(x, .5), .5*x**(2/3))
    assert dean_profile_volume(.5, 0, 8) == pytest.approx(4.8)
    assert dean_profile_volume(.5, 3, 3) == pytest.approx(0)


def test_dean_profile_validates_inputs():
    from coastal_processes import dean_equilibrium_profile, dean_profile_volume
    with pytest.raises(ValueError): dean_equilibrium_profile([-1, 2], .5)
    with pytest.raises(ValueError): dean_equilibrium_profile([0, 2], 0)
    with pytest.raises(ValueError): dean_profile_volume(.5, 4, 3)

def test_satellite_bathymetry_ratio_calibration_and_prediction():
    from coastal_processes import fit_satellite_bathymetry_ratio, satellite_bathymetry_ratio
    x = np.array([0., 1., 2., 3.]); y = 2. + 3.*x
    model = fit_satellite_bathymetry_ratio(x, y)
    assert model['slope'] == pytest.approx(3)
    assert model['intercept'] == pytest.approx(2)
    np.testing.assert_allclose(satellite_bathymetry_ratio([0, 1, np.nan], model), [2, 5, np.nan])
    np.testing.assert_allclose(satellite_bathymetry_ratio([-1, 1, 3], model, min_depth=2, max_depth=8), [np.nan, 5, np.nan], equal_nan=True)


def test_satellite_bathymetry_ratio_rejects_bad_calibration():
    from coastal_processes import fit_satellite_bathymetry_ratio, satellite_bathymetry_ratio
    with pytest.raises(ValueError): fit_satellite_bathymetry_ratio([1, 1], [2, 3])
    with pytest.raises(ValueError): satellite_bathymetry_ratio([1], {'slope': np.nan, 'intercept': 0})


def test_multibeam_grid_mean_median_counts_and_orientation():
    from coastal_processes import grid_multibeam_soundings
    x = [0.1, 0.2, 1.1, 0.2]; y = [1.9, 1.8, 1.9, 0.8]; z = [10, 14, 20, 30]
    mean, count, xc, yc = grid_multibeam_soundings(x, y, z, cell_size=1, origin=(0, 2))
    assert mean.shape == (2, 2)
    assert mean[0,0] == pytest.approx(12) and count[0,0] == 2
    assert mean[0,1] == pytest.approx(20) and mean[1,0] == pytest.approx(30)
    assert np.isnan(mean[1,1]) and count[1,1] == 0
    med, _, _, _ = grid_multibeam_soundings(x, y, z, cell_size=1, origin=(0,2), statistic='median')
    assert med[0,0] == pytest.approx(12)
    np.testing.assert_allclose(xc, [0.5,1.5]); np.testing.assert_allclose(yc, [1.5,0.5])


def test_multibeam_grid_validation():
    from coastal_processes import grid_multibeam_soundings
    with pytest.raises(ValueError): grid_multibeam_soundings([0], [0], [1], cell_size=0)
    with pytest.raises(ValueError): grid_multibeam_soundings([np.nan], [0], [1], cell_size=1)
    with pytest.raises(ValueError): grid_multibeam_soundings([0], [0], [1], cell_size=1, statistic='mode')
