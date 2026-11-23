# k-core decomposition

Dependency-free undirected graph implementation returning node core numbers and induced k-core adjacency. Input adjacency is symmetrised; duplicate edges and self-loops are ignored, and neighbour-only vertices are retained.

Run: python -m pip install -r requirements.txt && python -m pytest -q

Degree peeling repeatedly removes a minimum-current-degree vertex. Its removal degree is the core number; an unremoved neighbour is decremented only when its current degree exceeds the removed degree. A lazy min-heap gives O((V + E) log V) time and O(V + E) memory. Directed cores, weighted cores and parallel-edge multiplicity are not inferred.
