import numpy as np
import pytest
from terrain_derivatives import horn_slope_aspect

def test_east_rising_plane_has_westward_aspect():
    result=horn_slope_aspect(np.tile(np.arange(5,dtype=float),(5,1)))
    np.testing.assert_allclose(result["slope_degrees"][2,2],45)
    np.testing.assert_allclose(result["slope_percent"][2,2],100)
    np.testing.assert_allclose(result["aspect_degrees"][2,2],270)

def test_north_rising_plane_has_southward_aspect():
    dem=np.tile(np.arange(5,0,-1,dtype=float)[:,None],(1,5))
    result=horn_slope_aspect(dem)
    np.testing.assert_allclose(result["slope_degrees"][2,2],45)
    np.testing.assert_allclose(result["aspect_degrees"][2,2],180)

def test_rectangular_spacing_and_vertical_conversion():
    dem=np.tile(np.arange(5,dtype=float),(5,1))
    result=horn_slope_aspect(dem,cell_size_x=2,cell_size_y=5,z_factor=2)
    np.testing.assert_allclose(result["slope_percent"][2,2],100)
    np.testing.assert_allclose(result["aspect_degrees"][2,2],270)

def test_flat_has_zero_slope_and_undefined_aspect():
    result=horn_slope_aspect(np.ones((5,5)))
    assert result["slope_degrees"][2,2]==0
    assert result["slope_percent"][2,2]==0
    assert np.isnan(result["aspect_degrees"][2,2])

def test_edges_and_nodata_windows_are_nan():
    dem=np.ones((5,5)); dem[2,2]=np.nan
    result=horn_slope_aspect(dem)
    assert np.isnan(result["slope_degrees"][0,0])
    assert np.isnan(result["slope_degrees"][2,2])
    assert np.isnan(result["slope_degrees"][1,1])
    assert np.isnan(result["slope_degrees"][3,3])

def test_small_grids_return_nan_outputs():
    result=horn_slope_aspect(np.ones((2,4)))
    assert all(np.isnan(a).all() for a in result.values())

@pytest.mark.parametrize("kwargs",[{"cell_size_x":0},{"cell_size_y":-1},{"z_factor":0},{"cell_size_x":float("inf")}])
def test_invalid_spacing_rejected(kwargs):
    with pytest.raises(ValueError): horn_slope_aspect(np.ones((3,3)),**kwargs)

def test_non_2d_input_rejected():
    with pytest.raises(ValueError,match="2D"): horn_slope_aspect([1,2,3])


def test_zevenbergen_thorne_east_rising_plane_faces_west():
    from terrain_derivatives import zevenbergen_thorne_slope_aspect
    dem = np.tile(np.arange(5, dtype=float), (5, 1))
    result = zevenbergen_thorne_slope_aspect(dem)
    assert result["slope_degrees"][2, 2] == pytest.approx(45)
    assert result["slope_percent"][2, 2] == pytest.approx(100)
    assert result["aspect_degrees"][2, 2] == pytest.approx(270)


def test_zevenbergen_thorne_north_rising_plane_faces_south():
    from terrain_derivatives import zevenbergen_thorne_slope_aspect
    dem = np.tile(np.arange(5, 0, -1, dtype=float)[:, None], (1, 5))
    result = zevenbergen_thorne_slope_aspect(dem)
    assert result["slope_degrees"][2, 2] == pytest.approx(45)
    assert result["aspect_degrees"][2, 2] == pytest.approx(180)


def test_zevenbergen_thorne_matches_horn_on_planar_surface():
    from terrain_derivatives import zevenbergen_thorne_slope_aspect
    dem = np.fromfunction(lambda r, c: 3.0*c - 2.0*r + 7.0, (7, 8), dtype=float)
    horn = horn_slope_aspect(dem)
    zt = zevenbergen_thorne_slope_aspect(dem)
    for key in horn:
        np.testing.assert_allclose(zt[key][1:-1, 1:-1], horn[key][1:-1, 1:-1], equal_nan=True)


