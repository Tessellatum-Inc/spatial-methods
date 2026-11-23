# Louvain community detection

Louvain heuristically maximises weighted modularity. For an undirected graph with total edge weight m, node strengths k and resolution gamma, Q = sum over communities C of [internal_weight(C)/m - gamma * (total_strength(C)/(2m))^2]. Internal weight counts each undirected edge once.

## Multilevel method
1. Start with singleton communities.
2. Visit nodes in seeded order, evaluating modularity gain from insertion into neighbouring communities.
3. Apply positive-gain moves until local passes converge.
4. Contract communities to supernodes, summing inter-community weights.
5. Repeat until aggregation no longer reduces the graph.

The [Python implementation](../../implementations/python/louvain/README.md) includes modularity evaluation, resolution control and seeded runs. It does not guarantee a global optimum, connected communities or a unique partition. Leiden is a distinct method with connectivity refinements.
