# DCEL polygon subdivision core

A small doubly connected edge list (DCEL) builder for polygonal face boundaries. It validates non-zero signed area and rejects non-adjacent edge intersections using exact rational predicates over the normalized decimal coordinates.
It creates explicit vertices, paired directed half-edges, face boundary cycles,
and exterior twin cycles. At each vertex, outgoing edges are angularly ordered
and exterior links are derived from the planar rotation system.

This is a topology representation, **not** a general arrangement builder:
inputs must already be noded and valid. It does not split crossings, resolve
overlaps, infer shell/hole semantics, or merge disconnected exterior boundary
components into a single global unbounded-face object. Coordinates are exact
keys after finite-float conversion; robust geometric predicates are not claimed.

Run `python -m pytest -q` in this directory.
