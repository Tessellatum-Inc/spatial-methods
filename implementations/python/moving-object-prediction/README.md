# Moving-object prediction baseline

Pure-Python constant-velocity prediction, uncertainty-disk rectangle queries
and a displacement-error dead-reckoning update policy.

## State and units

Each object state is (x, y, vx, vy). Position and velocity must use a
consistent Cartesian coordinate system and compatible time units. Prediction
at horizon dt is (x + vx*dt). Inputs and computed predictions must remain
finite and representable as Python floats; arithmetic overflow raises
ValueError rather than returning infinite coordinates.

A predictive range query tests whether a disk of caller-supplied radius
around the predicted point intersects an axis-aligned rectangle. The radius
is a deterministic bounded-error envelope, not a probabilistic confidence
region. Rectangle and disk boundaries are inclusive.

The dead-reckoning policy compares the observed point with the constant-
velocity prediction and requests an update when Euclidean error exceeds the
tolerance. The comparison is strict.

## Limitations

This package is a linear scan, not an HR-tree, TPR-tree, MV3R-tree or
trajectory database. It does not index large populations, model acceleration
or road-constrained movement, estimate covariance, handle asynchronous
clocks, or answer continuous-time queries. Coordinates must be projected or
otherwise expressed in a meaningful Cartesian metric.

Run tests with `python -m pytest -q`. Only the standard library is required
at runtime.
