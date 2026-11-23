import numpy as np
import pytest
from moran_filter import moran_eigenvectors, moran_eigenvector_filter


def path_weights(n=6):
    w = np.zeros((n, n))
    for i in range(n - 1):
        w[i, i + 1] = w[i + 1, i] = 1
    return w


def test_positive_eigenvectors_are_orthonormal_and_centered():
    basis = moran_eigenvectors(path_weights())
    e = basis["eigenvectors"]
    np.testing.assert_allclose(e.T @ e, np.eye(e.shape[1]), atol=1e-12)
    np.testing.assert_allclose(np.ones(6) @ e, np.zeros(e.shape[1]), atol=1e-12)
    assert np.all(basis["eigenvalues"] > 0)


def test_eigenvalues_are_descending_and_component_cap_applies():
    full = moran_eigenvectors(path_weights())
    top = moran_eigenvectors(path_weights(), n_components=1)
    assert np.all(np.diff(full["eigenvalues"]) <= 0)
    assert top["eigenvectors"].shape == (6, 1)
    assert top["eigenvalues"][0] == pytest.approx(full["eigenvalues"][0])


def test_negative_eigenvectors_can_be_requested_explicitly():
    basis = moran_eigenvectors(path_weights(), positive_only=False)
    assert np.any(basis["eigenvalues"] < 0)
    assert np.any(basis["eigenvalues"] > 0)


def test_complete_graph_has_no_positive_centered_eigenvalues():
    w = np.ones((4, 4)) - np.eye(4)
    basis = moran_eigenvectors(w)
    assert basis["eigenvectors"].shape == (4, 0)


def test_fixed_filter_fit_has_expected_shapes():
    w = path_weights()
    x = np.arange(6, dtype=float)
    y = 2 + 3*x + np.array([0, 1, -1, 2, -2, 1.])
    result = moran_eigenvector_filter(y, x, w, n_components=2)
    assert result["coefficients"].shape == (1,)
    assert result["eigenvector_coefficients"].shape == (2,)
    assert result["fitted"].shape == (6,)
    assert result["residuals"].shape == (6,)


def test_adding_eigenvectors_cannot_increase_training_sse():
    w = path_weights()
    x = np.arange(6, dtype=float)
    y = np.array([1, 3, 2, 7, 5, 8.])
    sse = [
        moran_eigenvector_filter(y, x, w, n_components=k)["residual_sum_squares"]
        for k in range(3)
    ]
    assert sse[0] >= sse[1] - 1e-10
    assert sse[1] >= sse[2] - 1e-10


def test_zero_eigenvectors_is_ordinary_ols_with_intercept():
    w = path_weights()
    x = np.arange(6, dtype=float)
    y = np.array([2, 1, 4, 3, 7, 8.])
    result = moran_eigenvector_filter(y, x, w, n_components=0)
    design = np.column_stack([np.ones(6), x])
    beta = np.linalg.lstsq(design, y, rcond=None)[0]
    np.testing.assert_allclose(result["fitted"], design @ beta)


def test_no_positive_basis_is_valid_only_for_zero_components():
    w = np.ones((4, 4)) - np.eye(4)
    result = moran_eigenvector_filter([1, 2, 3, 4], None, w, n_components=0)
    assert result["eigenvectors"].shape == (4, 0)
    with pytest.raises(ValueError):
        moran_eigenvector_filter([1, 2, 3, 4], None, w, n_components=1)


@pytest.mark.parametrize("w", [
    np.ones((3, 2)), np.array([[0, 1], [0, 0]]),
    np.array([[0, -1], [-1, 0]]), np.array([[1, 0], [0, 0]]),
    np.array([[0, np.nan], [np.nan, 0]]), np.zeros((3, 3)),
])
def test_invalid_weights_rejected(w):
    with pytest.raises(ValueError):
        moran_eigenvectors(w)


def test_invalid_component_controls_rejected():
    w = path_weights()
    with pytest.raises(ValueError): moran_eigenvectors(w, n_components=-1)
    with pytest.raises(ValueError): moran_eigenvectors(w, n_components=99)
    with pytest.raises(ValueError): moran_eigenvectors(w, eigenvalue_tolerance=-1)
    with pytest.raises(ValueError): moran_eigenvectors(w, positive_only=1)


def test_invalid_regression_inputs_rejected():
    w = path_weights()
    with pytest.raises(ValueError): moran_eigenvector_filter([1, 2], None, w, n_components=0)
    with pytest.raises(ValueError): moran_eigenvector_filter([1, np.nan, 2, 3, 4, 5], None, w, n_components=0)
    with pytest.raises(ValueError): moran_eigenvector_filter([1, 2, 3, 4, 5, 6], [[1], [2]], w, n_components=0)
    with pytest.raises(ValueError): moran_eigenvector_filter([1, 2, 3, 4, 5, 6], None, w, n_components=0, add_intercept=1)
