import numpy as np
import pytest
from urban import (cluster_building_points, building_density_grid,
                   connected_urban_areas, head_tail_natural_city_threshold,
                   natural_city_candidates)


def test_building_dbscan_recovers_two_centroid_clusters_and_noise():
    points = np.array([[0.,0.],[.1,0.],[0.,.1],[10.,10.],[10.1,10.],[10.,10.1],[50.,50.]])
    labels = cluster_building_points(points, eps=.5, min_samples=2)
    assert labels[0] == labels[1] == labels[2]
    assert labels[3] == labels[4] == labels[5]
    assert labels[0] != labels[3]
    assert labels[6] == -1


def test_building_density_grid_matches_histogram_counts():
    points = np.array([[.2,.2],[.3,.3],[1.2,.2],[1.2,1.2]])
    density = building_density_grid(points, [0.,1.,2.], [0.,1.,2.])
    np.testing.assert_array_equal(density, [[2,1],[0,1]])


def test_connected_urban_areas_respects_connectivity_and_minimum_size():
    density = np.array([[2.,0.,2.],[0.,2.,0.],[0.,0.,0.]])
    four = connected_urban_areas(density, minimum_density=1, connectivity=4)
    eight = connected_urban_areas(density, minimum_density=1, connectivity=8)
    assert len(four["sizes"]) == 3
    assert len(eight["sizes"]) == 1
    filtered = connected_urban_areas(density, minimum_density=1,
                                     connectivity=8, minimum_cells=4)
    assert not filtered["mask"].any()


def test_head_tail_threshold_and_empty_grid():
    z = np.array([[0.,1.,2.,3.,4.,20.,30.,40.]])
    result = head_tail_natural_city_threshold(z)
    assert result["iterations"] >= 1
    assert result["threshold"] > 0
    empty = head_tail_natural_city_threshold(np.zeros((2,2)))
    assert np.isinf(empty["threshold"])
    assert not natural_city_candidates(np.zeros((2,2)))["mask"].any()


def test_urban_methods_validate_inputs():
    with pytest.raises(ValueError, match="points"):
        cluster_building_points([[0.,0.,1.]], eps=1.)
    with pytest.raises(ValueError, match="strictly increasing"):
        building_density_grid([[0.,0.]], [0.,1.,1.], [0.,1.])
    with pytest.raises(ValueError, match="connectivity"):
        connected_urban_areas(np.ones((2,2)), connectivity=6)
