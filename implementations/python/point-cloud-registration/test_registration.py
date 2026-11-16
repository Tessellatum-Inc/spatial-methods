import numpy as np
import pytest
from registration import iterative_closest_point, point_cloud_distances



def test_icp_recovers_known_rigid_transform_on_asymmetric_cloud():
    x, y, z = np.meshgrid(np.arange(6.), np.arange(5.) * 1.3,
                          np.arange(6.) * 0.7, indexing="ij")
    source = np.column_stack((x.ravel(), y.ravel(), z.ravel()))
    source += np.random.default_rng(41).normal(0, 0.015, source.shape)
    angle = 0.02
    rotation = np.array([[np.cos(angle), -np.sin(angle), 0.0],
                        [np.sin(angle), np.cos(angle), 0.0],
                        [0.0, 0.0, 1.0]])
    translation = np.array([0.025, -0.02, 0.015])
    target = source @ rotation + translation
    result = iterative_closest_point(source, target, max_iterations=80,
        tolerance=1e-12, max_correspondence_distance=0.5)
    np.testing.assert_allclose(result["aligned"], target, atol=1e-8)
    np.testing.assert_allclose(result["rotation"], rotation, atol=1e-8)
    np.testing.assert_allclose(result["translation"], translation, atol=1e-8)
    assert result["rmse"] < 1e-8
    assert result["fitness"] == 1.0


def test_icp_trimmed_correspondences_handle_distant_source_outliers():
    rng = np.random.default_rng(8)
    target = rng.normal(size=(250, 3))
    source = target.copy()
    source[:25] += np.array([8.0, -6.0, 5.0])
    result = iterative_closest_point(source, target, trim_fraction=0.8,
        max_iterations=100, max_correspondence_distance=2.0)
    assert result["rmse"] < 1e-7
    assert result["correspondence_count"] >= 200


def test_symmetric_cloud_distances_and_f_score():
    a = np.array([[0., 0., 0.], [1., 0., 0.], [0., 1., 0.]])
    b = a + np.array([0.1, 0., 0.])
    result = point_cloud_distances(a, b, threshold=0.11)
    assert result["chamfer_distance"] == pytest.approx(0.1)
    assert result["hausdorff_distance"] == pytest.approx(0.1)
    assert result["precision"] == result["recall"] == result["f_score"] == 1.0


def test_point_cloud_distance_independent_brute_force_oracle():
    rng = np.random.default_rng(2)
    a, b = rng.normal(size=(11, 3)), rng.normal(size=(13, 3))
    pairwise = np.linalg.norm(a[:, None, :] - b[None, :, :], axis=2)
    da, db = pairwise.min(axis=1), pairwise.min(axis=0)
    result = point_cloud_distances(a, b)
    assert result["chamfer_distance"] == pytest.approx((da.mean() + db.mean()) / 2)
    assert result["hausdorff_distance"] == pytest.approx(max(da.max(), db.max()))


@pytest.mark.parametrize("bad", [np.ones((4, 2)), np.array([[0., 0., np.nan]])])
def test_point_cloud_shape_and_finite_validation(bad):
    with pytest.raises(ValueError):
        point_cloud_distances(bad, np.ones((4, 3)))


def test_icp_rejects_invalid_controls_and_degenerate_matches():
    with pytest.raises(ValueError):
        iterative_closest_point(np.ones((3, 3)), np.ones((3, 3)), max_iterations=0)
    with pytest.raises(ValueError):
        iterative_closest_point(np.ones((3, 3)), np.ones((3, 3)), trim_fraction=0)
    with pytest.raises(ValueError):
        iterative_closest_point(np.zeros((5, 3)), np.ones((5, 3)))
    with pytest.raises(ValueError):
        iterative_closest_point(np.ones((3, 3)), np.ones((3, 3)),
                                max_correspondence_distance=0.0)


from registration import point_to_plane_icp


def test_point_to_plane_icp_recovers_small_rigid_pose_on_ellipsoid():
    rng = np.random.default_rng(22)
    directions = rng.normal(size=(2500, 3))
    directions /= np.linalg.norm(directions, axis=1)[:, None]
    target = directions * np.array([2.0, 1.4, 0.9])
    normals = target / np.array([2.0, 1.4, 0.9]) ** 2
    normals /= np.linalg.norm(normals, axis=1)[:, None]
    from scipy.spatial.transform import Rotation
    expected_rotation = Rotation.from_rotvec([0.004, -0.006, 0.005])
    expected_translation = np.array([0.008, -0.006, 0.005])
    source = expected_rotation.inv().apply(target - expected_translation)
    result = point_to_plane_icp(source, target, normals,
        max_iterations=20, tolerance=1e-12, max_correspondence_distance=0.1)
    np.testing.assert_allclose(result["aligned"], target, atol=1e-7)
    np.testing.assert_allclose(result["rotation"], expected_rotation.as_matrix().T,
                               atol=1e-7)
    np.testing.assert_allclose(result["translation"], expected_translation,
                               atol=1e-7)
    assert result["rmse"] < 1e-8
    assert result["fitness"] == 1.0


