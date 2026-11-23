import numpy as np
import pytest
from skater import skater


def test_chain_partition_cuts_between_feature_groups():
    x = np.array([[0.], [1.], [10.], [11.]])
    edges = [(0, 1, 1), (1, 2, 1), (2, 3, 1)]
    fit = skater(x, edges, 2)
    labels = fit["labels"]
    assert labels[0] == labels[1]
    assert labels[2] == labels[3]
    assert labels[0] != labels[2]
    assert fit["objective"] == pytest.approx(1.0)
    assert len(fit["mst_edges"]) == 3 and len(fit["cuts"]) == 1


def test_mst_uses_lowest_cost_edges_and_keeps_regions_connected():
    x = np.array([[0.], [1.], [8.], [9.]])
    edges = [(0, 1, 1), (1, 2, 4), (2, 3, 1), (0, 3, 20), (0, 2, 9)]
    fit = skater(x, edges, 2)
    assert {(u, v) for u, v, _ in fit["mst_edges"]} == {(0, 1), (1, 2), (2, 3)}
    assert fit["labels"][0] == fit["labels"][1]
    assert fit["labels"][2] == fit["labels"][3]
    assert fit["labels"][0] != fit["labels"][2]


def test_deterministic_ties_and_k_extremes():
    x = np.zeros((4, 2))
    edges = [(0, 1, 1), (1, 2, 1), (2, 3, 1), (0, 3, 1)]
    a = skater(x, edges, 3)
    b = skater(x, edges, 3)
    np.testing.assert_array_equal(a["labels"], b["labels"])
    assert len(a["cuts"]) == 2
    one = skater(x, edges, 1)
    assert len(set(one["labels"])) == 1
    all_singletons = skater(x, edges, 4)
    assert len(set(all_singletons["labels"])) == 4


def test_disconnected_graph_and_invalid_inputs_are_rejected():
    with pytest.raises(ValueError, match="connected"):
        skater(np.array([[0.], [1.], [2.]]), [(0, 1, 1)], 2)
    with pytest.raises(ValueError, match="finite"):
        skater(np.array([[0.], [np.nan]]), [(0, 1, 1)], 2)
    with pytest.raises(ValueError, match="between 1"):
        skater(np.array([[0.], [1.]]), [(0, 1, 1)], 3)
    with pytest.raises(ValueError, match="non-negative"):
        skater(np.array([[0.], [1.]]), [(0, 1, -1)], 2)
    with pytest.raises(ValueError, match="endpoints"):
        skater(np.array([[0.], [1.]]), [(0, 2, 1)], 2)
