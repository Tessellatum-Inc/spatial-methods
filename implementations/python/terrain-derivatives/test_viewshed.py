import numpy as np
import pytest
from viewshed import viewshed, cumulative_viewshed


def test_flat_grid_all_cells_visible_without_curvature():
    result = viewshed(np.zeros((5, 5)), (2, 2))
    assert result.all()


def test_intervening_ridge_blocks_cells_behind_it():
    dem = np.zeros((3, 7))
    dem[1, 3] = 5
    result = viewshed(dem, (1, 1), observer_height=0)
    assert result[1, 3]
    assert not result[1, 4]
    assert not result[1, 6]


def test_observer_and_target_heights_change_visibility():
    dem = np.zeros((1, 5))
    dem[0, 2] = 2
    low = viewshed(dem, (0, 0), observer_height=0, target_height=0)
    high = viewshed(dem, (0, 0), observer_height=3, target_height=0)
    assert not low[0, 4]
    assert high[0, 4]


def test_nodata_on_ray_makes_target_indeterminate():
    dem = np.zeros((1, 5))
    dem[0, 2] = np.nan
    assert not viewshed(dem, (0, 0))[0, 4]


def test_curvature_parameter_validation_and_flat_surface():
    dem = np.zeros((5, 5))
    result = viewshed(dem, (2, 2), earth_radius=6_371_000, refraction_coefficient=0.13)
    assert result[2, 4]
    with pytest.raises(ValueError):
        viewshed(dem, (2, 2), earth_radius=0)
    with pytest.raises(ValueError):
        viewshed(dem, (9, 9))


def test_cumulative_viewshed_counts_observers_and_validates():
    dem = np.zeros((3, 5))
    result = cumulative_viewshed(dem, [(1, 0), (1, 4)])
    assert result[1, 2] == 2
    assert result[1, 0] == 1
    with pytest.raises(ValueError):
        cumulative_viewshed(dem, [])
