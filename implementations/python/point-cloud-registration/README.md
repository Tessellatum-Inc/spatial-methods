# Point-cloud registration and geometric evaluation

This package provides point-to-point and point-to-plane rigid ICP baselines, plus symmetric point-cloud distance metrics.

## Install and test

    python -m pip install -r requirements.txt
    python -m pytest -q

## Point-to-point ICP

The iterative_closest_point function estimates a proper rigid transform from source to target using nearest-neighbour correspondences and an SVD/Kabsch least-squares fit. Coordinates are row vectors in a shared 3D Cartesian frame; the result obeys aligned = source @ rotation + translation. Optional maximum correspondence distance and trimmed fitting can reject distant matches.

## Point-to-plane ICP

The point_to_plane_icp function requires target-frame surface normals. It minimises signed point-to-plane residuals with a linearised six-parameter rigid update at each iteration. Normals are normalised internally; the method reports point-to-plane RMSE, transform, fitness and convergence diagnostics. The Jacobian must constrain all six degrees of freedom, so planar, symmetric or poorly distributed geometry is rejected or may be ill-conditioned. A useful initial pose and sufficient overlap remain essential.

Both methods are local optimisers. Neither implements generalized ICP, normal estimation, NDT, feature descriptors, RANSAC correspondence generation, loop closure or uncertainty. Point-to-plane accuracy depends on normal quality and spatial distribution; validate with independent checkpoints and residual maps.

## Point-cloud comparison

The point_cloud_distances function returns symmetric Chamfer and Hausdorff distances from nearest-neighbour distances. An optional distance threshold also returns precision, recall and F-score. These metrics are sampling-density-sensitive and do not replace registration diagnostics or semantic/topological validation.

See the canonical lesson at algorithms/geometry/point-cloud-registration.md.
