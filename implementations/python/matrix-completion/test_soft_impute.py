import numpy as np
import pytest
from soft_impute import soft_impute


def test_soft_impute_preserves_observed_values_and_fills_missing_cells():
    data = np.array([[1., 2., 3.], [2., np.nan, 6.], [3., 6., 9.]])
    result = soft_impute(data, regularization=0.01, max_rank=1, tolerance=1e-7)
    completed = np.asarray(result["completed"])
    assert result["converged"]
    assert np.isfinite(completed).all()
    assert completed[np.isfinite(data)] == pytest.approx(data[np.isfinite(data)])
    assert completed[1, 1] == pytest.approx(4, abs=.2)


def test_soft_impute_returns_complete_matrix_without_iteration():
    data = [[1, 2], [3, 4]]
    result = soft_impute(data, regularization=0.5)
    assert result["iterations"] == 0 and result["converged"]
    assert result["completed"] == data


def test_soft_impute_supports_rank_cap_and_zero_regularization():
    data = [[1., 2., np.nan], [2., 4., 6.], [3., 6., 9.]]
    result = soft_impute(data, regularization=0, max_rank=1)
    assert result["rank"] <= 1
    assert np.isfinite(result["completed"]).all()


@pytest.mark.parametrize("bad", [
    [[np.nan, np.nan], [np.nan, np.nan]],
    [[1, 2], [3, np.inf]],
    [1, 2, 3],
])
def test_soft_impute_rejects_invalid_matrix(bad):
    with pytest.raises(ValueError):
        soft_impute(bad, regularization=0.1)


@pytest.mark.parametrize("kwargs", [
    {"regularization": -1}, {"regularization": 1, "max_rank": 0},
    {"regularization": 1, "tolerance": 0},
    {"regularization": 1, "max_iterations": 0},
])
def test_soft_impute_rejects_invalid_controls(kwargs):
    with pytest.raises(ValueError):
        soft_impute([[1, np.nan], [2, 3]], **kwargs)
