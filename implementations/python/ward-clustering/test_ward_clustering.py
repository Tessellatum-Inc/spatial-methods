import numpy as np
import pytest
from ward_clustering import ward_linkage, cut_ward_tree, ward_clustering


def test_three_point_line_matches_hand_calculated_ward_heights():
    z = ward_linkage(np.array([[0.], [2.], [10.]]))
    np.testing.assert_allclose(z[:, :3], [[0, 1, 2], [2, 3, np.sqrt(108)]])
    np.testing.assert_array_equal(z[:, 3], [2, 3])


def test_cut_tree_and_wrapper_return_expected_partition():
    x = np.array([[0.], [2.], [10.], [11.]])
    z = ward_linkage(x)
    labels = cut_ward_tree(z, 4, 2)
    assert labels[0] == labels[1]
    assert labels[2] == labels[3]
    assert labels[0] != labels[2]
    fit = ward_clustering(x, 2)
    np.testing.assert_array_equal(fit["labels"], labels)


def test_ties_are_deterministic_and_identical_points_are_supported():
    x = np.zeros((4, 2))
    a = ward_linkage(x)
    b = ward_linkage(x)
    np.testing.assert_array_equal(a, b)
    assert a[0, 0:2].tolist() == [0.0, 1.0]
    assert np.all(a[:, 2] == 0)


def test_single_observation_can_be_cut_as_one_cluster():
    fit = ward_clustering(np.array([[4., 5.]]), 1)
    assert fit["linkage"].shape == (0, 4)
    assert fit["labels"].tolist() == [0]


def test_invalid_observations_and_k_are_rejected():
    with pytest.raises(ValueError, match="2-D"):
        ward_linkage(np.array([1., 2.]))
    with pytest.raises(ValueError, match="finite"):
        ward_linkage(np.array([[0.], [np.nan]]))
    with pytest.raises(ValueError, match="two observations"):
        ward_linkage(np.array([[1.]]))
    with pytest.raises(ValueError, match="between 1"):
        ward_clustering(np.array([[0.], [1.]]), 3)
    with pytest.raises(ValueError, match="linkage"):
        cut_ward_tree(np.empty((0, 4)), 3, 1)
