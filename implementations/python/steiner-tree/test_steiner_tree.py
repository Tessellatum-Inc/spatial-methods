import pytest

from steiner_tree import steiner_tree


def test_two_terminals_use_shortest_path():
    result = steiner_tree(
        ["A", "B", "C"], [("A", "B", 1), ("B", "C", 1), ("A", "C", 3)],
        ["A", "C"],
    )
    assert result["total_weight"] == pytest.approx(2)
    assert len(result["edges"]) == 2
    assert {"A", "B", "C"} == result["nodes"]


def test_three_terminal_star_is_optimal_steiner_tree():
    result = steiner_tree(
        ["S", "A", "B", "C"],
        [("S", "A", 1), ("S", "B", 1), ("S", "C", 1),
         ("A", "B", 2), ("B", "C", 2), ("A", "C", 2)],
        ["A", "B", "C"],
    )
    assert result["total_weight"] == pytest.approx(3)
    assert result["nodes"] == {"S", "A", "B", "C"}


def test_triangle_three_terminals_returns_two_edge_tree():
    result = steiner_tree(
        ["A", "B", "C"], [("A", "B", 1), ("B", "C", 1), ("A", "C", 1)],
        ["A", "B", "C"],
    )
    assert result["total_weight"] == pytest.approx(2)
    assert len(result["edges"]) == 2


def test_one_terminal_has_zero_cost_tree():
    result = steiner_tree(["A", "B"], [("A", "B", 4)], ["A"])
    assert result["total_weight"] == 0
    assert result["edges"] == []
    assert result["nodes"] == {"A"}


def test_parallel_edges_keep_minimum_weight_and_self_loops_are_ignored():
    result = steiner_tree(
        ["A", "B", "C"],
        [("A", "A", 0.1), ("A", "B", 5), ("A", "B", 2), ("B", "C", 1)],
        ["A", "C"],
    )
    assert result["total_weight"] == pytest.approx(3)


def test_disconnected_terminals_raise():
    with pytest.raises(ValueError, match="no connected"):
        steiner_tree(["A", "B"], [], ["A", "B"])


def test_terminal_limit_is_enforced():
    with pytest.raises(ValueError, match="max_terminals"):
        steiner_tree(["A", "B"], [("A", "B", 1)], ["A", "B"], max_terminals=1)


def test_invalid_nodes_terminals_and_weights_are_rejected():
    with pytest.raises(ValueError, match="unique"):
        steiner_tree(["A", "A"], [], ["A"])
    with pytest.raises(ValueError, match="non-empty and unique"):
        steiner_tree(["A"], [], [])
    with pytest.raises(ValueError, match="in nodes"):
        steiner_tree(["A"], [], ["B"])
    with pytest.raises(ValueError, match="strictly positive"):
        steiner_tree(["A", "B"], [("A", "B", 0)], ["A", "B"])
