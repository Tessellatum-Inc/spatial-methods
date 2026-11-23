import numpy as np
import pytest
from classification import (
    fit_gaussian_maximum_likelihood,
    predict_gaussian_maximum_likelihood,
    kmeans,
)


def test_gaussian_maximum_likelihood_recovers_separated_classes():
    rng = np.random.default_rng(12)
    a = rng.normal(loc=[-3, 0], scale=.25, size=(60, 2))
    b = rng.normal(loc=[3, 0], scale=.25, size=(60, 2))
    x = np.vstack((a, b))
    y = np.array(["water"] * len(a) + ["vegetation"] * len(b))
    model = fit_gaussian_maximum_likelihood(x, y)
    predicted, scores = predict_gaussian_maximum_likelihood(model, x, return_scores=True)
    assert np.mean(predicted == y) > .99
    assert scores.shape == (120, 2)


def test_gaussian_classifier_uses_supplied_priors():
    x = np.array([[-2., 0], [-2.1, .1], [-1.9, -.1],
                  [2., 0], [2.1, .1], [1.9, -.1]])
    y = np.array([0, 0, 0, 1, 1, 1])
    model = fit_gaussian_maximum_likelihood(x, y, priors={0: .9, 1: .1})
    assert model["log_priors"][0] > model["log_priors"][1]


def test_kmeans_finds_two_compact_spectral_groups_deterministically():
    x = np.array([[0., 0], [0.1, 0], [-.1, 0],
                  [10., 10], [10.1, 10], [9.9, 10]])
    first = kmeans(x, 2, n_init=5, random_state=5)
    second = kmeans(x, 2, n_init=5, random_state=5)
    assert first["inertia"] == pytest.approx(.04)
    assert np.array_equal(first["labels"], second["labels"])
    assert np.allclose(first["centroids"], second["centroids"])


def test_kmeans_one_cluster_returns_global_mean():
    x = np.array([[1., 2], [3., 4], [5., 6]])
    result = kmeans(x, 1, random_state=1)
    assert result["centroids"][0] == pytest.approx([3, 4])
    assert result["inertia"] == pytest.approx(16)


@pytest.mark.parametrize("kwargs", [
    {"n_clusters": 0}, {"n_clusters": 7}, {"n_clusters": 2, "n_init": 0},
    {"n_clusters": 2, "max_iterations": 0}, {"n_clusters": 2, "tolerance": -1},
])
def test_kmeans_rejects_invalid_controls(kwargs):
    x = np.arange(12.).reshape(6, 2)
    with pytest.raises(ValueError):
        kmeans(x, **kwargs)


def test_gaussian_classifier_rejects_bad_training_data_and_priors():
    x = np.arange(12.).reshape(6, 2)
    y = np.array([0, 0, 0, 1, 1, 1])
    with pytest.raises(ValueError):
        fit_gaussian_maximum_likelihood(x, y, priors={0: 1})
    with pytest.raises(ValueError):
        fit_gaussian_maximum_likelihood(x, np.zeros(6))
    bad_labels = y.astype(float)
    bad_labels[0] = np.nan
    with pytest.raises(ValueError):
        fit_gaussian_maximum_likelihood(x, bad_labels)


def test_isodata_splits_dispersed_cluster_and_is_deterministic():
    from classification import isodata
    x = np.array([[-4., 0], [-3., .1], [-2., -.1],
                  [2., .1], [3., -.1], [4., 0]])
    first = isodata(x, 1, max_clusters=2, split_std=1.0,
                    merge_distance=0.0, random_state=13)
    second = isodata(x, 1, max_clusters=2, split_std=1.0,
                     merge_distance=0.0, random_state=13)
    assert len(first["centroids"]) == 2
    assert first["inertia"] < 5
    assert np.array_equal(first["labels"], second["labels"])


def test_isodata_merges_nearby_centroids_and_respects_minimum_count():
    from classification import isodata
    x = np.array([[0., 0], [.1, 0], [1., 0], [1.1, 0],
                  [8., 0], [8.1, 0], [9., 0], [9.1, 0]])
    result = isodata(x, 4, min_clusters=2, max_clusters=4,
                     min_cluster_size=1, split_std=100,
                     merge_distance=2.0, random_state=2)
    assert len(result["centroids"]) >= 2
    assert result["cluster_sizes"].sum() == len(x)


def test_isodata_rejects_invalid_cluster_bounds():
    from classification import isodata
    x = np.arange(20.).reshape(10, 2)
    with pytest.raises(ValueError):
        isodata(x, 3, min_clusters=4, max_clusters=3)



def test_svm_linear_classifier_predicts_separated_spectral_classes():
    from classification import fit_svm_classifier, predict_svm_classifier
    x = np.array([[-2., -1], [-1.8, -.9], [-2.2, -.8],
                  [2., 1], [1.8, .9], [2.2, .8]])
    y = np.array(["water"] * 3 + ["vegetation"] * 3)
    model = fit_svm_classifier(x, y, kernel="linear", C=2)
    result = predict_svm_classifier(model, x, return_scores=True)
    assert np.mean(result["labels"] == y) == pytest.approx(1)
    assert result["decision_scores"].shape == (6,)


def test_svm_rbf_handles_nonlinear_xor_fixture():
    from classification import fit_svm_classifier, predict_svm_classifier
    x = np.array([[-1., -1], [-1., 1], [1., -1], [1., 1]] * 3)
    y = np.array([1, 0, 0, 1] * 3)
    model = fit_svm_classifier(x, y, kernel="rbf", C=10, gamma=1)
    assert np.mean(predict_svm_classifier(model, x) == y) == pytest.approx(1)


def test_random_forest_returns_class_probabilities_and_importance():
    from classification import fit_random_forest_classifier, predict_random_forest_classifier
    x = np.array([[0., 0], [.1, 0], [-.1, 0], [10., 10], [10.1, 10], [9.9, 10]])
    y = np.array([0, 0, 0, 1, 1, 1])
    model = fit_random_forest_classifier(x, y, n_estimators=40, random_state=4)
    result = predict_random_forest_classifier(model, x, return_probabilities=True)
    assert np.mean(result["labels"] == y) == pytest.approx(1)
    assert result["probabilities"].shape == (6, 2)
    assert result["feature_importances"].sum() == pytest.approx(1)


def test_svm_and_random_forest_reject_invalid_parameters_and_feature_counts():
    from classification import (fit_svm_classifier, predict_svm_classifier,
                                 fit_random_forest_classifier, predict_random_forest_classifier)
    x = np.array([[0., 0], [.1, 0], [10., 10], [10.1, 10]])
    y = np.array([0, 0, 1, 1])
    with pytest.raises(ValueError):
        fit_svm_classifier(x, y, C=0)
    with pytest.raises(ValueError):
        fit_svm_classifier(x, y, kernel="unknown")
    with pytest.raises(ValueError):
        fit_random_forest_classifier(x, y, n_estimators=0)
    svm = fit_svm_classifier(x, y)
    forest = fit_random_forest_classifier(x, y, n_estimators=5)
    with pytest.raises(ValueError):
        predict_svm_classifier(svm, np.ones((2, 3)))
    with pytest.raises(ValueError):
        predict_random_forest_classifier(forest, np.ones((2, 3)))
