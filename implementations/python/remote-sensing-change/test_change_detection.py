import numpy as np
import pytest

from change_detection import change_vector_analysis, post_classification_change


def test_cva_returns_after_minus_before_and_euclidean_magnitude():
    before = np.zeros((3, 4, 2))
    after = before.copy()
    after[1, 2] = [3.0, 4.0]
    result = change_vector_analysis(before, after, covariance=np.eye(2))
    np.testing.assert_allclose(result["difference"][1, 2], [3, 4])
    assert result["magnitude"][1, 2] == pytest.approx(5.0)
    assert result["magnitude"][0, 0] == pytest.approx(0.0)
    assert result["valid_mask"].all()


def test_cva_mahalanobis_matches_independent_linear_algebra_oracle():
    before = np.zeros((2, 3, 2))
    after = np.array([[[1., 0.], [0., 2.], [1., 1.]],
                      [[2., 0.], [0., 1.], [2., 2.]]])
    covariance = np.array([[4., 1.], [1., 2.]])
    ridge = 1e-5
    result = change_vector_analysis(before, after, covariance=covariance,
                                    regularization=ridge)
    expected_cov = covariance + ridge * np.eye(2)
    for row in range(2):
        for col in range(3):
            vector = after[row, col]
            expected = np.sqrt(vector @ np.linalg.solve(expected_cov, vector))
            assert result["mahalanobis_magnitude"][row, col] == pytest.approx(expected)


def test_cva_estimates_covariance_and_masks_nodata():
    before = np.zeros((2, 3, 2))
    after = np.array([[[1., 0.], [0., 2.], [1., 1.]],
                      [[2., 0.], [0., 1.], [np.nan, 2.]]])
    result = change_vector_analysis(before, after)
    assert result["valid_mask"].sum() == 5
    assert np.isnan(result["magnitude"][1, 2])
    assert np.isnan(result["mahalanobis_magnitude"][1, 2])
    assert np.all(np.linalg.eigvalsh(result["covariance"]) > 0)


def test_cva_rejects_invalid_shapes_covariance_and_regularization():
    with pytest.raises(ValueError):
        change_vector_analysis(np.zeros((3, 3)), np.zeros((3, 3)))
    with pytest.raises(ValueError):
        change_vector_analysis(np.zeros((2, 2, 2)), np.zeros((2, 2, 2)),
                               covariance=np.ones((3, 3)))
    with pytest.raises(ValueError):
        change_vector_analysis(np.zeros((2, 2, 2)), np.zeros((2, 2, 2)),
                               regularization=0)


def test_post_classification_transition_matrix_against_pixelwise_oracle():
    before = np.array([[1, 1, 2], [2, 3, 3]])
    after = np.array([[1, 2, 2], [3, 3, 1]])
    result = post_classification_change(before, after, class_values=[1, 2, 3])
    expected = np.zeros((3, 3), dtype=int)
    changed_count = 0
    for r in range(before.shape[0]):
        for c in range(before.shape[1]):
            expected[before[r, c] - 1, after[r, c] - 1] += 1
            changed_count += before[r, c] != after[r, c]
    np.testing.assert_array_equal(result["transition_matrix"], expected)
    assert result["changed_mask"].sum() == changed_count == 3
    assert result["transition_matrix"].sum() == before.size


def test_post_classification_change_handles_nodata_and_class_order():
    before = np.array([[4., 2.], [np.nan, 4.]])
    after = np.array([[2., 2.], [1., np.nan]])
    result = post_classification_change(before, after, class_values=[4, 2, 1])
    np.testing.assert_array_equal(result["transition_matrix"],
                                  [[0, 1, 0], [0, 1, 0], [0, 0, 0]])
    assert result["valid_mask"].sum() == 2
    assert result["changed_mask"].sum() == 1


def test_post_classification_change_rejects_missing_and_duplicate_classes():
    before = np.array([[1., 2.]])
    after = np.array([[1., 3.]])
    with pytest.raises(ValueError):
        post_classification_change(before, after, class_values=[1, 2])
    with pytest.raises(ValueError):
        post_classification_change(before, after, class_values=[1, 1, 2, 3])
