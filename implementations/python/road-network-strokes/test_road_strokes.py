import pytest

from road_strokes import generate_strokes


def test_straight_chain_becomes_one_stroke():
    nodes = {0: (0, 0), 1: (1, 0), 2: (2, 0), 3: (3, 0)}
    result = generate_strokes(nodes, [("a", 0, 1), ("b", 1, 2), ("c", 2, 3)])
    assert len(result) == 1
    assert set(result[0]["edge_ids"]) == {"a", "b", "c"}
    assert len(result[0]["node_ids"]) == 4
    assert not result[0]["closed"]


def test_right_angle_is_not_joined_at_default_threshold():
    nodes = {0: (0, 0), 1: (1, 0), 2: (1, 1)}
    result = generate_strokes(nodes, [("a", 0, 1), ("b", 1, 2)])
    assert len(result) == 2


def test_threshold_can_join_bent_edges():
    nodes = {0: (0, 0), 1: (1, 0), 2: (1, 1)}
    result = generate_strokes(nodes, [("a", 0, 1), ("b", 1, 2)], max_deviation_degrees=90)
    assert len(result) == 1


def test_three_way_junction_pairs_straightest_edges_only():
    nodes = {0: (0, 0), 1: (-1, 0), 2: (1, 0), 3: (0, 1)}
    result = generate_strokes(nodes, [("west", 0, 1), ("east", 0, 2), ("north", 0, 3)])
    assert len(result) == 2
    assert any(set(stroke["edge_ids"]) == {"west", "east"} for stroke in result)


def test_cycle_is_returned_as_closed_stroke():
    nodes = {0: (0, 0), 1: (1, 0), 2: (1, 1), 3: (0, 1)}
    edges = [("a", 0, 1), ("b", 1, 2), ("c", 2, 3), ("d", 3, 0)]
    result = generate_strokes(nodes, edges, max_deviation_degrees=90)
    assert len(result) == 1
    assert result[0]["closed"]
    assert result[0]["node_ids"][0] == result[0]["node_ids"][-1]


def test_every_edge_appears_exactly_once():
    nodes = {0: (0, 0), 1: (1, 0), 2: (2, 0), 3: (1, 1), 4: (2, 1)}
    edges = [("a", 0, 1), ("b", 1, 2), ("c", 1, 3), ("d", 2, 4)]
    result = generate_strokes(nodes, edges)
    all_ids = [edge for stroke in result for edge in stroke["edge_ids"]]
    assert sorted(all_ids) == sorted(edge[0] for edge in edges)


@pytest.mark.parametrize("nodes,edges", [
    ({0: (0, 0), 1: (0, 0)}, [("a", 0, 1)]),
    ({0: (0, 0)}, [("a", 0, 1)]),
    ({0: (0, 0), 1: (1, 0)}, [("a", 0, 1), ("a", 0, 1)]),
    ({0: (0, float("nan")), 1: (1, 0)}, [("a", 0, 1)]),
])
def test_invalid_graphs_rejected(nodes, edges):
    with pytest.raises(ValueError):
        generate_strokes(nodes, edges)


def test_invalid_angle_threshold_rejected():
    with pytest.raises(ValueError):
        generate_strokes({0: (0, 0), 1: (1, 0)}, [("a", 0, 1)], max_deviation_degrees=181)
