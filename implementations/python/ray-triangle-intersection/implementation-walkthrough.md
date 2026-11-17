# Implementation walkthrough: Möller–Trumbore

Let the triangle vertices be a,b,c, the ray origin o, and direction d. Define e1=b-a, e2=c-a, and p=d cross e2. The determinant delta=e1 dot p identifies parallel/degenerate cases and, with its sign, supports optional back-face culling.

For non-degenerate cases:

    u = ((o-a) dot p) / delta
    q = (o-a) cross e1
    v = (d dot q) / delta
    t = (e2 dot q) / delta

A point lies inside the triangle when u>=0, v>=0, and u+v<=1. The third barycentric weight is w=1-u-v. The implementation applies the caller's ray interval and a small tolerance around edges and vertices.

## Validation

Tests cover interior, edge and vertex hits, parallel misses, points outside the triangle, hits behind the ray origin, degenerate triangles, culling policy, non-unit directions and invalid inputs. The returned t is the parameter in o+t*d, not necessarily a physical distance.

## Geospatial caution

The algorithm is Euclidean. Use a suitable local Cartesian 3D frame with consistent units. Geographic longitude/latitude coordinates require transformation before applying this test.


## BVH construction and traversal

Each triangle is enclosed by an axis-aligned bounding box (AABB). A ray-box slab test clips the valid ray-parameter interval against the x, y and z slabs; a zero direction component is handled by checking whether the origin is already inside that slab.

The builder computes triangle centroids, sorts them on each axis and evaluates every possible split. For a candidate split:

    cost = surface_area(left_bounds) * left_count
         + surface_area(right_bounds) * right_count

The best split is used only when it improves on the leaf cost. This exact-centroid scan is a teaching implementation; production renderers commonly use binned SAH to reduce build time.

Traversal tests child bounds, visits the nearer child first, and tightens the current maximum ray parameter after a triangle hit. The tests compare the BVH result with a brute-force scan over seeded fixtures. The tree indexes the exact input triangle sequence and must not be reused with reordered geometry.
