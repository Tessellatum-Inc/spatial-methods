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
