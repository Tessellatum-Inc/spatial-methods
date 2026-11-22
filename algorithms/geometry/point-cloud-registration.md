# Point-cloud registration and geometric comparison

## Point-to-point iterative closest point

For each iteration, the source points are transformed, nearest target points are found, and a rigid least-squares transform is fitted to the paired coordinates. The SVD/Kabsch solution minimises the sum of squared point-to-point residuals for the current correspondences. Repeating correspondence search and rigid fitting yields a local optimiser, not a globally optimal registration.

The reference implementation uses row-vector coordinates and returns a rotation matrix and translation satisfying aligned = source @ rotation + translation. An optional maximum correspondence distance gates matches; trimmed fitting retains a declared fraction of the closest gated correspondences.

## Point-to-plane iterative closest point

When target surface normals are available, point-to-plane ICP minimises n dot (p - q), where p is a transformed source point, q its nearest target point and n the target normal. The implementation linearises the rigid motion into a six-parameter update and solves a least-squares system each iteration. Target normals are normalised internally; the method rejects correspondence geometry that does not constrain all six rigid degrees of freedom.

Point-to-plane ICP can converge faster and yield lower surface-normal residuals than point-to-point ICP near a good initial alignment. It is sensitive to normal quality and can be under-constrained on planes, symmetric objects or poorly distributed surfaces. The returned RMSE is a point-to-plane residual, not Euclidean nearest-neighbour RMSE.

## Geometric comparison

The package calculates symmetric Chamfer distance (the mean of the two directed nearest-neighbour mean distances), Hausdorff distance (the larger directed maximum), and optional threshold precision, recall and F-score. These measures depend on point sampling density and threshold choice.

## Scope and validation

Generalized ICP extends the correspondence objective with local covariance models. For source point covariance (C_s), target covariance (C_t), and current rotation (R), the combined residual covariance is (C_t + R C_s R^T). The implementation estimates each covariance from a k-neighbourhood, applies a relative eigenvalue floor for numerical stability, and minimizes the corresponding Mahalanobis residuals with a six-parameter Gauss–Newton update. It reports Euclidean and Mahalanobis residual measures separately. The result remains a local optimizer and is sensitive to neighbourhood scale and initial alignment.

These are rigid local-registration baselines, not NDT, colored ICP, FPFH/RANSAC, TEASER++, or learned registration. Validate with independent checkpoints, spatially distributed residuals and task-specific geometric constraints; a low nearest-neighbour or point-to-plane RMSE alone does not prove correct registration.

Run the independent synthetic and brute-force tests in the implementation package README.


## Normal distributions transform

Normal distributions transform (NDT) replaces explicit point-to-point matches with a piecewise Gaussian model of the target cloud. A voxel containing enough target samples is represented by its sample mean and covariance. A transformed source point contributes a Mahalanobis residual to the Gaussian of its containing voxel. The implementation builds regularised voxel covariances, associates points by hard voxel membership and solves a damped six-parameter Gauss–Newton update. Its transform follows the same row-vector convention as the ICP methods.

Voxel size controls the spatial scale of the probability model; minimum occupancy controls which cells are trusted. Too-small voxels produce sparse or unstable models, while too-large voxels blur local geometry. Hard voxel assignment creates discontinuities at cell boundaries, so this implementation is a bounded teaching baseline rather than a full multi-resolution production NDT system. It requires a reasonable initial pose and overlapping clouds. The reported RMSE is Euclidean distance to voxel means, not point-to-point nearest-neighbour RMSE.


## Acquisition context

For static terrestrial laser scanning, see the [terrestrial laser scanning and point-cloud acquisition method](../../collection/terrestrial-laser-scanning-and-point-cloud-acquisition.md). It explains scan-network planning, overlap and registrability, target/control/check-point roles, independent validation and why local registration residuals do not establish absolute accuracy.
