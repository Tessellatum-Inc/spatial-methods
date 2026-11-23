# Topology-preserving ring simplification

A pure-Python, single-ring Visvalingam implementation. Candidate vertices are
ordered by effective triangle area in a versioned min-heap. A removal is
accepted only if the replacement chord does not intersect any non-incident
current edge and the ring retains non-zero area and its original orientation.
Orientation and segment-intersection decisions use exact rational predicates
over the input's decimal float representations.

The routine accepts open or explicitly closed ring sequences and preserves
that closure convention. Threshold units are squared coordinate units.

Scope: one simple ring at a time. It does not preserve topology between
separate polygons, shells and holes, or an entire polygon coverage. Worst-case
runtime is O(n^2 log n) because each candidate chord is checked against the
current ring. Use a projected CRS and choose tolerance in meaningful units.
