# Implementation verification — proximity graphs

## Implemented algorithms

- Gabriel graph using the open diameter-disk predicate.
- Relative neighbourhood graph using the open lune predicate.
- Lune-based beta-skeleton for beta in [1, 2].
- Yao graph using equal-angle cones, nearest choice per cone and undirected union.
- Complete-graph Euclidean MST using Kruskal as a small-input reference.
- Delaunay-filtered Gabriel and RNG candidates, with explicit cocircular tie limitations.
- Delaunay-candidate Euclidean MST using sparse triangulation edges and Kruskal; collinear sites use adjacent sorted neighbours.

## Verification

Tests check defining geometric predicates, graph containment on fixtures, MST edge count and total length, invalid inputs, and seeded differential comparisons. The Delaunay MST test compares its total length with the complete-graph Kruskal reference on 56 seeded general-position point clouds across sizes 2–100. Collinear and small inputs are tested separately.

## Complexity and limitations

The all-pairs Gabriel/RNG/beta and Yao implementations are transparent small-data references. The complete-graph MST is O(n² log n). Delaunay candidate extraction plus Kruskal is O(n log n) for non-collinear planar sites, subject to SciPy/Qhull. The Delaunay-filtered Gabriel/RNG functions still use a per-candidate blocker scan and are O(n²), not the specialised linear-time constructions. The beta-skeleton is the lune-based variant only. No claim is made that the current Yao implementation is subquadratic.

## Reproduction

From the package directory: `python -m pip install -r requirements.txt && python -m pytest -q`.