def test_zevenbergen_thorne_strict_nodata_neighbourhood_and_flat_aspect():
    from terrain_derivatives import zevenbergen_thorne_slope_aspect
    dem = np.ones((5, 5))
    flat = zevenbergen_thorne_slope_aspect(dem)
    assert flat["slope_degrees"][2, 2] == 0
    assert np.isnan(flat["aspect_degrees"][2, 2])
    dem[2, 2] = np.nan
    result = zevenbergen_thorne_slope_aspect(dem)
    assert np.isnan(result["slope_degrees"][1, 1])
    assert np.isnan(result["slope_degrees"][2, 2])


def test_zevenbergen_thorne_rejects_invalid_spacing():
    from terrain_derivatives import zevenbergen_thorne_slope_aspect
    with pytest.raises(ValueError):
        zevenbergen_thorne_slope_aspect(np.ones((3, 3)), cell_size_x=0)


def test_curvature_of_planar_surface_is_zero():
    from terrain_derivatives import terrain_curvature
    dem = np.fromfunction(lambda r,c: 3.0*c - 2.0*r + 7.0, (7,8), dtype=float)
    result = terrain_curvature(dem)
    np.testing.assert_allclose(result["profile_curvature"][1:-1,1:-1], 0, atol=1e-12)
    np.testing.assert_allclose(result["plan_curvature"][1:-1,1:-1], 0, atol=1e-12)


def test_profile_curvature_of_cylindrical_parabola_and_zero_plan_curvature():
    from terrain_derivatives import terrain_curvature
    x = np.arange(-3,4,dtype=float)
    dem = np.tile(x*x, (7,1))
    result = terrain_curvature(dem)
    expected = -2.0 / (5.0 ** 1.5)
    assert result["profile_curvature"][3,4] == pytest.approx(expected)
    assert result["plan_curvature"][3,4] == pytest.approx(0.0, abs=1e-12)


def test_curvature_is_invariant_to_vertical_offset_and_respects_spacing():
    from terrain_derivatives import terrain_curvature
    x = np.arange(-3,4,dtype=float)
    dem = np.tile(x*x, (7,1))
    base = terrain_curvature(dem)
    shifted = terrain_curvature(dem + 100.0)
    np.testing.assert_allclose(base["profile_curvature"], shifted["profile_curvature"], equal_nan=True)
    np.testing.assert_allclose(base["plan_curvature"], shifted["plan_curvature"], equal_nan=True)
    scaled = terrain_curvature(dem, cell_size_x=2.0)
    assert abs(scaled["profile_curvature"][3,4]) < abs(base["profile_curvature"][3,4])


def test_curvature_flat_cells_edges_and_nodata_are_nan():
    from terrain_derivatives import terrain_curvature
    dem = np.ones((5,5))
    flat = terrain_curvature(dem)
    assert np.isnan(flat["profile_curvature"][2,2])
    assert np.isnan(flat["plan_curvature"][2,2])
    assert np.isnan(flat["profile_curvature"][0,0])
    dem[2,2] = np.nan
    masked = terrain_curvature(dem)
    assert np.isnan(masked["profile_curvature"][1,1])
    assert np.isnan(masked["plan_curvature"][2,2])


@pytest.mark.parametrize("kwargs",[{"cell_size_x":0},{"cell_size_y":-1},{"z_factor":0},{"cell_size_y":float("nan")}])
def test_curvature_rejects_invalid_units(kwargs):
    from terrain_derivatives import terrain_curvature
    with pytest.raises(ValueError):
        terrain_curvature(np.ones((3,3)), **kwargs)


# Topographic position index (TPI)

def test_tpi_flat_surface_is_zero_and_edges_are_nodata():
    from terrain_indices import topographic_position_index
    result = topographic_position_index(np.full((7, 8), 12.0), window_size=3)
    np.testing.assert_allclose(result[1:-1, 1:-1], 0.0)
    assert np.isnan(result[0]).all()
    assert np.isnan(result[:, 0]).all()


