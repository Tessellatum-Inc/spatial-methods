# Implementation walkthrough: DE-9IM and RCC-8

1. Validate that inputs are non-empty and valid.
2. For DE-9IM, delegate the nine intersections to the geometry engine and return its matrix string.
3. For RCC-8, restrict the contract to planar polygonal regions.
4. Check equality and disconnection first, then external connection.
5. Distinguish partial overlap from containment; for containment, test whether the region boundaries intersect to separate tangential from non-tangential proper parts.
6. Keep inverse relations directional: TPP and NTPP reverse to TPPi and NTPPi.
7. Reject unsupported or ambiguous cases rather than silently guessing.

The package wraps Shapely/GEOS predicates; it does not implement the topology engine.


## Cardinal direction extension

The optional `cardinal_direction(a, b)` method compares the axis-aligned minimum bounding rectangles. It returns the direction of B relative to A among N, NE, E, SE, S, SW, W, NW and OVERLAPPING. If interval endpoints touch, they count as separated in that axis, so adjacent objects can have an east/west or north/south relation. This convention is explicit and should not be confused with centroid bearings or a full directional calculus.
