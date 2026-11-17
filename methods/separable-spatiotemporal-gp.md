# Exact separable spatiotemporal Gaussian-process prediction

The separable baseline models a field as a product of spatial exponential and temporal exponential correlations. The spatial and temporal scales are distinct, but temporal lag does not alter the spatial dependence shape.

For locations s,s' and times t,t', covariance is

\[
C((s,t),(s',t'))=\sigma^2
\exp(-\|s-s'\|/a_s)\exp(-|t-t'|/a_t).
\]

Given training covariance K, cross-covariance K_* and prediction covariance K_**, Gaussian conditioning uses observation-noise variance and a separate numerical jitter on the training diagonal. Cholesky solves produce posterior mean and covariance without forming a matrix inverse.

The implementation assumes a zero prior mean and fixed covariance parameters. Coordinates must be projected Euclidean coordinates and times must share a consistent linear unit. Dense exact inference is suitable for small datasets only. This is model-based uncertainty, not a distribution-free coverage guarantee. Hyperparameter fitting, INLA/SPDE, functional data analysis, anisotropy, nonstationarity and nonseparable fitting are not implemented.
