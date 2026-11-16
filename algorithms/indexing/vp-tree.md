# Vantage-point trees for metric nearest-neighbour search

A vantage-point (VP) tree indexes observations using distances rather than axis-aligned coordinate splits. This makes the underlying idea applicable to metric spaces, provided the distance function obeys the triangle inequality.

## Construction

Choose one observation as a vantage point v. Compute its distances to the remaining observations, sort them and split around the median radius μ. Recursively build an inner subtree from the nearer observations and an outer subtree from the farther observations. A median split gives balanced tree depth even when many distances are equal, provided ties are split deterministically by observation identity.

## Exact k-nearest search

For query q, let d=d(q,v), and let τ be the current distance to the kth-best candidate (or infinity before k candidates have been found). By the triangle inequality:

- Every inner point x with d(v,x) ≤ μ satisfies d(q,x) ≥ d−μ.
- Every outer point x with d(v,x) ≥ μ satisfies d(q,x) ≥ μ−d.

Therefore an inner subtree can be pruned only when d−μ > τ, and an outer subtree only when μ−d > τ. Equality must be explored when deterministic tie handling is required.

## Complexity and trade-offs

The reference implementation sorts distances at every recursive node, giving O(n log² n) construction time and O(n) storage. Query performance depends on metric separation and data distribution; the worst case remains O(n). Unlike a k-d tree, a VP-tree does not rely on axis-aligned coordinate bounds, but its metric-distance pruning may be weaker for some spatial datasets.

## Scope of the repository implementation

The tested Python implementation is static, two-dimensional and Euclidean. It preserves duplicate observations and uses input order to resolve equal-distance results. It does not yet expose a generic metric interface, dynamic updates, approximate search, or high-dimensional benchmark claims.

See the [implementation and differential tests](../../implementations/python/vp-tree/README.md).

## References

- Yianilos, P. N. (1993). Data structures and algorithms for nearest neighbor search in general metric spaces. *Proceedings of SODA*, 311–321.
- Chávez, E., Navarro, G., Baeza-Yates, R. and Marroquín, J. L. (2001). Searching in metric spaces. *ACM Computing Surveys*, 33(3), 273–321.
