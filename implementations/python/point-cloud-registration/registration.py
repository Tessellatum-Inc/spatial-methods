"""Rigid point-cloud registration and geometric evaluation baselines."""
from __future__ import annotations
import numpy as np
from scipy.spatial import cKDTree


def _points(values, name):
    points = np.asarray(values, dtype=float)
    if points.ndim != 2 or points.shape[1] != 3 or points.shape[0] < 3:
        raise ValueError(f"{name} must have shape (n, 3) with n >= 3")
    if not np.all(np.isfinite(points)):
        raise ValueError(f"{name} must contain only finite coordinates")
    return points


def _rigid_fit(source, target):
    """Least-squares proper rigid transform for row-vector coordinates."""
    source_centre, target_centre = source.mean(axis=0), target.mean(axis=0)
    x, y = source - source_centre, target - target_centre
    if np.linalg.matrix_rank(x) < 2:
        raise ValueError("source correspondences must contain three non-collinear points")
    u, _, vt = np.linalg.svd(x.T @ y)
    rotation = u @ vt
    if np.linalg.det(rotation) < 0:
        u[:, -1] *= -1
        rotation = u @ vt
    translation = target_centre - source_centre @ rotation
    return rotation, translation


def iterative_closest_point(source, target, *, max_iterations=100,
                             tolerance=1e-7, max_correspondence_distance=None,
                             trim_fraction=1.0):
    """Align a 3D source cloud to target using nearest-neighbour point-to-point ICP.

    The row-vector transform obeys aligned = source @ rotation + translation.
    Distance gating and trimmed fitting can reject distant correspondences.
    This is a local rigid baseline requiring useful initial alignment, overlap
    and non-degenerate geometry; it does not estimate scale or deformation.
    """
    src, dst = _points(source, "source"), _points(target, "target")
    if isinstance(max_iterations, (bool, np.bool_)) or not isinstance(max_iterations, (int, np.integer)) or max_iterations < 1:
        raise ValueError("max_iterations must be a positive integer")
    try:
        tol, trim = float(tolerance), float(trim_fraction)
    except (TypeError, ValueError):
        raise ValueError("tolerance and trim_fraction must be numeric") from None
    if not np.isfinite(tol) or tol < 0:
        raise ValueError("tolerance must be finite and non-negative")
    if not np.isfinite(trim) or not 0 < trim <= 1:
        raise ValueError("trim_fraction must be in (0, 1]")
    gate = None
    if max_correspondence_distance is not None:
        try:
            gate = float(max_correspondence_distance)
        except (TypeError, ValueError):
            raise ValueError("max_correspondence_distance must be positive") from None
        if not np.isfinite(gate) or gate <= 0:
            raise ValueError("max_correspondence_distance must be positive")

    tree, aligned = cKDTree(dst), src.copy()
    rotation_total, translation_total = np.eye(3), np.zeros(3)
    previous_rmse, converged, rmse, used = np.inf, False, np.inf, 0
    for iteration in range(1, int(max_iterations) + 1):
        distances, indices = tree.query(aligned, k=1)
        candidates = np.flatnonzero(np.isfinite(distances) &
                                    (True if gate is None else distances <= gate))
        if candidates.size < 3:
            raise ValueError("fewer than three correspondences satisfy the distance gate")
        if trim < 1:
            count = max(3, int(np.floor(trim * candidates.size)))
            candidates = candidates[np.argsort(distances[candidates], kind="stable")[:count]]
        delta_rotation, delta_translation = _rigid_fit(aligned[candidates], dst[indices[candidates]])
        aligned = aligned @ delta_rotation + delta_translation
        rotation_total = rotation_total @ delta_rotation
        translation_total = translation_total @ delta_rotation + delta_translation
        new_distances, _ = tree.query(aligned, k=1)
        valid = np.isfinite(new_distances) & (True if gate is None else new_distances <= gate)
        if not np.any(valid):
            raise ValueError("registration produced no valid correspondences")
        rmse = float(np.sqrt(np.mean(new_distances[valid] ** 2)))
        used = int(valid.sum())
        if abs(previous_rmse - rmse) <= tol:
            converged = True
            break
        previous_rmse = rmse
    return {"aligned": aligned, "rotation": rotation_total,
            "translation": translation_total, "rmse": rmse,
            "iterations": iteration, "converged": converged,
            "correspondence_count": used, "fitness": used / src.shape[0]}


