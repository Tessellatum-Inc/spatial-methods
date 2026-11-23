# Walkthrough: Kruskal minimum spanning tree

Kruskal considers edges in non-decreasing weight order. A disjoint-set union (DSU) structure tracks the connected components formed by already accepted edges. An edge is accepted only when its endpoints currently belong to different components; this prevents cycles. Path compression and union by rank keep DSU operations close to constant amortized time.

When the graph is disconnected, the same procedure returns a minimum spanning forest. The implementation reports the component count and distinguishes a forest from a spanning tree.
