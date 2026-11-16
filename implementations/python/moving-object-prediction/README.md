# Moving-object prediction baseline

Pure-Python constant-velocity prediction, uncertainty-aware predictive
rectangle queries and a displacement-error dead-reckoning update policy.

## State and units

Each object state is (x, y, vx, vy). Position and velocity must use a
consistent Cartesian coordinate system and compatible time units. Prediction
at horizon dt is (x + vx*dt, y + vy*dt).

A predictive range query tests whether a disk of caller-supplied radius around
the predicted point intersects an axis-aligned rectangle. The radius is a
simple uncertainty envelope, not a probabilistic confidence region.

The dead-reckoning policy compares the observed point with the constant-
velocity prediction and requests an update when Euclidean error exceeds the
tolerance. The comparison is strict.

## Limitations

This package is not an HR-tree, TPR-tree, MV3R-tree or trajectory database. It
does not index large populations, model acceleration or road-constrained
movement, estimate covariance, handle asynchronous clocks, or answer
continuous-time queries. Coordinates must be projected or otherwise expressed
in a meaningful Cartesian metric.

## Run

    python -m pytest -q

Only the Python standard library is required at runtime; pytest is the test
runner.
