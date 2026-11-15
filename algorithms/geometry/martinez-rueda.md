# Martinez–Rueda polygon clipping — implementation status

Implemented stages:

- X-ordered endpoint processing with a dynamic y-interval sweep status that prunes y-disjoint candidate pairs.
- Cross-source segment intersection discovery and ordered segment splitting.
- Midpoint inside/outside classification for intersection, union, difference and symmetric difference.
- Directed-fragment stitching into closed rings, including disconnected outputs, islands and clockwise hole rings.
- Input support for one shell plus disjoint, non-nested holes per source; ring orientation is normalized to shell-CCW / hole-CW.
- Simple-ring and ring-collection validation.

The sweep status is a bounding-box interval broad phase, not the full Martinez–Rueda neighbour-ordered sweep with dynamically scheduled intersection events; dense/overlapping inputs can still require quadratic candidate checks. Multiple independent shells per input, full touching/coincident handling, adaptive exact predicates and explicit Polygon/MultiPolygon shell-hole grouping remain outstanding. Output is a flat list of oriented rings.

See [implementation and tests](../../implementations/python/martinez-rueda/README.md).