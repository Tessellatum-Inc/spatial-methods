import math

import pytest

from network_queries import many_to_many_dijkstra, network_isochrone


def graph_fixture():
    return {
        "A": [("B", 2), ("C", 1)],
        "B": [("D", 2), ("E", 5)],
        "C": [("B", 0.5), ("D", 5)],
        "D": [("E", 1)],
        "E": [],
        "ISLAND": [],
    }


def test_many_to_many_returns_paths_and_costs_for_each_pair():
    result = many_to_many_dijkstra(graph_fixture(), ["A", "D"], ["B", "D", "E"])
    assert result["A"]["B"] == (["A", "C", "B"], 1.5)
    assert result["A"]["D"] == (["A", "C", "B", "D"], 3.5)
    assert result["D"]["E"] == (["D", "E"], 1.0)


def test_many_to_many_includes_unreachable_and_identity_pairs():
    result = many_to_many_dijkstra(graph_fixture(), ["A"], ["A", "ISLAND", "missing"])
    assert result["A"]["A"] == (["A"], 0.0)
    assert result["A"]["ISLAND"] == (None, math.inf)
    assert result["A"]["missing"] == (None, math.inf)


def test_many_to_many_defaults_to_all_graph_nodes():
    result = many_to_many_dijkstra(graph_fixture(), ["ISLAND"])
    assert set(result["ISLAND"]) == set(graph_fixture())
    assert result["ISLAND"]["ISLAND"] == (["ISLAND"], 0.0)


def test_isochrone_includes_nodes_at_exact_budget_and_frontier_arcs():
    result = network_isochrone(graph_fixture(), "A", 3.5)
    assert result["distances"] == {"A": 0.0, "B": 1.5, "C": 1.0, "D": 3.5}
    assert ("D", "E", 4.5) in result["frontier_edges"]
    assert all(distance <= 3.5 for distance in result["distances"].values())


def test_frontier_excludes_edges_to_nodes_already_inside_isochrone():
    graph = {"A": [("B", 3), ("C", 1)], "C": [("B", 0.5)], "B": []}
    result = network_isochrone(graph, "A", 2)
    assert result["distances"]["B"] == 1.5
    assert ("A", "B", 3.0) not in result["frontier_edges"]


def test_isochrone_budget_zero_returns_only_source():
    result = network_isochrone(graph_fixture(), "A", 0)
    assert result["distances"] == {"A": 0.0}
    assert len(result["frontier_edges"]) == 2


@pytest.mark.parametrize("budget", [-1, math.inf, math.nan])
def test_isochrone_rejects_invalid_budget(budget):
    with pytest.raises(ValueError, match="budget"):
        network_isochrone(graph_fixture(), "A", budget)


def test_queries_reject_negative_or_non_finite_edge_weights():
    with pytest.raises(ValueError, match="non-negative"):
        many_to_many_dijkstra({"A": [("B", -1)]}, ["A"])
    with pytest.raises(ValueError, match="non-negative"):
        network_isochrone({"A": [("B", math.inf)]}, "A", 10)