def point_cloud_distances(first, second, *, threshold=None):
    """Return symmetric Chamfer/Hausdorff distances and optional threshold F-score."""
    a, b = _points(first, "first"), _points(second, "second")
    da, db = cKDTree(b).query(a, k=1)[0], cKDTree(a).query(b, k=1)[0]
    result = {"chamfer_distance": float((da.mean() + db.mean()) / 2),
              "hausdorff_distance": float(max(da.max(), db.max())),
              "first_to_second_mean": float(da.mean()),
              "second_to_first_mean": float(db.mean())}
    if threshold is not None:
        try:
            limit = float(threshold)
        except (TypeError, ValueError):
            raise ValueError("threshold must be finite and positive") from None
        if not np.isfinite(limit) or limit <= 0:
            raise ValueError("threshold must be finite and positive")
        precision, recall = float(np.mean(da <= limit)), float(np.mean(db <= limit))
        result.update({"precision": precision, "recall": recall,
                       "f_score": 0.0 if precision + recall == 0 else
                       2 * precision * recall / (precision + recall)})
    return result

def point_to_plane_icp(source, target, target_normals, *, max_iterations=50,
                        tolerance=1e-8, max_correspondence_distance=None,
                        trim_fraction=1.0):
    """Align 3D points by minimising point-to-plane correspondence residuals.

    Target normals must be supplied in the target frame. Each iteration solves
    the linearised six-parameter rigid update with residual n dot (p - q).
    The result uses the same row-vector transform convention as point-to-point
    ICP. This local method needs a good initial pose, overlap and spatially
    diverse normals; planar or symmetric geometry can be under-constrained.
    """
    from scipy.spatial.transform import Rotation

    src, dst = _points(source, "source"), _points(target, "target")
    normals = np.asarray(target_normals, dtype=float)
    if normals.shape != dst.shape or not np.all(np.isfinite(normals)):
        raise ValueError("target_normals must be finite and match target shape")
    lengths = np.linalg.norm(normals, axis=1)
    if np.any(lengths <= np.finfo(float).eps):
        raise ValueError("target_normals must be non-zero")
    normals = normals / lengths[:, None]
    if isinstance(max_iterations, (bool, np.bool_)) or not isinstance(max_iterations, (int, np.integer)) or max_iterations < 1:
        raise ValueError("max_iterations must be a positive integer")
    try:
        tol, trim = float(tolerance), float(trim_fraction)
    except (TypeError, ValueError):
        raise ValueError("tolerance and trim_fraction must be numeric") from None
    if not np.isfinite(tol) or tol < 0 or not np.isfinite(trim) or not 0 < trim <= 1:
        raise ValueError("tolerance must be non-negative and trim_fraction in (0, 1]")
    gate = None if max_correspondence_distance is None else float(max_correspondence_distance)
    if gate is not None and (not np.isfinite(gate) or gate <= 0):
        raise ValueError("max_correspondence_distance must be positive")

    tree = cKDTree(dst)
    aligned = src.copy()
    total_rotation = Rotation.identity()
    total_translation = np.zeros(3)
    previous_rmse = np.inf
    converged = False
    used = 0
    for iteration in range(1, int(max_iterations) + 1):
        distances, indices = tree.query(aligned, k=1)
        candidates = np.flatnonzero(np.isfinite(distances) &
                                    (True if gate is None else distances <= gate))
        if candidates.size < 6:
            raise ValueError("fewer than six correspondences satisfy the distance gate")
        if trim < 1:
            count = max(6, int(np.floor(trim * candidates.size)))
            candidates = candidates[np.argsort(distances[candidates], kind="stable")[:count]]
        p, q = aligned[candidates], dst[indices[candidates]]
        n = normals[indices[candidates]]
        residual = np.einsum("ij,ij->i", n, p - q)
        jacobian = np.column_stack((np.cross(p, n), n))
        update, _, rank, _ = np.linalg.lstsq(jacobian, -residual, rcond=None)
        if rank < 6:
            raise ValueError("point-to-plane correspondences do not constrain all six rigid degrees of freedom")
        delta_rotation = Rotation.from_rotvec(update[:3])
        delta_translation = update[3:]
        aligned = delta_rotation.apply(aligned) + delta_translation
        total_translation = delta_rotation.apply(total_translation) + delta_translation
        total_rotation = delta_rotation * total_rotation

        post_distances, post_indices = tree.query(aligned, k=1)
        valid = np.isfinite(post_distances) & (True if gate is None else post_distances <= gate)
        if not np.any(valid):
            raise ValueError("registration produced no valid correspondences")
        post_residual = np.einsum(
            "ij,ij->i", normals[post_indices[valid]],
            aligned[valid] - dst[post_indices[valid]])
        rmse = float(np.sqrt(np.mean(post_residual ** 2)))
        used = int(valid.sum())
        if abs(previous_rmse - rmse) <= tol:
            converged = True
            break
        previous_rmse = rmse

    return {"aligned": aligned, "rotation": total_rotation.as_matrix().T,
            "translation": total_translation, "rmse": rmse,
            "iterations": iteration, "converged": converged,
            "correspondence_count": used, "fitness": used / src.shape[0]}



