# Contraction hierarchies

Contraction hierarchies (CH) accelerate repeated shortest-path queries in a static weighted directed graph. A preprocessing order ranks vertices from least to most important. Contracting vertex v considers every active incoming edge u→v and outgoing edge v→w. If no witness path from u to w of cost at most w(u,v)+w(v,w) exists without visiting v or previously contracted vertices, a shortcut u→w is inserted.

After preprocessing, a query runs bidirectional Dijkstra over upward edges: the forward search follows edges to higher-ranked vertices; the backward search traverses incoming edges from lower-ranked vertices. The minimum sum at a common meeting vertex is the shortest-path distance. Shortcut references are recursively expanded to recover the original route.

## Implemented baseline

The Python package accepts directed nonnegative weighted edges, a supplied contraction permutation or deterministic static-degree order, deliberately retains all potentially shortest two-edge shortcuts without witness pruning, and answers exact static queries with shortcut unpacking. Seeded random directed graphs are checked against independent all-pairs Dijkstra distances.

## Limits

This is a correctness-focused teaching implementation, not a high-performance road router. Witness pruning is disabled, which can produce many shortcuts; the default order is a static degree heuristic, and no priority updates, nested dissection, witness caps, stall-on-demand, turn costs, dynamic customization, time-dependent costs or multimodal transfers are implemented.

## Sources

- Geisberger, R., Sanders, P., Schultes, D., & Delling, D. (2008). Contraction Hierarchies: Faster and Simpler Hierarchical Routing in Road Networks. In *Experimental Algorithms*, LNCS 5038, 319–333. https://doi.org/10.1007/978-3-540-68552-4_24.
- Geisberger, R., Sanders, P., Schultes, D., & Vetter, C. (2012). Exact Routing in Large Road Networks Using Contraction Hierarchies. *Transportation Science*, 46(3), 388–404. https://doi.org/10.1287/trsc.1110.0401.

No source code or figures are reproduced.
