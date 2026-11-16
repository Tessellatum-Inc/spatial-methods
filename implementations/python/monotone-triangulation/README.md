# Y-monotone polygon triangulation

A stack-based triangulator for a single strictly y-monotone simple polygon. It
normalizes orientation, validates simplicity and monotonicity, uses exact
rational orientation predicates, and returns counter-clockwise triangles.

## Scope

- Requires all input vertices to have distinct y-coordinates. Horizontal edges
  and equal-height event ties are rejected explicitly rather than ordered
  heuristically.
- Accepts either input winding and removes a repeated closing vertex and
  consecutive duplicate vertices.
- Rejects self-intersections and non-monotone rings.
- Does not partition an arbitrary simple polygon into monotone pieces, support
  holes, or perform constrained-Delaunay refinement.

The stack method is O(n log n), dominated by sorting vertices; the stack scan
and output are linear. Exact rational arithmetic can increase predicate cost.

## Verification

Tests check triangle count, CCW orientation, exact area conservation, both
windings, non-monotone rejection, tied-y rejection and self-intersection
rejection. Area and count are necessary invariants, not a full proof of
non-overlap; independent triangulation comparisons remain a follow-up.
