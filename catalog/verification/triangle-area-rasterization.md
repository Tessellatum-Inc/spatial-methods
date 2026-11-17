# Source verification — triangle fractional-area rasterization

## Identity and technical definition
The coverage fraction is the intersection area of a triangle and a grid cell divided by the cell area. Convex clipping against four axis-aligned half-planes followed by the shoelace formula computes the clipped area.

## Implementation and tests
The Python baseline accepts one non-degenerate triangle, grid dimensions, lower-left origin and positive x/y cell dimensions. Tests cover an analytic right-triangle cell split, orientation invariance, area conservation, non-square cells, partial raster overlap and invalid geometry/grid controls.

## Limits and rights
Floating-point area calculations; triangle only. Arbitrary concave polygon components, holes, multipolygons and rotated/sheared grids remain open. Original code and explanatory text.
