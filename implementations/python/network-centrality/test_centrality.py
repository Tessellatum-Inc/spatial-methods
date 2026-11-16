import math

import pytest

from centrality import betweenness_centrality, closeness_centrality, pagerank


def test_brandes_betweenness_on_directed_chain():
    graph = {"A": [("B", 1)], "B": [("C", 1)], "C": []}
    scores = betweenness_centrality(graph)
    assert scores == pytest.approx({"A": 0, "B": 0.5, "C": 0})


def test_brandes_betweenness_on_directed_diamond():
    graph = {"A": [("B", 1), ("C", 1)], "B": [("D", 1)], "C": [("D", 1)], "D": []}
    scores = betweenness_centrality(graph)
    assert scores["B"] == pytest.approx(1 / 12)
    assert scores["C"] == pytest.approx(1 / 12)
    raw = betweenness_centrality(graph, normalized=False)
    assert raw["B"] == pytest.approx(0.5)
    assert raw["C"] == pytest.approx(0.5)
    assert scores["A"] == scores["D"] == 0


def test_weighted_brandes_uses_shortest_path_dag():
    graph = {"A": [("B", 1), ("C", 5)], "B": [("C", 1)], "C": [("D", 1)], "D": []}
    scores = betweenness_centrality(graph, weighted=True, normalized=False)
    assert scores["B"] > 0
    assert scores["C"] > 0


def test_betweenness_handles_disconnected_and_small_graphs():
    assert betweenness_centrality({"A": [], "B": []}) == {"A": 0, "B": 0}
    assert betweenness_centrality({"A": [("B", 1)]}) == {"A": 0, "B": 0}


def test_closeness_is_inward_and_reachability_corrected():
    graph = {"A": [("B", 1)], "B": [("C", 1)], "C": [], "X": []}
    scores = closeness_centrality(graph)
    assert scores["C"] == pytest.approx(4 / 9)
    assert scores["B"] == pytest.approx(1 / 3)
    assert scores["A"] == 0
    assert scores["X"] == 0


def test_closeness_on_complete_directed_graph():
    graph = {u: [(v, 1) for v in "ABC" if v != u] for u in "ABC"}
    assert closeness_centrality(graph) == pytest.approx({"A": 1, "B": 1, "C": 1})


def test_pagerank_sums_to_one_and_ranks_linked_authority():
    graph = {"A": [("B", 1), ("C", 1)], "B": [("C", 1)], "C": [("A", 1)]}
    scores = pagerank(graph)
    assert sum(scores.values()) == pytest.approx(1)
    assert scores["C"] > scores["B"]


def test_pagerank_dangling_nodes_redistribute_rank():
    scores = pagerank({"A": [("B", 1)], "B": []})
    assert sum(scores.values()) == pytest.approx(1)
    assert all(value > 0 for value in scores.values())


def test_pagerank_weighted_outgoing_edges_change_transition_probability():
    scores = pagerank({"A": [("B", 9), ("C", 1)], "B": [], "C": []})
    assert scores["B"] > scores["C"]


def test_pagerank_personalization_is_respected():
    scores = pagerank({"A": [], "B": []}, personalization={"A": 9, "B": 1})
    assert scores["A"] == pytest.approx(0.9)
    assert scores["B"] == pytest.approx(0.1)


@pytest.mark.parametrize("alpha", [-0.1, 1, math.inf, math.nan])
def test_pagerank_rejects_invalid_damping(alpha):
    with pytest.raises(ValueError, match="alpha"):
        pagerank({"A": []}, alpha=alpha)


def test_pagerank_rejects_invalid_personalization_and_iteration_cap():
    with pytest.raises(ValueError, match="personalization"):
        pagerank({"A": [], "B": []}, personalization={"A": -1, "B": 1})
    with pytest.raises(ValueError, match="max_iter"):
        pagerank({"A": []}, max_iter=0)
    with pytest.raises(RuntimeError, match="did not converge"):
        pagerank({"A": [("A", 1)], "B": [("A", 1)]}, max_iter=1, tolerance=1e-30)


def test_betweenness_rejects_zero_weight_in_weighted_mode():
    with pytest.raises(ValueError, match="strictly positive"):
        betweenness_centrality({"A": [("B", 0)]}, weighted=True)
