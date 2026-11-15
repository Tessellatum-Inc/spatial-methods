# Constrained Delaunay triangulation of a polygon

A constrained Delaunay triangulation (CDT) preserves specified segments even when they would not appear in an unconstrained Delaunay triangulation. For a simple polygon with no holes, the boundary itself is the constraint set.

## Lawson edge-flip baseline

1. Build any valid triangulation; this implementation reuses exact-predicate ear clipping.
2. Build an edge-to-triangle incidence map.
3. For each interior edge shared by two triangles, test whether the opposite vertex lies inside the other triangle's circumcircle.
4. If the quadrilateral is convex and the exact incircle predicate is positive, flip the diagonal.
5. Repeat until no unconstrained interior edge is locally illegal.

Cocircular edges are left unchanged, so the result is weakly Delaunay. Tests verify (n-2) CCW triangles, exact area conservation, boundary preservation and local incircle legality on convex, concave, clockwise and seeded radial rings.

## Limits

This is a polygon-boundary CDT baseline, not a general constrained mesh engine: no holes, internal constraint segments, Steiner points, constrained-segment recovery, refinement or mesh-quality guarantees. Edge incidence is rebuilt after each flip, so this is not intended for large meshes.

See the [Python implementation](../../implementations/python/constrained-delaunay/README.md) and [verification record](../../catalog/verification/constrained-delaunay.md).
