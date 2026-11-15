# Martinez–Rueda polygon clipping — implementation status

Implemented stages:

- X-ordered endpoint processing with an augmented dynamic y-interval treap status.
- Expected-logarithmic status insertion/removal and expected O(log n + k) y-interval overlap reporting; y-disjoint active segments are pruned before exact intersection tests.
- Cross-source segment intersection discovery and ordered segment splitting.
- Midpoint inside/outside classification for intersection, union, difference and symmetric difference.
- Directed-fragment stitching into closed rings, including disconnected outputs, islands and clockwise hole rings.
- Input support for one shell plus disjoint, non-nested holes per source; ring orientation is normalized to shell-CCW / hole-CW.
- Simple-ring and ring-collection validation.

This is not yet the full Martinez–Rueda sweep: the status is an interval broad phase rather than the neighbour-ordered structure with dynamically scheduled intersection events, so dense/overlapping inputs can still be quadratic. Multiple independent shells per input, full touching/coincident handling, adaptive exact predicates and explicit Polygon/MultiPolygon shell-hole grouping remain outstanding. Output is a flat list of oriented rings.

See [implementation and tests](../../implementations/python/martinez-rueda/README.md).