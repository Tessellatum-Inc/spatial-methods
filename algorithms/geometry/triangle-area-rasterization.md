# Fractional-area rasterization of a triangle

For a grid cell C and a triangle T, the fractional coverage is

\[
f_C=\frac{\operatorname{area}(C\cap T)}{\operatorname{area}(C)},\qquad 0\leq f_C\leq1.
\]

The implementation enumerates cells intersecting the triangle's bounding box, clips the convex triangle against each cell's four axis-aligned half-planes, and computes the clipped polygon area with the shoelace formula. It supports non-square cells, arbitrary finite grid origin, partial overlap with the raster extent and either triangle orientation.

This is an exact-area geometric definition evaluated with floating-point arithmetic; it is not exact rational arithmetic. The implementation is deliberately limited to one convex triangle. It does not implement arbitrary concave polygon components, holes, multipolygons, rotated/sheared affine grids, or a general overlay engine.

Implementation: [Python rasterization package](../../implementations/python/rasterization/README.md).
