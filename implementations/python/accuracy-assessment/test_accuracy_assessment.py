import pytest
from accuracy_assessment import accuracy_metrics, confusion_matrix, figure_of_merit


def test_confusion_matrix_rows_reference_columns_prediction():
    labels, matrix = confusion_matrix(["a","a","b","b"], ["a","b","b","a"])
    assert labels == ["a","b"]
    assert matrix == [[1,1],[1,1]]


def test_confusion_matrix_supplied_label_order_and_validation():
    labels, matrix = confusion_matrix([1,2], [2,2], labels=[2,1,3])
    assert labels == [2,1,3]
    assert matrix == [[1,0,0],[1,0,0],[0,0,0]]
    with pytest.raises(ValueError): confusion_matrix([], [])
    with pytest.raises(ValueError): confusion_matrix([1], [1,2])
    with pytest.raises(ValueError): confusion_matrix([1], [1], labels=[1,1])
    with pytest.raises(ValueError): confusion_matrix([2], [2], labels=[1])


def test_overall_class_accuracy_kappa_and_disagreement():
    result = accuracy_metrics([[1,1],[1,1]])
    assert result["overall_accuracy"] == pytest.approx(0.5)
    assert result["producer_accuracy"] == [0.5,0.5]
    assert result["user_accuracy"] == [0.5,0.5]
    assert result["kappa"] == pytest.approx(0)
    assert result["quantity_disagreement"] == pytest.approx(0)
    assert result["allocation_disagreement"] == pytest.approx(0.5)


def test_kappa_degenerate_and_zero_margins():
    result = accuracy_metrics([[4,0],[0,0]])
    assert result["kappa"] is None
    assert result["producer_accuracy"] == [1.0, None]
    assert result["user_accuracy"] == [1.0, None]


def test_quantity_allocation_decomposition():
    result = accuracy_metrics([[2,0],[1,1]])
    assert result["overall_accuracy"] == pytest.approx(0.75)
    assert result["quantity_disagreement"] == pytest.approx(0.25)
    assert result["allocation_disagreement"] == pytest.approx(0)


def test_figure_of_merit():
    assert figure_of_merit([1,1,0,0], [1,0,1,0]) == pytest.approx(1/3)
    assert figure_of_merit([0,0], [0,0]) is None
    with pytest.raises(ValueError): figure_of_merit([], [])
    with pytest.raises(ValueError): figure_of_merit([1], [2])
    with pytest.raises(ValueError): figure_of_merit([1], [1,0])


from accuracy_assessment import (
    expected_calibration_error, mean_absolute_error, r2_score,
    root_mean_squared_error,
)


def test_regression_metrics_match_analytic_values():
    assert mean_absolute_error([1, 2, 3], [1, 2, 1]) == pytest.approx(2/3)
    assert root_mean_squared_error([1, 2, 3], [1, 2, 1]) == pytest.approx((4/3)**.5)
    assert r2_score([1, 2, 3], [1, 2, 2]) == pytest.approx(.5)


def test_regression_metrics_support_sample_weights():
    assert mean_absolute_error([0, 2], [1, 0], [1, 3]) == pytest.approx(1.75)
    assert root_mean_squared_error([0, 2], [1, 0], [1, 3]) == pytest.approx(3.25**.5)
    assert r2_score([0, 2, 4], [0, 1, 4], [1, 2, 1]) == pytest.approx(.75)


def test_r2_constant_target_policy_is_finite_and_explicit():
    assert r2_score([2, 2], [2, 2]) == 1.0
    assert r2_score([2, 2], [2, 3]) == 0.0


def test_regression_metrics_reject_invalid_inputs():
    with pytest.raises(ValueError):
        mean_absolute_error([], [])
    with pytest.raises(ValueError):
        root_mean_squared_error([1], [1, 2])
    with pytest.raises(ValueError):
        r2_score([1, float("nan")], [1, 2])
    with pytest.raises(ValueError):
        mean_absolute_error([1, 2], [1, 2], [1, -1])
    with pytest.raises(ValueError):
        r2_score([1, 2], [1, 2], [0, 0])


