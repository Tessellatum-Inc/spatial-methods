import math

import numpy as np
import pytest

from mobility_metrics import (
    maximum_predictability,
    radius_of_gyration,
    step_lengths,
    turning_angles,
    visit_entropy,
)


def test_radius_of_gyration_matches_two_point_case():
    assert radius_of_gyration([(0, 0), (2, 0)]) == pytest.approx(1.0)


def test_weighted_radius_of_gyration():
    assert radius_of_gyration([(0, 0), (2, 0)], weights=[3, 1]) == pytest.approx(math.sqrt(0.75))


def test_step_lengths_and_signed_turns():
    points = [(0, 0), (1, 0), (1, 1), (0, 1)]
    assert step_lengths(points) == pytest.approx([1, 1, 1])
    assert turning_angles(points) == pytest.approx([math.pi / 2, math.pi / 2])


def test_visit_entropy_and_effective_states():
    result = visit_entropy(["a", "a", "b", "b"])
    assert result["entropy_nats"] == pytest.approx(math.log(2))
    assert result["effective_states"] == pytest.approx(2)


def test_predictability_fano_bounds():
    assert maximum_predictability(0, 4) == pytest.approx(1)
    assert maximum_predictability(math.log(4), 4) == pytest.approx(0.25)
    value = maximum_predictability(math.log(2), 4)
    assert 0.25 < value < 1


def test_predictability_is_monotone_decreasing_in_entropy():
    entropies = np.linspace(0, math.log(5), 10)
    predictions = [maximum_predictability(float(h), 5) for h in entropies]
    assert np.all(np.diff(predictions) <= 1e-12)


def test_invalid_coordinates_and_duplicate_turn_points_rejected():
    with pytest.raises(ValueError):
        step_lengths([(0, 0)])
    with pytest.raises(ValueError):
        turning_angles([(0, 0), (0, 0), (1, 1)])
    with pytest.raises(ValueError):
        radius_of_gyration([(0, 0), (1, 1)], weights=[0, 0])


def test_empty_or_unhashable_visits_rejected():
    with pytest.raises(ValueError):
        visit_entropy([])
    with pytest.raises(ValueError):
        visit_entropy([[1], [2]])


def test_invalid_entropy_rejected():
    with pytest.raises(ValueError):
        maximum_predictability(2, 2)
