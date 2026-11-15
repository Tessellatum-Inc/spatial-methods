# Directed network centrality

Dependency-free reference implementations of three core directed-graph metrics:

- **Betweenness:** Brandes dependency accumulation, with BFS for unweighted graphs and Dijkstra for strictly positive weighted graphs. Endpoints are excluded; normalized directed scores divide by (n-1)(n-2).
- **Closeness:** inward directed closeness, with the Wasserman–Faust correction for disconnected graphs.
- **PageRank:** weighted outgoing transition probabilities, power iteration, teleportation and dangling-node redistribution. Optional personalization is supported.

These routines accept adjacency mappings of node to (neighbour, weight) pairs. They do not silently convert directed graphs to undirected ones. Betweenness weighted mode requires strictly positive weights so shortest-path predecessor relations remain well-defined. PageRank weights must be finite and non-negative. These are transparent baselines, not graph-engine replacements; very large graphs should use sparse or compiled graph libraries.

## Run

~~~bash
python -m pip install -r requirements.txt
python -m pytest -q
~~~

## Complexity

Unweighted Brandes runs in O(VE); weighted Brandes runs one Dijkstra search per source, approximately O(V(E+V) log V) with a binary heap. Closeness performs one reverse BFS per node, O(V(V+E)). PageRank performs O(E) work per power iteration.
