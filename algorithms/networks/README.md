# Network algorithms

This index links the algorithm dossiers to their runnable reference implementations. The packages are deliberately scoped teaching baselines; their READMEs describe assumptions, limitations, and test commands.

## Graph search and routing

- [Shortest paths](shortest-paths.md) — Dijkstra and A* foundations; [Python package](../../implementations/python/shortest-paths/README.md).
- [Turn-aware and time-dependent routing](turn-aware-time-dependent-routing.md) — edge-state Dijkstra with turn restrictions/penalties and FIFO earliest-arrival routing; [Python package](../../implementations/python/road-routing/README.md).
- [HMM map matching](map-matching.md) — candidate generation and Viterbi decoding using caller-supplied network distances; [Python package](../../implementations/python/map-matching/README.md).
- [Multi-criteria shortest paths](multi-criteria-shortest-paths.md) — Pareto label-setting for additive non-negative vector costs; [Python package](../../implementations/python/shortest-paths/README.md).

## Transit routing

- [RAPTOR](raptor.md) — round-based timetable earliest-arrival baseline with footpaths; [Python package](../../implementations/python/raptor/README.md).
- [Connection Scan Algorithm](connection-scan.md) — departure-ordered timetable scan with transfer constraints; [Python package](../../implementations/python/csa/README.md).

## Facility location and allocation\n\n- [Flow-capturing location model](flow-capturing-location.md) — exact and greedy maximum captured-flow site selection over known network paths.\n\n## Matching and allocation\n\n- [Stable matching](stable-matching.md) — resident-proposing deferred acceptance for capacity-constrained institutions, with a separate blocking-pair audit; [Python package](../../implementations/python/stable-matching/README.md).\n\n## Network structure and partitioning

- [Centrality](centrality.md) — betweenness, closeness, and PageRank; [Python package](../../implementations/python/network-centrality/README.md).
- [Label propagation](label-propagation.md) — seeded label-propagation community detection; [Python package](../../implementations/python/network-communities/README.md).
- [Louvain](louvain.md) — multilevel modularity optimisation; [Python package](../../implementations/python/louvain/README.md). This is not Leiden and does not guarantee internally connected communities.
- [K-core](k-core.md) — degree peeling and core decomposition; [Python package](../../implementations/python/k-core/README.md).
- [Kernighan–Lin](kernighan-lin.md) — balanced graph bisection by pair swaps; [Python package](../../implementations/python/kernighan-lin/README.md).
- [Spectral partitioning](spectral-partitioning.md) — normalized-Laplacian Fiedler sweep; [Python package](../../implementations/python/spectral-partitioning/README.md).

## Network optimisation

- [Maximum flow and minimum cut](maximum-flow-min-cut.md) — Dinic's blocking-flow algorithm and Edmonds–Karp augmenting paths; [Dinic Python package](../../implementations/python/network-flow/README.md), [Edmonds–Karp Python package](../../implementations/python/max-flow-min-cut/README.md).
- [Minimum spanning tree and forest](minimum-spanning-tree.md) — Kruskal with disjoint-set union; [Python package](../../implementations/python/minimum-spanning-tree/README.md).
- [Steiner tree](steiner-tree.md) — exact Dreyfus–Wagner subset dynamic programming for small terminal sets; [Python package](../../implementations/python/steiner-tree/README.md).

## Not yet implemented as production/reference packages

The source inventory remains broader than this index. In particular, Leiden, Infomap, METIS-style multilevel partitioning, sparse spectral solvers, transit feed/calendar/realtime semantics, non-FIFO time-dependent routing, and highway/arc-flag/transit-node routing accelerators remain separate work items. Do not interpret a dossier or source-inventory mention as an implementation claim.
