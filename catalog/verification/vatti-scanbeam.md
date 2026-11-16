# Verification — native Vatti scanbeam foundation

## Implemented
- Scanbeam extraction from all ring vertices.
- Lower-to-upper non-horizontal edge records with original traversal winding.
- Horizontal edge records.
- Local-minimum extraction across single vertices and horizontal plateaus.
- Exact rational dx/dy ordering of local-minimum bounds.

## Tests authored
- Rectangle scanbeam and minimum fixture.
- Clockwise/counter-clockwise equivalence.
- Non-horizontal minimum.
- Horizontal bottom plateau.
- Multiple local minima.
- Invalid, non-finite and repeated-vertex inputs.

## Not implemented
- Active-edge list maintenance and scanbeam transitions.
- Edge-edge intersection calculation and event ordering.
- Winding/fill-state propagation.
- Output contour construction and Boolean operations.

Tests have been authored but must run in CI before this component is marked verified.
