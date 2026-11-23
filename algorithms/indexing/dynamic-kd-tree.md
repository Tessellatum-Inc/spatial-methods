# Dynamic k-d tree

A dynamic k-d tree supports spatial queries while points are inserted and
deleted. This implementation uses a scapegoat-style rebuilding policy:
insertions follow split planes and rebuild a subtree when one child exceeds
the configured alpha fraction of its size. Deletions are lazy; a subtree is
rebuilt when its inactive-node fraction exceeds the allowed threshold.

The tree assigns stable monotonically increasing IDs to inserted points.
Nearest-neighbour, k-nearest, radius and inclusive rectangle queries ignore
deleted nodes and break distance ties by ID. Subtree rebuilding chooses the
axis with greatest coordinate spread and partitions by deterministic median.

The implementation is a reference design, not a worst-case logarithmic
dynamic index. Rebuilding sorts each subtree, so a rebuild of m active points
costs O(m log² m), and adversarial updates can trigger repeated rebuilds.
Queries remain distribution-dependent and the index is limited to planar
Euclidean coordinates.

## Runnable implementation

[Dynamic and static k-d tree package](../../implementations/python/kd-tree/README.md).


## Reference

The balancing approach is inspired by partial-rebuilding and scapegoat-tree methods; this implementation is a k-d-tree adaptation and does not claim the original binary-search-tree amortized bounds.

- Galperin, I., & Rivest, R. L. (1993). Scapegoat Trees. *Proceedings of the Fourth Annual ACM-SIAM Symposium on Discrete Algorithms*, 165–174.
