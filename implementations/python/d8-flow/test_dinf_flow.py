import numpy as np
import pytest

from dinf_flow import dinf_flow_weights
from mfd_flow import mfd_flow_accumulation


def test_planar_surface_routes_into_the_correct_facet_with_angular_split():
    # z = 20 - 2*x - y: downslope aspect is between E and SE.
    dem = np.array([
        [23, 21, 19, 17, 15],
        [22, 20, 18, 16, 14],
        [21, 19, 17, 15, 13],
        [20, 18, 16, 14, 12],
        [19, 17, 15, 13, 11],
    ], dtype=float)
    weights = dinf_flow_weights(dem)
    east, southeast = weights[2, 2, 0], weights[2, 2, 1]
    assert east > 0 and southeast > 0
    assert east + southeast == pytest.approx(1.0)
    assert east == pytest.approx(1.0 - (np.arctan2(1.0, 2.0) / (np.pi / 4)))
    assert southeast == pytest.approx(np.arctan2(1.0, 2.0) / (np.pi / 4))
    assert np.count_nonzero(weights[2, 2]) == 2


def test_planar_surface_direction_is_independent_of_absolute_elevation():
    dem = np.array([[8, 6, 4], [7, 5, 3], [6, 4, 2]], dtype=float)
    shifted = dinf_flow_weights(dem + 10000.0)
    base = dinf_flow_weights(dem)
    assert shifted[1, 1] == pytest.approx(base[1, 1])


def test_rectangular_cells_change_facet_aspect_and_partition():
    dem = np.array([[8, 6, 4], [7, 5, 3], [6, 4, 2]], dtype=float)
    square = dinf_flow_weights(dem)
    rectangular = dinf_flow_weights(dem, cell_size=(2.0, 1.0))
    assert not np.allclose(square[1, 1], rectangular[1, 1])
    assert rectangular[1, 1].sum() == pytest.approx(1.0)


def test_dinf_routes_only_to_lower_neighbours_and_conserves_accumulation():
    dem = np.array([
        [9, 8, 7, 6],
        [8, 7, 6, 5],
        [7, 6, 5, 4],
        [6, 5, 4, 3],
    ], dtype=float)
    weights = dinf_flow_weights(dem)
    directions = ((0, 1), (1, 1), (1, 0), (1, -1),
                  (0, -1), (-1, -1), (-1, 0), (-1, 1))
    for row, col in np.ndindex(dem.shape):
        assert weights[row, col].sum() in (0.0, pytest.approx(1.0))
        for index, fraction in enumerate(weights[row, col]):
            if fraction:
                dr, dc = directions[index]
                assert dem[row + dr, col + dc] < dem[row, col]
    accumulation = mfd_flow_accumulation(dem, weights)
    assert accumulation[3, 3] == pytest.approx(dem.size)


def test_dinf_sinks_flats_and_invalid_cells_have_no_outflow():
    dem = np.array([[3.0, 3.0, 3.0], [3.0, 1.0, 3.0], [3.0, 3.0, 3.0]])
    weights = dinf_flow_weights(dem)
    assert np.all(weights[1, 1] == 0.0)
    assert weights[0, 0, 1] == pytest.approx(1.0)  # the corner drains southeast into the pit
    nodata = np.array([[5.0, -9999.0, 4.0]])
    masked = dinf_flow_weights(nodata, nodata=-9999)
    assert np.all(masked[0, 1] == 0.0)


def test_dinf_uses_available_downhill_edge_next_to_nodata():
    dem = np.array([[4.0, 3.0, np.nan], [5.0, 2.0, np.nan], [6.0, 1.0, np.nan]])
    weights = dinf_flow_weights(dem)
    assert weights[1, 1].sum() == pytest.approx(1.0)
    assert weights[1, 1, 2] == pytest.approx(1.0)  # south is the only lower valid neighbour


def test_dinf_rejects_invalid_cell_spacing_and_masks():
    with pytest.raises(ValueError):
        dinf_flow_weights([[2.0, 1.0]], cell_size=(1.0, 0.0))
    with pytest.raises(ValueError):
        dinf_flow_weights([[2.0, 1.0]], valid_mask=np.ones((2, 2)))