def test_tpi_detects_ridge_and_valley_relative_to_local_mean():
    from terrain_indices import topographic_position_index
    dem = np.zeros((7, 7), dtype=float)
    dem[3, 3] = 10.0
    result = topographic_position_index(dem, window_size=3)
    assert result[3, 3] > 0
    dem[3, 3] = -10.0
    result = topographic_position_index(dem, window_size=3)
    assert result[3, 3] < 0


def test_tpi_uses_larger_window_and_ignores_nodata_when_permitted():
    from terrain_indices import topographic_position_index
    dem = np.zeros((9, 9), dtype=float)
    dem[4, 4] = 9.0
    dem[3, 3] = np.nan
    strict = topographic_position_index(dem, window_size=5)
    permissive = topographic_position_index(
        dem, window_size=5, min_valid_fraction=0.9
    )
    assert np.isnan(strict[4, 4])
    assert permissive[4, 4] > 0


@pytest.mark.parametrize("kwargs", [
    {"window_size": 2}, {"window_size": 0}, {"window_size": 3.0},
    {"min_valid_fraction": 0}, {"min_valid_fraction": 1.1},
    {"min_valid_fraction": float("nan")},
])
def test_tpi_rejects_invalid_parameters(kwargs):
    from terrain_indices import topographic_position_index
    with pytest.raises(ValueError):
        topographic_position_index(np.ones((5, 5)), **kwargs)


def test_tpi_requires_nonempty_2d_input():
    from terrain_indices import topographic_position_index
    with pytest.raises(ValueError):
        topographic_position_index(np.ones(5))
    with pytest.raises(ValueError):
        topographic_position_index(np.empty((0, 3)))


# Riley terrain ruggedness index (TRI)

def test_riley_tri_matches_eight_neighbour_definition():
    from terrain_indices import riley_terrain_ruggedness_index
    dem = np.zeros((5, 5), dtype=float)
    dem[2, 2] = 3.0
    result = riley_terrain_ruggedness_index(dem)
    assert result[2, 2] == pytest.approx(np.sqrt(8 * 9.0))
    assert np.isnan(result[0, 0])


def test_riley_tri_is_zero_on_flat_and_scales_with_vertical_units():
    from terrain_indices import riley_terrain_ruggedness_index
    dem = np.full((5, 5), 7.0)
    assert riley_terrain_ruggedness_index(dem)[2, 2] == 0.0
    dem[2, 2] = 8.0
    base = riley_terrain_ruggedness_index(dem)[2, 2]
    doubled = riley_terrain_ruggedness_index(dem, z_factor=2)[2, 2]
    assert doubled == pytest.approx(2 * base)


def test_riley_tri_requires_complete_nodata_free_neighbourhood():
    from terrain_indices import riley_terrain_ruggedness_index
    dem = np.ones((5, 5))
    dem[1, 1] = np.nan
    result = riley_terrain_ruggedness_index(dem)
    assert np.isnan(result[2, 2])
    assert np.isnan(result[1, 1])


@pytest.mark.parametrize("z_factor", [0, -1, float("inf"), float("nan")])
def test_riley_tri_rejects_invalid_vertical_scale(z_factor):
    from terrain_indices import riley_terrain_ruggedness_index
    with pytest.raises(ValueError):
        riley_terrain_ruggedness_index(np.ones((3, 3)), z_factor=z_factor)


# Hypsometric curve and integral

def test_hypsometric_curve_normalizes_elevation_and_area_fraction():
    from terrain_indices import hypsometric_curve
    dem = np.array([[0, 1, 2], [1, 2, 3]], dtype=float)
    result = hypsometric_curve(dem)
    np.testing.assert_allclose(result["relative_elevation"], [1, 2/3, 1/3, 0])
    np.testing.assert_allclose(result["area_fraction_above"], [1/6, 3/6, 5/6, 1])
    assert result["hypsometric_integral"] == pytest.approx(0.5)
    assert result["valid_cell_count"] == 6


