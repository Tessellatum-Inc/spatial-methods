# Moving-object prediction baseline

Pure-Python constant-velocity prediction, deterministic uncertainty-disk
rectangle queries, continuous linear-motion queries, constant-acceleration
prediction-path queries, and a displacement-error dead-reckoning update policy.

## State and units

Constant-velocity states are (x, y, vx, vy). Accelerated continuous-query
states are (x, y, vx, vy, ax, ay), using
p(t) = p0 + v0*t + 0.5*a*t². Position, velocity, acceleration and time must
use compatible Cartesian units. Inputs and computed coordinates must remain
finite and representable as Python floats; invalid or overflowing values raise
ValueError.

The predictive range query tests whether a disk of caller-supplied radius
around the predicted point intersects an axis-aligned rectangle. The radius
is a deterministic bounded-error envelope, not a probabilistic confidence
region. Rectangle and disk boundaries are inclusive.

The constant-velocity continuous query uses Liang–Barsky segment clipping.
The accelerated continuous query solves the quadratic boundary equations,
partitions the finite time interval at their real roots, and checks both
boundary events and intervening intervals. It therefore detects a curved
path that enters and exits between horizon endpoints, including isolated
tangency. Results report first contact. Root arithmetic is floating-point;
the query is not a probabilistic uncertainty envelope.

The dead-reckoning policy compares observed position with the constant-
velocity prediction and requests an update when Euclidean error exceeds the
tolerance. The comparison is strict.

## Limitations

This package is a linear scan, not an HR-tree, TPR-tree, MV3R-tree or
trajectory database. It does not index large populations, estimate covariance,
model road-constrained movement, handle asynchronous clocks, or validate
against an external trajectory dataset. Acceleration is assumed constant
throughout each query. Coordinates must be projected or otherwise expressed
in a meaningful Cartesian metric.

Run tests with `python -m pytest -q`. Only the standard library is required
at runtime.
