# Implementation walkthrough: Bowyer–Watson

## 1. Start with an enclosing face

The algorithm begins with a counter-clockwise super-triangle containing the input bounding box. This temporary face ensures that the insertion cavity is closed even when a new site lies on the convex hull.

## 2. Find the cavity

For each input site, inspect the current triangles and evaluate the oriented in-circle determinant. For a counter-clockwise triangle, a positive value means the inserted point is strictly inside its circumcircle. Those triangles form the cavity and are removed.

A zero determinant is treated as a cocircular tie and does not remove that triangle. The rule is intentionally conservative and deterministic for a fixed insertion order; it does not make the Delaunay triangulation unique.

## 3. Extract the cavity boundary

Count each undirected edge of the removed triangles. Edges appearing twice are internal to the cavity; edges appearing once form its boundary. Connect each boundary edge to the inserted site, discarding zero-area triangles and orienting every new face counter-clockwise.

## 4. Remove temporary geometry

After all sites have been inserted, discard every triangle that still references a super-triangle vertex. The remaining faces are the finite triangulation.

## Complexity and limitations

This transparent implementation scans all current triangles for every insertion and rebuilds cavity edge counts. It is therefore not the optimized O(n log n) implementation often associated with spatially indexed incremental triangulation; worst-case work can be quadratic or worse depending on cavity sizes and list rebuilding. A production implementation needs efficient point location, adjacency structures, robust handling of degeneracies, and a carefully bounded super-triangle strategy.

The package uses exact rational predicates over decimal-string coordinates, which avoids floating-point sign errors for the represented inputs. It is a planar Euclidean teaching baseline, not a constrained triangulator, mesh-refinement engine, or geodesic method.
