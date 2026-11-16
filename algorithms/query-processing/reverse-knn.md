# Reverse k-nearest-neighbour queries

A reverse k-nearest-neighbour (RkNN) query asks which data objects regard a
query location as one of their k nearest neighbours. Instead of finding the
neighbours of q, it finds data objects whose neighbour lists would contain q.

## Exact tie policy

For a data point p and external query q, q qualifies when fewer than k data
points are strictly closer to p than q is. All points tied at the kth distance
are included; no arbitrary record-order tie break is imposed.

## Indexed reference plan

1. Build a 2D k-d tree over the data records.
2. For each query q and data record p, compute d(p,q).
3. Radius-query the tree around p with radius d(p,q).
4. Count candidates whose squared distance to p is strictly less than d(p,q)^2.
   Stop once k strictly closer records are found.
5. Include p when the count is below k.

The implementation expands the radius by one representable floating-point
step before querying, then applies the strict squared-distance predicate.
The radius query is a candidate generator; it does not decide membership.

## Complexity and limitations

The tree is built once. Each data/query pair triggers one radius query, so
performance depends on candidate counts. Worst-case work is O(m*n^2) for m
queries and n data records, especially when query radii cover most of the
data. This is an indexed teaching baseline, not a claimed subquadratic
reverse-kNN index. It assumes planar Euclidean coordinates and static data;
network, spherical and dynamic variants remain open.

See the implementation and brute-force differential tests in the
reverse-knn package.
