# Walkthrough: Dreyfus–Wagner Steiner tree

For each non-empty terminal subset S and possible root vertex v, the dynamic program stores the minimum cost of a connected subgraph spanning S and containing v.

- A singleton subset is initialized at its terminal.
- For larger subsets, the best merge at v combines two disjoint terminal subsets whose trees meet at v.
- A multi-source Dijkstra closure then propagates each subset's best root cost through the graph.
- The full-set state is minimized over all possible root vertices.
- Parent records reconstruct shortest-path extensions and subset merges into the final edge set.

The subset dimension is exponential. Keep the terminal limit small; this exact algorithm is useful for learning and small instances, not large production networks.
