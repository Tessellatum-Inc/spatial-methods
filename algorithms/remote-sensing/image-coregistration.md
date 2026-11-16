# Image co-registration: phase correlation and affine RANSAC

## Translation by phase correlation

Phase correlation normalizes the cross-power spectrum of two images and locates the inverse-FFT correlation peak. The returned row/column shift is the translation to apply to the moving image to align it to the reference. Optional parabolic peak interpolation estimates subpixel displacement. FFT correlation is circular, so large shifts can wrap; tapering reduces edge discontinuities but may alter weak edge content.

## Affine transform from matched points

The affine estimator uses matched (x,y) coordinate pairs and RANSAC. Each candidate is estimated from three non-collinear correspondences, scored by Euclidean residual threshold, and refitted to the consensus inliers. It returns a 2×2 matrix and offset satisfying target = source @ matrix.T + offset.

## Scope

These functions estimate global translation or affine geometry. They do not detect features, establish correspondences, model local deformation, orthorectify terrain, correct sensor geometry, or guarantee a physically meaningful registration. Feature matching and transform estimation must be evaluated together using independent checkpoints and residual maps. Pixel coordinates are not map coordinates unless the image georeferencing is explicitly applied.


## ORB feature correspondences

The companion ORB matcher detects keypoints and binary descriptors in each image, matches moving-image descriptors to reference-image descriptors with Hamming distance, and filters ambiguous pairs using a nearest-neighbour ratio test. Its output coordinates feed the affine RANSAC estimator above. This closes a basic classical feature-detection-and-matching path, but does not implement SIFT, AKAZE, learned matchers, multimodal matching or local deformation models.
