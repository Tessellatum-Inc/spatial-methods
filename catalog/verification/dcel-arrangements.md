# Verification — DCEL polygon subdivision core

## Implemented

- Vertex deduplication by finite coordinate pair.
- Directed half-edge creation and reciprocal twin pairing.
- Shared boundary pairing for adjacent faces represented with opposite edge direction.
- Input face boundary cycles with next/previous links.\n- Exact-rational orientation and segment predicates for rejecting zero-area and self-intersecting input rings.
- Pairwise input-edge validation rejects un-noded crossings, T-junctions and partial collinear overlaps.
- Cross-ring noding guard rejects proper crossings, T-junctions and partial collinear overlaps; already-shared complete edges are deduplicated.
- Exact rational counter-clockwise angular ordering of outgoing-edge fans (using decimal rationalization of stored coordinates).
- Exterior-cycle successor selection skips bounded-face half-edges and remains on exterior edges at shared multi-face junctions.
- Three-adjacent-face chain regression checks complete exterior-cycle closure and edge membership.
- Explicit invariant checker for twin, next and previous reciprocity.

## Tests authored

Single polygon with exterior twin cycle; two adjacent faces sharing a boundary, including collinear outer boundary edges that meet at one shared noded endpoint;
two disconnected components; malformed/open rings; duplicate same-direction
boundaries; non-finite coordinates, un-noded crossings, T-junctions and partial collinear overlaps.

## Scope boundary

This is not yet a complete planar arrangement or Boolean overlay. It assumes
noded input boundaries and does not split crossings, resolve collinear overlaps,
infer shell/hole containment, or unify disconnected components of the unbounded
face. Tests must be run in CI before this implementation is marked verified. The exact angular comparator and exterior-only successor correction are authored but not yet CI-verified.


## Latest correction awaiting CI

The collinear-overlap guard now distinguishes a genuine positive-length overlap or endpoint-on-interior T-junction from two collinear edges that merely share one endpoint. The latter is valid noded topology. A regression test covers adjacent rectangular faces whose bottom boundary edges are collinear and meet at their common vertex. This correction is authored but not yet CI-verified.
