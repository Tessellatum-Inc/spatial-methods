# Proximity graph baselines

Implements:
- Gabriel graph using the open-diameter-disk definition;
- relative neighbourhood graph using the open-lune definition;
- lune-based beta-skeleton for beta in [1,2] (beta=1 Gabriel, beta=2 RNG under the stated open-region convention);
- Yao graph using equal-angle cones, nearest selection, deterministic tie-breaking and undirected union;
- Euclidean minimum spanning tree using Kruskal over all point pairs;
- sparse Delaunay-candidate Euclidean MST (with a collinear fallback).

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


## Indexed exact Yao construction

`yao_graph_kdtree` uses SciPy's cKDTree to search the globally nearest sites in
progressively larger batches until each angular cone has a candidate. Once a
candidate is found, no unqueried site can be closer; a radius query then
collects distance ties so the existing input-index tie rule is preserved.
Seeded tests compare the indexed output exactly with the quadratic reference
across several cone counts and orientations. This is an exact adaptive
nearest-neighbour strategy, but its worst case remains O(n²); it is not the
optimal O(n log n) algorithm from the literature.


## Memory-bounded dense Prim MST

`euclidean_mst_prim` constructs the Euclidean MST with dense Prim's algorithm.
It evaluates pairwise distances as vertices enter the tree, retaining only
one best connection and parent per outside vertex. This takes O(n²) time but
O(n) auxiliary space; it does not allocate or sort the complete O(n²)-edge
graph as Kruskal does. Seeded tests compare its total length with both the
complete-graph Kruskal oracle and the sparse Delaunay-candidate MST.


## Degeneracy-focused differential checks

The test suite now adds integer-grid clouds, where equal edge lengths,
symmetric configurations, collinear subsets and cocircular subsets occur
frequently. Dense Prim and Delaunay-candidate Kruskal are compared with the
complete-graph Kruskal reference; every result is checked for tree structure
(connectivity, acyclicity and n−1 edges), not only total length. The indexed
Yao implementation is also compared edge-for-edge with the quadratic
reference on tie-heavy lattice inputs and multiple cone orientations.


## Indexed Delaunay beta-skeleton

`delaunay_filtered_beta_skeleton` narrows candidate edges to a planar Delaunay triangulation, then uses a cKDTree radius query to enumerate only possible blockers in one of the two defining disks. Each candidate is still checked against both disks using the same strict-interior tolerance as the all-pairs reference. Seeded differential tests compare five beta values across general-position clouds up to 75 sites. This is expected to reduce blocker work on well-distributed data, but worst-case complexity remains quadratic; it is not the specialised optimal beta-skeleton algorithm. Qhull's choice among cocircular triangulations can omit boundary-tie candidates.
