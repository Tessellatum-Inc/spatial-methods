# Möller–Trumbore ray/triangle intersection

Given a ray r(t)=o+t*d and triangle vertices a,b,c, determine whether the half-line intersects the triangle. A hit returns t, barycentric coordinates and the intersection point.

Set e1=b-a, e2=c-a, p=d cross e2, and delta=e1 dot p. A near-zero determinant indicates a parallel ray or degenerate triangle. Otherwise:

    u = ((o-a) dot p) / delta
    q = (o-a) cross e1
    v = (d dot q) / delta
    t = (e2 dot q) / delta

A hit satisfies u>=0, v>=0, u+v<=1 and the requested ray-parameter interval. The third barycentric weight is w=1-u-v. The determinant sign supports optional back-face culling.

The test takes constant time per triangle; testing all n faces independently is O(n). BVHs and kd-trees are separate acceleration structures and are not included. Floating-point tolerances are not exact predicates. The ray direction need not be normalised, so t is not a physical distance unless it is.

For geospatial use, work in a consistent Cartesian 3D coordinate frame. Raw longitude/latitude are not suitable Euclidean coordinates. See the [tested Python implementation](../../implementations/python/ray-triangle-intersection/README.md), [walkthrough](../../implementations/python/ray-triangle-intersection/implementation-walkthrough.md), and Möller and Trumbore (1997), “Fast, Minimum Storage Ray-Triangle Intersection,” DOI: 10.1080/10867651.1997.10487468.
