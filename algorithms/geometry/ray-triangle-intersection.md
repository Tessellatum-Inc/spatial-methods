# Möller–Trumbore ray/triangle intersection

Given a ray r(t)=o+t*d and triangle vertices a,b,c, determine whether the half-line intersects the triangle. A hit returns t, barycentric coordinates and the intersection point.

Set e1=b-a, e2=c-a, p=d cross e2, and delta=e1 dot p. A near-zero determinant indicates a parallel ray or degenerate triangle. Otherwise:

    u = ((o-a) dot p) / delta
    q = (o-a) cross e1
    v = (d dot q) / delta
    t = (e2 dot q) / delta

A hit satisfies u>=0, v>=0, u+v<=1 and the requested ray-parameter interval. The third barycentric weight is w=1-u-v. The determinant sign supports optional back-face culling.

The test takes constant time per triangle; a brute-force mesh query is O(n). The accompanying package also includes AABB slab tests and a binary BVH with exact-centroid SAH split scans. Its near-first traversal tightens the closest-hit bound and is tested against seeded brute-force queries. Exact split scans are transparent but slower to build than binned SAH. kd-tree ray traversal remains a separate method. Floating-point tolerances are not exact predicates. The ray direction need not be normalised, so t is not a physical distance unless it is.

For geospatial use, work in a consistent Cartesian 3D coordinate frame. Raw longitude/latitude are not suitable Euclidean coordinates. See the [tested Python implementation](../../implementations/python/ray-triangle-intersection/README.md), [walkthrough](../../implementations/python/ray-triangle-intersection/implementation-walkthrough.md), and Möller and Trumbore (1997), “Fast, Minimum Storage Ray-Triangle Intersection,” DOI: 10.1080/10867651.1997.10487468.


## Frustum/AABB culling

For an inward-facing plane n dot x + d >= 0, the AABB support vertex in the direction of n maximises the plane expression. If that vertex is still negative (outside tolerance), the entire box is outside that plane and can be culled. Testing all six frustum planes is constant time per box. This is conservative plane culling only; occlusion queries, hierarchical-Z, matrix-to-plane extraction and level-of-detail selection are separate methods.


## Spatial kd-tree ray traversal

A spatial kd-tree partitions space rather than merely grouping object bounds. This reference chooses the longest node axis, splits at the median triangle-box centroid and places a triangle in every child cell its AABB intersects. Straddling triangles are therefore duplicated in the tree, but a query tests each original triangle at most once.

Traversal intersects the ray with each child cell, visits the nearer cell first and prunes cells whose entry parameter exceeds the best known hit. The builder stops at the leaf-size threshold, a maximum depth, or a non-progressing split. It is a deterministic median-split teaching baseline; production kd-trees commonly use surface-area cost models and more sophisticated clipping/duplication policies.

The seeded differential tests compare nearest hits with brute-force triangle scans and include split-plane-parallel rays. The [Python package](../../implementations/python/ray-triangle-intersection/README.md) documents the spatial duplication and coordinate-system limitations.
