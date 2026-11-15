# Martinez–Rueda polygon clipping — implementation status

Implemented stages:

- X-ordered endpoint events and active x-overlap candidate testing.
- Cross-source segment-intersection discovery and ordered segment splitting.
- Midpoint inside/outside classification for intersection, union, difference and symmetric difference.
- Directed-fragment stitching into closed rings, including disconnected output rings and clockwise hole rings for containment differences.
- Simple-ring validation and explicit rejection of unsupported collinear overlaps.

This is a useful staged Boolean baseline, but not yet a complete Martinez–Rueda engine. The active set checks all x-overlapping pairs (quadratic worst case) rather than maintaining the full neighbour-ordered sweep status and scheduling only adjacent events. Inputs are limited to one simple shell ring per source; input holes, multipolygon inputs, complete touching/coincident handling, adaptive exact predicates and explicit shell/hole polygon grouping remain outstanding. The output is a flat list of oriented rings.

See [implementation and tests](../../implementations/python/martinez-rueda/README.md).