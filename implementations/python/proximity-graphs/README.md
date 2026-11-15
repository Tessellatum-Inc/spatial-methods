# Proximity graph baselines

Implements:
- Gabriel graph using the open-diameter-disk definition;
- relative neighbourhood graph using the open-lune definition;
- lune-based beta-skeleton for beta in [1,2] (beta=1 Gabriel, beta=2 RNG under the stated open-region convention);
- Yao graph using equal-angle cones, nearest selection, deterministic tie-breaking and undirected union;
- Euclidean minimum spanning tree using Kruskal over all point pairs.

## Run

~~~bash
python -m pip install -r requirements.txt
python -m pytest -q
~~~

## Contract and limits

Points are distinct finite planar x,y pairs. Edges are returned as input-index pairs; MST edges also include Euclidean length. The implementation uses direct all-pairs tests and is intended for small datasets and correctness checks, not large production workloads.

The strict interior tests implement open-region conventions. Points exactly on a Gabriel disk or RNG lune boundary do not block an edge. Tie conventions should be documented when comparing to another library.

The all-pairs Gabriel/RNG/beta-skeleton implementations are O(n³); the direct Yao implementation is O(n²), and the complete-graph MST is O(n² log n). The sparse Delaunay MST is O(n log n) for non-collinear planar sites. These are teaching implementations, not a specialised production geometry library.


## Sparse Delaunay Euclidean MST

The sparse MST function constructs a Delaunay triangulation, extracts its linear-size edge set and runs Kruskal only on those candidates. The Euclidean MST is contained in the Delaunay graph. Collinear sites bypass Qhull and are connected in lexicographic order. Seeded tests compare total tree length with the complete-graph Kruskal oracle. For non-collinear sites this is an O(n log n) teaching implementation, subject to SciPy/Qhull numerical predicates.

## Delaunay-filtered variants

The package also exposes `delaunay_filtered_gabriel_graph` and `delaunay_filtered_rng`. They construct a SciPy/Qhull Delaunay triangulation, then apply the corresponding open-region blocker test only to triangulation edges. This reduces the candidate set from all O(n²) pairs to O(n) planar edges, and the straightforward blocker scan gives an O(n²) total baseline.

These functions are intended for non-degenerate, general-position Euclidean point sets. Qhull selects one triangulation in cocircular cases, so boundary-tie edges omitted by that triangulation may also be absent from the filtered graph. The implementation is not the specialised linear-time RNG post-processing algorithm in Lingas (1994). Compare the Delaunay-filtered results with the all-pairs reference functions on general-position fixtures.
