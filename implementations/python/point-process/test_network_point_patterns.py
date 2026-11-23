import math
import pytest

from network_point_patterns import network_event_distance_matrix, network_ripley_k


def test_network_distances_use_direct_same_edge_and_network_routes():
    edges = [("a", "b", 10), ("b", "c", 10), ("a", "c", 30)]
    events = [(0, 2), (0, 8), (1, 4)]
    matrix = network_event_distance_matrix(edges, events)
    assert matrix[0][1] == pytest.approx(6)
    assert matrix[1][2] == pytest.approx(6)
    assert matrix[0][2] == pytest.approx(12)


def test_network_distance_uses_shorter_alternate_route_around_cycle():
    edges = [("a", "b", 10), ("b", "c", 10), ("c", "d", 10), ("d", "a", 2)]
    events = [(0, 1), (2, 9)]
    matrix = network_event_distance_matrix(edges, events)
    # a-side route: 1 + 2 + 1 + 1 = 5 (d-to-c 1), shorter than via b/c.
    assert matrix[0][1] == pytest.approx(4)


def test_network_k_counts_ordered_pairs_and_scales_by_total_network_length():
    edges = [(0, 1, 10), (1, 2, 10)]
    events = [(0, 2), (0, 8), (1, 4)]
    result = network_ripley_k(edges, events, [5, 6, 12])
    assert result["network_length"] == 20
    assert result["k_values"] == pytest.approx([0, 40/3, 20])
    assert result["edge_correction"] == "none"


def test_disconnected_event_pairs_have_infinite_distance_and_do_not_count():
    edges = [(0, 1, 5), (2, 3, 5)]
    result = network_ripley_k(edges, [(0, 2), (1, 2)], [100])
    assert math.isinf(result["distance_matrix"][0][1])
    assert result["k_values"] == [0]


def test_network_validation_rejects_bad_edges_and_events():
    with pytest.raises(ValueError, match="positive finite"):
        network_event_distance_matrix([(0, 1, 0)], [(0, 0), (0, 0)])
    with pytest.raises(ValueError, match="edge_index"):
        network_event_distance_matrix([(0, 1, 2)], [(1, 0), (0, 1)])
    with pytest.raises(ValueError, match="within its edge"):
        network_event_distance_matrix([(0, 1, 2)], [(0, 0), (0, 3)])
    with pytest.raises(ValueError, match="at least two"):
        network_event_distance_matrix([(0, 1, 2)], [(0, 1)])
    with pytest.raises(ValueError, match="radii"):
        network_ripley_k([(0, 1, 2)], [(0, 0), (0, 1)], [])


def test_parallel_edges_are_supported_and_choose_shortest_path():
    edges = [(0, 1, 10), (0, 1, 3)]
    events = [(0, 1), (0, 9)]
    matrix = network_event_distance_matrix(edges, events)
    assert matrix[0][1] == pytest.approx(5)
