# Moving-object prediction and predictive range queries

For reported position p=(x,y), velocity v=(vx,vy) and elapsed time dt, the
constant-velocity estimate is p(dt)=p+v*dt. This short-horizon baseline
assumes velocity remains constant and coordinates and time units are
compatible. Inputs and calculated coordinates must be finite; arithmetic
overflow is rejected rather than propagated as infinity.

Given an axis-aligned rectangle R and uncertainty radius r, predict each
object's center and retain it when the disk of radius r intersects R. The
implementation computes the Euclidean distance from the predicted center to
the nearest point on R and tests whether that distance is at most r. This is
a deterministic bounded-error envelope, not a probabilistic confidence
statement. Rectangle and disk boundaries are inclusive.

A new state report is requested when observed position differs from the
extrapolated position by more than a caller-supplied tolerance. The threshold
is strict. Production systems may use anisotropic uncertainty, acceleration
bounds, network constraints or communication cost.

For a continuous query over a finite horizon, constant velocity traces a line
segment. Liang–Barsky clipping finds the earliest intersection of that segment
with a closed axis-aligned rectangle, including a path that enters and exits
before the horizon endpoint. This exact point-path query has no uncertainty
envelope; it is distinct from the endpoint disk query.

For constant acceleration, each coordinate follows
p(t)=p0+v0*t+0.5*a*t². The accelerated continuous query solves the four
coordinate/boundary quadratic equations, retains real roots in the requested
time interval, and partitions the interval at those events. Checking event
times catches isolated tangencies; checking an interior point of each
root-free interval determines whether the path is inside there. The earliest
contact is returned. This is a deterministic point trajectory, not a
covariance region or probabilistic prediction. The result is exact up to
floating-point root arithmetic and a small scale-aware boundary tolerance.

For n objects, either continuous query is a linear scan with O(n) time and
O(k) result storage for k matches. A TPR-tree or another spatiotemporal index
is needed for repeated large-population queries.

The [reference package](../../implementations/python/moving-object-prediction/README.md)
is not a TPR-tree, HR-tree, trajectory database or probabilistic motion model.
It assumes constant velocity or constant acceleration over each finite query.

Reference: Saltenis, S., Jensen, C. S., Leutenegger, S. T., & Lopez, M. A.
(2000). Indexing the Positions of Continuously Moving Objects. Proceedings
of SIGMOD, 331–342. https://doi.org/10.1145/342009.335426
