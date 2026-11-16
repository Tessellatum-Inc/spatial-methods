# Walkthrough: directed network centrality

## Betweenness — Brandes

For each source, shortest-path counts (sigma) and predecessor lists are accumulated during BFS or Dijkstra. A reverse stack pass propagates dependency scores. This avoids enumerating every shortest path explicitly. Directed normalization divides by (n-1)(n-2), with endpoints excluded.

## Closeness

The implementation reports inward closeness: how easily other nodes can reach a target. It searches from the target on the reversed graph. The Wasserman–Faust correction multiplies the inverse mean distance by the fraction of the graph that can reach the target, avoiding an unfairly high score for isolated components.

## PageRank

Each node distributes its score over outgoing edges in proportion to edge weight. Nodes with no outgoing edges are dangling nodes; their rank is redistributed according to the teleportation/personalization vector. Iteration stops when the L1 change is below tolerance, or raises if the iteration cap is reached.

## Limitations

No multigraph edge identities, temporal edges, turn-state expansion, stochastic transitions, centrality uncertainty intervals or community detection are included.
