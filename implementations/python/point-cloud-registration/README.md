# Point-cloud registration and geometric evaluation

This package provides point-to-point, point-to-plane and generalized rigid ICP baselines, plus symmetric point-cloud distance metrics.

## Install and test

    python -m pip install -r requirements.txt
    python -m pytest -q

## Point-to-point ICP

The iterative_closest_point function estimates a proper rigid transform from source to target using nearest-neighbour correspondences and an SVD/Kabsch least-squares fit. Coordinates are row vectors in a shared 3D Cartesian frame; the result obeys aligned = source @ rotation + translation. Optional maximum correspondence distance and trimmed fitting can reject distant matches.

## Point-to-plane ICP

The point_to_plane_icp function requires target-frame surface normals. It minimises signed point-to-plane residuals with a linearised six-parameter rigid update at each iteration. Normals are normalised internally; the method reports point-to-plane RMSE, transform, fitness and convergence diagnostics. The Jacobian must constrain all six degrees of freedom, so planar, symmetric or poorly distributed geometry is rejected or may be ill-conditioned. A useful initial pose and sufficient overlap remain essential.

Both methods are local optimisers. These methods do not provide normal estimation, feature descriptors, RANSAC correspondence generation, loop closure or uncertainty. Point-to-plane accuracy depends on normal quality and spatial distribution; validate with independent checkpoints and residual maps.

## Point-cloud comparison

The point_cloud_distances function returns symmetric Chamfer and Hausdorff distances from nearest-neighbour distances. An optional distance threshold also returns precision, recall and F-score. These metrics are sampling-density-sensitive and do not replace registration diagnostics or semantic/topological validation.

See the canonical lesson at algorithms/geometry/point-cloud-registration.md.


## Generalized ICP

The `generalized_icp` function estimates regularised local covariance matrices from each cloud's k-neighbourhoods. Each correspondence is weighted by the inverse combined covariance (C_t + R C_s R^T), and a six-parameter Gauss–Newton update estimates the rigid pose. It reports Euclidean nearest-neighbour RMSE and covariance-weighted Mahalanobis RMSE separately. The neighbourhood size and relative eigenvalue floor are explicit controls. This is a compact teaching implementation of the GICP objective, not a replacement for optimized production implementations; neighbourhood scale, initialization, overlap and outliers materially affect results.


## Normal distributions transform (NDT)

The `normal_distributions_transform` function builds a Gaussian target model in fixed cubic voxels, retaining cells with at least the configured number of points. Each source point is associated with its containing populated voxel, and a covariance-weighted six-parameter Gauss–Newton update estimates the rigid pose. The returned RMSE is the Euclidean residual to voxel means; fitness is the fraction of source points associated with retained voxels. This hard-assignment implementation is a compact NDT teaching baseline: voxel size, minimum occupancy, initial pose and voxel-boundary effects matter. It does not implement multi-resolution NDT, neighbouring-voxel likelihood aggregation or production line-search strategies.


## Acquisition context

The [terrestrial laser scanning and point-cloud acquisition method](../../../collection/terrestrial-laser-scanning-and-point-cloud-acquisition.md) describes field planning, scan overlap, control and independent validation for static TLS. The algorithms here are local computational registration baselines; they do not replace a scan-network design or independent survey checks.
