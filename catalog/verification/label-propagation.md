# Verification record: label propagation

## Source identity
- Compendium: *Spatial Analysis Algorithms: Complete Compendium*
- Original location: Section 1, page 2
- Source entry: community detection — Louvain, Leiden, Infomap, label propagation

## Implemented scope
- Seeded asynchronous unweighted label propagation.
- Undirected adjacency projection; isolates retain their initial labels.
- Random tie breaking and maximum-sweep guard.

## Tests
- Two-node convergence, disconnected components, isolate retention.
- Asymmetric adjacency symmetrisation.
- Seed reproducibility and node/label preservation.
- Empty graph and invalid iteration/seed controls.

## Limits
This implements only the label-propagation member of the grouped source row. Louvain, Leiden, Infomap, Kernighan–Lin, spectral partitioning and METIS are not implemented by this package. The heuristic has no modularity optimality guarantee and may be order/seed sensitive.