def _local_covariances(points, tree, neighbors, regularization):
    """Estimate regularised local 3D covariance matrices from k-neighbourhoods."""
    _, indices = tree.query(points, k=neighbors)
    covariances = np.empty((len(points), 3, 3), dtype=float)
    for i, ids in enumerate(np.atleast_2d(indices)):
        neighbourhood = points[ids]
        centred = neighbourhood - neighbourhood.mean(axis=0)
        covariance = centred.T @ centred / max(len(ids) - 1, 1)
        values, vectors = np.linalg.eigh(covariance)
        floor = max(float(values[-1]) * regularization,
                    np.finfo(float).eps * max(float(values[-1]), 1.0))
        covariances[i] = (vectors * np.maximum(values, floor)) @ vectors.T
    return covariances


def generalized_icp(source, target, *, neighbors=20, max_iterations=50,
                    tolerance=1e-7, max_correspondence_distance=None,
                    trim_fraction=1.0, covariance_regularization=1e-3):
    """Generalized ICP (GICP) with local anisotropic covariance weighting.

    Local covariances are estimated from k-neighbourhoods in each cloud.
    For each nearest-neighbour pair, the residual is weighted by the inverse
    of C_target + R C_source R.T. A six-parameter Gauss-Newton rigid update
    is solved in the target frame. Coordinates are row vectors and the
    returned transform obeys aligned = source @ rotation + translation.

    This is a local rigid optimizer: it needs a useful initial pose, overlap,
    adequate sampling and well-conditioned 3D neighbourhoods. It is not
    globally convergent and does not estimate scale or deformation.
    """
    from scipy.spatial.transform import Rotation

    src, dst = _points(source, "source"), _points(target, "target")
    if isinstance(neighbors, (bool, np.bool_)) or not isinstance(neighbors, (int, np.integer)) or not 3 <= neighbors <= min(len(src), len(dst)):
        raise ValueError("neighbors must be an integer between 3 and both cloud sizes")
    if isinstance(max_iterations, (bool, np.bool_)) or not isinstance(max_iterations, (int, np.integer)) or max_iterations < 1:
        raise ValueError("max_iterations must be a positive integer")
    try:
        tol, trim, reg = float(tolerance), float(trim_fraction), float(covariance_regularization)
    except (TypeError, ValueError):
        raise ValueError("tolerance, trim_fraction and covariance_regularization must be numeric") from None
    if not np.isfinite(tol) or tol < 0:
        raise ValueError("tolerance must be finite and non-negative")
    if not np.isfinite(trim) or not 0 < trim <= 1:
        raise ValueError("trim_fraction must be in (0, 1]")
    if not np.isfinite(reg) or not 0 < reg < 1:
        raise ValueError("covariance_regularization must be in (0, 1)")
    gate = None if max_correspondence_distance is None else float(max_correspondence_distance)
    if gate is not None and (not np.isfinite(gate) or gate <= 0):
        raise ValueError("max_correspondence_distance must be positive")

    source_tree, target_tree = cKDTree(src), cKDTree(dst)
    source_cov = _local_covariances(src, source_tree, int(neighbors), reg)
    target_cov = _local_covariances(dst, target_tree, int(neighbors), reg)
    aligned = src.copy()
    total_rotation = Rotation.identity()
    total_translation = np.zeros(3)
    previous_rmse, converged = np.inf, False
    used, mahalanobis_rmse = 0, np.inf

    for iteration in range(1, int(max_iterations) + 1):
        distances, indices = target_tree.query(aligned, k=1)
        candidates = np.flatnonzero(np.isfinite(distances) &
                                    (True if gate is None else distances <= gate))
        if candidates.size < 6:
            raise ValueError("fewer than six correspondences satisfy the distance gate")
        if trim < 1:
            count = max(6, int(np.floor(trim * candidates.size)))
            candidates = candidates[np.argsort(distances[candidates], kind="stable")[:count]]

        rotation = total_rotation.as_matrix()
        hessian, gradient = np.zeros((6, 6)), np.zeros(6)
        weighted_error = 0.0
        for i in candidates:
            p, q = aligned[i], dst[indices[i]]
            covariance = target_cov[indices[i]] + rotation @ source_cov[i] @ rotation.T
            precision = np.linalg.inv(covariance)
            residual = p - q
            x, y, z = p
            skew = np.array([[0.0, -z, y], [z, 0.0, -x], [-y, x, 0.0]])
            jacobian = np.column_stack((-skew, np.eye(3)))
            hessian += jacobian.T @ precision @ jacobian
            gradient += jacobian.T @ precision @ residual
            weighted_error += float(residual @ precision @ residual)
        if np.linalg.matrix_rank(hessian) < 6:
            raise ValueError("GICP correspondences do not constrain all six rigid degrees of freedom")
        update = np.linalg.solve(hessian, -gradient)
        delta_rotation = Rotation.from_rotvec(update[:3])
        delta_translation = update[3:]
        aligned = delta_rotation.apply(aligned) + delta_translation
        total_translation = delta_rotation.apply(total_translation) + delta_translation
        total_rotation = delta_rotation * total_rotation

        post_distances, post_indices = target_tree.query(aligned, k=1)
        valid = np.isfinite(post_distances) & (True if gate is None else post_distances <= gate)
        if valid.sum() < 6:
            raise ValueError("registration produced fewer than six valid correspondences")
        euclidean_rmse = float(np.sqrt(np.mean(post_distances[valid] ** 2)))
        post_rotation = total_rotation.as_matrix()
        post_weighted = 0.0
        for i in np.flatnonzero(valid):
            covariance = target_cov[post_indices[i]] + post_rotation @ source_cov[i] @ post_rotation.T
            residual = aligned[i] - dst[post_indices[i]]
            post_weighted += float(residual @ np.linalg.solve(covariance, residual))
        mahalanobis_rmse = float(np.sqrt(post_weighted / valid.sum()))
        used = int(valid.sum())
        if abs(previous_rmse - euclidean_rmse) <= tol and np.linalg.norm(update) <= np.sqrt(tol + 1e-15):
            converged = True
            break
        previous_rmse = euclidean_rmse

    return {"aligned": aligned, "rotation": total_rotation.as_matrix().T,
            "translation": total_translation, "rmse": euclidean_rmse,
            "mahalanobis_rmse": mahalanobis_rmse, "iterations": iteration,
            "converged": converged, "correspondence_count": used,
            "fitness": used / src.shape[0]}
