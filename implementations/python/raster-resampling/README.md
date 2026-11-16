# Raster resampling: nearest, bilinear, cubic and Lanczos

This teaching implementation resamples a 2D array to a new shape over the same extent and orientation. It implements nearest-neighbour, bilinear, Keys cubic-convolution (Catmull–Rom, a=-0.5) and Lanczos-3 interpolation. It is not a full geospatial warp.

## Install and test

~~~bash
python -m pip install -r requirements.txt
python -m pytest -q
~~~

## Method selection

- **Nearest neighbour** copies the closest source cell. It preserves categorical labels and class codes.
- **Bilinear** uses the four surrounding samples. It is appropriate for many continuous surfaces, but smooths local extremes.
- **Cubic convolution** uses a 4×4 support and a Keys cubic kernel with a=-0.5. It often produces visually smoother imagery than bilinear interpolation, but may overshoot near sharp transitions.
- **Lanczos-3** uses a 6×6 windowed-sinc support. It preserves more high-frequency detail in many imagery workflows, but can ring near strong edges.

Cubic and Lanczos should not be used for nominal categories. Neither method is guaranteed to preserve the source value range.

## NoData policy

All non-finite source values are NoData.

- **strict:** any nonzero-weight missing sample invalidates the output.
- **renormalize:** omit missing samples and renormalize the remaining kernel weights. For negative-lobed cubic and Lanczos kernels this changes the effective filter; if the remaining signed weight is numerically close to zero, the result is NoData rather than an unstable division.

The implementation uses edge extension (replicating the nearest edge cell) when a kernel footprint crosses the array boundary.

## Scope and limitations

- Source and target grids cover the same extent and orientation; only output shape changes.
- Pixel centres are mapped linearly in source-index coordinates.
- There is no CRS transformation, affine georeferencing, rotated-grid support, area-weighted aggregation or antialiasing prefilter for substantial downsampling.
- This is a transparent reference implementation, not a replacement for GDAL/rasterio production warping.

See the [canonical lesson](../../../algorithms/raster/resampling.md) and [intern walkthrough](implementation-walkthrough.md).