def test_expected_calibration_error_top_label_bins():
    probabilities = [[.9, .1], [.8, .2], [.4, .6], [.3, .7]]
    labels = [0, 1, 1, 0]
    assert expected_calibration_error(probabilities, labels, n_bins=2) == pytest.approx(.25)
    assert expected_calibration_error([[1, 0], [0, 1]], [0, 1]) == pytest.approx(0)


def test_expected_calibration_error_respects_sample_weights():
    probabilities = [[.9, .1], [.8, .2], [.4, .6], [.3, .7]]
    labels = [0, 1, 1, 0]
    assert expected_calibration_error(probabilities, labels, n_bins=2, sample_weight=[1, 3, 1, 1]) == pytest.approx(13/30)


def test_expected_calibration_error_rejects_invalid_probabilities_and_labels():
    with pytest.raises(ValueError):
        expected_calibration_error([], [])
    with pytest.raises(ValueError):
        expected_calibration_error([[.8, .3]], [0])
    with pytest.raises(ValueError):
        expected_calibration_error([[.5, .5], [.2, .8]], [0])
    with pytest.raises(ValueError):
        expected_calibration_error([[.5, .5]], [2])
    with pytest.raises(ValueError):
        expected_calibration_error([[.5, .5]], [0], n_bins=0)


from accuracy_assessment import normalized_mutual_information, recall_at_k


def test_recall_at_k_macro_query_recall_and_empty_queries():
    assert recall_at_k([{"a", "b"}, {"c"}], [["x", "b", "a"], ["d", "c"]], 2) == pytest.approx(.75)
    assert recall_at_k([set(), {"a"}], [[], ["a"]], 1) == pytest.approx(1.0)
    assert recall_at_k([set()], [[]], 3) is None


def test_recall_at_k_validates_query_counts_and_k():
    with pytest.raises(ValueError):
        recall_at_k([], [], 1)
    with pytest.raises(ValueError):
        recall_at_k([{"a"}], [], 1)
    with pytest.raises(ValueError):
        recall_at_k([{"a"}], [["a"]], 0)


def test_normalized_mutual_information_is_permutation_invariant():
    assert normalized_mutual_information(["a", "a", "b", "b"], [1, 1, 0, 0]) == pytest.approx(1.0)
    assert normalized_mutual_information(["a", "a", "b", "b"], [0, 1, 0, 1]) == pytest.approx(0.0)
    assert normalized_mutual_information(["a", "a"], ["x", "x"]) == pytest.approx(1.0)


def test_normalized_mutual_information_validates_inputs():
    with pytest.raises(ValueError):
        normalized_mutual_information([], [])
    with pytest.raises(ValueError):
        normalized_mutual_information(["a"], ["x", "y"])


from accuracy_assessment import (
    ensemble_crps, kling_gupta_efficiency, nash_sutcliffe_efficiency,
)


def test_nash_sutcliffe_efficiency_matches_analytic_values():
    assert nash_sutcliffe_efficiency([1, 2, 3], [1, 2, 2]) == pytest.approx(.5)
    assert nash_sutcliffe_efficiency([1, 2, 3], [1, 2, 3]) == pytest.approx(1)
    assert nash_sutcliffe_efficiency([2, 2], [2, 3]) == 0


def test_kling_gupta_efficiency_2009_components():
    assert kling_gupta_efficiency([1, 2, 3], [1, 2, 3]) == pytest.approx(1)
    assert kling_gupta_efficiency([1, 2, 3], [2, 4, 6]) == pytest.approx(1-2**.5)
    assert kling_gupta_efficiency([0, 0, 0], [1, 2, 3]) is None
    assert kling_gupta_efficiency([1, 2, 3], [2, 2, 2]) is None


def test_kge_supports_sample_weights():
    assert kling_gupta_efficiency([1, 2, 3], [1, 2, 3], [1, 2, 1]) == pytest.approx(1)