def test_hypsometric_curve_excludes_nodata_and_respects_valid_mask():
    from terrain_indices import hypsometric_curve
    dem = np.array([[0, 1], [2, np.nan]], dtype=float)
    result = hypsometric_curve(dem, valid_mask=np.array([[1, 1], [0, 1]], dtype=bool))
    assert result["valid_cell_count"] == 2
    assert result["minimum_elevation"] == 0
    assert result["maximum_elevation"] == 1
    assert result["hypsometric_integral"] == pytest.approx(0.5)


def test_hypsometric_curve_is_invariant_to_positive_vertical_affine_transform():
    from terrain_indices import hypsometric_curve
    dem = np.arange(1, 13, dtype=float).reshape(3, 4)
    first = hypsometric_curve(dem)
    second = hypsometric_curve(dem * 10 + 500)
    np.testing.assert_allclose(first["relative_elevation"], second["relative_elevation"])
    np.testing.assert_allclose(first["area_fraction_above"], second["area_fraction_above"])
    assert first["hypsometric_integral"] == pytest.approx(second["hypsometric_integral"])


@pytest.mark.parametrize("dem", [
    np.ones((2, 2)), np.array([[np.nan, 1.0]]), np.empty((0, 2)),
])
def test_hypsometric_curve_rejects_undefined_or_insufficient_relief(dem):
    from terrain_indices import hypsometric_curve
    with pytest.raises(ValueError):
        hypsometric_curve(dem)


def test_hypsometric_curve_rejects_mismatched_mask():
    from terrain_indices import hypsometric_curve
    with pytest.raises(ValueError, match="valid_mask"):
        hypsometric_curve(np.ones((2, 2)), valid_mask=np.ones((3, 3)))


# Cut-and-fill volume

def test_cut_fill_depths_and_volumes_on_mixed_surface():
    from terrain_indices import cut_fill_volume
    existing = np.array([[5, 2], [4, 3]], dtype=float)
    design = np.array([[3, 4], [4, 1]], dtype=float)
    result = cut_fill_volume(existing, design, cell_size_x=2, cell_size_y=3)
    np.testing.assert_allclose(result["cut_depth"], [[2, 0], [0, 2]])
    np.testing.assert_allclose(result["fill_depth"], [[0, 2], [0, 0]])
    assert result["cut_volume"] == pytest.approx(24)
    assert result["fill_volume"] == pytest.approx(12)
    assert result["net_cut_volume"] == pytest.approx(12)
    assert result["valid_cell_count"] == 4


def test_cut_fill_identical_surfaces_have_zero_volumes():
    from terrain_indices import cut_fill_volume
    dem = np.arange(9, dtype=float).reshape(3, 3)
    result = cut_fill_volume(dem, dem)
    assert result["cut_volume"] == 0
    assert result["fill_volume"] == 0
    assert result["net_cut_volume"] == 0


def test_cut_fill_masks_nodata_and_explicitly_excluded_cells():
    from terrain_indices import cut_fill_volume
    existing = np.array([[5, np.nan], [2, 9]], dtype=float)
    design = np.zeros((2, 2))
    mask = np.array([[True, True], [False, True]])
    result = cut_fill_volume(existing, design, valid_mask=mask)
    np.testing.assert_allclose(result["cut_depth"], [[5, np.nan], [np.nan, 9]], equal_nan=True)
    assert result["cut_volume"] == pytest.approx(14)
    assert result["valid_cell_count"] == 2


@pytest.mark.parametrize("kwargs", [
    {"cell_size_x": 0}, {"cell_size_y": -1},
    {"cell_size_x": float("inf")}, {"cell_size_y": float("nan")},
])
def test_cut_fill_rejects_invalid_cell_sizes(kwargs):
    from terrain_indices import cut_fill_volume
    with pytest.raises(ValueError, match="cell sizes"):
        cut_fill_volume(np.ones((2, 2)), np.zeros((2, 2)), **kwargs)


