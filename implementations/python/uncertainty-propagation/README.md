# Uncertainty propagation and sensitivity

Dependency-free baselines for coordinate positional RMSE, first-order covariance
propagation, Monte Carlo propagation under independent uniform inputs, and
first-order/total-order Sobol sensitivity indices.

Run `python -m pip install -r requirements.txt && python -m pytest -q`.

## First-order covariance propagation

`covariance_propagation(jacobian, covariance)` evaluates

\[
\mathbf{C}_{yy}=\mathbf{J}\,\mathbf{C}_{xx}\,\mathbf{J}^{T},
\qquad
u(y_i)=\sqrt{(\mathbf{C}_{yy})_{ii}}.
\]

The Jacobian has shape (outputs, inputs); the input covariance has shape
(inputs, inputs). The routine checks finite values, dimensions, symmetry and
positive semidefiniteness. Singular positive-semidefinite matrices are allowed.
A small numerical tolerance is used for floating-point symmetry and PSD checks.

This is a first-order local approximation. The caller must supply a Jacobian
appropriate to the expansion point and a defensible joint covariance model.
The routine does not estimate the Jacobian, infer correlations, handle
nonlinear/non-Gaussian effects, or validate the physical measurement model.
For strongly nonlinear models, use an appropriate Monte Carlo method with a
joint sampler that preserves the required dependence structure.

The existing `monte_carlo_uniform` and `sobol_first_total` routines assume
independent uniform inputs. Sobol indices are not valid as a general
correlated-input decomposition. Estimates can be noisy or slightly outside
[0,1]. This package does not implement arbitrary input distributions,
correlated-input Monte Carlo sampling, second-order indices, polynomial chaos,
or survey-design variance estimators.
