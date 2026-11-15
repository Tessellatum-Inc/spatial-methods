# Verification — DCEL polygon subdivision core

## Implemented

- Vertex deduplication by finite coordinate pair.
- Directed half-edge creation and reciprocal twin pairing.
- Shared boundary pairing for adjacent faces represented with opposite edge direction.
- Input face boundary cycles with next/previous links.
- Angular outgoing-edge order and exterior twin-cycle linkage.
- Explicit invariant checker for twin, next and previous reciprocity.

## Tests authored

Single polygon with exterior twin cycle; two adjacent faces sharing a boundary;
two disconnected components; malformed/open rings; duplicate same-direction
boundaries; and non-finite coordinates.

## Scope boundary

This is not yet a complete planar arrangement or Boolean overlay. It assumes
noded input boundaries and does not split crossings, resolve collinear overlaps,
infer shell/hole containment, or unify disconnected components of the unbounded
face. Tests must be run in CI before this implementation is marked verified.
