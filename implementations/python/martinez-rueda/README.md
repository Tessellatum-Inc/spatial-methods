# Martinez–Rueda polygon overlay — staged implementation

The implementation provides x-ordered endpoint processing with an augmented dynamic y-interval treap status, cross-source segment candidate filtering, segment intersections and splitting, midpoint inside/outside classification for intersection/union/difference/XOR, and directed-fragment stitching into closed output rings. The interval treap supports expected-logarithmic insertion/removal and expected O(log n + k) interval-overlap reporting. It prunes y-disjoint active segments before exact intersection tests.

Input supports one shell plus zero or more disjoint, non-nested holes per source. Output is a flat collection of oriented rings: shells are counter-clockwise and holes clockwise. Disconnected results and islands inside holes are represented as separate rings.

**Important distinction:** this is an augmented interval broad phase, not the full Martinez–Rueda neighbour-ordered status with dynamically scheduled intersection events. Dense or heavily overlapping data can still require quadratic candidate checks. Inputs do not support multiple independent shells per source. Positive-length collinear overlaps and touching/near-coincident boundary configurations are not fully supported. Results are not grouped into explicit Polygon/MultiPolygon objects with shell-to-hole ownership. Numerical predicates use an absolute epsilon, not adaptive exact arithmetic.

Run `python -m pytest -q` in this directory.