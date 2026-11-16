# Doubly connected edge lists and planar arrangements

A DCEL stores a planar subdivision using vertices, directed half-edges and
faces. Every half-edge has an origin, twin, next, previous and incident face.
The twin pair represents one undirected edge with opposite directions. The
next/previous links encode boundary cycles; vertices maintain outgoing-edge
incidence.

The implementation in this repository builds this structure from already
noded polygon face rings. It pairs shared boundaries when adjacent faces encode
the same geometric edge in opposite directions. At vertices, outgoing edges are sorted counter-clockwise with an exact rational angular comparator rather than `atan2`. For an incoming exterior half-edge, traversal scans clockwise from its twin and selects the next exterior half-edge, skipping bounded-face edges at multi-face junctions.

This is deliberately a representation layer rather than a complete Boolean
arrangement engine. It does not node intersections, support overlapping
segments, infer nested shell/hole topology, or collapse multiple disconnected
components of the unbounded face into one face record. Those operations require
a robust noder and explicit arrangement face classification.

## Core invariants

- Every half-edge has exactly one reciprocal twin with reversed endpoints.
- Every half-edge belongs to a closed next/previous cycle.
- `next.prev` and `prev.next` are reciprocal.
- Face boundary cycles are retained from their input ring.
- Exterior cycles are separately discoverable.

## Complexity

For V vertices and E undirected edges, vertex creation and edge pairing use
hash maps in expected O(V+E). The correctness-first check for un-noded
crossings, T-junctions and partial collinear overlaps currently costs O(E²).
Exact angular sorting of outgoing edges costs
O(sum(deg(v) log deg(v))) rational comparisons. Cycle construction and invariant validation are
O(E). The representation uses O(V+E) storage.

## Limitations

Input rings must be closed, finite, simple enough for the intended planar
rotation system, and already noded. Duplicate same-direction edges are rejected.
A full arrangement pipeline still needs exact noding, robust orientation and
intersection predicates, face-cycle containment/assembly, and Boolean labels.
