# Steiner tree in a weighted network

The Steiner tree problem seeks a minimum-weight connected subgraph spanning a specified terminal set; intermediate non-terminal vertices may be used. Unlike a minimum spanning tree over all vertices, only the terminals are mandatory.

The Dreyfus–Wagner algorithm uses subset dynamic programming over terminal groups, combining partial trees at a common vertex and applying shortest-path closure. It is exact but exponential in the number of terminals.

See the [tested implementation](../../implementations/python/steiner-tree/README.md), [tests](../../implementations/python/steiner-tree/test_steiner_tree.py) and [verification record](../../catalog/verification/steiner-tree.md).
