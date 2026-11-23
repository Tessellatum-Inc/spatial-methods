# Intern walkthrough: contraction hierarchies

1. **Choose an order.** Vertices are ranked from least to most important. The teaching baseline accepts a permutation and otherwise uses static degree.
2. **Contract a vertex.** For every active incoming edge u→v and outgoing edge v→w, consider the path u→v→w.
3. **Search for a witness.** Run Dijkstra from u to w while avoiding v and all previously contracted vertices. If a path no more expensive than the candidate exists, no shortcut is needed.
4. **Add a shortcut.** Otherwise store u→w with the sum of the two edge weights and references to the child edges.
5. **Query.** Search upward from the source and upward in reverse from the target. Their best common meeting vertex yields the shortest distance.
6. **Unpack.** Recursively replace shortcut edges with their original constituent edges.

The random-graph tests compare every source/target pair with an independent Dijkstra oracle. This verifies exact distance preservation for the implemented static model, not road-network-scale performance.
