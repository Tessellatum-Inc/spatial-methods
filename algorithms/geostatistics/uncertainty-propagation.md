# Monte Carlo uncertainty propagation and Sobol sensitivity

Monte Carlo propagation samples uncertain inputs, evaluates a model and summarizes the resulting output distribution. This implementation uses independent uniform inputs over user-specified bounds and reports the output mean, sample standard deviation and requested quantiles.

For independent inputs, Sobol indices decompose output variance into contributions from individual inputs and their interactions. The Saltelli pick-freeze estimator evaluates two independent sample matrices and hybrid matrices in which one input column is exchanged.

\[
S_i=\frac{\mathbb{E}[f(B)(f(A_B^{(i)})-f(A))]}{\operatorname{Var}(Y)},\qquad
S_{T_i}=\frac{\mathbb{E}[(f(A)-f(A_B^{(i)}))^2]}{2\operatorname{Var}(Y)}.
\]

The first-order index captures an input's isolated contribution; the total-order index includes its interactions.

## Assumptions and limits

Inputs are independent and uniform over supplied bounds. The model must be vectorized; Sobol analysis requires scalar output. Dependent inputs, arbitrary distributions, spatially correlated errors, Latin-hypercube sampling, polynomial chaos and confidence intervals are not supported. Increase sample count and compare estimates to assess Monte Carlo convergence.

## Verification

Tests compare Monte Carlo moments with analytic uniform-input results, check reproducibility, recover known first-/total-order indices for an additive model and test interaction behaviour.

See the [implementation package](../../implementations/python/uncertainty-propagation/README.md).
