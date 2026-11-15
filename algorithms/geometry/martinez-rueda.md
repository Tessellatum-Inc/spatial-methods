# Martinez–Rueda polygon clipping — implementation status

Implemented stages:

- X-ordered endpoint events, active x-overlap candidate testing, cross-source intersections and segment splitting.
- Midpoint inside/outside classification for intersection, union, difference and symmetric difference.
- Directed-fragment stitching into closed rings, including disconnected outputs, islands and clockwise hole rings.
- Input support for one shell plus disjoint, non-nested holes per source; ring orientation is normalized to shell-CCW / hole-CW.
- Simple-ring and ring-collection validation.

This is a staged Boolean baseline, not yet a complete Martinez–Rueda engine. The active set checks all x-overlapping pairs (quadratic worst case) rather than maintaining the full neighbour-ordered sweep status and scheduling only adjacent events. Multiple independent shells per input, full touching/coincident handling, adaptive exact predicates and explicit Polygon/MultiPolygon shell-hole grouping remain outstanding. The output is a flat list of oriented rings.

See [implementation and tests](../../implementations/python/martinez-rueda/README.md).