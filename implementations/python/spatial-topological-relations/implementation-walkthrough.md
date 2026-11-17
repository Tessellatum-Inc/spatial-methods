# Implementation walkthrough: DE-9IM and RCC-8

1. Validate that inputs are non-empty and valid.
2. For DE-9IM, delegate the nine intersections to the geometry engine and return its matrix string.
3. For RCC-8, restrict the contract to planar polygonal regions.
4. Check equality and disconnection first, then external connection.
5. Distinguish partial overlap from containment; for containment, test whether the region boundaries intersect to separate tangential from non-tangential proper parts.
6. Keep inverse relations directional: TPP and NTPP reverse to TPPi and NTPPi.
7. Reject unsupported or ambiguous cases rather than silently guessing.

The package wraps Shapely/GEOS predicates; it does not implement the topology engine.
