# Moving-object prediction and predictive range queries

For reported position p=(x,y), velocity v=(vx,vy) and elapsed time dt, the
constant-velocity estimate is p(dt) = p + v dt. This is a short-horizon
baseline that assumes velocity remains constant and coordinates and time
units are compatible.

Given an axis-aligned rectangle R and uncertainty radius r, predict each
object's center and retain it when the disk of radius r intersects R. The
implementation computes the Euclidean distance from the predicted center to
the nearest point on R and tests whether that distance is at most r. This is
a deterministic bounded-error envelope, not a probabilistic confidence
statement.

A new state report is requested when the observed position differs from the
extrapolated position by more than a caller-supplied tolerance. Production
systems may use anisotropic uncertainty, acceleration bounds, network
constraints or communication cost.

For n objects, a linear scan of one rectangle query costs O(n) time and
O(k) result storage for k matches. A TPR-tree or another spatiotemporal index
is needed for repeated large-population queries.

The [reference package](../../implementations/python/moving-object-prediction/README.md)
is not a TPR-tree, HR-tree, trajectory database or probabilistic motion model.

Reference: Saltenis, S., Jensen, C. S., Leutenegger, S. T., & Lopez, M. A.
(2000). Indexing the Positions of Continuously Moving Objects. Proceedings
of SIGMOD, 331–342. https://doi.org/10.1145/342009.335426
