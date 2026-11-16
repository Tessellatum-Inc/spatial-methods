# k-core decomposition

A k-core is the maximal induced subgraph in which every retained vertex has degree at least k. A vertex's core number is the largest k for which it belongs to a k-core. This nested density hierarchy is not itself a community partition.

## Degree peeling

1. Symmetrise adjacency and remove duplicate edges and self-loops.
2. Initialise each vertex's degree.
3. Repeatedly remove a minimum-degree vertex.
4. Record the current minimum as its core number.
5. Decrement an unremoved neighbour only when its current degree exceeds the removed degree.

The conditional decrement is essential; decrementing every neighbour can produce incorrect core numbers. A lazy min-heap gives O((V + E) log V) time and O(V + E) memory.

The [Python reference implementation](../../implementations/python/k-core/README.md) returns core numbers and induced k-core adjacency. It includes vertices named only as neighbours and treats the input as undirected and unweighted.

Tests cover paths, a triangle with a pendant vertex, cliques, disconnected components, isolates, asymmetric adjacency, duplicate edges, self-loops, neighbour-only vertices and invalid k values. This is a tested teaching baseline, not a specialised linear-time implementation.
