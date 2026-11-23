# Laplace approximation and slice sampling

## Laplace approximation

Given log posterior density l(theta), find its mode theta_hat and approximate the negative Hessian H=-d²l/dtheta² at the mode. The local posterior is Gaussian with covariance H^-1, and the log marginal likelihood approximation is l(theta_hat) + d/2 log(2 pi) - 1/2 log|H|. The implementation uses numerical central differences and requires a positive-definite Hessian. This is a local approximation and is unreliable for strongly multimodal or highly skewed posteriors.

## Componentwise slice sampling

For each coordinate, draw a vertical slice level below the current log density, construct a horizontal bracket by stepping out, then shrink the bracket until a point on the slice is accepted. The implementation uses a fixed width and bounded stepping-out count, with systematic coordinate updates. It does not automatically tune width or compute effective sample size, R-hat or other convergence diagnostics.
