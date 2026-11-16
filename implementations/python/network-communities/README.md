# Label-propagation community detection

A dependency-free asynchronous label-propagation baseline for unweighted undirected graphs. Each node adopts the most frequent label among its neighbours; ties are broken randomly. A seeded node-order shuffle makes runs reproducible for a fixed input order and seed. The graph is symmetrised: every listed adjacency is treated as an undirected edge. Isolates retain their own labels.

## Run

~~~bash
python -m pip install -r requirements.txt
python -m pytest -q
~~~

## Algorithm and limits

Initial labels are unique node identifiers. Each sweep visits nodes in seeded random order and immediately applies updates. The method stops after a sweep with no changes or at the iteration cap. It is a fast heuristic, not a globally optimized modularity method. It can oscillate or converge to different partitions under different node orders/seeds; no modularity guarantee or stability estimate is provided. It is not Louvain, Leiden or Infomap, and does not implement weighted, directed, overlapping or hierarchical communities.
