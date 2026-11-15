# Spectral graph partitioning

For an undirected weighted graph, let A be its symmetric adjacency matrix and D the diagonal degree matrix. The symmetric normalized Laplacian is L = I - D^(-1/2) A D^(-1/2). Its second-smallest eigenvector is the Fiedler vector; sorting vertices by this coordinate gives candidate cuts.

The implementation evaluates every non-trivial prefix cut in that order and selects the one minimising normalized cut: cut(A,B)/vol(A) + cut(A,B)/vol(B). This is a spectral relaxation followed by a discrete sweep, not an exact minimum-cut solver. Isolates are assigned after partitioning the positive-degree subgraph.

The [Python implementation](../../implementations/python/spectral-partitioning/README.md) uses a dense symmetric eigensolver. It is suitable as a transparent small-graph baseline; O(n^3) eigendecomposition and O(n^2) storage are unsuitable for very large sparse networks. Tests cover dense blocks with a weak bridge, paths, disconnected components, isolates, all-isolate graphs and invalid input.
