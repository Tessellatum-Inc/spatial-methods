import pytest

from pareto_paths import pareto_shortest_paths


def test_returns_tradeoff_paths_and_discards_dominated_direct_path():
    graph = {
        "s": [("a", (1, 8)), ("b", (7, 1)), ("c", (4, 4)), ("t", (12, 12))],
        "a": [("t", (1, 2))],
        "b": [("t", (3, 1))],
        "c": [("t", (4, 4))],
        "t": [],
    }
    paths = pareto_shortest_paths(graph, "s", "t", n_objectives=2)
    assert [path["costs"] for path in paths] == [
        (2.0, 10.0), (8.0, 8.0), (10.0, 2.0)
    ]
    assert {path["path"] for path in paths} == {
        ("s", "a", "t"), ("s", "c", "t"), ("s", "b", "t")
    }


def test_dominated_labels_are_removed_at_intermediate_nodes():
    graph = {
        "s": [("a", (1, 1)), ("b", (2, 2))],
        "a": [("x", (1, 1))],
        "b": [("x", (1, 1))],
        "x": [("t", (1, 1))],
        "t": [],
    }
    paths = pareto_shortest_paths(graph, "s", "t", n_objectives=2)
    assert len(paths) == 1
    assert paths[0]["costs"] == (3.0, 3.0)
    assert paths[0]["path"] == ("s", "a", "x", "t")


def test_supports_three_objectives_and_zero_cost_edges():
    graph = {
        "s": [("a", (0, 1, 2)), ("b", (1, 0, 2)), ("c", (1, 2, 0))],
        "a": [("t", (1, 0, 1))],
        "b": [("t", (0, 2, 0))],
        "c": [("t", (1, 0, 1))],
        "t": [],
    }
    paths = pareto_shortest_paths(graph, "s", "t", n_objectives=3)
    assert len(paths) == 3
    assert {path["costs"] for path in paths} == {
        (1.0, 1.0, 3.0), (1.0, 2.0, 2.0), (2.0, 2.0, 1.0)
    }


def test_zero_cost_cycles_do_not_create_infinite_labels():
    graph = {
        "s": [("a", (0, 0))],
        "a": [("s", (0, 0)), ("t", (1, 1))],
        "t": [],
    }
    paths = pareto_shortest_paths(graph, "s", "t", n_objectives=2)
    assert len(paths) == 1
    assert paths[0]["path"] == ("s", "a", "t")


def test_unreachable_target_and_source_equal_target():
    assert pareto_shortest_paths(
        {"s": [("a", (1, 1))], "a": []}, "s", "z", n_objectives=2
    ) == []
    assert pareto_shortest_paths(
        {"s": []}, "s", "s", n_objectives=2
    ) == [{"costs": (0.0, 0.0), "path": ("s",)}]


def test_label_cap_raises_instead_of_silently_truncating():
    graph = {
        "s": [("a", (1, 5)), ("b", (5, 1))],
        "a": [("t", (0, 0))],
        "b": [("t", (0, 0))],
        "t": [],
    }
    with pytest.raises(RuntimeError, match="not truncated"):
        pareto_shortest_paths(
            graph, "s", "t", n_objectives=2, max_labels_per_node=1
        )


@pytest.mark.parametrize("graph,n", [
    ({"s": [("t", (-1, 2))], "t": []}, 2),
    ({"s": [("t", (1,))], "t": []}, 2),
    ({"s": [("t", (1, float("nan")))], "t": []}, 2),
])
def test_rejects_invalid_edge_costs(graph, n):
    with pytest.raises(ValueError):
        pareto_shortest_paths(graph, "s", "t", n_objectives=n)


def test_rejects_invalid_controls_and_adjacency():
    with pytest.raises(ValueError):
        pareto_shortest_paths({"s": []}, "s", "t", n_objectives=0)
    with pytest.raises(ValueError):
        pareto_shortest_paths({"s": None}, "s", "t", n_objectives=2)
    with pytest.raises(ValueError):
        pareto_shortest_paths(
            {"s": [("t", (1, 2))]}, "s", "t",
            n_objectives=2, max_labels_per_node=0
        )


def _enumerate_simple_path_costs(graph, source, target, dimensions):
    found = []

    def visit(node, path, costs):
        if node == target:
            found.append((tuple(costs), tuple(path)))
            return
        for neighbour, edge_costs in graph.get(node, []):
            if neighbour not in path:
                visit(neighbour, path + [neighbour],
                      tuple(a + b for a, b in zip(costs, edge_costs)))

    visit(source, [source], (0.0,) * dimensions)
    frontier = []
    for costs, path in found:
        if any(all(a <= b for a, b in zip(other, costs))
               for other, _ in found if other != costs):
            continue
        if any(other == costs for other, _ in frontier):
            continue
        frontier.append((costs, path))
    return {costs for costs, _ in frontier}


def test_pareto_frontier_matches_exhaustive_simple_path_oracle_on_seeded_graphs():
    import random

    rng = random.Random(271828)
    for _ in range(120):
        count = rng.randint(2, 7)
        graph = {node: [] for node in range(count)}
        for u in range(count):
            for v in range(count):
                if u != v and rng.random() < 0.24:
                    graph[u].append((v, (rng.randint(0, 8), rng.randint(0, 8))))
        expected = _enumerate_simple_path_costs(graph, 0, count - 1, 2)
        actual = pareto_shortest_paths(graph, 0, count - 1, n_objectives=2)
        assert {item["costs"] for item in actual} == expected
        for item in actual:
            assert item["path"][0] == 0 and item["path"][-1] == count - 1
            assert len(item["path"]) == len(set(item["path"]))


def test_pareto_paths_reject_nonfinite_accumulated_costs():
    graph = {
        "s": [("a", (1e308, 1e308))],
        "a": [("t", (1e308, 1e308))],
        "t": [],
    }
    with pytest.raises(ValueError, match="overflowed"):
        pareto_shortest_paths(graph, "s", "t", n_objectives=2)
