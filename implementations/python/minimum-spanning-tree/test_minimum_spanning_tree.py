import math

import pytest

from minimum_spanning_tree import minimum_spanning_tree


def test_kruskal_returns_known_minimum_spanning_tree():
    nodes = ["A", "B", "C", "D"]
    edges = [
        ("A", "B", 1), ("A", "C", 4), ("B", "C", 2),
        ("B", "D", 5), ("C", "D", 3),
    ]
    result = minimum_spanning_tree(nodes, edges)
    assert result["total_weight"] == pytest.approx(6)
    assert len(result["edges"]) == 3
    assert result["components"] == 1
    assert result["is_spanning_tree"] is True


def test_disconnected_graph_returns_minimum_spanning_forest():
    result = minimum_spanning_tree(
        ["A", "B", "C", "D"], [("A", "B", 2), ("C", "D", 1)]
    )
    assert result["total_weight"] == pytest.approx(3)
    assert result["components"] == 2
    assert result["is_spanning_tree"] is False


def test_negative_weights_parallel_edges_and_self_loops():
    result = minimum_spanning_tree(
        ["A", "B", "C"],
        [("A", "A", -100), ("A", "B", 3), ("A", "B", -2), ("B", "C", 1)],
    )
    assert result["total_weight"] == pytest.approx(-1)
    assert len(result["edges"]) == 2


def test_equal_weight_ties_are_deterministic_by_input_order():
    edges = [("A", "B", 1), ("B", "C", 1), ("A", "C", 1)]
    first = minimum_spanning_tree(["A", "B", "C"], edges)
    second = minimum_spanning_tree(["A", "B", "C"], edges)
    assert first == second
    assert [edge["edge_index"] for edge in first["edges"]] == [0, 1]


def test_empty_and_singleton_graphs():
    assert minimum_spanning_tree([], [])["is_spanning_tree"] is True
    result = minimum_spanning_tree(["A"], [])
    assert result["components"] == 1
    assert result["edges"] == []


def test_invalid_endpoints_weights_and_nodes_are_rejected():
    with pytest.raises(ValueError, match="unique"):
        minimum_spanning_tree(["A", "A"], [])
    with pytest.raises(ValueError, match="endpoint"):
        minimum_spanning_tree(["A"], [("A", "B", 1)])
    with pytest.raises(ValueError, match="finite"):
        minimum_spanning_tree(["A", "B"], [("A", "B", math.inf)])
    with pytest.raises(ValueError, match="three"):
        minimum_spanning_tree(["A", "B"], [("A", "B")])


def test_total_weight_uses_accurate_summation_for_mixed_magnitudes():
    result = minimum_spanning_tree(
        [0, 1, 2, 3],
        [(0, 1, -1e16), (1, 2, 1.0), (2, 3, 1e16)],
    )
    assert result["total_weight"] == 1.0


def test_total_weight_overflow_is_reported_explicitly():
    with pytest.raises(OverflowError, match="exceeds finite"):
        minimum_spanning_tree(
            [0, 1, 2],
            [(0, 1, 1e308), (1, 2, 1e308)],
        )


def _brute_force_mst_weight(nodes, edges):
    from itertools import combinations

    best = math.inf
    for subset in combinations(edges, len(nodes) - 1):
        parent = {node: node for node in nodes}

        def find(node):
            while parent[node] != node:
                node = parent[node]
            return node

        valid = True
        for u, v, _weight in subset:
            ru, rv = find(u), find(v)
            if ru == rv:
                valid = False
                break
            parent[ru] = rv
        if valid and len({find(node) for node in nodes}) == 1:
            best = min(best, math.fsum(edge[2] for edge in subset))
    return best


def test_kruskal_matches_exhaustive_spanning_tree_oracle_on_seeded_graphs():
    import random

    rng = random.Random(8675309)
    for _ in range(100):
        count = rng.randint(2, 6)
        edges = [(node, node + 1, rng.randint(-20, 30))
                 for node in range(count - 1)]
        for u in range(count):
            for v in range(u + 2, count):
                if rng.random() < 0.45:
                    edges.append((u, v, rng.randint(-20, 30)))
        expected = _brute_force_mst_weight(list(range(count)), edges)
        actual = minimum_spanning_tree(list(range(count)), edges)
        assert actual["total_weight"] == pytest.approx(expected)
        assert len(actual["edges"]) == count - 1
