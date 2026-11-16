import numpy as np
import pytest
from zoning import spatially_constrained_ward, zoning_scale_effect


def test_spatial_ward_merges_similar_adjacent_units():
    x = np.array([[0.],[.1],[10.],[10.1]])
    edges = np.array([[0,1],[1,2],[2,3]])
    result = spatially_constrained_ward(x, edges, n_zones=2)
    labels = result["labels"]
    assert labels[0] == labels[1]
    assert labels[2] == labels[3]
    assert labels[0] != labels[2]
    assert result["zone_sizes"].tolist() == [2,2]
    assert result["within_zone_sse"] == pytest.approx(.01)


def test_spatial_zoning_scale_effect_is_monotone_in_zone_count():
    x = np.array([[0.],[1.],[4.],[5.]])
    edges = np.array([[0,1],[1,2],[2,3]])
    result = zoning_scale_effect(x, edges, [4,3,2,1])
    assert np.all(np.diff(result["within_zone_sse"]) >= -1e-12)
    assert result["within_zone_sse"][0] == pytest.approx(0.)
    assert result["within_zone_sse"][-1] == pytest.approx(17.)


def test_spatial_ward_rejects_disconnected_graph_for_impossible_zone_count():
    with pytest.raises(ValueError, match="disconnected"):
        spatially_constrained_ward([[0.],[1.],[10.],[11.]],
                                   [[0,1],[2,3]], n_zones=1)


def test_spatial_zoning_validates_inputs():
    with pytest.raises(ValueError, match="attributes"):
        spatially_constrained_ward([], [], n_zones=1)
    with pytest.raises(ValueError, match="adjacency_edges"):
        spatially_constrained_ward([[0.],[1.]], [[0,1.5]], n_zones=1)
