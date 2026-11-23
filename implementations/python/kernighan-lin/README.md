# Kernighan–Lin balanced graph bisection

Dependency-free weighted/unweighted undirected graph bisection. The algorithm starts from an equal-size partition, repeatedly locks the best pair of opposite-side vertices by gain, then applies the best positive cumulative-gain prefix. It stops at a one-pass local optimum or max_passes.

Run: python -m pip install -r requirements.txt && python -m pytest -q

The input is symmetrised; if both directions specify an edge, their weights are averaged. Weights must be finite and non-negative. The implementation targets balanced bisection only: it rejects empty and odd-sized graphs, and is not a multilevel METIS replacement or a general multiway partitioner. Worst-case work per pass is O(n^3) in this straightforward reference implementation.
