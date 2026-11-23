# Conjugate Gaussian linear inverse problem

For a linear observation model y = A x + epsilon with Gaussian prior x ~ N(m0,C0) and independent Gaussian noise epsilon ~ N(0,R), the posterior is Gaussian. The marginal observation covariance is S = A C0 Aᵀ + R. The posterior mean is m0 + C0 Aᵀ S⁻¹(y - A m0), and the posterior covariance is C0 - C0 Aᵀ S⁻¹ A C0.

The implementation uses Cholesky factorisation and triangular solves rather than explicitly constructing S⁻¹. It also evaluates the Gaussian log marginal likelihood. This is an exact linear-Gaussian baseline, not a nonlinear or PDE-constrained inverse solver.
