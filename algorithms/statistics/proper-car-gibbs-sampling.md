# Gibbs sampling for a proper Gaussian CAR field

Let W be symmetric nonnegative adjacency, D its diagonal degree matrix and tau a positive precision. The proper CAR prior has precision Q=tau(D-rho W), which must be positive definite. With independent observations y_i|x_i distributed Normal(x_i, v_i), each coordinate has full conditional precision tau*d_i + 1/v_i and mean [tau*d_i*mu + tau*rho*sum_j w_ij(x_j-mu) + y_i/v_i] divided by that precision. Missing observations omit the likelihood term. A systematic scan draws each coordinate conditional on the latest values of the others.

The implementation checks positive definiteness by Cholesky factorization and rejects isolated nodes. Hyperparameters are fixed, not estimated. This is a Gaussian CAR posterior sampler, not a general-purpose Bayesian inference engine; it does not implement hyperparameter updates, non-Gaussian likelihoods, SAR models, adaptive samplers or convergence diagnostics such as effective sample size and R-hat.
