# Verification record: directed network centrality

## Source identity
- Compendium: *Spatial Analysis Algorithms: Complete Compendium*
- Original location: Section 1, page 2
- Source entry: centrality — betweenness, closeness, PageRank

## Implemented methods
- Brandes directed node betweenness (BFS unweighted; Dijkstra strictly-positive weighted)
- Inward directed closeness with Wasserman–Faust reachability correction
- Weighted directed PageRank with dangling-node redistribution and personalization

## Tests
- Directed chain and diamond analytical fixtures
- Weighted shortest-path ordering
- Disconnected and small graph behaviour
- Inward reachability and complete directed graph closeness
- PageRank normalisation, dangling nodes, weighted transitions and personalization
- Invalid weights, damping, iteration caps and non-convergence

## Review boundary
The grouped source row remains partial: space-syntax metrics and additional centrality variants are not implemented here. Source identity, bibliography, claims and rights review remain required before full verification.
