# Implementation verification — Greiner–Hormann polygon intersection

## Algorithm identity

Greiner, G. and Hormann, K. (1998), “Efficient clipping of arbitrary polygons,” *ACM Transactions on Graphics*, 17(2), 71–83. The implementation follows the linked-list intersection-node strategy: paired boundary events are ordered along each edge, classified as entry/exit, and traversed by switching between polygon boundaries.

## Implemented scope

The independent Python implementation accepts one simple, hole-free ring per input. Concave rings are supported. It returns all area components of the intersection, including disconnected components. Ring orientation is normalized to counter-clockwise. Disjoint and containment cases are handled without crossing events.

The current implementation compares every pair of edges during event discovery (O(nm)); it is an instructional baseline, not the asymptotically optimized algorithm.

## Verification

Tests cover overlapping rectangles, concave U-shaped polygons producing two disconnected components, containment, disjointness, clockwise input normalization, self-crossing input rejection, and explicit rejection of vertex-touch events. Seeded verification includes 1,000 axis-aligned rectangle cases against an interval-arithmetic oracle, 250 rotated-rectangle cases against Shapely/GEOS, and 300 randomized concave U-shape cases against a closed-form disconnected-area oracle.

## Limitations

Only proper transverse crossings are supported. Vertex touches and collinear/coincident boundary events raise NotImplementedError. Holes, self-intersecting input, line-only or point-only output, precision-grid topology, and arbitrary polygon Boolean operations are not implemented. A separate GEOS-backed package in this repository provides broader union, difference, symmetric difference and mixed-dimensional touch-result behavior for valid polygonal inputs.

## Reproduction

From the package directory: `python -m pip install -r requirements.txt && python -m pytest -q`. The algorithm itself uses only the Python standard library; Shapely is used as an independent test oracle.

## Rights

The implementation is independently written from the published algorithm description. No source code or figures are reproduced.
