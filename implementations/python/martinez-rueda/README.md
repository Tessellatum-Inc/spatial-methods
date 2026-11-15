# Martinez–Rueda polygon overlay — staged implementation

The implementation provides endpoint event ordering, active x-overlap candidate testing, cross-source segment intersections, segment splitting, midpoint inside/outside classification for intersection/union/difference/XOR, and directed-fragment stitching into closed output rings. It supports one shell plus zero or more disjoint, non-nested holes per input source. Output is a flat collection of oriented rings: shells are counter-clockwise and holes clockwise. Disconnected results and islands inside holes are represented as separate rings.

**Still incomplete:** the active set checks all x-overlapping pairs and is quadratic in the worst case; it is not the full Martinez–Rueda neighbour-ordered sweep-status algorithm. Inputs do not support multiple independent shells per source. Positive-length collinear overlaps and touching/near-coincident boundary configurations are not fully supported. Results are not grouped into explicit Polygon/MultiPolygon objects with shell-to-hole ownership. Numerical predicates use an absolute epsilon, not adaptive exact arithmetic.

Run `python -m pytest -q` in this directory.