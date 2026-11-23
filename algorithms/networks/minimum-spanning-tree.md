# Minimum spanning tree

A minimum spanning tree (MST) is a minimum-total-weight subset of edges connecting all vertices of a connected undirected weighted graph without cycles. Kruskal's algorithm sorts edges by weight and accepts an edge only when it joins two previously separate components, using a disjoint-set union structure.

The implementation returns a minimum spanning forest for disconnected inputs, supports parallel edges and negative finite weights, ignores self-loops, and resolves equal-weight ties by input order.

See the [tested implementation](../../implementations/python/minimum-spanning-tree/README.md), [tests](../../implementations/python/minimum-spanning-tree/test_minimum_spanning_tree.py) and [verification record](../../catalog/verification/minimum-spanning-tree.md).
