import itertools

import pytest

from flow_capturing import flow_capturing_exact, flow_capturing_greedy


def test_exact_model_captures_each_path_weight_once():
    paths = {"p1": ["a", "b"], "p2": ["b", "c"], "p3": ["d"]}
    weights = {"p1": 10, "p2": 7, "p3": 5}
    result = flow_capturing_exact(paths, weights, ["a", "b", "c", "d"], 1)
    assert result == {"sites": ("b",), "objective": 17.0,
                      "captured_paths": ("p1", "p2")}


def test_exact_model_matches_independent_subset_oracle():
    paths = {"r1": ["a", "b"], "r2": ["b", "c"], "r3": ["a", "d"],
             "r4": ["c", "d"], "r5": ["b", "d"]}
    weights = {"r1": 3, "r2": 5, "r3": 7, "r4": 11, "r5": 13}
    sites = ["a", "b", "c", "d"]
    for p in range(5):
        candidates = []
        for subset in itertools.combinations(sites, p):
            covered = sum(weights[path_id] for path_id, path_sites in paths.items()
                          if set(subset) & set(path_sites))
            candidates.append((covered, subset))
        best = max(score for score, _ in candidates)
        actual = flow_capturing_exact(paths, weights, sites, p)
        assert actual["objective"] == best


def test_greedy_matches_exact_when_one_site_is_selected():
    paths = {"a": ["x"], "b": ["x", "y"], "c": ["y"]}
    weights = {"a": 3, "b": 5, "c": 2}
    assert flow_capturing_greedy(paths, weights, ["x", "y"], 1) == \
           flow_capturing_exact(paths, weights, ["x", "y"], 1)


def test_greedy_objective_never_exceeds_exact_optimum():
    paths = {"a": ["s1", "s2"], "b": ["s2", "s3"], "c": ["s4"],
             "d": ["s1", "s4"], "e": ["s3", "s4"]}
    weights = {"a": 9, "b": 7, "c": 6, "d": 4, "e": 3}
    exact = flow_capturing_exact(paths, weights, ["s1", "s2", "s3", "s4"], 2)
    greedy = flow_capturing_greedy(paths, weights, ["s1", "s2", "s3", "s4"], 2)
    assert greedy["objective"] <= exact["objective"]


def test_empty_path_and_zero_budget_are_valid():
    assert flow_capturing_exact({"empty": []}, {"empty": 8}, ["x"], 0) == {
        "sites": (), "objective": 0.0, "captured_paths": (),
    }


@pytest.mark.parametrize("paths,weights,sites,p", [
    ({"p": ["x"]}, {}, ["x"], 1),
    ({"p": ["unknown"]}, {"p": 1}, ["x"], 1),
    ({"p": ["x", "x"]}, {"p": 1}, ["x"], 1),
    ({"p": ["x"]}, {"p": -1}, ["x"], 1),
    ({"p": ["x"]}, {"p": float("nan")}, ["x"], 1),
    ({"p": ["x"]}, {"p": 1}, ["x", "x"], 1),
    ({"p": ["x"]}, {"p": 1}, ["x"], 2),
])
def test_invalid_models_are_rejected(paths, weights, sites, p):
    with pytest.raises(ValueError):
        flow_capturing_exact(paths, weights, sites, p)


def test_greedy_ties_are_deterministic_by_candidate_order():
    paths = {"a": ["second", "first"]}
    weights = {"a": 1}
    result = flow_capturing_greedy(paths, weights, ["second", "first"], 1)
    assert result["sites"] == ("second",)
