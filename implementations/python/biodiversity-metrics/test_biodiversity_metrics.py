import numpy as np
import pytest
from biodiversity_metrics import area_of_occupancy, extent_of_occurrence, landscape_patch_metrics, shannon_diversity, species_richness, weighted_endemism


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


def test_landscape_patch_metrics_counts_components_and_internal_edges():
    raster = np.array([
        [1, 1, 2],
        [1, 2, 2],
        [3, 3, 2],
    ])
    result = landscape_patch_metrics(raster, cell_size=10, connectivity=4)
    assert result["valid_cells"] == 9
    assert result["total_patch_count"] == 3
    assert result["classes"][1]["patch_count"] == 1
    assert result["classes"][2]["patch_count"] == 1
    assert result["classes"][3]["patch_count"] == 1
    assert result["classes"][2]["largest_patch_index"] == pytest.approx(4 / 9 * 100)
    # Four horizontal/vertical class boundaries in this 3x3 fixture.
    assert result["edge_count"] == 4
    assert result["edge_length"] == pytest.approx(40)
    assert result["edge_density_per_ha"] == pytest.approx(40 / 0.09)


def test_landscape_connectivity_changes_diagonal_patch_count():
    raster = np.array([[1, 0], [0, 1]])
    four = landscape_patch_metrics(raster, connectivity=4)
    eight = landscape_patch_metrics(raster, connectivity=8)
    assert four["classes"][1]["patch_count"] == 2
    assert eight["classes"][1]["patch_count"] == 1


def test_landscape_nodata_and_validation():
    raster = np.array([[1., 1., -9999.], [2., np.nan, 2.]])
    result = landscape_patch_metrics(raster, nodata=-9999)
    assert result["valid_cells"] == 4
    with pytest.raises(ValueError):
        landscape_patch_metrics(np.array([[1., np.nan]]))
    with pytest.raises(ValueError):
        landscape_patch_metrics(np.array([[1]]), connectivity=6)
    with pytest.raises(ValueError):
        landscape_patch_metrics(np.array([[-9999]]), nodata=-9999)


def test_shannon_diversity_uniform_and_single_class():
    assert shannon_diversity(np.array([[1, 1], [1, 1]])) == pytest.approx(0)
    assert shannon_diversity(np.array([[1, 2], [1, 2]])) == pytest.approx(np.log(2))
    assert shannon_diversity(np.array([[1., np.nan], [2., 2.]])) == pytest.approx(
        -(1/3*np.log(1/3) + 2/3*np.log(2/3))
    )
