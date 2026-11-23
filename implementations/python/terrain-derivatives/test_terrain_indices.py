import numpy as np
import pytest
from terrain_indices import topographic_wetness_index

def test_matches_conventional_log_area_over_tangent_slope():
    area=np.array([[10.0]])
    slope=np.array([[30.0]])
    result=topographic_wetness_index(area,slope)
    expected = np.log(10 / np.tan(np.radians(30)))
    np.testing.assert_allclose(result, np.array([[expected]]))

def test_flat_slope_uses_declared_positive_floor():
    result=topographic_wetness_index([[10]],[[0]],slope_floor_degrees=1)
    expected = np.log(10 / np.tan(np.radians(1)))
    np.testing.assert_allclose(result, np.array([[expected]]))

def test_nonpositive_area_and_nodata_are_masked():
    result=topographic_wetness_index([[0,np.nan,10]],[[20,20,np.nan]])
    assert np.isnan(result).all()

def test_shape_slope_and_floor_contracts():
    with pytest.raises(ValueError,match="same shape"):
        topographic_wetness_index([[1]],[[1,2]])
    with pytest.raises(ValueError,match="\[0, 90\)"):
        topographic_wetness_index([[1]],[[90]])
    with pytest.raises(ValueError,match="slope_floor"):
        topographic_wetness_index([[1]],[[10]],slope_floor_degrees=0)
    with pytest.raises(ValueError,match="slope_floor"):
        topographic_wetness_index([[1]],[[10]],slope_floor_degrees="flat")


def test_sky_view_factor_is_one_on_flat_terrain_and_masks_unsupported_edges():
    from terrain_indices import sky_view_factor
    result = sky_view_factor(np.zeros((21, 21)), max_distance=4.0, azimuth_count=16)
    assert result[10, 10] == pytest.approx(1.0)
    assert np.isnan(result[0, :]).all()
    assert np.isnan(result[:, 0]).all()


def test_sky_view_factor_detects_enclosing_ridge_and_rectangular_cells():
    from terrain_indices import sky_view_factor
    dem = np.full((31, 31), 5.0)
    dem[15, 15] = 0.0
    result = sky_view_factor(
        dem, cell_size_x=2.0, cell_size_y=1.0,
        max_distance=4.0, azimuth_count=32, sample_spacing=.5,
    )
    assert 0.0 <= result[15, 15] < 0.8
    assert np.isnan(result[0, 0])


def test_sky_view_factor_nodata_on_any_ray_invalidates_cell():
    from terrain_indices import sky_view_factor
    dem = np.zeros((21, 21))
    dem[10, 12] = np.nan
    result = sky_view_factor(dem, max_distance=4.0, azimuth_count=16)
    assert np.isnan(result[10, 10])


@pytest.mark.parametrize("kwargs", [
    {"cell_size_x": 0}, {"cell_size_y": -1}, {"max_distance": 0},
    {"azimuth_count": 3}, {"sample_spacing": 0},
])
def test_sky_view_factor_rejects_invalid_parameters(kwargs):
    from terrain_indices import sky_view_factor
    args = {"max_distance": 2.0}
    args.update(kwargs)
    with pytest.raises(ValueError):
        sky_view_factor(np.zeros((9, 9)), **args)
