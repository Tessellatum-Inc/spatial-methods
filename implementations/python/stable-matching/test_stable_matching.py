import pytest

from stable_matching import blocking_pairs, stable_matching


def test_classic_resident_proposing_example_is_stable():
    residents = {
        "A": ["X", "Y", "Z"],
        "B": ["Y", "X", "Z"],
        "C": ["Y", "Z", "X"],
    }
    hospitals = {
        "X": ["B", "A", "C"],
        "Y": ["A", "B", "C"],
        "Z": ["A", "B", "C"],
    }
    result = stable_matching(residents, hospitals)
    assert result == {"A": "X", "B": "Y", "C": "Z"}
    assert blocking_pairs(residents, hospitals, result) == []


def test_hospital_capacity_can_exceed_one():
    residents = {"a": ["h"], "b": ["h"], "c": ["h"]}
    hospitals = {"h": ["b", "a", "c"]}
    result = stable_matching(residents, hospitals, {"h": 2})
    assert result == {"a": "h", "b": "h", "c": None}
    assert blocking_pairs(residents, hospitals, result, {"h": 2}) == []


def test_incomplete_lists_make_unlisted_pairs_unacceptable():
    residents = {"a": ["x", "y"], "b": ["x"]}
    hospitals = {"x": ["b", "a"], "y": []}
    assert stable_matching(residents, hospitals) == {"a": "y", "b": "x"}


def test_hospital_may_reject_resident_not_on_its_list():
    residents = {"a": ["x", "y"]}
    hospitals = {"x": [], "y": ["a"]}
    assert stable_matching(residents, hospitals) == {"a": "y"}


def test_zero_capacity_hospital_is_never_assigned():
    residents = {"a": ["x", "y"]}
    hospitals = {"x": ["a"], "y": ["a"]}
    assert stable_matching(residents, hospitals, {"x": 0, "y": 1}) == {"a": "y"}


def test_unmatched_resident_exhausts_preferences():
    residents = {"a": ["x"], "b": ["x"]}
    hospitals = {"x": ["a", "b"]}
    assert stable_matching(residents, hospitals) == {"a": "x", "b": None}


def test_empty_market():
    assert stable_matching({}, {}) == {}


@pytest.mark.parametrize("residents,hospitals,capacities", [
    ({"a": ["x", "x"]}, {"x": ["a"]}, None),
    ({"a": ["unknown"]}, {"x": ["a"]}, None),
    ({"a": ["x"]}, {"x": ["a", "a"]}, None),
    ({"a": ["x"]}, {"x": ["unknown"]}, None),
    ({"a": ["x"]}, {"x": ["a"]}, {"x": -1}),
    ({"a": ["x"]}, {"x": ["a"]}, {"x": 1.5}),
    ({"a": ["x"]}, {"x": ["a"]}, {"unknown": 1}),
])
def test_invalid_preferences_and_capacities_are_rejected(residents, hospitals, capacities):
    with pytest.raises(ValueError):
        stable_matching(residents, hospitals, capacities)


def test_blocking_pair_audit_detects_an_unstable_assignment():
    residents = {"a": ["x", "y"], "b": ["x", "y"]}
    hospitals = {"x": ["a", "b"], "y": ["b", "a"]}
    unstable = {"a": "y", "b": "x"}
    assert blocking_pairs(residents, hospitals, unstable) == [("a", "x")]


def test_blocking_pair_audit_rejects_over_capacity_assignment():
    with pytest.raises(ValueError, match="capacity"):
        blocking_pairs(
            {"a": ["x"], "b": ["x"]},
            {"x": ["a", "b"]},
            {"a": "x", "b": "x"},
            {"x": 1},
        )