def test_cut_fill_rejects_shape_and_mask_mismatch():
    from terrain_indices import cut_fill_volume
    with pytest.raises(ValueError, match="shape"):
        cut_fill_volume(np.ones((2, 2)), np.zeros((3, 3)))
    with pytest.raises(ValueError, match="valid_mask"):
        cut_fill_volume(np.ones((2, 2)), np.zeros((2, 2)), valid_mask=np.ones((3, 3)))


def test_multiscale_curvature_is_zero_for_a_planar_surface_at_all_scales():
    from terrain_derivatives import multiscale_terrain_curvature
    dem = np.fromfunction(lambda r, c: 2.0*c - 3.0*r + 7.0, (61, 63), dtype=float)
    result = multiscale_terrain_curvature(dem, [1.0, 2.5, 5.0])
    assert set(result) == {1.0, 2.5, 5.0}
    # Exclude the Gaussian support zone near the reflective raster boundary.
    for scale_result in result.values():
        np.testing.assert_allclose(scale_result["profile_curvature"][20:-20, 20:-20], 0, atol=1e-11)
        np.testing.assert_allclose(scale_result["plan_curvature"][20:-20, 20:-20], 0, atol=1e-11)


def test_multiscale_curvature_suppresses_short_wavelength_noise():
    from terrain_derivatives import multiscale_terrain_curvature
    rows, cols = np.indices((31, 31))
    dem = 0.02 * cols**2 + 0.01 * rows**2 + 0.8 * ((rows + cols) % 2 * 2 - 1)
    result = multiscale_terrain_curvature(dem, [0.5, 2.0, 4.0])
    centre = (15, 15)
    magnitudes = [abs(result[s]["profile_curvature"][centre]) for s in (0.5, 2.0, 4.0)]
    assert magnitudes[2] < magnitudes[0]


def test_multiscale_curvature_respects_rectangular_cell_spacing_and_nodata_contract():
    from terrain_derivatives import multiscale_terrain_curvature
    dem = np.fromfunction(lambda r, c: 0.1*c**2 + 0.2*r**2, (15, 17), dtype=float)
    result = multiscale_terrain_curvature(dem, [2.0], cell_size_x=2.0, cell_size_y=3.0)
    assert result[2.0]["profile_curvature"].shape == dem.shape
    assert np.isnan(result[2.0]["profile_curvature"][0]).all()
    dem[7, 7] = np.nan
    with pytest.raises(ValueError, match="fully finite"):
        multiscale_terrain_curvature(dem, [2.0])


@pytest.mark.parametrize("scales", [[], [0], [-1], [1, 1], [float("nan")]])
def test_multiscale_curvature_rejects_invalid_scales(scales):
    from terrain_derivatives import multiscale_terrain_curvature
    with pytest.raises(ValueError):
        multiscale_terrain_curvature(np.ones((5, 5)), scales)


def test_multiscale_curvature_rejects_invalid_spacing():
    from terrain_derivatives import multiscale_terrain_curvature
    with pytest.raises(ValueError):
        multiscale_terrain_curvature(np.ones((5, 5)), [1.0], cell_size_x=0)


def test_local_relief_model_removes_constant_and_preserves_local_peak_sign():
    from terrain_indices import local_relief_model
    flat = local_relief_model(np.full((11, 11), 25.0), scale=2.0)
    np.testing.assert_allclose(flat, 0.0, atol=1e-12)
    dem = np.zeros((21, 21)); dem[10, 10] = 10.0
    result = local_relief_model(dem, scale=2.0)
    assert result[10, 10] > 0
    assert result[10, 9] < 0


