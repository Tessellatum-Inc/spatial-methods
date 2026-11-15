# Quad-edge subdivision primitives

Implements the Guibas–Stolfi four-dart representation and its rotation/origin-ring navigation identities, plus `make_edge`, `splice`, `connect`, and `delete_edge`.

The module is a topological substrate only. It does not include point-location, geometric predicates, face-label management, constrained edges, or a Delaunay triangulation algorithm. Applications must supply robust orientation/incircle predicates and maintain geometric embedding invariants. Deletion detaches the primal darts but retains the edge record for auditability.
