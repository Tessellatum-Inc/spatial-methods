This package begins a from-scratch Vatti-family clipping implementation. It
extracts sorted scanbeam levels, separates horizontal edges, creates directed
non-horizontal bound edges with winding deltas, and identifies local minima
(including minima connected by a horizontal bottom plateau).

**Additional active-edge foundation:** for a selected scanbeam band, it
orders all spanning bounds at the exact rational midpoint and computes exact
pairwise crossing events strictly inside that band. The event generator is
intentionally O(m²), making it a transparent correctness baseline rather
than Vatti's optimized neighbour-based intersection scheduler.

It splits each band at pairwise crossing levels and recomputes the edge order
on either side, exposing the expected swaps. A small cumulative winding transition helper is also present. Horizontal
scanbeam events are now extracted for horizontal/bound endpoint or interior
contacts, and horizontal/horizontal point contacts versus positive-length
overlaps are distinguished. These are reference calculations rather than a
production sweep scheduler: crossing discovery remains O(m²), and winding
transitions are not yet derived from a complete arrangement. Fill-rule
predicates (even-odd, non-zero, positive, negative) and Boolean point
classification (intersection, union, difference, XOR) are now implemented as
separate, testable truth-table helpers. They consume winding counts; the new `fill_transitions` helper now propagates
separate subject and clip counts across a caller-supplied left-to-right active
edge sequence and records when the selected Boolean result changes. The new `sweep_boolean` coordinates the whole reference pass: scanbeam-level
records include edge starts/ends, horizontal edges, horizontal contact events
and local minima; each crossing-free band slice is classified; and each
Boolean-filled interval is emitted as an exact-rational trapezoid/triangle
cell.

This is not yet a production Vatti clipper. The reference sweep still uses
O(m²) pairwise crossing discovery and re-sorts each slice; horizontal events
are recorded at scanbeam levels but coincident/overlapping bound bundles do
not yet have full clipping semantics. Filled cells are not yet stitched into
output contours, so holes and connected-component ring assembly remain open.

## Boolean contour assembly

The reference API now includes `clip_rings(decomposition, subject_ring_ids,
clip_ring_ids, operation, fill_rule)`. It runs the cell sweep and assembles
the resulting cells into closed output rings:

- Nodes shared cell edges at every exact-rational cell vertex, including
  unequal subdivisions along the same straight seam.
- Cancels oppositely directed internal edges.
- Walks the remaining directed boundary with an exact polar-angle comparator.
- Removes redundant collinear vertices while preserving rational coordinates.
- Preserves disconnected shells and clockwise hole rings.

The contour stage is tested against overlapping rectangles for all four
Boolean operations, including XOR's two disconnected components. A nested
subject fixture checks a clockwise hole and a separate clip component.

This is still a cell-boundary assembly reference, not the full Vatti
intersection-list algorithm. Coincident input boundaries, horizontal-boundary
state transitions, robust touch-point policies and an optimized neighbour
event queue remain open. The algorithm has not been certified against an
independent geometry kernel yet.


## Degeneracy handling and event scheduling

The sweep now groups coincident active bounds by exact rational slope and
intercept. Each bundle retains all source edges and sums subject and clip
winding deltas independently. This handles identical boundaries, opposite
edge directions, and shared vertical segments without processing duplicate
crossing events.

Crossings are scheduled from adjacent bundles in a rational event heap.
When several edges meet at one point, the entire incident block is reordered
together by slope, then only newly adjacent pairs are scheduled. This replaces
the previous all-pairs crossing scan in the Boolean sweep. The older
`crossings_in_band()` and `sweep_active_edge_slices()` remain available as
transparent reference utilities and regression comparators.

Horizontal-boundary contacts are carried into the cell arrangement as exact
noding points. The filled state on either side of a scanbeam level is still
derived from the non-horizontal bound bundles; horizontal edges define and
node the level boundary rather than incrementing the open-band winding count.
This distinction is important at shared horizontal edges and vertex contacts.

The test matrix now includes coincident rings, opposite direction copies,
full and partial shared boundaries, vertex-only contact, multiway crossing
events, and a Shapely differential oracle for all four Boolean operations.
Shapely is used only as an independent test oracle, not by the implementation.