def test_local_relief_model_masks_nodata_and_handles_holes():
    from terrain_indices import local_relief_model
    dem = np.full((9, 9), 4.0); dem[4, 4] = np.nan
    result = local_relief_model(dem, scale=1.5)
    assert np.isnan(result[4, 4])
    np.testing.assert_allclose(result[np.isfinite(result)], 0.0, atol=1e-12)


def test_local_relief_model_rejects_invalid_scale_or_spacing():
    from terrain_indices import local_relief_model
    with pytest.raises(ValueError): local_relief_model(np.ones((5, 5)), scale=0)
    with pytest.raises(ValueError): local_relief_model(np.ones((5, 5)), scale=1, cell_size_x=-1)


def test_multiscale_tpi_returns_each_requested_scale():
    from terrain_indices import multiscale_topographic_position_index
    dem = np.zeros((15, 15)); dem[7, 7] = 8.0
    result = multiscale_topographic_position_index(dem, [3, 5, 9])
    assert list(result) == [3, 5, 9]
    assert result[3][7, 7] > 0 and result[9][7, 7] > 0


def test_multiscale_tpi_rejects_duplicate_and_even_windows():
    from terrain_indices import multiscale_topographic_position_index
    with pytest.raises(ValueError): multiscale_topographic_position_index(np.ones((5, 5)), [3, 3])
    with pytest.raises(ValueError): multiscale_topographic_position_index(np.ones((5, 5)), [4])

def test_local_extrema_detects_peak_and_pit_with_nodata_windows():
    from terrain_indices import detect_local_extrema
    peak = np.zeros((5, 5)); peak[2, 2] = 10
    maxima, minima = detect_local_extrema(peak)
    assert maxima[2, 2] and not minima[2, 2]
    pit = np.ones((5, 5)); pit[2, 2] = -5
    maxima, minima = detect_local_extrema(pit)
    assert minima[2, 2] and not maxima[2, 2]
    pit[1, 1] = np.nan
    maxima, minima = detect_local_extrema(pit)
    assert not minima[2, 2]


def test_local_extrema_prominence_window_and_flat_surface():
    from terrain_indices import detect_local_extrema
    dem = np.zeros((7, 7)); dem[3, 3] = 2
    maxima, minima = detect_local_extrema(dem, window_size=5, min_prominence=3)
    assert not maxima.any() and not minima.any()
    maxima, minima = detect_local_extrema(np.ones((5, 5)))
    assert not maxima.any() and not minima.any()
    with pytest.raises(ValueError): detect_local_extrema(dem, window_size=4)
    with pytest.raises(ValueError): detect_local_extrema(dem, min_prominence=-1)


def test_reservoir_stage_storage_analytic_curve():
    from terrain_indices import reservoir_stage_storage
    dem = np.array([[0., 1.], [2., np.nan]])
    result = reservoir_stage_storage(dem, [1., 2., 3.], cell_area=10)
    np.testing.assert_allclose(result['inundated_area'], [10, 20, 30])
    np.testing.assert_allclose(result['storage'], [10, 30, 60])
    assert result['valid_cell_count'] == 3


def test_reservoir_stage_storage_mask_and_validation():
    from terrain_indices import reservoir_stage_storage
    dem = np.array([[0., 1.], [2., 3.]])
    result = reservoir_stage_storage(dem, [2., 4.], cell_area=2, valid_mask=[[True, False], [True, True]])
    np.testing.assert_allclose(result['storage'], [4, 14])
    with pytest.raises(ValueError): reservoir_stage_storage(dem, [2., 1.])
    with pytest.raises(ValueError): reservoir_stage_storage(dem, [1.], cell_area=0)
    with pytest.raises(ValueError): reservoir_stage_storage(dem, [1.], valid_mask=[[True]])

def test_scs_curve_number_runoff_threshold_and_known_values():
    from terrain_indices import scs_curve_number_runoff
    assert scs_curve_number_runoff(10, 80) == pytest.approx(0)
    s = 25400/80 - 254
    p = 100
    expected = (p - .2*s)**2 / (p - .2*s + s)
    assert scs_curve_number_runoff(p, 80) == pytest.approx(expected)
    assert scs_curve_number_runoff([0, 10, 100], 100).tolist() == [0, 10, 100]


