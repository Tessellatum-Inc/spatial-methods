# Image co-registration: phase correlation and affine RANSAC

## Translation by phase correlation

Phase correlation normalizes the cross-power spectrum of two images and locates the inverse-FFT correlation peak. The returned row/column shift is the translation to apply to the moving image to align it to the reference. Optional parabolic peak interpolation estimates subpixel displacement. FFT correlation is circular, so large shifts can wrap; tapering reduces edge discontinuities but may alter weak edge content.

## Affine transform from matched points

The affine estimator uses matched (x,y) coordinate pairs and RANSAC. Each candidate is estimated from three non-collinear correspondences, scored by Euclidean residual threshold, and refitted to the consensus inliers. It returns a 2×2 matrix and offset satisfying target = source @ matrix.T + offset.

## Scope

These functions estimate global translation or affine geometry. They do not detect features, establish correspondences, model local deformation, orthorectify terrain, correct sensor geometry, or guarantee a physically meaningful registration. Feature matching and transform estimation must be evaluated together using independent checkpoints and residual maps. Pixel coordinates are not map coordinates unless the image georeferencing is explicitly applied.


## ORB feature correspondences

The local-feature matcher supports ORB and AKAZE binary descriptors (Hamming distance) and SIFT descriptors (L2 distance). It detects keypoints in both images, matches moving-image descriptors to reference-image descriptors and filters ambiguous pairs with a nearest-neighbour ratio test. Its output coordinates feed the affine RANSAC estimator above. These are classical single-modality methods; learned matchers, optical-SAR matching and local deformation models remain open.


## Enhanced correlation coefficient registration

ECC optimises a global parametric warp by maximising a photometrically normalised correlation objective. The reference implementation supports translation, Euclidean, affine and projective homography models through OpenCV. Its returned matrix follows OpenCV's inverse-map convention and is used with WARP_INVERSE_MAP when resampling the moving image. ECC is a local optimiser; use phase correlation or feature correspondences to initialise large shifts, and inspect overlap and independent checkpoints. It is not a substitute for sensor-model orthorectification or local deformation modelling.


## Tiled local correlation for displacement fields

The local phase-correlation field method runs the global phase-correlation estimator over a regular grid of image windows. Each window yields a subpixel translation, allowing spatial variation in apparent displacement to be inspected rather than forcing one global transform. Textureless windows are masked. This is a compact local correlation baseline, not the full COSI-Corr method; robust geophysical displacement analysis also needs stable feature content, uncertainty estimation, decorrelation screening, orthorectification and conversion from pixel displacement to ground coordinates.


## Mutual-information registration

The translation-only mutual-information estimator maximises the joint-histogram mutual information between the reference and shifted moving image. It can tolerate nonlinear intensity relationships better than direct pixelwise correlation, making it a useful baseline for some multimodal image pairs. Histogram binning, overlap changes, interpolation and search bounds influence the objective; inspect the returned overlap and use independent checkpoints. This is not a full multimodal affine or deformable registration system.
