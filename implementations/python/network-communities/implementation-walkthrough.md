# Walkthrough: label propagation

1. Give every node its own initial label.
2. Convert the supplied adjacency to an undirected neighbourhood set.
3. Shuffle node visitation order with a reproducible pseudo-random generator.
4. For each node, count neighbour labels and adopt a label with maximum frequency.
5. Break ties randomly; update immediately (asynchronous propagation).
6. Stop when a full sweep changes no labels or the iteration limit is reached.

The result is a partition represented by node-valued community labels. A community label is not a stable identifier across runs. This local majority heuristic is useful as a compact baseline but does not optimize a global objective and is not a substitute for Louvain, Leiden or Infomap.
