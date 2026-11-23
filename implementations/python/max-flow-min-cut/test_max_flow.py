import itertools
import random

import pytest

from max_flow import edmonds_karp, minimum_cut


def test_classic_six_node_network_max_flow_and_cut():
    edges = [
        ("s", "v1", 16), ("s", "v2", 13), ("v1", "v2", 10),
        ("v2", "v1", 4), ("v1", "v3", 12), ("v3", "v2", 9),
        ("v2", "v4", 14), ("v4", "v3", 7), ("v3", "t", 20),
        ("v4", "t", 4),
    ]
    value, _ = edmonds_karp(edges, "s", "t")
    cut, source_side, sink_side = minimum_cut(edges, "s", "t")
    assert value == pytest.approx(23)
    assert cut == pytest.approx(23)
    assert "s" in source_side and "t" in sink_side
    assert source_side.isdisjoint(sink_side)


def test_parallel_and_antiparallel_edges():
    edges = [("s", "a", 2), ("s", "a", 3), ("a", "s", 7), ("a", "t", 4)]
    value, flow = edmonds_karp(edges, "s", "t")
    assert value == pytest.approx(4)
    assert flow[("s", "a")] <= 5
    assert flow[("a", "t")] == pytest.approx(4)


def test_disconnected_sink_has_zero_flow():
    assert edmonds_karp([("s", "a", 3), ("b", "t", 4)], "s", "t")[0] == 0
    cut, left, right = minimum_cut([("s", "a", 3), ("b", "t", 4)], "s", "t")
    assert cut == 0
    assert "s" in left and "t" in right


def test_zero_capacity_edges_are_valid():
    assert edmonds_karp([("s", "t", 0)], "s", "t")[0] == 0


@pytest.mark.parametrize("edges,source,sink", [
    ([("s", "t", -1)], "s", "t"),
    ([("s", "t", float("nan"))], "s", "t"),
    ([("s", "t", float("inf"))], "s", "t"),
    ([("s", "s", 1)], "s", "t"),
    ([("s", "t", True)], "s", "t"),
])
def test_invalid_network_edges_rejected(edges, source, sink):
    with pytest.raises(ValueError):
        edmonds_karp(edges, source, sink)


def test_source_and_sink_must_differ():
    with pytest.raises(ValueError):
        edmonds_karp([("s", "t", 1)], "s", "s")


def _brute_min_cut(edges, source, sink):
    nodes = sorted({source, sink} | {u for u, _, _ in edges} | {v for _, v, _ in edges})
    middle = [node for node in nodes if node not in (source, sink)]
    best = float("inf")
    for mask in range(1 << len(middle)):
        left = {source} | {node for i, node in enumerate(middle) if mask & (1 << i)}
        capacity = sum(c for u, v, c in edges if u in left and v not in left)
        best = min(best, capacity)
    return best


def test_seeded_random_graphs_match_independent_exhaustive_min_cut_oracle():
    rng = random.Random(2701)
    for _ in range(100):
        n = rng.randint(2, 7)
        nodes = list(range(n))
        edges = []
        for u in nodes:
            for v in nodes:
                if u != v and rng.random() < 0.24:
                    edges.append((u, v, rng.randint(0, 9)))
        if not edges:
            edges = [(0, n - 1, 0)]
        expected = _brute_min_cut(edges, 0, n - 1)
        actual, _ = edmonds_karp(edges, 0, n - 1)
        cut, _, _ = minimum_cut(edges, 0, n - 1)
        assert actual == pytest.approx(expected)
        assert cut == pytest.approx(expected)


def test_sub_tolerance_positive_capacity_is_not_discarded():
    edges = [("s", "a", 1e-16), ("a", "t", 1e-16)]
    value, _ = edmonds_karp(edges, "s", "t")
    cut, left, right = minimum_cut(edges, "s", "t")
    assert value == pytest.approx(1e-16, rel=1e-12)
    assert cut == pytest.approx(value, rel=1e-12)
    assert "s" in left and "t" in right
