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
