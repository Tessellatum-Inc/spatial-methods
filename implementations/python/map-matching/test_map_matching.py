import math
import pytest
from map_matching import generate_candidates, match_trace

def roads():
    return {"east": [(0, 0), (100, 0)], "north": [(50, -50), (50, 50)]}

def test_candidate_projection_and_radius():
    c = generate_candidates((20, 4), roads(), 10)
    assert c[0].edge_id == "east"
    assert (c[0].x, c[0].y) == (20, 0)
    assert c[0].distance == 4
    assert generate_candidates((20, 20), roads(), 5) == []

def test_viterbi_prefers_network_consistent_trace():
    obs = [(10, 2), (50, 3), (90, 2)]
    def distance(a, b):
        return 40 if a.edge_id == b.edge_id == "east" else 100
    result = match_trace(obs, roads(), distance, search_radius=10, emission_sigma=5, transition_beta=10)
    assert [m.edge_id for m in result] == ["east"] * 3
    assert [m.x for m in result] == [10, 50, 90]
    assert all(math.isfinite(m.log_probability) for m in result)

def test_unreachable_transition_is_rejected():
    with pytest.raises(ValueError, match="connected candidate"):
        match_trace([(10, 0), (90, 0)], roads(),
                    lambda a, b: math.inf, search_radius=1)

def test_no_candidate_reports_observation_index():
    with pytest.raises(ValueError, match="observation 1"):
        match_trace([(10, 0), (200, 200)], roads(), lambda a, b: 0)

def test_empty_trace():
    assert match_trace([], roads(), lambda a, b: 0) == []

def test_invalid_parameters_and_network_distance():
    with pytest.raises(ValueError):
        match_trace([(0, 0)], roads(), lambda a, b: 0, emission_sigma=0)
    with pytest.raises(ValueError):
        match_trace([(0, 0), (1, 0)], roads(), lambda a, b: -1)
