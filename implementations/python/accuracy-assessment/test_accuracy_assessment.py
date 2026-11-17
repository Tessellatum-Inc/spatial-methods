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
