# Verification — native Vatti scanbeam foundation

## Implemented
- Scanbeam extraction from all ring vertices.
- Lower-to-upper non-horizontal edge records with original traversal winding.
- Horizontal edge records.
- Local-minimum extraction across single vertices and horizontal plateaus.
- Exact rational dx/dy ordering of local-minimum bounds.
- Active-edge ordering at a scanbeam-band midpoint.
- Exact pairwise crossing events strictly within a band.

## Tests authored
- Rectangle scanbeam and minimum fixture.
- Clockwise/counter-clockwise equivalence.
- Non-horizontal minimum and horizontal bottom plateau.
- Multiple local minima.
- Active-edge order and exact bow-tie crossing event.
- Invalid band, non-finite and repeated-vertex inputs.

## Not implemented
- Incremental active-edge insertion, removal and reordering at events.
- Efficient neighbour-only intersection scheduling.
- Horizontal-edge clipping transitions.
- Winding/fill-state propagation.
- Output contour construction and Boolean operations.

Tests have been authored but must run in CI before this component is marked
verified.