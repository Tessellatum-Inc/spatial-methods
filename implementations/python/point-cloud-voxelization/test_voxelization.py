import numpy as np
import pytest
from voxelization import voxelize


def test_groups_points_and_returns_consistent_aggregates():
    points = np.array([[0.1, 0.1, 0.1], [0.2, 0.2, 0.2],
                       [1.1, 0.1, 0.1], [1.2, 0.2, 0.2]])
    out = voxelize(points, 1.0, origin=(0, 0, 0))
    assert out["voxel_indices"].tolist() == [[0, 0, 0], [1, 0, 0]]
    assert out["counts"].tolist() == [2, 2]
    assert np.allclose(out["centroids"], [[.15, .15, .15], [1.15, .15, .15]])
    assert np.allclose(out["minima"][0], [.1, .1, .1])
    assert np.allclose(out["maxima"][1], [1.2, .2, .2])


def test_half_open_boundaries_and_negative_coordinates():
    points = np.array([[-1., 0, 0], [0., 0, 0], [1., 0, 0]])
    out = voxelize(points, 1., origin=(-1., 0, 0))
    assert out["voxel_indices"][:, 0].tolist() == [0, 1, 2]


def test_anisotropic_voxel_size_and_default_origin():
    points = np.array([[2., 4., 6.], [2.5, 5., 7.], [4., 8., 10.]])
    out = voxelize(points, (1., 2., 4.))
    assert np.allclose(out["origin"], [2, 4, 6])
    assert out["voxel_indices"].tolist() == [[0, 0, 0], [2, 2, 1]]


@pytest.mark.parametrize("points,size", [
    (np.ones(3), 1), (np.ones((0, 3)), 1), (np.ones((2, 3)), 0),
    (np.ones((2, 3)), (1, -1, 1)), (np.array([[0, 0, np.nan]]), 1),
])
def test_invalid_inputs_raise(points, size):
    with pytest.raises(ValueError):
        voxelize(points, size)


def test_point_to_voxel_mapping_reconstructs_counts():
    points = np.random.default_rng(1).normal(size=(100, 3))
    out = voxelize(points, .5)
    assert np.array_equal(np.bincount(out["point_to_voxel"]), out["counts"])
