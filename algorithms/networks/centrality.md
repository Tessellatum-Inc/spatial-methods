# Directed network centrality: betweenness, closeness and PageRank

## Betweenness centrality

For a directed graph, node betweenness counts the fraction of ordered source-target shortest paths that pass through a node, excluding endpoints. Brandes' algorithm accumulates shortest-path multiplicities and dependencies without enumerating every path. Unweighted graphs use BFS; strictly positive weighted graphs use Dijkstra. The normalized directed score divides by (n−1)(n−2) for n > 2.

## Closeness centrality

This implementation uses inward closeness: a node scores highly when other nodes can reach it by short paths. It runs BFS from each target on the reversed graph and applies the Wasserman–Faust correction:

C(v) = (r/(n−1)) × (r/Σu d(u,v))

where r is the number of other nodes that can reach v. Unreachable nodes are excluded from the distance sum but penalized through the reachability fraction.

## PageRank

PageRank is the stationary score of a random surfer who follows outgoing edges with probability alpha and teleports with probability 1−alpha. Weighted edges determine transition probabilities. Dangling nodes redistribute their rank according to the teleportation vector; optional personalization changes that vector.

## Implementation and verification

The dependency-free directed reference package includes Brandes, corrected closeness and weighted PageRank, with analytical graph fixtures and input-validation tests. See the [implementation](../../implementations/python/network-centrality/README.md), [tests](../../implementations/python/network-centrality/test_centrality.py) and [verification record](../../catalog/verification/network-centrality.md).

## Scope

These methods are not interchangeable with undirected centrality conventions. The package does not implement space-syntax integration, edge betweenness, current-flow centrality, temporal centrality or community detection.
