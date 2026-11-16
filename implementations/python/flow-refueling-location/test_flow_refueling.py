import itertools
import pytest
from flow_refueling import flow_refueling_exact

def test_exact_frml_requires_a_feasible_sequence_of_refueling_stops():
    paths = {"route": {"length": 18, "sites": {"a": 7, "b": 12}}}
    result = flow_refueling_exact(paths, {"route": 10}, ["a", "b"], 2, 10)
    assert result == {"sites": ("a", "b"), "objective": 10.0, "feasible_paths": ("route",)}

def test_single_station_may_be_insufficient_even_when_it_captures_path():
    paths = {"route": {"length": 18, "sites": {"a": 7, "b": 12}}}
    result = flow_refueling_exact(paths, {"route": 10}, ["a", "b"], 1, 10)
    assert result["objective"] == 0

def test_exact_solver_matches_independent_subset_oracle():
    paths = {
        "r1": {"length": 18, "sites": {"a": 7, "b": 12}},
        "r2": {"length": 25, "sites": {"a": 8, "b": 16}},
        "r3": {"length": 25, "sites": {"c": 5, "d": 20}},
    }
    weights = {"r1": 10, "r2": 20, "r3": 5}
    sites = ["a", "b", "c", "d"]
    for p in range(5):
        scores = []
        for chosen in itertools.combinations(sites, p):
            total = 0
            for path_id, path in paths.items():
                ordered = sorted(path["sites"][site] for site in chosen if site in path["sites"])
                previous = 0
                feasible = True
                for stop in ordered:
                    if stop - previous > 10:
                        feasible = False
                    previous = stop
                feasible = feasible and path["length"] - previous <= 10
                if feasible:
                    total += weights[path_id]
            scores.append(total)
        actual = flow_refueling_exact(paths, weights, sites, p, 10)
        assert actual["objective"] == max(scores)

def test_short_route_needs_no_station():
    result = flow_refueling_exact({"short": {"length": 8, "sites": {}}}, {"short": 3}, ["a"], 0, 10)
    assert result == {"sites": (), "objective": 3.0, "feasible_paths": ("short",)}

def test_station_gap_equal_to_range_is_feasible():
    paths = {"route": {"length": 20, "sites": {"a": 10}}}
    result = flow_refueling_exact(paths, {"route": 1}, ["a"], 1, 10)
    assert result["objective"] == 1

@pytest.mark.parametrize("paths,weights,sites,p,rng", [
    ({"r": {"length": 10, "sites": {}}}, {}, ["a"], 1, 5),
    ({"r": {"length": 10, "sites": {}}}, {"r": 1}, ["a", "a"], 1, 5),
    ({"r": {"length": 10, "sites": {}}}, {"r": 1}, ["a"], 2, 5),
    ({"r": {"length": 10, "sites": {"a": 11}}}, {"r": 1}, ["a"], 1, 5),
    ({"r": {"length": 10, "sites": {}}}, {"r": -1}, ["a"], 1, 5),
    ({"r": {"length": 10, "sites": {}}}, {"r": 1}, ["a"], 1, 0),
])
def test_invalid_frml_models_are_rejected(paths, weights, sites, p, rng):
    with pytest.raises(ValueError):
        flow_refueling_exact(paths, weights, sites, p, rng)
