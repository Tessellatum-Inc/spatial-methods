# Topology-preserving ring simplification

The Python implementation uses a Visvalingam effective-area priority queue,
with lazy heap invalidation. Before removing a vertex it checks the proposed
replacement chord against all non-incident current edges using rational
orientation predicates. It also prevents zero-area collapse and orientation
reversal. This guarantees a simple output ring for a valid simple input ring.

The implementation is intentionally scoped to a single ring; it is not a
coverage-preserving or shell/hole-aware polygon simplifier. Candidate
validation is quadratic per removal in the worst case.
