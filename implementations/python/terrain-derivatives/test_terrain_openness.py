import numpy as np
import pytest
from terrain_openness import terrain_openness


def test_flat_surface_has_ninety_degree_positive_and_negative_openness():
    result = terrain_openness(np.zeros((15, 15)), max_distance=3, azimuth_count=8)
    assert result["positive_openness"][7, 7] == pytest.approx(90)
    assert result["negative_openness"][7, 7] == pytest.approx(90)


def test_surrounding_ridge_reduces_positive_openness():
    dem = np.zeros((21, 21))
    dem[7:14, 7:14] = 5
    dem[10, 10] = 0
    result = terrain_openness(dem, max_distance=4, azimuth_count=16)
    assert result["positive_openness"][10, 10] < 90
    assert result["negative_openness"][10, 10] == pytest.approx(90)


def test_surrounding_pit_wall_reduces_negative_openness():
    dem = np.zeros((21, 21))
    dem[7:14, 7:14] = -5
    dem[10, 10] = 0
    result = terrain_openness(dem, max_distance=4, azimuth_count=16)
    assert result["negative_openness"][10, 10] < 90


def test_nodata_or_boundary_rays_are_masked():
    dem = np.zeros((15, 15))
    dem[7, 9] = np.nan
    result = terrain_openness(dem, max_distance=3, azimuth_count=8)
    assert np.isnan(result["positive_openness"][7, 7])
    assert np.isnan(result["positive_openness"][0, 0])


@pytest.mark.parametrize("kwargs", [
    {"max_distance": 0}, {"cell_size_x": 0}, {"sample_spacing": -1},
    {"azimuth_count": 2},
])
def test_invalid_parameters(kwargs):
    with pytest.raises(ValueError):
        terrain_openness(np.zeros((9, 9)), **({"max_distance": 2} | kwargs))
