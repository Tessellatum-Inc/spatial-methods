# Label-propagation community detection

Label propagation assigns each node the most common community label among its neighbours. Starting from unique labels, nodes are visited in shuffled order and updated asynchronously. Ties are broken randomly. The method is computationally light and often converges quickly, but the result can depend on visitation order and random seed.

The included baseline symmetrises adjacency lists and treats the graph as unweighted and undirected. Isolated nodes retain their own labels. It does not optimize modularity, guarantee a unique partition, or provide Louvain, Leiden or Infomap functionality.

See the [tested implementation](../../implementations/python/network-communities/README.md), [tests](../../implementations/python/network-communities/test_label_propagation.py) and [verification record](../../catalog/verification/label-propagation.md).
