# Constrained Delaunay triangulation of a polygon

A constrained Delaunay triangulation (CDT) preserves specified segments even when they would not appear in an unconstrained Delaunay triangulation. For a simple polygon with no holes, the boundary itself is the constraint set.

## Lawson edge-flip baseline

1. Build any valid triangulation; this implementation reuses exact-predicate ear clipping.
2. Build an edge-to-triangle incidence map.
3. For each interior edge shared by two triangles, test whether the opposite vertex lies inside the other triangle's circumcircle.
4. If the quadrilateral is convex and the exact incircle predicate is positive, flip the diagonal.
5. Repeat until no unconstrained interior edge is locally illegal.

Cocircular edges are left unchanged, so the result is weakly Delaunay. The additional `constrained_delaunay_with_diagonals` entry point accepts non-crossing segments between existing normalized polygon vertices. It splits the polygon along those diagonals and triangulates each resulting piece, keeping every supplied diagonal as a piece boundary. Tests verify constraint-edge incidence, exact area conservation, invalid crossing/exterior constraints, and shared-endpoint constraint sets.

## Limits

This remains a polygonal CDT baseline, not a general constrained mesh engine: no holes, arbitrary segment recovery, Steiner points, refinement or mesh-quality guarantees. Interior constraints are restricted to non-crossing diagonals between existing polygon vertices and are enforced by polygon partitioning rather than general edge recovery. Edge incidence is rebuilt after each flip, so this is not intended for large meshes.

See the [Python implementation](../../implementations/python/constrained-delaunay/README.md) and [verification record](../../catalog/verification/constrained-delaunay.md).
