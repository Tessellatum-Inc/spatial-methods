# Martinez–Rueda polygon clipping — implementation status

Implemented stages:

- X-ordered endpoint processing with an augmented dynamic y-interval treap status.
- Expected-logarithmic status insertion/removal and expected O(log n + k) y-interval overlap reporting; y-disjoint active segments are pruned before exact intersection tests. A min-heap handles x-window expiry without scanning the active set at each event. Split parameters remain exact `Fraction` values through sorting and deduplication.
- Cross-source segment intersection discovery and ordered segment splitting; pairwise segment determinants and intersection parameters use exact rational arithmetic over decimal input representations, avoiding the previous scale-dependent determinant-versus-epsilon comparison. Split-parameter ordering and deduplication are exact rather than epsilon-based, preserving distinct nearby crossings; fragment midpoints are evaluated as rational coordinates.
- Midpoint inside/outside classification for intersection, union, difference and symmetric difference.
- Directed-fragment stitching into closed rings, including disconnected outputs, islands and clockwise hole rings.
- Input support for one shell plus disjoint, non-nested holes per source; ring orientation is normalized to shell-CCW / hole-CW.
- Simple-ring and ring-collection validation.
- Polygon-like output assembly: CCW shells are grouped with directly contained CW holes; islands inside holes remain separate components.

This is not yet the full Martinez–Rueda sweep: the status is an interval broad phase rather than the neighbour-ordered structure with dynamically scheduled intersection events, so dense/overlapping inputs can still be quadratic. Multiple independent shells per input, full touching/coincident handling and exact fragment stitching remain outstanding. Signed area/orientation and zero-area rejection now use exact rational shoelace arithmetic. Ring simplicity uses exact decimal-coordinate orientation/intersection predicates; point-in-ring uses exact even-odd ray crossing with boundary points treated as outside. Shell/hole grouping is limited to the supported non-touching ring configurations and is not a general validity/repair operation.

See [implementation and tests](../../implementations/python/martinez-rueda/README.md).
