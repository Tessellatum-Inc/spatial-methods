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