def test_ensemble_crps_matches_single_and_two_member_oracles():
    assert ensemble_crps([1], [[3]]) == pytest.approx(2)
    assert ensemble_crps([1], [[0, 2]]) == pytest.approx(.5)
    assert ensemble_crps([1], [[0, 1, 2]]) == pytest.approx(2/9)


def test_ensemble_crps_supports_case_weights():
    assert ensemble_crps([0, 0], [[0], [2]], [3, 1]) == pytest.approx(.5)


def test_ensemble_crps_rejects_invalid_inputs():
    with pytest.raises(ValueError):
        ensemble_crps([], [])
    with pytest.raises(ValueError):
        ensemble_crps([1], [[]])
    with pytest.raises(ValueError):
        ensemble_crps([1], [[float("nan")]])
    with pytest.raises(ValueError):
        ensemble_crps([1, 2], [[1]], [1, 1])


def test_pontius_quantity_and_allocation_disagreement_named_functions():
    from accuracy_assessment import quantity_disagreement, allocation_disagreement
    matrix = [[2, 0], [1, 1]]
    assert quantity_disagreement(matrix) == pytest.approx(.25)
    assert allocation_disagreement(matrix) == pytest.approx(0)
    assert quantity_disagreement(matrix) + allocation_disagreement(matrix) == pytest.approx(
        1 - accuracy_metrics(matrix)["overall_accuracy"]
    )


def test_cramers_v_matches_independence_and_perfect_association_fixtures():
    from accuracy_assessment import cramers_v
    assert cramers_v([[10, 10], [10, 10]]) == pytest.approx(0)
    assert cramers_v([[20, 0], [0, 20]]) == pytest.approx(1)
    assert cramers_v([[20, 0, 0], [0, 20, 0]]) == pytest.approx(1)
    assert cramers_v([[10, 0], [0, 0], [0, 10]]) == pytest.approx(1)
    assert cramers_v([[10, 0], [0, 0]]) is None


def test_cramers_v_rejects_invalid_contingency_tables():
    from accuracy_assessment import cramers_v
    for bad in ([], [[1, 2], [3]], [[1, -1], [0, 1]], [[1.0, 0], [0, 1]]):
        with pytest.raises(ValueError):
            cramers_v(bad)


def test_mean_absolute_class_area_error_uses_explicit_class_weights():
    from accuracy_assessment import mean_absolute_class_area_error
    assert mean_absolute_class_area_error([100, 200, 300], [110, 180, 330]) == pytest.approx(20)
    assert mean_absolute_class_area_error([100, 200], [110, 180], [3, 1]) == pytest.approx(12.5)
    assert mean_absolute_class_area_error([0, 0], [0, 0]) == 0


def test_mean_absolute_class_area_error_rejects_invalid_inputs():
    from accuracy_assessment import mean_absolute_class_area_error
    for args in (([], []), ([1], [1, 2]), ([1, -1], [1, 1]), ([1], [float("nan")])):
        with pytest.raises(ValueError):
            mean_absolute_class_area_error(*args)
    with pytest.raises(ValueError):
        mean_absolute_class_area_error([1, 2], [1, 2], [0, 0])
    with pytest.raises(ValueError):
        mean_absolute_class_area_error([1, 2], [1, 2], [1])



def test_multiclass_matthews_correlation_coefficient_analytic_fixtures():
    from accuracy_assessment import matthews_correlation_coefficient
    assert matthews_correlation_coefficient([[5, 0], [0, 7]]) == pytest.approx(1.0)
    assert matthews_correlation_coefficient([[0, 5], [5, 0]]) == pytest.approx(-1.0)
    assert matthews_correlation_coefficient(
        [[5, 2, 0], [1, 4, 1], [0, 2, 6]]
    ) == pytest.approx(169 / 292)


def test_multiclass_matthews_correlation_coefficient_degenerate_and_invalid():
    from accuracy_assessment import matthews_correlation_coefficient
    assert matthews_correlation_coefficient([[4, 0], [0, 0]]) is None
    for bad in ([], [[1, 2], [3]], [[1, -1], [0, 1]], [[1.0, 0], [0, 1]]):
        with pytest.raises(ValueError):
            matthews_correlation_coefficient(bad)
