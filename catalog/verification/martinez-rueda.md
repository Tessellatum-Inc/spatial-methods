# Martinez–Rueda verification record

Implemented: endpoint event ordering; active x-overlap candidate tracking; proper cross-source segment intersections; split-parameter collection; ordered edge fragments; midpoint inside/outside classification for intersection, union, difference and symmetric difference; reversed clip fragments for A-minus-B.

Tests authored for overlapping/disjoint rectangles, concave crossings, shared endpoints, collinear-overlap rejection, invalid inputs, 150 seeded rectangle cases, analytic rectangle Boolean areas and containment orientation. Tests have not been executed here.

Outstanding: neighbour-ordered sweep status and event scheduling, self-intersection validation, robust predicates, holes/multipart classification, operation output-ring stitching and degenerate/coincident geometry.