import numpy as np
import pytest

from random_hyperplane_lsh import RandomHyperplaneLSH


def test_query_reranks_candidates_by_exact_cosine_similarity():
    vectors = np.array([[1., 0.], [.9, .1], [-1., 0.], [0., 1.]])
    index = RandomHyperplaneLSH(n_planes=3, n_tables=12, seed=4).fit(vectors)
    results = index.query([1., 0.], top_k=4)
    assert results and results[0].index == 0
    for result in results:
        expected = vectors[result.index] @ np.array([1., 0.]) / np.linalg.norm(vectors[result.index])
        assert result.similarity == pytest.approx(expected)


def test_candidates_are_sorted_unique_and_include_self():
    vectors = np.eye(4)
    index = RandomHyperplaneLSH(2, 6, seed=11).fit(vectors)
    candidates = index.query_candidates(vectors[2])
    assert candidates == sorted(set(candidates))
    assert 2 in candidates


def test_seed_reproduces_candidate_sets_and_rankings():
    vectors = np.array([[1, 2], [2, 1], [-1, -2], [.5, .2]], dtype=float)
    left = RandomHyperplaneLSH(5, 7, seed=19).fit(vectors)
    right = RandomHyperplaneLSH(5, 7, seed=19).fit(vectors)
    assert left.query_candidates([1, 1]) == right.query_candidates([1, 1])
    assert left.query([1, 1]) == right.query([1, 1])


@pytest.mark.parametrize("planes,tables", [(0, 2), (2, 0), (-1, 2), (2, -1), (True, 2)])
def test_invalid_hash_dimensions(planes, tables):
    with pytest.raises(ValueError):
        RandomHyperplaneLSH(planes, tables)


@pytest.mark.parametrize("vectors", [[], [[1, np.nan]], [[1, np.inf]], [[0., 0.]]])
def test_invalid_fit_vectors(vectors):
    with pytest.raises(ValueError):
        RandomHyperplaneLSH().fit(np.asarray(vectors, dtype=float))


def test_query_requires_fit_and_matching_dimension():
    index = RandomHyperplaneLSH()
    with pytest.raises(RuntimeError):
        index.query([1., 0.])
    index.fit([[1., 0.], [0., 1.]])
    with pytest.raises(ValueError):
        index.query([1., 0., 0.])


def test_zero_query_and_invalid_top_k():
    index = RandomHyperplaneLSH().fit([[1., 0.], [0., 1.]])
    with pytest.raises(ValueError):
        index.query([0., 0.])
    with pytest.raises(ValueError):
        index.query([1., 0.], top_k=0)
