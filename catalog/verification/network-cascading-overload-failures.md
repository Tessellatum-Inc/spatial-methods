# Verification record — Motter–Lai cascading overload baseline

- **Primary source:** Motter & Lai (2002), Physical Review E 66, 065102(R), DOI 10.1103/PhysRevE.66.065102.
- **Method identity:** shortest-path node load, capacity proportional to intact-network load, iterative overload removal after an initial attack.
- **Implementation:** unweighted undirected graph, node betweenness, synchronous rounds, configurable tolerance, optional round guard.
- **Tests:** betweenness on a path, high-tolerance no-secondary-failure case, cascade bounds and invalid inputs.
- **Not reproduced:** original paper's network ensembles or quantitative figures; no physical flow simulation or spatial hazard model.
- **Status:** primary algorithm definition checked against the published article and author-hosted full text; teaching implementation reviewed; empirical reproduction not performed.