def test_point_to_plane_icp_rejects_degenerate_normal_geometry():
    cloud = np.array([[x, y, 0.0] for x in range(4) for y in range(4)], dtype=float)
    normals = np.tile([0.0, 0.0, 1.0], (len(cloud), 1))
    with pytest.raises(ValueError, match="do not constrain"):
        point_to_plane_icp(cloud + [0, 0, 0.01], cloud, normals)
    normals[0] = 0
    with pytest.raises(ValueError, match="non-zero"):
        point_to_plane_icp(cloud, cloud, normals)



from scipy.spatial import cKDTree
from registration import generalized_icp


def test_generalized_icp_recovers_small_rigid_pose_on_anisotropic_cloud():
    rng = np.random.default_rng(73)
    target = rng.normal(size=(700, 3)) * np.array([2.0, 1.1, 0.6])
    from scipy.spatial.transform import Rotation
    expected = Rotation.from_rotvec([0.002, -0.003, 0.0015])
    translation = np.array([0.004, -0.003, 0.002])
    source = expected.inv().apply(target - translation)
    result = generalized_icp(source, target, neighbors=24, max_iterations=35,
        tolerance=1e-10, max_correspondence_distance=0.15)
    np.testing.assert_allclose(result["aligned"], target, atol=2e-5)
    np.testing.assert_allclose(result["rotation"], expected.as_matrix().T, atol=2e-5)
    np.testing.assert_allclose(result["translation"], translation, atol=2e-5)
    assert result["rmse"] < 2e-5
    assert result["mahalanobis_rmse"] >= 0
    assert result["fitness"] == 1.0


def test_gicp_covariance_weighting_has_independent_analytic_fixture():
    from registration import _local_covariances
    points = np.array([[0., 0., 0.], [1., 0., 0.], [0., 2., 0.],
                       [0., 0., 3.], [1., 2., 1.]])
    cov = _local_covariances(points, cKDTree(points), 5, 1e-3)[0]
    centred = points - points.mean(axis=0)
    expected = centred.T @ centred / 4
    values = np.linalg.eigvalsh(expected)
    assert np.all(np.linalg.eigvalsh(cov) > 0)
    assert np.linalg.eigvalsh(cov)[-1] == pytest.approx(values[-1])


def test_gicp_rejects_invalid_controls_and_underdetermined_geometry():
    cloud = np.array([[float(x), 0., 0.] for x in range(12)])
    with pytest.raises(ValueError, match="neighbors"):
        generalized_icp(cloud, cloud, neighbors=2)
    with pytest.raises(ValueError, match="regularization"):
        generalized_icp(cloud, cloud, covariance_regularization=0)
    with pytest.raises(ValueError, match="do not constrain"):
        generalized_icp(cloud, cloud, neighbors=3)



def test_ndt_recovers_small_translation_from_voxel_gaussian_model():
    rng = np.random.default_rng(314)
    chunks = []
    for x in range(4):
        for y in range(4):
            for z in range(4):
                chunks.append(np.array([x, y, z]) + rng.uniform(0.08, 0.92, (70, 3)))
    target = np.vstack(chunks)
    shift = np.array([0.012, -0.009, 0.007])
    source = target - shift
    result = normal_distributions_transform(source, target, voxel_size=1.0,
        min_points_per_voxel=20, max_iterations=50, tolerance=1e-10)
    np.testing.assert_allclose(result["aligned"], target, atol=2e-3)
    np.testing.assert_allclose(result["translation"], shift, atol=2e-3)
    assert result["voxel_count"] == 64
    assert result["fitness"] > 0.95


def test_ndt_rejects_invalid_parameters_and_sparse_voxel_model():
    cloud = np.random.default_rng(3).normal(size=(40, 3))
    with pytest.raises(ValueError, match="voxel_size"):
        normal_distributions_transform(cloud, cloud, voxel_size=0)
    with pytest.raises(ValueError, match="min_points"):
        normal_distributions_transform(cloud, cloud, min_points_per_voxel=2)
    with pytest.raises(ValueError, match="two populated"):
        normal_distributions_transform(cloud, cloud, voxel_size=100,
                                       min_points_per_voxel=50)


from registration import normal_distributions_transform
