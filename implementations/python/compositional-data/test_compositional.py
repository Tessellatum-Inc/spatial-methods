import math
import pytest
from compositional import closure, multiplicative_zero_replacement, clr_transform, aitchison_distance

def test_closure_is_scale_invariant_and_sums_to_one():
    assert closure([2, 3, 5]) == pytest.approx(closure([20, 30, 50]))
    assert sum(closure([2, 3, 5])) == pytest.approx(1)

def test_clr_coordinates_sum_to_zero():
    transformed = clr_transform([2, 3, 5])
    assert sum(transformed) == pytest.approx(0)
    expected = [math.log(2) - math.log(30) / 3, math.log(3) - math.log(30) / 3, math.log(5) - math.log(30) / 3]
    assert transformed == pytest.approx(expected)

def test_clr_is_invariant_to_common_scale():
    assert clr_transform([2, 3, 5]) == pytest.approx(clr_transform([200, 300, 500]))

def test_aitchison_distance_is_scale_invariant_and_symmetric():
    a, b = [2, 3, 5], [4, 2, 4]
    assert aitchison_distance(a, b) == pytest.approx(aitchison_distance([20, 30, 50], [40, 20, 40]))
    assert aitchison_distance(a, b) == pytest.approx(aitchison_distance(b, a))

def test_identical_compositions_have_zero_distance():
    assert aitchison_distance([1, 2, 3], [10, 20, 30]) == pytest.approx(0)

def test_multiplicative_zero_replacement_preserves_nonzero_ratio():
    replaced = multiplicative_zero_replacement([0, 2, 4], 0.01)
    assert replaced == pytest.approx([0.01, 0.33, 0.66])
    assert replaced[2] / replaced[1] == pytest.approx(2)

def test_clr_requires_explicit_zero_replacement():
    with pytest.raises(ValueError):
        clr_transform([0, 1, 2])
    assert sum(clr_transform([0, 1, 2], zero_replacement=0.001)) == pytest.approx(0)

@pytest.mark.parametrize("values", [[], [0, 0], [1, -1], [1, float("nan")], [True, 1]])
def test_invalid_compositions_are_rejected(values):
    with pytest.raises(ValueError):
        closure(values)

def test_zero_replacement_rejects_excessive_mass_and_mismatched_dimensions():
    with pytest.raises(ValueError):
        multiplicative_zero_replacement([0, 0, 1], 0.5)
    with pytest.raises(ValueError):
        aitchison_distance([1, 2], [1, 2, 3])
