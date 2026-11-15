import math

import pytest

from maximum_flow import maximum_flow_min_cut


def test_dinic_matches_classic_six_node_max_flow_min_cut():
    graph = {
        "s": [("v1", 16), ("v2", 13)],
        "v1": [("v2", 10), ("v3", 12)],
        "v2": [("v1", 4), ("v4", 14)],
        "v3": [("v2", 9), ("t", 20)],
        "v4": [("v3", 7), ("t", 4)],
        "t": [],
    }
    result = maximum_flow_min_cut(graph, "s", "t")
    assert result["value"] == pytest.approx(23)
    assert result["cut_capacity"] == pytest.approx(23)
    assert result["source_side"] == {"s", "v1", "v2", "v4"}
    assert result["sink_side"] == {"v3", "t"}


def test_parallel_and_antiparallel_arcs_remain_distinct():
    graph = {
        "s": [("a", 2), ("a", 3), ("b", 1)],
        "a": [("s", 4), ("t", 4)],
        "b": [("a", 2), ("t", 1)],
        "t": [],
    }
    result = maximum_flow_min_cut(graph, "s", "t")
    assert result["value"] == pytest.approx(5)
    assert len(result["edge_flows"]) == 7
    assert all(edge["flow"] <= edge["capacity"] + 1e-12
               for edge in result["edge_flows"])
    assert result["cut_capacity"] == pytest.approx(result["value"])


def test_zero_capacity_and_unreachable_sink():
    result = maximum_flow_min_cut({"s": [("a", 0)], "a": []}, "s", "t")
    assert result["value"] == 0
    assert result["source_side"] == {"s"}
    assert result["sink_side"] == {"a", "t"}


def test_flow_conservation_at_intermediate_nodes():
    graph = {"s": [("a", 4), ("b", 3)], "a": [("b", 2), ("t", 2)],
             "b": [("t", 4)], "t": []}
    result = maximum_flow_min_cut(graph, "s", "t")
    net = {}
    for edge in result["edge_flows"]:
        net[edge["from"]] = net.get(edge["from"], 0) - edge["flow"]
        net[edge["to"]] = net.get(edge["to"], 0) + edge["flow"]
    for node in ("a", "b"):
        assert net[node] == pytest.approx(0)
    assert -net["s"] == pytest.approx(result["value"])
    assert net["t"] == pytest.approx(result["value"])


@pytest.mark.parametrize("capacity", [-1, math.inf, math.nan])
def test_invalid_capacities_are_rejected(capacity):
    with pytest.raises(ValueError, match="capacities"):
        maximum_flow_min_cut({"s": [("t", capacity)]}, "s", "t")


def test_self_loops_and_identical_terminals_are_rejected():
    with pytest.raises(ValueError, match="self-loop"):
        maximum_flow_min_cut({"s": [("s", 1)]}, "s", "t")
    with pytest.raises(ValueError, match="different"):
        maximum_flow_min_cut({"s": []}, "s", "s")
