import math

import pytest

from c_logit_route_choice import c_logit_route_choice


LENGTHS = {"a": 1., "b": 1., "c": 1., "d": 2., "e": 1.}


def test_single_route_has_zero_commonality_and_probability_one():
    result = c_logit_route_choice([["a", "b"]], LENGTHS, [4.])
    assert result["commonality_factors"] == pytest.approx([0.])
    assert result["probabilities"] == pytest.approx([1.])


def test_disjoint_routes_reduce_to_multinomial_logit():
    routes = [["a", "b"], ["c", "d"]]
    utilities = [1.2, .4]
    result = c_logit_route_choice(routes, LENGTHS, utilities)
    expected = math.exp(1.2) / (math.exp(1.2) + math.exp(.4))
    assert result["commonality_factors"] == pytest.approx([0., 0.])
    assert result["probabilities"][0] == pytest.approx(expected)


def test_identical_routes_receive_equal_commonality_penalty():
    result = c_logit_route_choice([["a", "b"], ["a", "b"]], LENGTHS, [0., 0.])
    assert result["commonality_factors"] == pytest.approx([math.log(2), math.log(2)])
    assert result["probabilities"] == pytest.approx([.5, .5])


def test_partial_overlap_matches_hand_calculated_commonality():
    result = c_logit_route_choice([["a", "b"], ["b", "c"]], LENGTHS, [0., 0.], gamma=1)
    expected = math.log(1 + .5)
    assert result["commonality_factors"] == pytest.approx([expected, expected])
    assert result["shared_lengths"] == ((2., 1.), (1., 2.))


def test_overlap_penalty_reduces_probability_relative_to_mnl():
    routes = [["a", "b", "c"], ["a", "d"], ["e"]]
    utilities = [0., 0., 0.]
    mnl = c_logit_route_choice(routes, LENGTHS, utilities, beta_cf=0)
    adjusted = c_logit_route_choice(routes, LENGTHS, utilities, beta_cf=2)
    assert adjusted["probabilities"][2] > mnl["probabilities"][2]
    assert adjusted["probabilities"][0] < mnl["probabilities"][0]


def test_beta_zero_is_exact_multinomial_logit_and_probabilities_sum_to_one():
    result = c_logit_route_choice([["a"], ["b"], ["c"]], LENGTHS, [1000., 999., 998.], beta_cf=0)
    assert sum(result["probabilities"]) == pytest.approx(1.)
    assert result["probabilities"][0] > result["probabilities"][1] > result["probabilities"][2]


@pytest.mark.parametrize("kwargs", [
    {"beta_cf": -1}, {"beta_cf": float("nan")}, {"beta_cf": True},
    {"gamma": 0}, {"gamma": float("inf")}, {"gamma": "1"},
])
def test_invalid_model_parameters_are_rejected(kwargs):
    with pytest.raises(ValueError):
        c_logit_route_choice([["a"], ["b"]], LENGTHS, [0., 0.], **kwargs)


@pytest.mark.parametrize("routes,lengths,utilities", [
    ([], LENGTHS, []),
    ([[]], LENGTHS, [0.]),
    ([["missing"]], LENGTHS, [0.]),
    ([["a", "a"]], LENGTHS, [0.]),
    ([["a"], ["b"]], LENGTHS, [0.]),
    ([["a"]], {"a": 0}, [0.]),
    ([["a"]], {"a": float("inf")}, [0.]),
    ([["a"]], LENGTHS, [float("nan")]),
])
def test_invalid_route_inputs_are_rejected(routes, lengths, utilities):
    with pytest.raises(ValueError):
        c_logit_route_choice(routes, lengths, utilities)


def test_non_mapping_lengths_and_non_sequence_utilities_are_rejected():
    with pytest.raises(ValueError):
        c_logit_route_choice([["a"]], [1.], [0.])
    with pytest.raises(ValueError):
        c_logit_route_choice([["a"]], {"a": 1.}, None)
