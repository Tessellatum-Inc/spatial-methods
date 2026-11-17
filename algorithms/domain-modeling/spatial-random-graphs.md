# Spatial random graphs: distance-decay attachment and small-world rewiring

## Spatial preferential attachment

Given coordinates (x_i), an evolving graph can attach each new vertex to earlier vertices using a mixture of popularity and distance. This teaching generator starts with a complete graph on (m+1) vertices. Each later vertex (i) selects (m) distinct predecessors with weights

\[
w_{ij}=k_j^{\alpha}\exp\left(-\frac{\lVert x_i-x_j\rVert}{\ell}\right),
\]

where (k_j) is the current degree, (alpha) controls degree preference and (ell) is a distance scale. Sampling uses log weights for numerical stability. The output is an undirected adjacency matrix.

This is one explicit spatial attachment model, not a canonical reproduction of every spatial scale-free network model. Results depend on the seed layout, initial clique, exponent and distance scale.

## Watts–Strogatz small-world graph

The Watts–Strogatz construction starts with a ring lattice of (n) vertices, each connected to (k) nearby vertices where (k) is even. Each clockwise edge is rewired with probability (eta) to a randomly selected non-neighbor. The implementation preserves the edge count and avoids self-loops and duplicate edges. Rewiring does not guarantee that the graph remains connected.

## Contracts and limitations

- Coordinates must be finite and use a consistent Euclidean coordinate space; geographic longitude/latitude should be projected or converted before distance weighting.
- The spatial attachment model is undirected and uses a complete initial seed graph.
- The small-world generator requires even (k) with (2 \le k < n).
- Both return dense Boolean adjacency matrices, so memory is (O(n^2)); they are reference generators, not large-network storage engines.
- Seeded random streams make the construction reproducible for a fixed NumPy version and input.

The Section 7 source entry also names spatial random graphs, distance-decay preferential attachment, small-world and scale-free networks. These two bounded generators address part of that family; spatially embedded scale-free variants and validation against empirical networks remain open.
