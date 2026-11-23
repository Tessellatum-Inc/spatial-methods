# Nicholl–Lee–Nicholl line clipping

Nicholl–Lee–Nicholl (NLN) clips a finite 2D line segment against an axis-aligned rectangular window. Unlike iterative endpoint replacement, it uses the first endpoint's region and slope relative to rays through window corners to select the relevant boundary or boundary pair directly.

## Implemented case structure

The teaching implementation maps the first endpoint by rotations/reflections into canonical inside, left or top-left regions. It then classifies the segment slope against the rectangle-corner rays, calculates the selected boundary intersections, orders intersections along the segment and restores the original coordinate orientation. Vertical and horizontal segments, including edge-coincident segments, have explicit interval handling. A boundary start directed immediately outside is retained as a zero-length touch under the closed-window policy.

## Validation

The implementation is compared with Liang–Barsky on hand-selected cases and 2,000 seeded random segments over a non-square rectangle. Additional tests cover horizontal/vertical segments, boundary-outward starts, degenerate windows and zero-length segments.

## Limits

This is a floating-point rectangular-window implementation. It is not a polygon clipper, does not support arbitrary convex windows and is not an exact-predicate kernel. The differential oracle establishes output agreement on the tested domain, not an asymptotic operation-count guarantee.

## Sources

- Nicholl, T. M., Lee, D. T., & Nicholl, R. A. (1987). An efficient new algorithm for 2-D line clipping: Its development and analysis. *Computer Graphics*, 21(4), SIGGRAPH '87, 253–262. https://doi.org/10.1145/37401.37432.

Implementation: [line clipping package](../../implementations/python/line-clipping/README.md).
