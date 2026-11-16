# Verification — Vatti-family polygon clipping adapter

## Implemented

- Adapter to Clipper's integer-coordinate Vatti-family engine.
- Intersection, union, difference and symmetric difference.
- Explicit integer precision scale and finite/range validation.
- Even-odd, non-zero, positive and negative fill-rule selection.
- PolyTree extraction into shells, holes and nested island components.
- Multiple rings and disconnected output components.

## Tests authored

- Analytic rectangle areas for all four Boolean operations.
- Disconnected intersection components.
- Difference producing a hole.
- Nested island extraction.
- Even-odd resolution of a self-crossing bow-tie.
- Invalid operation, fill-rule, scale and precision-grid collapse.

## Verification boundary

Tests use analytic area expectations and direct shoelace area calculation.
They verify adapter semantics, not Clipper's internal Vatti implementation.
No from-scratch Vatti scanbeam implementation is claimed. CI execution must be
checked before this package is marked verified.
