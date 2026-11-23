import numpy as np
import pytest
from k_means import kmeans


def clustered():
    return np.array([[0., 0.], [0., 1.], [1., 0.],
                     [9., 9.], [9., 10.], [10., 9.]])


def test_separated_clusters_and_independent_inertia_recomputation():
    x = clustered()
    fit = kmeans(x, 2, random_state=12, n_init=5)
    labels = fit["labels"]
    assert labels[0] == labels[1] == labels[2]
    assert labels[3] == labels[4] == labels[5]
    assert labels[0] != labels[3]
    independent = sum(np.sum((x[labels == j] - x[labels == j].mean(axis=0)) ** 2)
                      for j in range(2))
    assert fit["inertia"] == pytest.approx(independent)
    assert fit["inertia"] == pytest.approx(8.0 / 3.0)


def test_seeded_runs_are_identical():
    a = kmeans(clustered(), 2, random_state=7, n_init=4)
    b = kmeans(clustered(), 2, random_state=7, n_init=4)
    np.testing.assert_array_equal(a["labels"], b["labels"])
    np.testing.assert_allclose(a["centers"], b["centers"])
    assert a["inertia"] == b["inertia"]


def test_empty_clusters_are_repaired_for_duplicate_observations():
    fit = kmeans(np.zeros((5, 2)), 3, random_state=2, n_init=2)
    assert set(fit["labels"]) == {0, 1, 2}
    assert fit["inertia"] == pytest.approx(0)


def test_k_equal_n_produces_nonempty_assignments():
    fit = kmeans(np.array([[0.], [1.], [2.]]), 3, n_init=1)
    assert set(fit["labels"]) == {0, 1, 2}
    assert fit["inertia"] == pytest.approx(0)


@pytest.mark.parametrize("k", [0, -1, 7, True, 1.5])
def test_invalid_cluster_count(k):
    with pytest.raises(ValueError, match="k"):
        kmeans(clustered(), k)


def test_invalid_data_and_controls():
    with pytest.raises(ValueError, match="2-D"):
        kmeans(np.array([1., 2.]), 1)
    with pytest.raises(ValueError, match="finite"):
        kmeans(np.array([[0.], [np.nan]]), 1)
    with pytest.raises(ValueError, match="max_iter"):
        kmeans(clustered(), 2, max_iter=0)
    with pytest.raises(ValueError, match="n_init"):
        kmeans(clustered(), 2, n_init=0)
    with pytest.raises(ValueError, match="tol"):
        kmeans(clustered(), 2, tol=-1)
