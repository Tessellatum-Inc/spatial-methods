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


def test_empty_candidate_set_is_valid_when_no_stations_are_selected():
    paths = {"short": {"length": 8, "sites": {}}, "zero": {"length": 0, "sites": {}}}
    result = flow_refueling_exact(paths, {"short": 3, "zero": 2}, [], 0, 10)
    assert result == {"sites": (), "objective": 5.0, "feasible_paths": ("short", "zero")}


def test_empty_candidate_set_cannot_serve_a_route_beyond_range():
    result = flow_refueling_exact({"long": {"length": 11, "sites": {}}}, {"long": 4}, [], 0, 10)
    assert result == {"sites": (), "objective": 0.0, "feasible_paths": ()}


def test_station_at_origin_or_destination_is_a_valid_refuel_option():
    paths = {"origin": {"length": 18, "sites": {"a": 0}}, "destination": {"length": 18, "sites": {"b": 18}}}
    result = flow_refueling_exact(paths, {"origin": 2, "destination": 3}, ["a", "b"], 1, 10)
    assert result["objective"] == 3.0
    assert result["feasible_paths"] == ("destination",)


@pytest.mark.parametrize("value", [True, float("inf"), float("-inf"), float("nan"), 10**10000])
def test_non_finite_or_non_numeric_range_values_are_rejected(value):
    with pytest.raises(ValueError):
        flow_refueling_exact({"r": {"length": 1, "sites": {}}}, {"r": 1}, ["a"], 0, value)


def test_non_iterable_candidate_sites_raise_a_model_error():
    with pytest.raises(ValueError, match="candidate_sites"):
        flow_refueling_exact({"r": {"length": 1, "sites": {}}}, {"r": 1}, None, 0, 5)


def test_seeded_random_small_instances_match_independent_route_and_subset_oracle():
    import random
    rng = random.Random(20261117)
    for _ in range(40):
        sites = [f"s{i}" for i in range(rng.randint(1, 6))]
        paths, weights = {}, {}
        for path_index in range(rng.randint(1, 5)):
            length = rng.randint(0, 35)
            available = rng.sample(sites, rng.randint(0, len(sites)))
            path_id = f"r{path_index}"
            paths[path_id] = {"length": length, "sites": {site: rng.randint(0, length) for site in available}}
            weights[path_id] = rng.randint(0, 20)
        vehicle_range, p = rng.randint(1, 12), rng.randint(0, len(sites))

        def oracle_feasible(path, selected):
            stops = sorted(path["sites"][site] for site in selected if site in path["sites"])
            boundaries = [0, *stops, path["length"]]
            return all(boundaries[i + 1] - boundaries[i] <= vehicle_range for i in range(len(boundaries) - 1))

        subsets = list(itertools.combinations(sites, p))
        expected = max(sum(weights[k] for k, path in paths.items() if oracle_feasible(path, chosen)) for chosen in subsets)
        actual = flow_refueling_exact(paths, weights, sites, p, vehicle_range)
        assert actual["objective"] == expected
        assert actual["sites"] in subsets
        assert sum(weights[k] for k in actual["feasible_paths"]) == actual["objective"]
