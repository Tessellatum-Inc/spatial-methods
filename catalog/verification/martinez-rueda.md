# Martinez–Rueda verification record

Implemented: endpoint event ordering; active x-overlap candidate tracking; proper cross-source intersections; split-parameter collection; ordered fragments; midpoint inside/outside classification for intersection, union, difference and XOR; directed-fragment stitching into closed rings; disconnected ring outputs; clockwise hole rings for containment differences; simple-ring validation.

Tests authored for overlapping/disjoint rectangles, concave crossings and disconnected intersection, shared endpoints, collinear-overlap rejection, invalid/self-crossing rings, 150 seeded rectangle cases, analytic rectangle Boolean areas/components, containment with hole orientation, disjoint union and clockwise inputs. Tests have not been executed here.

Outstanding: neighbour-ordered sweep status/event scheduling, input holes and multipolygons, explicit shell/hole grouping, complete touching/coincident handling, adaptive exact predicates and broader independent differential testing.