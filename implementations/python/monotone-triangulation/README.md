# Y-monotone polygon triangulation

A two-stage triangulation toolkit: a general simple-polygon partition sweep
followed by a stack-based triangulator for each strictly y-monotone piece. It
normalizes orientation, validates simplicity, uses exact rational predicates,
and returns counter-clockwise triangles.

## Scope

- Requires all input vertices to have distinct y-coordinates. Horizontal edges
  and equal-height event ties are rejected explicitly rather than ordered
  heuristically.
- Accepts either input winding and removes a repeated closing vertex and
  consecutive duplicate vertices.
- Rejects self-intersections and non-monotone rings.
- `partition_y_monotone` implements start/end/split/merge/regular event handling
  and returns a set of strictly y-monotone rings for a simple input polygon.
- `triangulate_general` partitions first, then applies the stack triangulator.
- The sweep status is intentionally a Python list in this reference version,
  so partitioning is O(n^2) worst case; it is not the O(n log n) balanced-tree
  implementation described in computational-geometry textbooks.
- Horizontal edges, equal-height events, consecutive collinear triples, holes and self-intersecting inputs are
  not supported. Constrained-Delaunay refinement is also out of scope.

The stack method is O(n log n), dominated by sorting vertices; its stack scan
is linear. Exact rational arithmetic can increase predicate cost.

## Verification

Tests check triangle count, CCW orientation, exact area conservation, both
windings, non-monotone rejection, tied-y rejection, self-intersection rejection
and a concave U-shaped polygon requiring multiple monotone pieces. Independent
triangulation comparisons and edge-incidence/overlap checks remain follow-ups.


**Implementation note:** The triangulator validates strict y-monotonicity, then uses exact rational ear clipping as the robust reference path. This is O(n²), not the O(n log n) stack bound. The general-polygon path first partitions with the start/end/split/merge/regular sweep; that sweep currently uses a list status and is also O(n²). Horizontal event ties and holes remain unsupported.
