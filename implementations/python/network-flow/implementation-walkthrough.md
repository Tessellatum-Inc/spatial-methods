# Walkthrough: Dinic maximum flow

Dinic alternates between two phases:

1. BFS builds a level graph from the source using residual arcs with positive capacity.
2. A depth-first blocking-flow routine sends as much flow as possible along level-increasing paths.
3. When no more blocking flow can be sent, BFS is repeated on the updated residual network.
4. When the sink is no longer residual-reachable, the flow is maximum.
5. The residual-reachable set is the source side of a minimum cut; original arcs crossing from that set to its complement form the cut.

Every input arc gets its own reverse residual arc, so parallel and antiparallel original arcs are not conflated. Returned flow values are indexed by input arc order.
