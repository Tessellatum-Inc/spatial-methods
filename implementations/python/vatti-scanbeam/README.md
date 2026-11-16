This package begins a from-scratch Vatti-family clipping implementation. It
extracts sorted scanbeam levels, separates horizontal edges, creates directed
non-horizontal bound edges with winding deltas, and identifies local minima
(including minima connected by a horizontal bottom plateau).

**Additional active-edge foundation:** for a selected scanbeam band, it
orders all spanning bounds at the exact rational midpoint and computes exact
pairwise crossing events strictly inside that band. The event generator is
intentionally O(m²), making it a transparent correctness baseline rather
than Vatti's optimized neighbour-based intersection scheduler.

It can now split a band at pairwise crossing levels and recompute the edge
order on either side, exposing the expected swaps. A small cumulative winding transition helper is also present. Horizontal
scanbeam events are now extracted for horizontal/bound endpoint or interior
contacts, and horizontal/horizontal point contacts versus positive-length
overlaps are distinguished. These are reference calculations rather than a
production sweep scheduler: crossing discovery remains O(m²), and winding
transitions are not yet derived from a complete arrangement. Fill-rule
predicates (even-odd, non-zero, positive, negative) and Boolean point
classification (intersection, union, difference, XOR) are now implemented as
separate, testable truth-table helpers. They consume winding counts; the new `fill_transitions` helper now propagates
separate subject and clip counts across a caller-supplied left-to-right active
edge sequence and records when the selected Boolean result changes. It still
does not schedule/reorder edges itself or assemble output contours.

It does **not** yet update an active-edge list incrementally in-place, process
horizontal edges through clipping, or emit output contours. It is therefore a tested algorithmic foundation, not a
polygon clipper and not a complete Vatti implementation.