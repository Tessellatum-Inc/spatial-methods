# Verification record: k-core decomposition

- **Source:** Section 1, page 2, grouped entry “Flows and trees”.
- **Identity:** A k-core is a maximal induced subgraph with minimum degree at least k; node core numbers define the nested hierarchy.
- **Implementation:** Dependency-free undirected degree peeling with lazy min-heap.
- **Complexity:** O((V + E) log V) time; O(V + E) memory.
- **Tests:** Paths, clique, triangle-plus-tail, disconnected components, isolates, asymmetric adjacency, duplicates, self-loops, neighbour-only vertices and input validation.
- **Boundary:** Directed and weighted variants are not implemented. This completes the k-core member only; the grouped source row remains partial pending independent identity, bibliography, claims and rights review.
