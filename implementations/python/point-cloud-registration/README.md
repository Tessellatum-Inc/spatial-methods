# Point-cloud registration and geometric evaluation

This package provides a transparent 3D point-to-point iterative closest point (ICP) baseline and symmetric point-cloud distance metrics.

## Install and test

    python -m pip install -r requirements.txt
    python -m pytest -q

## Rigid point-to-point ICP

The iterative_closest_point function estimates a proper rigid transform from source to target using nearest-neighbour correspondences and an SVD/Kabsch least-squares fit. Coordinates are row vectors in a shared 3D Cartesian frame; the result obeys aligned = source @ rotation + translation. Optional maximum correspondence distance and trimmed fitting can reject distant matches. The output includes aligned points, transform, RMSE, iteration count, convergence flag, correspondence count and fitness.

ICP is a local optimiser. It needs a useful initial alignment, sufficient overlap and geometry that constrains all three dimensions. Symmetric or repetitive structures, poor initialisation, partial overlap, density differences and outliers can produce incorrect local minima. This implementation is point-to-point only: it does not implement point-to-plane or generalized ICP, normal estimation, NDT, feature descriptors, RANSAC correspondence generation, loop closure or uncertainty.

## Point-cloud comparison

The point_cloud_distances function returns symmetric Chamfer and Hausdorff distances from nearest-neighbour distances. An optional distance threshold also returns precision, recall and F-score. These metrics are sampling-density-sensitive and do not replace registration diagnostics, point-to-plane residuals, spatially distributed checkpoints or semantic/topological validation.

See the canonical lesson at algorithms/geometry/point-cloud-registration.md.
