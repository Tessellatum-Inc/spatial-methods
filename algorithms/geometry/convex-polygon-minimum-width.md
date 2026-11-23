# Convex-polygon minimum width by rotating calipers

The width of a planar convex set is the minimum distance between two parallel
supporting lines that enclose it. For a polygon, at least one support line in
an optimal pair is collinear with a hull edge. For each directed hull edge,
the opposite support vertex maximises its perpendicular distance from that
edge. The minimum of these maximum distances is the polygon's minimum width.

## Algorithm

1. Construct the strict counter-clockwise convex hull.
2. Keep an index at the vertex farthest from the current hull edge.
3. As the edge advances counter-clockwise, advance the opposite index while
   the signed triangle area increases.
4. Divide the maximum doubled triangle area by the edge length to obtain the
   distance between the parallel support lines.
5. Return the smallest width over all hull edges.

Convexity makes the antipodal support index monotone, so it advances at most
one full circuit. The sweep is O(h), after O(n log n) hull construction.

## Scope and numerical limits

The implementation accepts a finite planar point cloud, deduplicates sites
through the hull routine, and returns zero for fewer than three hull vertices.
It uses floating-point cross products and Euclidean lengths; it is not an
exact-predicate kernel. Coordinates must share a planar Cartesian CRS and
linear unit. The result is a scalar width, not the oriented rectangle's
corners or area.

## Verification

Seeded random point clouds compare the caliper result with an independent
O(h²) oracle that scans every hull edge against every hull vertex. Additional
fixtures cover squares, rectangles, collinear inputs, and invariance under
translation and rotation.

See the [geometry metrics package](../../implementations/python/geometry-metrics/README.md).
