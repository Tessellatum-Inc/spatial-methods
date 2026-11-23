import pytest
from map_classification import classify, equal_interval_breaks, jenks_natural_breaks, quantile_breaks


def test_equal_interval_breaks_and_class_assignment():
    breaks = equal_interval_breaks([0, 2, 10], 5)
    assert breaks == pytest.approx([0, 2, 4, 6, 8, 10])
    assert classify([0, 2, 2.1, 10], breaks) == [0, 0, 1, 4]


def test_quantile_breaks_linear_interpolation():
    assert quantile_breaks([0, 10, 20, 30], 2) == pytest.approx([0, 15, 30])
    assert quantile_breaks([1, 1, 2, 2], 2) == pytest.approx([1, 1.5, 2])


def test_jenks_finds_low_within_class_variance_partition():
    breaks = jenks_natural_breaks([1, 2, 3, 10, 11, 12], 2)
    assert breaks == [1.0, 3.0, 12.0]
    assert classify([1, 2, 3, 10, 11, 12], breaks) == [0, 0, 0, 1, 1, 1]


def test_jenks_one_class_and_duplicate_values():
    assert jenks_natural_breaks([2, 2, 3, 3], 1) == [2.0, 3.0]
    assert jenks_natural_breaks([1, 1, 5, 5], 2) == [1.0, 1.0, 5.0]


@pytest.mark.parametrize("values,k", [([], 1), ([1, float("nan")], 1), ([1, 2], 0), ([1, 2], 3)])
def test_invalid_classification_inputs(values, k):
    with pytest.raises(ValueError):
        jenks_natural_breaks(values, k)


def test_classify_rejects_outside_values_and_bad_breaks():
    with pytest.raises(ValueError):
        classify([-1], [0, 1])
    with pytest.raises(ValueError):
        classify([0.5], [1, 0])
    with pytest.raises(ValueError):
        classify([float("inf")], [0, 1])
