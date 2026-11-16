# Point-cloud registration and geometric comparison

## Point-to-point iterative closest point

For each iteration, the source points are transformed, nearest target points are found, and a rigid least-squares transform is fitted to the paired coordinates. The SVD/Kabsch solution minimises the sum of squared point-to-point residuals for the current correspondences. Repeating correspondence search and rigid fitting yields a local optimiser, not a globally optimal registration.

The reference implementation uses row-vector coordinates and returns a rotation matrix and translation satisfying aligned = source @ rotation + translation. An optional maximum correspondence distance gates matches; trimmed fitting retains a declared fraction of the closest gated correspondences. RMSE, fitness and convergence diagnostics are returned.

## Geometric comparison

The package also calculates symmetric Chamfer distance (the mean of the two directed nearest-neighbour mean distances), Hausdorff distance (the larger directed maximum), and optional threshold precision, recall and F-score. These measures depend on point sampling density and threshold choice.

## Scope and validation

This is a point-to-point rigid baseline, not point-to-plane ICP, generalized ICP, normal-distributions transform (NDT), colored ICP, FPFH/RANSAC, TEASER++, or learned registration. ICP is sensitive to initial pose, overlap, density and repeated geometry. Validate with independent checkpoints, spatially distributed residuals and task-specific geometric constraints; a low nearest-neighbour RMSE alone does not prove correct registration.

Run the independent synthetic and brute-force tests in the implementation package README.
