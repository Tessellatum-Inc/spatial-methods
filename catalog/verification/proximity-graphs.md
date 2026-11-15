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


## Indexed Yao differential verification

The cKDTree Yao variant is compared edge-for-edge with the independent
quadratic implementation on seeded point clouds of 2, 3, 8, 25 and 80 sites,
for 3, 4, 8 and 16 cones and two cone orientations. Empty/singleton inputs,
symmetric directional ties and invalid boolean cone counts are also covered.
The indexed method is exact under the same floating-point angle and
input-index tie conventions; worst-case complexity remains quadratic.


## Memory-bounded Prim differential verification

Dense Prim is checked against complete-graph Kruskal and the Delaunay-candidate
MST over 54 seeded point clouds with sizes 0, 1, 2, 3, 5, 12, 35, 100 and 250.
Tests include collinear points, equal-distance square edges, duplicate sites,
and non-finite coordinates. The algorithm uses O(n) auxiliary storage and
O(n²) distance evaluations; it is not an asymptotically faster construction.


## Expanded degeneracy and structural checks

An additional 176 seeded integer-grid point clouds (sizes 2–23, eight clouds
per size) compare dense Prim and Delaunay-candidate Kruskal against the
complete-graph Kruskal reference. These clouds deliberately create repeated
edge lengths, collinear subsets, symmetric layouts and cocircular subsets.
Each returned sparse/Prim edge list is also checked structurally for exactly
n−1 valid edges, acyclicity and connectivity. Separate symmetric and
cocircular fixtures exercise Qhull tie cases. The indexed Yao implementation
is additionally compared edge-for-edge with its quadratic reference on 100
seeded integer-lattice clouds across four cone counts and two orientations.


## Indexed Delaunay beta-skeleton differential verification

The indexed variant is compared edge-for-edge with the all-pairs lune-based
reference for beta = 1, 1.25, 1.5, 1.75 and 2 on seeded general-position
clouds of 5, 12, 30 and 75 sites. The cKDTree query is only a candidate
blocker filter: both defining disks are checked with the strict-interior
predicate. Collinear inputs and invalid beta values are rejected. This
remains a practical indexed baseline, not an optimal asymptotic construction;
Qhull cocircular tie behaviour is an explicit limitation.
