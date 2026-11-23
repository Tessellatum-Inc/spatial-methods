# SLIC-style superpixels

Dependency-free SLIC-style clustering for rectangular raster feature arrays.
Each pixel supplies one or more finite feature values; colour imagery should
normally be converted to a perceptual space such as CIELAB by the caller.

The method initializes a regular grid of cluster centres, moves each seed to
a locally low-gradient pixel, then alternates local assignment and centre
updates. The joint distance is

    D^2 = d_feature^2 + (m/S)^2 d_spatial^2

where S is region_size and m is compactness. The output contains an integer
label raster, final centres and iteration count.

## Limits

This implementation omits connected-component enforcement/cleanup, so a
label may be disconnected in difficult images. It does not perform colour
space conversion, multi-resolution segmentation, graph cuts, MRF/CRF
inference, active contours or level sets. Results depend on feature scaling,
region_size and compactness. It is a transparent reference baseline, not a
replacement for optimized image-segmentation libraries.

## Tests

    python -m pytest -q
