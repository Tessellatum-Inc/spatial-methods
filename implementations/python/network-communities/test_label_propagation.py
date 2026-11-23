import pytest

from label_propagation import label_propagation


def _partition(labels):
    groups = {}
    for node, label in labels.items():
        groups.setdefault(label, set()).add(node)
    return {frozenset(group) for group in groups.values()}


def test_two_node_component_converges_to_one_community():
    labels = label_propagation({"A": ["B"], "B": ["A"]}, seed=2)
    assert labels["A"] == labels["B"]


def test_disconnected_components_do_not_exchange_labels():
    labels = label_propagation(
        {"A": ["B"], "B": ["A"], "C": ["D"], "D": ["C"], "I": []},
        seed=5,
    )
    assert labels["A"] == labels["B"]
    assert labels["C"] == labels["D"]
    assert labels["A"] != labels["C"]
    assert labels["I"] == "I"


def test_asymmetric_adjacency_is_treated_as_undirected():
    labels = label_propagation({"A": ["B"], "B": []}, seed=1)
    assert labels["A"] == labels["B"]


def test_seeded_run_is_reproducible():
    graph = {
        "A": ["B", "C"], "B": ["A", "C", "D"], "C": ["A", "B", "D"],
        "D": ["B", "C", "E"], "E": ["D", "F"], "F": ["E"],
    }
    assert label_propagation(graph, seed=17) == label_propagation(graph, seed=17)


def test_all_nodes_are_preserved_and_labels_are_node_identifiers():
    labels = label_propagation({"A": ["B"], "C": []}, seed=3)
    assert set(labels) == {"A", "B", "C"}
    assert set(labels.values()) <= set(labels)


def test_empty_graph_returns_empty_partition():
    assert label_propagation({}) == {}


@pytest.mark.parametrize("max_iter", [0, -1, 1.5, True])
def test_invalid_iteration_cap_is_rejected(max_iter):
    with pytest.raises(ValueError, match="max_iter"):
        label_propagation({"A": []}, max_iter=max_iter)


def test_invalid_seed_is_rejected():
    with pytest.raises(ValueError, match="seed"):
        label_propagation({"A": []}, seed=True)
