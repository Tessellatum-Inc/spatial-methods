import numpy as np
import pytest
from biodiversity_metrics import area_of_occupancy, extent_of_occurrence, species_richness, weighted_endemism


def test_eoo_triangle_area_and_hull_vertices():
    result = extent_of_occurrence([[0., 0.], [4., 0.], [0., 3.], [1., 1.], [0., 0.]])
    assert result["area"] == pytest.approx(6.)
    assert set(map(tuple, result["polygon"])) == {(0., 0.), (4., 0.), (0., 3.)}


def test_eoo_degenerate_collinear_and_singleton():
    line = extent_of_occurrence([[0., 0.], [1., 1.], [2., 2.]])
    assert line["area"] == 0. and len(line["polygon"]) == 2
    point = extent_of_occurrence([[2., 3.], [2., 3.]])
    assert point["area"] == 0.
    np.testing.assert_array_equal(point["polygon"], [[2., 3.]])


def test_aoo_counts_unique_grid_cells():
    result = area_of_occupancy([[100., 100.], [1999., 1500.], [2100., 100.], [-1., 100.], [100., 100.]], cell_size=2000.)
    assert result["occupied_cells"] == 3
    assert result["area"] == 12_000_000.
    assert set(map(tuple, result["cell_indices"])) == {(0, 0), (1, 0), (-1, 0)}


def test_richness_and_weighted_endemism_direct_oracle():
    matrix = np.array([[1, 1, 0], [1, 0, 0], [0, 1, 1]])
    np.testing.assert_array_equal(species_richness(matrix), [2, 1, 2])
    np.testing.assert_allclose(weighted_endemism(matrix), [1., .5, 1.5])


@pytest.mark.parametrize("bad", [np.ones(2), np.array([[1., np.nan]])])
def test_occurrence_validation(bad):
    with pytest.raises(ValueError):
        extent_of_occurrence(bad)


def test_grid_and_presence_validation():
    with pytest.raises(ValueError, match="cell_size"):
        area_of_occupancy([[0., 0.]], cell_size=0)
    with pytest.raises(ValueError, match="origin"):
        area_of_occupancy([[0., 0.]], origin=(0.,))
    with pytest.raises(ValueError, match="binary"):
        species_richness([[0, 2]])
