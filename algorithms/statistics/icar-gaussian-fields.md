# Intrinsic conditional autoregressive (ICAR) Gaussian fields

## Purpose

An intrinsic conditional autoregressive model represents a spatially structured Gaussian effect on an undirected graph. It is a common building block for areal disease mapping and hierarchical spatial models. Unlike a proper CAR model, its precision matrix is singular by construction.

## Graph and precision

Let A be a symmetric, non-negative adjacency/weight matrix with zero diagonal, and let D contain its row sums. The graph Laplacian is

\[
Q_0=D-A,\qquad Q=\tau Q_0,\quad \tau>0.
\]

For node i, the full conditional distribution is

\[
u_i\mid u_{-i}\sim
N\left(
\frac{\sum_j a_{ij}u_j}{d_i},
\frac{1}{\tau d_i}
\right),
\]

provided d_i>0. The joint quadratic form is

\[
u'Q_0u=\frac12\sum_i\sum_j a_{ij}(u_i-u_j)^2.
\]

It penalises differences across linked nodes, not the overall level of the field.

## Why the precision is singular

Every connected component contributes one constant-vector null direction. If the graph has c connected components, then Q_0 has c zero eigenvalues (assuming each component is connected in the supplied graph). Therefore the unconstrained Gaussian density is improper: the field's level is unidentified.

A common identifying constraint is a separate sum-to-zero condition for each connected component:

\[
\sum_{i\in C_k}u_i=0,\qquad k=1,\ldots,c.
\]

A single global sum-to-zero constraint is insufficient when the graph is disconnected; it leaves c-1 component-level null directions.

## Constrained spectral simulation

For each connected component, eigendecompose its Laplacian block:

\[
Q_{0,k}=V_k\Lambda_kV_k',
\]

where the constant eigenvector is excluded and Lambda contains the positive eigenvalues. A constrained draw is

\[
u_k=V_{k,+}\Lambda_{k,+}^{-1/2}z/\sqrt{\tau},
\qquad z\sim N(0,I).
\]

This gives a Gaussian draw on the component-wise sum-to-zero subspace. The simulator reports graph component labels and the log pseudo-determinant. The companion `icar_log_density` evaluates the normalized density with respect to Euclidean measure on the constrained subspace, using the precision pseudo-determinant and Laplacian quadratic energy. It rejects fields that violate any component's constraint; the density is not defined with respect to ordinary N-dimensional Lebesgue measure.

## Implemented teaching baseline

The file implementations/python/spatial-econometrics/icar.py provides icar_sample, a dense spectral simulator. It checks symmetry, non-negative weights, zero diagonal, finite values, positive node degrees and positive precision. It detects graph components and enforces one sum-to-zero constraint per component.

The accompanying tests cover a connected lattice, a disconnected graph, deterministic seeded draws, finite pseudo-determinants and invalid inputs.

## Interpretation and limits

- The conditional variance 1/(tau d_i) is not the marginal variance of u_i. Marginal variances depend on the whole constrained graph.
- The sum-to-zero constraint identifies component levels; it does not make the ICAR field equivalent to a proper CAR covariance model.
- The intrinsic field has no separately identified global intercept unless the model's constraints and fixed effects are specified consistently.
- This is a field simulator, not a fitted regression model. It does not estimate tau, perform posterior inference, or implement BYM/BYM2, Leroux CAR, INLA or SPDE methods.
- Dense eigendecomposition is intended for small teaching graphs. Large graphs require sparse methods and careful treatment of constraints and scaling.

## Relation to proper CAR

The [Gaussian proper-CAR regression](proper-car-gaussian-regression.md) uses Q=tau(D-alpha A) with alpha restricted to a positive-definite interval. ICAR is the intrinsic boundary case Q=tau(D-A), with a singular precision and explicit constraints. The two models must not be conflated.

## Further reading

- Besag, J. (1974). Spatial interaction and the statistical analysis of lattice systems. *Journal of the Royal Statistical Society: Series B*, 36(2), 192–236.
- Rue, H. and Held, L. (2005). *Gaussian Markov Random Fields: Theory and Applications*. Chapman & Hall/CRC.
