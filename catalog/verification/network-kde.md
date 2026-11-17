# Network KDE implementation verification

Implemented: undirected weighted graph construction; Dijkstra shortest paths;
one-dimensional Gaussian kernel evaluation at graph vertices; optional
non-negative event weights and target subsets; disconnected-component
handling; shortest parallel-edge handling.

Independent tests compare outputs against hand-computed shortest-path
distances and a separately written Gaussian formula. They cover weights,
parallel paths, disconnected components and invalid inputs.

Not implemented: within-edge event positions, continuous edge integration,
network edge correction, bandwidth selection, network K and SANET methods.
This is a bounded vertex-sampled baseline, not a full network point-process
analysis system.
