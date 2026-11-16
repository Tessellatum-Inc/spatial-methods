# Vatti polygon clipping

Vatti's general polygon clipping framework uses scanbeam processing and
boundary-intersection events to perform polygon Boolean operations. It is not
restricted to convex clipping windows or one connected output ring. Fill rules
determine how input contours describe interior regions.

## Repository implementation

The Python package at
[implementations/python/vatti-clipping](../../implementations/python/vatti-clipping/README.md)
adapts Clipper's integer-coordinate Vatti-family engine through Pyclipper. It
exposes intersection, union, difference and XOR and converts the PolyTree
hierarchy into shells, holes and nested island components.

This is **library-backed Vatti-family coverage**, not a from-scratch
implementation. A native implementation would still need local-minima
processing, scanbeam ordering, horizontal-edge handling, intersection events,
winding transitions and contour assembly.

## Precision and fill rules

The wrapper rounds coordinates to a user-selected integer grid. Even-odd,
non-zero, positive and negative fill rules are exposed. Quantization is
explicit and may collapse narrow features or change near-coincident topology.

## References

- Vatti, B. R. (1992), "A generic solution to polygon clipping",
  Communications of the ACM, 35(7), 56–63.
- Clipper2 documentation: https://www.angusj.com/clipper2/Docs/Overview.htm
- Pyclipper: https://github.com/fontanf/pyclipper
