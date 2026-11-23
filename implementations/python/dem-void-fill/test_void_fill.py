import math
import pytest
from void_fill import inverse_distance_void_fill

def test_single_center_void_is_filled_from_four_neighbours():
    grid = [[1, 2, 3], [4, None, 6], [7, 8, 9]]
    result = inverse_distance_void_fill(grid, min_neighbors=4)
    assert result["elevation"][1][1] == pytest.approx(5)
    assert result["filled_mask"][1][1]

def test_valid_cells_are_preserved_exactly():
    grid = [[1, 2, 3], [4, None, 6], [7, 8, 9]]
    result = inverse_distance_void_fill(grid, min_neighbors=4)
    for r in range(3):
        for c in range(3):
            if grid[r][c] is not None:
                assert result["elevation"][r][c] == grid[r][c]
                assert not result["filled_mask"][r][c]

def test_nodata_sentinel_and_nan_are_recognized():
    grid = [[1, -9999, 3], [4, float("nan"), 6], [7, 8, 9]]
    result = inverse_distance_void_fill(grid, nodata=-9999, min_neighbors=3)
    assert result["filled_mask"][0][1]
    assert result["filled_mask"][1][1]
    assert math.isfinite(result["elevation"][0][1])

def test_synchronous_iterations_expand_into_large_void():
    grid = [[1, 1, 1, 1, 1], [1, None, None, None, 1], [1, None, None, None, 1], [1, None, None, None, 1], [1, 1, 1, 1, 1]]
    one = inverse_distance_void_fill(grid, max_radius=1, min_neighbors=2, max_iterations=1)
    many = inverse_distance_void_fill(grid, max_radius=1, min_neighbors=2, max_iterations=4)
    assert one["elevation"][2][2] is None
    assert many["elevation"][2][2] == pytest.approx(1)

def test_unfillable_cells_remain_none():
    grid = [[1, None, None, None, 2]]
    result = inverse_distance_void_fill(grid, max_radius=1, min_neighbors=3, max_iterations=2)
    assert result["elevation"][0][1] is None
    assert result["elevation"][0][2] is None

def test_pixel_sizes_change_distance_weights():
    grid = [[None, 10, None], [0, None, None], [None, None, None]]
    unit = inverse_distance_void_fill(grid, max_radius=2, min_neighbors=2)
    stretched = inverse_distance_void_fill(grid, max_radius=2, min_neighbors=2, pixel_size_x=10, pixel_size_y=1)
    assert unit["elevation"][1][1] == pytest.approx(5)
    assert stretched["elevation"][1][1] > 9

@pytest.mark.parametrize("kwargs", [
    {"max_radius": 0}, {"min_neighbors": 0}, {"max_iterations": 0},
    {"power": 0}, {"pixel_size_x": -1}, {"pixel_size_y": float("inf")},
])
def test_invalid_parameters_are_rejected(kwargs):
    with pytest.raises(ValueError):
        inverse_distance_void_fill([[1, None], [2, 3]], **kwargs)

@pytest.mark.parametrize("grid", [[], [[1, 2], [3]], [[None, None]], [[True, 1]]])
def test_invalid_or_unanchored_grids_are_rejected(grid):
    with pytest.raises(ValueError):
        inverse_distance_void_fill(grid)
