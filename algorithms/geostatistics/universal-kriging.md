# Universal kriging

Universal kriging extends ordinary kriging by representing the unknown mean as a specified drift basis. For observation locations (s_i), values (z_i), and basis vector (f(s)),

\[
Z(s)=f(s)^T\beta+\epsilon(s),
\]

where the residual process has a stationary covariance defined by a caller-supplied variogram model. The universal-kriging system combines the observation covariance matrix with the drift design matrix and enforces unbiasedness for every basis term.

The implementation supports constant, linear and quadratic polynomial drift. It solves the dense augmented covariance system for each target and reports the conditional prediction variance. The variogram parameters are supplied explicitly.

## Limits

This is a small-data dense solver. It does not fit variograms or handle anisotropy, nonstationarity, co-kriging, external drift, regression kriging, indicator/disjunctive, block, areal or spatiotemporal variants. Prediction variance is conditional on the supplied variogram and drift model.

## Verification

Synthetic planar and quadratic surfaces test exact drift reproduction; a constant field tests ordinary-kriging behaviour at sampled points; rank-deficient geometry and invalid parameters are rejected.

See the [implementation package](../../implementations/python/universal-kriging/README.md).
