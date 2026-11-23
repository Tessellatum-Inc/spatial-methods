import numpy as np
import pytest

from logratio import (
    alr, alr_inverse, aitchison_distance, closure, clr, helmert_basis,
    ilr, ilr_inverse,
)


def test_closure_normalises_rows_and_is_scale_invariant():
    x = np.array([[2., 3., 5.], [4., 1., 5.]])
    np.testing.assert_allclose(closure(x).sum(axis=1), 1.0)
    np.testing.assert_allclose(closure(x), closure(x * 17.0))


def test_clr_is_centered_and_scale_invariant():
    x = np.array([2., 3., 5.])
    transformed = clr(x)
    assert transformed.sum() == pytest.approx(0.0)
    np.testing.assert_allclose(transformed, clr(x * 100.0))


def test_ilr_round_trip_for_vectors_and_matrices():
    x = np.array([[2., 3., 5.], [1., 4., 2.], [3., 2., 7.]])
    np.testing.assert_allclose(ilr_inverse(ilr(x)), closure(x), rtol=1e-12, atol=1e-12)
    np.testing.assert_allclose(ilr_inverse(ilr(x[0])), closure(x[0]), rtol=1e-12, atol=1e-12)


def test_helmert_basis_is_orthonormal_and_orthogonal_to_ones():
    basis = helmert_basis(6)
    np.testing.assert_allclose(basis.T @ basis, np.eye(5), atol=1e-14)
    np.testing.assert_allclose(np.ones(6) @ basis, np.zeros(5), atol=1e-14)


def test_aitchison_distance_equals_euclidean_distance_in_ilr_space():
    a = np.array([2., 3., 5.])
    b = np.array([5., 2., 3.])
    assert aitchison_distance(a, b) == pytest.approx(np.linalg.norm(ilr(a) - ilr(b)))


def test_alr_round_trip_with_each_denominator():
    x = np.array([2., 3., 5., 7.])
    for denominator in range(4):
        np.testing.assert_allclose(
            alr_inverse(alr(x, denominator), denominator), closure(x), atol=1e-12
        )


def test_logratio_transforms_reject_zeros_and_negative_values():
    with pytest.raises(ValueError):
        clr([0., 1., 2.])
    with pytest.raises(ValueError):
        ilr([1., 0., 2.])
    with pytest.raises(ValueError):
        alr([1., -1., 2.])


@pytest.mark.parametrize("x", [
    [0., 0.], [1.], [-1., 2.], [1., float("nan")], [[1., 2.], [0., 0.]]
])
def test_closure_rejects_invalid_compositions(x):
    with pytest.raises(ValueError):
        closure(x)


def test_alr_rejects_invalid_denominator_and_inverse_coordinates():
    with pytest.raises(ValueError):
        alr([1., 2., 3.], denominator=3)
    with pytest.raises(ValueError):
        alr_inverse([1., 2.], denominator=3)
    with pytest.raises(ValueError):
        ilr_inverse([float("nan"), 1.])


def test_distance_requires_matching_shapes_and_positive_parts():
    with pytest.raises(ValueError):
        aitchison_distance([1., 2., 3.], [1., 2.])
    with pytest.raises(ValueError):
        aitchison_distance([0., 1., 2.], [1., 2., 3.])
