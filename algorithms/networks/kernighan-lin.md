# Kernighan–Lin graph bisection

Kernighan–Lin improves a balanced two-way partition of an undirected weighted graph. For a vertex v, define D(v) as its total edge weight to the opposite block minus its weight to its own block. Swapping a in A with b in B changes the cut by gain g(a,b) = D(a) + D(b) - 2w(a,b).

A pass repeatedly selects the unlocked pair with maximum gain, locks both vertices and updates the D values. Because an early swap may be locally harmful but enable a better sequence, the algorithm records cumulative gain after every pair and applies only the prefix with the greatest positive cumulative gain. Repeat until no positive prefix remains.

The [Python implementation](../../implementations/python/kernighan-lin/README.md) supports balanced bisection, non-negative finite weights and deterministic initialisation. It is a transparent O(n^3)-per-pass teaching baseline, not a multilevel graph partitioner. Tests exercise a weak-bridge two-community fixture, unweighted paths, isolates, input partition validation and invalid weights.
