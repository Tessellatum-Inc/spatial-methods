# Verification record: Louvain community detection

- **Source:** Section 1, page 2, grouped entry “Community detection: Louvain, Leiden, Infomap, label propagation”.
- **Method:** Seeded local modularity moves followed by graph aggregation over multiple levels.
- **Implementation:** Dependency-free weighted undirected reference algorithm; reciprocal edge weights are averaged.
- **Tests:** Two K4 blocks joined by a weak bridge, modularity improvement, seeded reproducibility, empty graph, isolates, asymmetric adjacency, resolution response and input validation.
- **Boundary:** Heuristic baseline only. It does not provide Leiden's connectivity refinements, Infomap's flow objective or a global optimum. Grouped source entry remains partial.
