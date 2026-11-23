# Spectral graph bisection

A normalized-Laplacian spectral partitioner for undirected weighted graphs. It computes the Fiedler vector with a dense symmetric eigensolver and selects the minimum normalized-cut threshold over the sorted vector coordinates.

Run: python -m pip install -r requirements.txt && python -m pytest -q

Reciprocal adjacency weights are averaged; iterable adjacency means unit weights. Self-loops and zero-weight edges are ignored. Isolates are assigned after partitioning the positive-degree subgraph. Dense eigendecomposition costs O(n^3) time and O(n^2) memory, so this is a small/medium teaching baseline, not a sparse large-graph implementation. Disconnected graphs have a non-unique Fiedler eigenspace; the sweep chooses a valid zero-cut split but equivalent results may vary with numerical eigensolver details.
