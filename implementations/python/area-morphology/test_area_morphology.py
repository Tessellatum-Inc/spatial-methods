import numpy as np
import pytest

from area_morphology import area_closing, area_opening


def test_area_opening_removes_small_bright_island():
    image = np.zeros((5, 5))
    image[1:4, 1:4] = 1
    image[0, 0] = 5
    result = area_opening(image, min_area=2)
    assert result[0, 0] == 0
    assert np.all(result[1:4, 1:4] == 1)


def test_area_opening_preserves_large_component_and_is_idempotent():
    image = np.array([[0, 2, 2, 0], [0, 2, 2, 0], [3, 0, 0, 4]], dtype=float)
    opened = area_opening(image, min_area=4)
    assert np.all(opened <= image)
    assert np.array_equal(area_opening(opened, min_area=4), opened)


def test_area_closing_fills_small_dark_hole():
    image = np.full((5, 5), 3.0)
    image[2, 2] = 0
    result = area_closing(image, min_area=2)
    assert result[2, 2] == 3
    assert np.all(result == 3)


def test_connectivity_changes_diagonal_component_area():
    image = np.array([[2, 0], [0, 2]], dtype=float)
    four = area_opening(image, min_area=2, connectivity=4)
    eight = area_opening(image, min_area=2, connectivity=8)
    assert np.all(four == 0)
    assert np.all(eight == image)


@pytest.mark.parametrize("kwargs", [
    {"min_area": 0},
    {"min_area": 1, "connectivity": 6},
])
def test_invalid_parameters_rejected(kwargs):
    with pytest.raises(ValueError):
        area_opening([[1, 1], [1, 1]], **kwargs)


def test_invalid_raster_rejected():
    with pytest.raises(ValueError):
        area_opening([[1, float("nan")]], min_area=2)
