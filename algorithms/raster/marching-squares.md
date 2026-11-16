# Marching squares

Marching squares extracts an isoline from a scalar field sampled on a regular or rectilinear 2D grid. Each cell is classified by whether its four corner values are above or below a contour level. Edges whose endpoint classifications differ contain a crossing, located by linear interpolation.

There are 16 binary corner cases. Most produce zero or one segment. The two diagonal saddle cases produce four edge crossings and require a connectivity decision. This reference implementation uses the bilinear cell-centre value as an asymptotic-style decider: it chooses the pairing consistent with the centre's side of the contour. This is a practical local rule; exact bilinear saddle topology can require evaluating the bilinear interpolant's saddle value rather than its arithmetic corner mean.

## Reference implementation

The [Python implementation](../../implementations/python/marching-squares/README.md) returns independent segments for each contour level. It skips any cell touching a non-finite or masked corner and linearly interpolates edge positions. Stitching segments into ordered polylines, polygonising filled contours, and marching cubes for 3D volumes are separate algorithms and are not claimed as implemented.

## Coordinate and data assumptions

- Rows increase with y and columns increase with x.
- Optional x and y axes must be finite and strictly increasing.
- Values must be a two-dimensional scalar grid.
- A contour exactly equal to all four corners of a flat cell does not emit a duplicate contour segment.
- This implementation does not reproject, resample, or infer a coordinate reference system.
