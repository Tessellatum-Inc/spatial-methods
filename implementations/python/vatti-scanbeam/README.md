# Native Vatti scanbeam decomposition — foundation

This package begins a from-scratch Vatti-family clipping implementation. It
extracts sorted scanbeam levels, separates horizontal edges, creates directed
non-horizontal bound edges with winding deltas, and identifies local minima
(including minima connected by a horizontal bottom plateau).

It does **not** yet perform active-edge processing, calculate edge
intersections, update winding counts, emit output contours or execute Boolean
operations. It is therefore a tested algorithmic foundation, not a polygon
clipper and not a complete Vatti implementation.

## Coordinate and edge conventions

Coordinates are Cartesian with y increasing upward. A scanbeam is a distinct
vertex y-coordinate. Non-horizontal edges are stored lower-to-upper; their
winding delta records whether the original ring traversed them upward (+1) or
downward (-1). Horizontal edges are retained separately because they require
special processing at scanbeam boundaries.

For each local minimum, the two incident rising bounds are ordered by their
exact rational dx/dy slopes. Decimal input coordinates are interpreted through
their shortest round-trip string representation for this comparison. Ring
orientation is not restricted.

## Run

    python -m pytest -q

The next implementation stage is the active-edge list and scanbeam transition
logic, including horizontal-edge handling and intersection event ordering.
