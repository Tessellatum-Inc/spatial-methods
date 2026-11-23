# Minimum spanning tree and forest

Kruskal's algorithm sorts undirected weighted edges by weight and uses a disjoint-set union structure with path compression and union by rank. It returns a minimum spanning tree for a connected graph and a minimum spanning forest for disconnected graphs. Parallel edges are supported; self-loops are ignored; negative finite weights are valid.

## Run

~~~bash
python -m pip install -r requirements.txt
python -m pytest -q
~~~

## Limits

This is a clear O(E log E) reference implementation. It does not implement Euclidean MST, dynamic MST updates, constrained/Steiner trees, directed arborescences, or specialised external-memory graph processing. Equal-weight ties are resolved by input order for reproducibility.
