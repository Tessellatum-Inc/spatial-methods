# Verification — native Vatti scanbeam foundation

## Implemented
- Scanbeam extraction from all ring vertices.
- Lower-to-upper non-horizontal edge records with original traversal winding.
- Horizontal edge records.
- Local-minimum extraction across single vertices and horizontal plateaus.
- Exact rational dx/dy ordering of local-minimum bounds.
- Active-edge ordering at a scanbeam-band midpoint.
- Exact pairwise crossing events strictly within a band.
- Crossing-level band subdivision and edge-order swaps on either side.
- Cumulative signed winding transition helper.
- Horizontal/bound endpoint and interior intersection events.
- Horizontal/horizontal point-contact and overlap classification.
- Four fill-rule winding predicates and four Boolean-operation truth tables.
- Subject/clip winding propagation over an explicitly ordered active-edge list.
- Boolean-result entry/exit transitions for intersection, union, difference and XOR.

## Tests authored
- Rectangle scanbeam and minimum fixture.
- Clockwise/counter-clockwise equivalence.
- Non-horizontal minimum and horizontal bottom plateau.
- Multiple local minima.
- Active-edge order and exact bow-tie crossing event.
- Invalid band, non-finite and repeated-vertex inputs.

## Not implemented
- Efficient neighbour-only intersection scheduling and in-place active-edge updates.
- Efficient neighbour-only intersection scheduling.
- Full horizontal-edge clipping transitions and their integration into active-edge updates.
- Deriving the correct active-edge order from a complete sweep, including coincident-edge rules and horizontal-event integration.
- Output contour construction and Boolean operations.

Tests have been authored but must run in CI before this component is marked
verified.