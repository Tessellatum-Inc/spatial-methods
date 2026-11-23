# Implementation verification — convex-polygon minimum width

## Implemented scope

The geometry-metrics package now exposes `convex_polygon_minimum_width`.
It constructs a strict convex hull, then uses a monotone antipodal support
pointer to compute the minimum parallel-support distance in O(h) time.

## Verification

Tests cover known square and rectangle widths, empty and collinear inputs,
translation/rotation invariance, and seeded clouds from 3 through 150 points.
The randomized test compares against an independent edge-by-edge, vertex-by-
vertex O(h²) width oracle.

## Complexity and limitations

Total complexity is O(n log n) for hull construction plus O(h) for the
rotating-calipers sweep, with O(h) hull storage. Floating-point predicates
are used; near-degenerate inputs may require a robust geometry kernel.