def test_scs_curve_number_runoff_broadcasting_and_validation():
    from terrain_indices import scs_curve_number_runoff
    result = scs_curve_number_runoff([20, 50], [60, 90])
    assert result.shape == (2,) and result[1] > result[0]
    with pytest.raises(ValueError): scs_curve_number_runoff(-1, 80)
    with pytest.raises(ValueError): scs_curve_number_runoff(10, 0)
    with pytest.raises(ValueError): scs_curve_number_runoff(10, 101)
    with pytest.raises(ValueError): scs_curve_number_runoff(10, 80, abstraction_ratio=-.1)


def test_scs_curve_number_antecedent_conversions_are_ordered_and_bounded():
    from terrain_indices import scs_curve_number_antecedent
    dry, wet = scs_curve_number_antecedent(np.array([40., 70., 95.]))
    assert np.all(dry < [40, 70, 95])
    assert np.all(wet > [40, 70, 95])
    assert np.all((dry >= 1) & (wet <= 100))
    with pytest.raises(ValueError): scs_curve_number_antecedent(0)



def test_green_ampt_no_ponding_and_ponded_analytic_step():
    from terrain_indices import green_ampt_infiltration_step
    result = green_ampt_infiltration_step(0, 5, 10, 100, .2, 1)
    assert result["infiltration"] == pytest.approx(5)
    assert result["runoff_excess"] == pytest.approx(0)
    # With F0=100 mm, suction term A=20 mm and rain=20 mm/h,
    # the surface is ponded throughout; implicit solution is bracketed.
    result = green_ampt_infiltration_step(100, 20, 5, 100, .2, 1)
    assert 5 < result["infiltration"] < 20
    assert result["ponded"] and result["runoff_excess"] > 0
    assert result["cumulative_infiltration"] == pytest.approx(100 + result["infiltration"])


def test_green_ampt_ponding_threshold_and_validation():
    from terrain_indices import green_ampt_infiltration_step
    # Initially unponded; rainfall first fills the capillary ponding threshold.
    result = green_ampt_infiltration_step(0, 20, 5, 100, .2, .01)
    assert result["infiltration"] == pytest.approx(.2)
    assert result["runoff_excess"] == pytest.approx(0)
    with pytest.raises(ValueError): green_ampt_infiltration_step(0, 1, 0, 10, .2, 1)
    with pytest.raises(ValueError): green_ampt_infiltration_step(0, 1, 5, 10, 2, 1)


def test_unit_hydrograph_convolution_full_series_and_mass_scaling():
    from terrain_indices import unit_hydrograph_convolution
    result = unit_hydrograph_convolution([1, 2], [0, 1, 2], time_step=.5)
    np.testing.assert_allclose(result["discharge"], [0, 1, 4, 4])
    np.testing.assert_allclose(result["time"], [0, .5, 1, 1.5])
    scaled = unit_hydrograph_convolution([2, 4], [0, 1, 2])
    np.testing.assert_allclose(scaled["discharge"], 2 * np.convolve([1, 2], [0, 1, 2]))


def test_unit_hydrograph_rejects_invalid_series():
    from terrain_indices import unit_hydrograph_convolution
    with pytest.raises(ValueError): unit_hydrograph_convolution([], [1])
    with pytest.raises(ValueError): unit_hydrograph_convolution([1], [-1])
    with pytest.raises(ValueError): unit_hydrograph_convolution([1], [1], time_step=0)



def test_green_ampt_zero_suction_reduces_to_conductivity_limit():
    from terrain_indices import green_ampt_infiltration_step
    result = green_ampt_infiltration_step(0, 20, 5, 0, .2, 1)
    assert result["infiltration"] == pytest.approx(5)
    assert result["runoff_excess"] == pytest.approx(15)
    assert result["ponded"]
