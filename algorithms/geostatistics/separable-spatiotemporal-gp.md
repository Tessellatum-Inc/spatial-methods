# Separable spatiotemporal Gaussian-process regression

For spatial locations s and s' in a common Euclidean coordinate system and times t and t', the implemented covariance is

\[
C((s,t),(s',t'))=\sigma^2
\exp(-\|s-s'\|/a_s)\exp(-|t-t'|/a_t).
\]

Spatial and temporal exponential correlations multiply. This is stationary, isotropic, separable and uses fixed user-supplied scales. Unlike a nonseparable model, temporal lag does not alter the spatial dependence shape.

For training covariance K, observation-noise variance τ² and numerical jitter ε, the system matrix is A=K+(τ²+ε)I. Cholesky solves yield posterior mean K_*' A^-1 y and covariance K_**-K_*' A^-1 K_* without explicitly forming an inverse.

Coordinates must be projected planar coordinates with common linear units; times must share one linear unit. The prior mean is zero and hyperparameters are not estimated. Dense exact inference is small-data only. INLA/SPDE, functional data analysis, anisotropy, nonstationarity, nonseparable fitting and scalable approximations are outside this implementation.
