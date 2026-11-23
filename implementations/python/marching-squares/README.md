# Marching-squares contour extraction

A NumPy reference implementation of the marching-squares algorithm for extracting isoline segments from a rectilinear 2D grid.

- Linear interpolation locates crossings on cell edges.
- Saddle cells use the bilinear cell-centre value to choose connectivity.
- Cells touching NaN or an invalid-mask vertex are skipped.
- Coordinates may be supplied as strictly increasing one-dimensional x/y axes.
- Output is a mapping from contour level to independent line segments; segment stitching into polylines is a separate operation.

Install NumPy and pytest, then run pytest -q in this directory. See the [algorithm note](../../../algorithms/raster/marching-squares.md).
