# Verification record — moving-object prediction baseline

## Scope
This record covers finite-input constant-velocity extrapolation, deterministic
uncertainty-disk intersection against axis-aligned rectangles, strict
displacement-error dead-reckoning triggers, and continuous rectangle contact
for constant-velocity and constant-acceleration point trajectories. It does
not verify spatiotemporal index structures or probabilistic prediction.

## Mathematical and numerical checks
The constant-velocity predictor evaluates p(t)=p0+v*t. The endpoint range
query clamps the predicted point to the rectangle and compares Euclidean
distance with the supplied radius, which is the disk/rectangle intersection
condition. The update policy compares Euclidean prediction error with a
strict greater-than tolerance.

The linear continuous query uses Liang–Barsky clipping on the finite segment.
The accelerated query evaluates p(t)=p0+v0*t+0.5*a*t². Real roots of each
coordinate's rectangle-boundary equation partition the requested interval;
event points and root-free intervals are checked in chronological order.
This detects crossings with outside endpoints and isolated tangencies.
Root calculations use floating-point arithmetic and a scale-aware boundary
tolerance.

All scalar inputs and computed coordinates must be finite. Overflow is
rejected. Rectangle and disk tangency are inclusive.

## Independent tests
The package test module covers constant-velocity prediction, zero horizon,
inclusive rectangle boundaries, uncertainty-disk intersection and tangency,
mapping-order preservation, strict update thresholds, malformed states,
invalid bounds, non-finite values, arithmetic overflow, linear path crossings,
initially-inside cases, boundary contact, accelerated enter/exit paths,
isolated accelerated tangency, linear-degenerate acceleration, no-contact
paths, malformed acceleration states and overflow rejection. The package is
registered in the repository Python CI matrix.

A passing CI run is required before claiming environment-level verification.
No external trajectory dataset or reference implementation comparison is
claimed.

## Remaining scope
HR-tree, MV3R-tree, TPR-tree, SETI, PIST, STR-tree and TB-tree structures;
covariance regions and uncertainty-aware continuous queries; stochastic or
time-varying acceleration; road-network constraints; dead-reckoning policy
optimization; and empirical trajectory validation remain unimplemented.
