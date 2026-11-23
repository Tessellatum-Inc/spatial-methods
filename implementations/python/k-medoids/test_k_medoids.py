import numpy as np
import pytest

from k_medoids import clara, euclidean_dissimilarity, pam


def clustered_points():
    return np.array([
        (0.0, 0.0), (0.0, 1.0), (1.0, 0.0),
        (10.0, 10.0), (10.0, 11.0), (11.0, 10.0),
    ])


def test_pam_recovers_two_separated_groups_and_uses_observed_medoids():
    points = clustered_points()
    distances = euclidean_dissimilarity(points)
    result = pam(distances, 2)
    assert set(result["medoids"]).issubset(set(range(len(points))))
    assert len(set(result["labels"][:3])) == 1
    assert len(set(result["labels"][3:])) == 1
    assert result["labels"][0] != result["labels"][3]
    direct = distances[:, result["medoids"]].min(axis=1).sum()
    assert result["cost"] == pytest.approx(direct)
    assert result["converged"]


def test_pam_matches_brute_force_optimum_on_small_line_fixture():
    points = np.array([(0.0,), (1.0,), (9.0,), (10.0,)])
    distances = euclidean_dissimilarity(points)
    result = pam(distances, 2)
    optimum = min(
        distances[:, list(pair)].min(axis=1).sum()
        for pair in ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
    )
    assert result["cost"] == pytest.approx(optimum)
    assert optimum == pytest.approx(2.0)


def test_pam_is_deterministic_and_handles_k_equal_n():
    distances = euclidean_dissimilarity(clustered_points())
    a, b = pam(distances, 2), pam(distances, 2)
    np.testing.assert_array_equal(a["medoids"], b["medoids"])
    np.testing.assert_array_equal(a["labels"], b["labels"])
    all_medoids = pam(distances, len(distances))
    assert all_medoids["cost"] == pytest.approx(0)
    assert set(all_medoids["medoids"]) == set(range(len(distances)))
    np.testing.assert_array_equal(all_medoids["labels"], np.arange(len(distances)))


def test_pam_rejects_invalid_dissimilarity_matrices():
    with pytest.raises(ValueError, match="square"):
        pam([[0, 1, 2], [1, 0, 1]], 1)
    with pytest.raises(ValueError, match="symmetric"):
        pam([[0, 1], [2, 0]], 1)
    with pytest.raises(ValueError, match="non-negative"):
        pam([[0, -1], [-1, 0]], 1)
    with pytest.raises(ValueError, match="diagonal"):
        pam([[1, 1], [1, 0]], 1)
    with pytest.raises(ValueError, match="finite"):
        pam([[0, np.nan], [np.nan, 0]], 1)


@pytest.mark.parametrize("k", [0, -1, 7, 1.5, True])
def test_pam_rejects_invalid_cluster_counts(k):
    with pytest.raises(ValueError, match="k"):
        pam(euclidean_dissimilarity(clustered_points()), k)


def test_pam_rejects_invalid_iteration_controls():
    distances = euclidean_dissimilarity(clustered_points())
    with pytest.raises(ValueError, match="max_iter"):
        pam(distances, 2, max_iter=0)
    with pytest.raises(ValueError, match="tol"):
        pam(distances, 2, tol=-1)


def test_clara_is_reproducible_and_scores_candidates_on_full_data():
    distances = euclidean_dissimilarity(clustered_points())
    a = clara(distances, 2, n_samples=8, sample_size=5, random_state=19)
    b = clara(distances, 2, n_samples=8, sample_size=5, random_state=19)
    np.testing.assert_array_equal(a["medoids"], b["medoids"])
    np.testing.assert_array_equal(a["labels"], b["labels"])
    assert a["cost"] == pytest.approx(b["cost"])
    assert a["samples_evaluated"] == 8
    assert a["sample_size"] == 5
    assert a["cost"] == pytest.approx(distances[:, a["medoids"]].min(axis=1).sum())


def test_clara_with_full_sample_matches_pam_objective():
    distances = euclidean_dissimilarity(clustered_points())
    exact_sample = clara(distances, 2, n_samples=3, sample_size=len(distances), random_state=4)
    fitted = pam(distances, 2)
    assert exact_sample["cost"] == pytest.approx(fitted["cost"])


def test_clara_rejects_invalid_sampling_controls():
    distances = euclidean_dissimilarity(clustered_points())
    with pytest.raises(ValueError, match="n_samples"):
        clara(distances, 2, n_samples=0)
    with pytest.raises(ValueError, match="sample_size"):
        clara(distances, 2, sample_size=1)
    with pytest.raises(ValueError, match="sample_size"):
        clara(distances, 2, sample_size=99)


def test_clarans_is_reproducible_and_returns_full_data_objective():
    from k_medoids import clarans
    distances = euclidean_dissimilarity(clustered_points())
    a = clarans(distances, 2, max_neighbors=30, num_local=5, random_state=31)
    b = clarans(distances, 2, max_neighbors=30, num_local=5, random_state=31)
    np.testing.assert_array_equal(a["medoids"], b["medoids"])
    np.testing.assert_array_equal(a["labels"], b["labels"])
    assert a["cost"] == pytest.approx(b["cost"])
    assert a["cost"] == pytest.approx(distances[:, a["medoids"]].min(axis=1).sum())
    assert len(set(a["medoids"])) == 2
    assert a["local_minima"] == 5
    assert a["neighbor_evaluations"] >= 5 * 30


def test_clarans_finds_separated_clusters_and_handles_k_equal_n():
    from k_medoids import clarans
    points = clustered_points()
    distances = euclidean_dissimilarity(points)
    result = clarans(distances, 2, max_neighbors=40, num_local=8, random_state=7)
    assert result["labels"][0] == result["labels"][1] == result["labels"][2]
    assert result["labels"][3] == result["labels"][4] == result["labels"][5]
    assert result["labels"][0] != result["labels"][3]
    all_medoids = clarans(distances, len(distances))
    assert all_medoids["cost"] == pytest.approx(0)
    assert set(all_medoids["medoids"]) == set(range(len(distances)))
    np.testing.assert_array_equal(all_medoids["labels"], np.arange(len(distances)))


def test_clarans_rejects_invalid_search_controls():
    from k_medoids import clarans
    distances = euclidean_dissimilarity(clustered_points())
    with pytest.raises(ValueError, match="max_neighbors"):
        clarans(distances, 2, max_neighbors=0)
    with pytest.raises(ValueError, match="num_local"):
        clarans(distances, 2, num_local=0)
