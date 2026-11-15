# Martinez–Rueda polygon overlay — staged implementation

The implementation now has two concrete stages: (1) x-ordered endpoint events, active x-overlap candidate testing, proper cross-source segment intersections and ordered segment splitting; (2) midpoint-based inside/outside classification of split fragments for intersection, union, difference and symmetric difference. Difference reverses selected clip-boundary fragments to maintain shell/hole orientation. Shared endpoints are allowed; positive-length collinear overlap is rejected.

**Still incomplete:** the active set checks all x-overlapping pairs (quadratic worst case), rather than maintaining Martinez–Rueda's neighbour-ordered sweep status and scheduling only neighbour events. Selected fragments are not stitched into closed output rings. Classification currently accepts exactly one simple shell ring per input; holes, multipolygons, invalid/self-intersecting rings, robust predicates and near-coincident cases are not supported. `fragment_area_contribution` is only a valid area check when the selected fragments form closed boundaries.

Run `python -m pytest -q` in this directory.