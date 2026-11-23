# Vatti-family polygon Boolean operations

This package exposes intersection, union, difference and symmetric difference
for polygon ring collections, including disconnected components, holes and
nested islands. It uses Clipper through the Pyclipper binding.

**Implementation classification:** this is a runnable adapter to Clipper's
integer-coordinate Vatti-family engine. It is not a from-scratch transcription
of Vatti's scanbeam algorithm. The engine performs clipping; this package
defines the Python input contract, precision conversion, fill-rule selection
and shell/hole component extraction.

## Precision model

Input coordinates are rounded to an integer grid using scale (default
1,000,000). One integer unit represents 1/scale coordinate units. Narrow
features may collapse; the adapter rejects rings that lose area or fewer than
three distinct vertices. Choose a scale appropriate to the coordinate system
and extent. This is a precision model, not a CRS transformation.

## Example

    from vatti_clipping import boolean_clip
    parcel = [(0, 0), (8, 0), (8, 6), (0, 6)]
    project = [(5, -1), (10, -1), (10, 4), (5, 4)]
    pieces = boolean_clip([parcel], [project], "intersection", scale=1000)

Self-crossing input contours are first simplified into simple contours using\nthe selected fill rule. Supported fill rules: even_odd, non_zero, positive and negative. Nested islands
inside holes are emitted as separate polygon components.

## Limits

- Integer quantization can alter topology at the chosen scale.
- Z/M values, feature attributes and CRS metadata are not retained.
- Geodesic overlay is not implemented; use a suitable planar CRS.
- Robustness and fill-rule semantics are inherited from Clipper.
- This package is not independent evidence for a from-scratch Vatti engine.

Run pytest in this directory.
