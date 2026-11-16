# Optical flow: Lucas–Kanade, TV-L1, Farnebäck and DIS

This package contains three executable optical-flow treatments:

- A single-scale dense local Lucas–Kanade implementation using SciPy's vectorised local-window filters, plus a pure-Python reference implementation for small fixtures and step-by-step study.
- A scikit-image TV-L1 variational dense-flow wrapper.
- An OpenCV-backed Farnebäck dense-flow wrapper based on polynomial expansion.
- An OpenCV-backed DIS dense inverse-search wrapper with explicit speed/quality preset and refinement parameters.

## Install and run

    python -m pip install -r requirements.txt
    python -m pytest -q

## Coordinate and image contract

Inputs are equally shaped, finite, single-channel 2D image frames on the same pixel grid. The dense wrappers convert numeric inputs to 8-bit grayscale by clipping to [0,255]; scale and normalise scientific imagery deliberately before calling them. Output u is horizontal column displacement and v is vertical row displacement from the first frame toward the second. The flow is in pixels, not map units.

For a georeferenced raster, convert (u,v) using the raster affine linear transform. Do not interpret apparent image motion as physical ground motion without accounting for platform motion, orthorectification, terrain parallax, acquisition interval and image formation.

## TV-L1 variational flow

The TV-L1 wrapper calls scikit-image's `optical_flow_tvl1`, returning horizontal (u/column) and vertical (v/row) displacement fields. It rescales the uint8 frame inputs to [0,1] and exposes attachment, tightness, warping and iteration controls. This is a library-backed implementation, not a from-scratch solver.

## Farnebäck

The wrapper calls OpenCV's calcOpticalFlowFarneback and exposes pyramid scale, levels, window size, iterations, polynomial neighbourhood and sigma. It is a library-backed implementation, not a from-scratch reproduction of the polynomial expansion method.

## DIS

The wrapper calls OpenCV's DISOpticalFlow implementation and exposes the ultrafast, fast and medium presets, finest scale, patch size/stride, gradient-descent iterations and variational-refinement toggle. It is a library-backed implementation, not a from-scratch reproduction of the inverse-search algorithm.

## Tests

Synthetic translated texture fixtures check the direction and approximate magnitude of both dense flow fields. Invalid input and parameter contracts are also tested. These fixtures do not constitute a broad benchmark across occlusion, radiometric change, large motion, textureless regions or real satellite sequences.

See the [method-selection guide](../../../methods/optical-flow.md) for assumptions, failure modes and evaluation recommendations.


The pure-Python `lucas_kanade_dense_reference` function exposes the local normal-equation accumulation directly and uses the smallest structure-tensor eigenvalue as its conditioning test. It is intentionally slower than the vectorised `lucas_kanade` function and is included as a transparent reference, not a production path.


## Image co-registration

The companion `image_registration.py` module provides FFT phase correlation for global row/column translation and RANSAC affine estimation from matched (x,y) point pairs. Phase correlation returns the shift to apply to the moving image; affine estimation returns a 2×2 matrix, offset and inlier diagnostics. These are transform estimators, not feature detectors or orthorectification. See [the canonical lesson](../../../algorithms/remote-sensing/image-coregistration.md) and `test_image_registration.py`.


## ORB feature matching

The image-registration module exposes ORB and AKAZE binary feature detection plus SIFT floating-point descriptors. It returns moving-image source coordinates and reference-image target coordinates after a Hamming-distance nearest-neighbour ratio test. Pass those arrays to the affine RANSAC estimator to obtain a robust moving-to-reference transform. Intensities are interpreted on a 0–255 scale; scale scientific imagery before use. These are classical single-image-modality feature baselines, not cross-modal optical-SAR matchers. SIFT uses L2 descriptor distance; ORB and AKAZE use Hamming distance. Repeated texture, weak texture, strong seasonal change and radiometric differences can produce incorrect matches.


## Enhanced-correlation coefficient (ECC) registration

The ecc_register function estimates translation, Euclidean, affine or projective homography alignment by maximising the enhanced correlation coefficient. It returns an OpenCV inverse-map warp matrix, aligned moving image and correlation coefficient. The warp matrix is applied internally with WARP_INVERSE_MAP. ECC is a local optimiser and is sensitive to initial displacement, overlap and radiometric differences; initialise large offsets with phase correlation or feature-based matching. Inputs are interpreted on a 0–255 intensity scale and the aligned output is float32 in [0,1].
