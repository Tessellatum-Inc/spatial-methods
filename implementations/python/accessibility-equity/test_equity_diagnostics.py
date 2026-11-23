import math
import pytest
from equity_diagnostics import (weighted_gini, weighted_lorenz_curve, weighted_quantile,
    accessibility_summary, group_accessibility_summary, group_mean_gap)


def test_gini_equal_unequal_and_zero():
    assert weighted_gini([4, 4, 4]) == pytest.approx(0)
    assert weighted_gini([0, 10]) == pytest.approx(.5)
    assert weighted_gini([0, 0, 10]) == pytest.approx(2/3)
    assert weighted_gini([0, 0, 0]) == 0
    p, l = weighted_lorenz_curve([0, 0, 0])
    assert l == pytest.approx(p)


def test_weights_equivalent_to_replication():
    assert weighted_gini([0, 10], [2, 1]) == pytest.approx(weighted_gini([0, 0, 10]))


def test_lorenz_endpoints_and_weighting():
    p, a = weighted_lorenz_curve([0, 10], [2, 1])
    assert p == pytest.approx([0, 2/3, 1])
    assert a == pytest.approx([0, 0, 1])


def test_quantiles():
    assert weighted_quantile([1, 9, 5], .5, [1, 1, 2]) == 5
    assert weighted_quantile([1, 9], 0) == 1
    assert weighted_quantile([1, 9], 1) == 9


def test_summary_and_shortfall():
    s = accessibility_summary([2, 8], [3, 1], minimum_threshold=5)
    assert s["weighted_mean"] == pytest.approx(3.5)
    assert s["population_share_below_threshold"] == pytest.approx(.75)


def test_groups_and_gap():
    g = group_accessibility_summary([2, 4, 8], ["A", "A", "B"], [1, 3, 2])
    gap = group_mean_gap(g)
    assert g["A"]["weighted_mean"] == pytest.approx(3.5)
    assert gap["absolute_gap"] == pytest.approx(4.5)
    assert gap["lowest_to_highest_ratio"] == pytest.approx(3.5/8)


@pytest.mark.parametrize("values", [[], [-1, 2], [1, math.inf], [1, math.nan]])
def test_invalid_values(values):
    with pytest.raises(ValueError):
        weighted_gini(values)


@pytest.mark.parametrize("weights", [[], [-1, 2], [1, math.inf], [0, 0]])
def test_invalid_weights(weights):
    with pytest.raises(ValueError):
        weighted_gini([1, 2], weights)


def test_mismatched_groups_and_invalid_quantile():
    with pytest.raises(ValueError):
        group_accessibility_summary([1, 2], ["A"])
    with pytest.raises(ValueError):
        weighted_quantile([1, 2], 1.1)


def test_summary_minimum_and_maximum_ignore_zero_population_weight():
    summary = accessibility_summary([0, 5, 100], [0, 2, 0])
    assert summary["minimum"] == 5
    assert summary["maximum"] == 5
    assert summary["weighted_mean"] == 5


def test_zero_weight_group_omitted_and_zero_ratio():
    g = group_accessibility_summary([2, 8], ["A", "B"], [1, 0])
    assert list(g) == ["A"]
    assert group_mean_gap({"A": {"weighted_mean": 0}, "B": {"weighted_mean": 0}})["lowest_to_highest_ratio"] == 1


def test_empty_group_gap_rejected():
    with pytest.raises(ValueError):
        group_mean_gap({})



def test_atkinson_known_values_and_aversion():
    from equity_diagnostics import weighted_atkinson
    assert weighted_atkinson([2, 2, 2], 1) == pytest.approx(0)
    assert weighted_atkinson([1, 3], 1) == pytest.approx(1 - math.sqrt(3)/2)
    assert weighted_atkinson([1, 3], 2) == pytest.approx(.25)
    assert weighted_atkinson([1, 3], .5) == pytest.approx(
        1 - (((1 + math.sqrt(3))/2) ** 2) / 2
    )


def test_atkinson_zero_values_and_weight_replication():
    from equity_diagnostics import weighted_atkinson
    assert weighted_atkinson([0, 10], .5, [2, 1]) == pytest.approx(2/3)
    assert weighted_atkinson([0, 10], 1, [2, 1]) == pytest.approx(1)
    assert weighted_atkinson([0, 10], 2, [2, 1]) == pytest.approx(1)
    assert weighted_atkinson([0, 10], 1, [2, 1]) == pytest.approx(
        weighted_atkinson([0, 0, 10], 1)
    )


def test_theil_t_known_values_scale_and_weights():
    from equity_diagnostics import weighted_theil_t
    assert weighted_theil_t([4, 4, 4]) == pytest.approx(0)
    assert weighted_theil_t([0, 10], [2, 1]) == pytest.approx(math.log(3))
    assert weighted_theil_t([0, 10], [2, 1]) == pytest.approx(
        weighted_theil_t([0, 0, 10])
    )
    assert weighted_theil_t([0, 100], [2, 1]) == pytest.approx(math.log(3))


def test_theil_all_zero_and_atkinson_invalid_aversion():
    from equity_diagnostics import weighted_atkinson, weighted_theil_t
    assert weighted_theil_t([0, 0, 0]) == 0
    assert weighted_atkinson([0, 0, 0], 2) == 0
    for epsilon in [-1, math.inf, math.nan]:
        with pytest.raises(ValueError):
            weighted_atkinson([1, 2], epsilon)
