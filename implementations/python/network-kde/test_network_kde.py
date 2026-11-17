import math
import pytest
from network_kde import network_kde


def test_path_graph_matches_independent_gaussian_oracle():
    result = network_kde([("a", "b", 1), ("b", "c", 2)], ["a", "c"],
                         bandwidth=2, target_nodes=["a", "b", "c"])
    scale = math.sqrt(2 * math.pi) * 2
    expected = [(1 + math.exp(-0.5 * (3 / 2) ** 2)) / scale,
                (1 + math.exp(-0.5 * (1 / 2) ** 2)) / scale,
                (1 + math.exp(-0.5 * (3 / 2) ** 2)) / scale]
    assert result["density"] == pytest.approx(expected)


def test_cheapest_parallel_path_and_event_weights():
    result = network_kde([("a", "b", 9), ("a", "c", 1), ("c", "b", 1)],
                         ["b"], bandwidth=1, target_nodes=["a"], event_weights=[2])
    assert result["density"] == pytest.approx([2 * math.exp(-2) / math.sqrt(2 * math.pi)])


def test_disconnected_events_do_not_contribute():
    result = network_kde([("a", "b", 1), ("x", "y", 1)], ["x"],
                         bandwidth=1, target_nodes=["a", "b"])
    assert result["density"] == [0.0, 0.0]


def test_zero_weights_and_target_subset():
    result = network_kde([("a", "b", 1), ("b", "c", 1)], ["a"],
                         bandwidth=1, target_nodes=["c"], event_weights=[0])
    assert result["nodes"] == ["c"] and result["density"] == [0.0]


@pytest.mark.parametrize("h", [0, -1, float("nan"), float("inf"), True])
def test_invalid_bandwidth(h):
    with pytest.raises(ValueError, match="bandwidth"):
        network_kde([("a", "b", 1)], ["a"], bandwidth=h)


def test_invalid_graph_and_events():
    with pytest.raises(ValueError, match="at least one edge"):
        network_kde([], ["a"], bandwidth=1)
    with pytest.raises(ValueError, match="distinct nodes"):
        network_kde([("a", "a", 1)], ["a"], bandwidth=1)
    with pytest.raises(ValueError, match="event node"):
        network_kde([("a", "b", 1)], ["z"], bandwidth=1)
    with pytest.raises(ValueError, match="event_weights"):
        network_kde([("a", "b", 1)], ["a"], bandwidth=1, event_weights=[1, 2])
    with pytest.raises(ValueError, match="non-negative"):
        network_kde([("a", "b", 1)], ["a"], bandwidth=1, event_weights=[-1])
