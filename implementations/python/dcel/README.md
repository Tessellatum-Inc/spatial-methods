# DCEL polygon subdivision core

A small doubly connected edge list (DCEL) builder for polygonal face boundaries. It validates non-zero signed area and rejects non-adjacent edge intersections using exact rational predicates over the normalized decimal coordinates.
It creates explicit vertices, paired directed half-edges, face boundary cycles,
and exterior twin cycles. At each vertex, outgoing edges are ordered counter-clockwise with an exact rational angular comparator. Exterior links scan clockwise from the incoming twin to the next exterior half-edge, skipping bounded-face edges at shared junctions.

This is a topology representation, **not** a general arrangement builder:
inputs must already be noded and valid. It does not split crossings, resolve
overlaps, infer shell/hole semantics, or merge disconnected exterior boundary
components into a single global unbounded-face object. Coordinates are stored as finite floats for the public vertex records; validation and angular ordering convert their decimal representations to exact rational values. This avoids trigonometric ordering ambiguity but does not recover precision already lost during float conversion.

Run `python -m pytest -q` in this directory.
