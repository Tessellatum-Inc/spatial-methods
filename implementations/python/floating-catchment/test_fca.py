import numpy as np
import pytest
from fca import two_step_fca, enhanced_two_step_fca


def test_two_step_fca_matches_hand_calculation():
    # Two demand points, one facility: ratio = 10 / (100 + 50) = 1/15.
    result = two_step_fca([[1], [3]], [100, 50], [10], 3)
    assert result["supply_demand_ratios"] == pytest.approx([1/15])
    assert result["accessibility"] == pytest.approx([1/15, 1/15])


def test_catchment_radius_excludes_outside_and_keeps_boundary():
    result = two_step_fca([[2], [2.01]], [10, 10], [4], 2)
    assert result["catchment_weights"][:, 0].tolist() == [1, 0]
    assert result["accessibility"].tolist() == pytest.approx([.4, 0])


def test_e2sfca_distance_decay_zones_and_accessibility():
    result = enhanced_two_step_fca(
        [[0, 4], [2, 8], [7, 3]], [10, 20, 30], [6, 9],
        [2, 5, 10], [1, .5, .1],
    )
    expected_weights = np.array([[1, .5], [.5, .1], [.1, .5]])
    assert result["catchment_weights"] == pytest.approx(expected_weights)
    ratios = [6/(10*1+20*.5+30*.1), 9/(10*.5+20*.1+30*.5)]
    assert result["supply_demand_ratios"] == pytest.approx(ratios)
    assert result["accessibility"] == pytest.approx(expected_weights @ ratios)


def test_unserved_demand_and_unreachable_supply_are_zero_safe():
    result = two_step_fca([[100, 100]], [20], [5, 7], 1)
    assert result["accessibility"] == pytest.approx([0])
    assert result["supply_demand_ratios"] == pytest.approx([0, 0])


@pytest.mark.parametrize("distance,demand,supply", [
    ([[-1]], [1], [1]), ([[np.nan]], [1], [1]),
    ([[1, 2]], [-1], [1, 2]), ([[1]], [1], [-1]),
    ([[1, 2]], [1], [1]),
])
def test_invalid_core_inputs_are_rejected(distance, demand, supply):
    with pytest.raises(ValueError):
        two_step_fca(distance, demand, supply, 5)


def test_invalid_radius_and_zone_definitions_are_rejected():
    with pytest.raises(ValueError):
        two_step_fca([[1]], [1], [1], 0)
    with pytest.raises(ValueError):
        enhanced_two_step_fca([[1]], [1], [1], [2, 1], [1, .5])
    with pytest.raises(ValueError):
        enhanced_two_step_fca([[1]], [1], [1], [2], [0])
