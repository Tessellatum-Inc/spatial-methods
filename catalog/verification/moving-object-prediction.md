# Verification record — moving-object prediction baseline

## Scope
This record covers finite-input constant-velocity extrapolation, deterministic
uncertainty-disk intersection against axis-aligned rectangles, and a strict
displacement-error dead-reckoning trigger. It does not verify spatiotemporal
index structures or probabilistic trajectory prediction.

## Mathematical and numerical checks
The predictor evaluates p(t)=p0+v*t in a Cartesian coordinate system with
compatible distance and time units. The range query clamps the predicted
point to the rectangle to obtain its nearest point, then compares Euclidean
distance with the supplied radius. This is the exact disk/rectangle
intersection condition. The update policy compares Euclidean prediction error
with a strict greater-than tolerance.

All scalar inputs and computed coordinates must be finite. Overflow is
rejected. Rectangle and disk tangency are included because the intersection
test uses distance less than or equal to radius.

## Tests
The independent package test module covers constant velocity, zero horizon,
inclusive rectangle boundaries, uncertainty-disk intersection and tangency,
mapping-order preservation, strict update thresholds, malformed states,
invalid bounds, non-finite values, arithmetic overflow, continuous path\ncrossings, initially-inside cases, boundary contact and invalid continuous-query states. The package is
registered in the repository Python CI matrix.

A passing CI run is required before claiming environment-level verification.
No external trajectory dataset or reference implementation comparison is
claimed.

## Remaining scope
HR-tree, MV3R-tree, TPR-tree, SETI, PIST, STR-tree and TB-tree structures;
curved paths and uncertainty-aware continuous queries; acceleration and covariance models; road-network
constraints; dead-reckoning policy optimization; and empirical trajectory
validation remain unimplemented.
