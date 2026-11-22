# Positional accuracy and uncertainty propagation

**Status:** Curated method; dependency-free reference implementation; synthetic tests  
**Scope:** Coordinate RMSE, local first-order covariance propagation, independent-uniform Monte Carlo and Sobol sensitivity.

## 1. Positional accuracy

For reference coordinates \(\mathbf{x}_i\) and estimates \(\hat{\mathbf{x}}_i\),
coordinate errors are \(\mathbf{e}_i=\hat{\mathbf{x}}_i-\mathbf{x}_i\).
The per-axis bias and RMSE are

\[
b_j=\frac{1}{n}\sum_{i=1}^{n}e_{ij},
\qquad
RMSE_j=\sqrt{\frac{1}{n}\sum_{i=1}^{n}e_{ij}^{2}}.
\]

The pooled coordinate RMSE implemented here is
\[
RMSE_{pool}=\sqrt{\frac{1}{nd}\sum_{i=1}^{n}\sum_{j=1}^{d}e_{ij}^{2}},
\]
where \(d\) is the coordinate dimension. It is an average per coordinate
component, not the root mean squared Euclidean point error (which omits the
division by \(d\)). Report the definition rather than calling both quantities
simply “RMSE”.

## 2. First-order propagation with correlated inputs

For a vector-valued model \(\mathbf{y}=f(\mathbf{x})\), linearised at a
specified expansion point, let \(\mathbf{J}=\partial f/\partial\mathbf{x}\)
be its Jacobian and \(\mathbf{C}_{xx}\) the joint input covariance. Then

\[
\mathbf{C}_{yy}\approx
\mathbf{J}\mathbf{C}_{xx}\mathbf{J}^{T}.
\]

For a scalar output this reduces to
\[
u_c^2(y)\approx\mathbf{c}^{T}\mathbf{C}_{xx}\mathbf{c}.
\]
Off-diagonal covariance terms matter whenever the measurement model and
sensitivity coefficients make them matter. A common-mode error may cancel in
a relative difference while remaining in absolute coordinates.

The companion Python function `covariance_propagation` accepts a supplied
Jacobian and covariance matrix, validates dimensions, finite values,
symmetry and positive semidefiniteness, and returns the propagated covariance
and marginal standard uncertainties. Positive-semidefinite singular input
covariances are valid and are not rejected merely for being singular.

This is a local first-order approximation, not a universal uncertainty
estimator. It does not estimate the Jacobian or covariance model, infer
correlations from shared equipment, or account automatically for strong
nonlinearity, non-Gaussian distributions, uncertain model structure or
unmodelled systematic effects. The numerical result is only as defensible as
the measurands, frames, units, sensitivity coefficients and covariance model.

## 3. Monte Carlo and sensitivity

The companion Monte Carlo routine samples independent uniform input bounds
and reports scalar-output summaries. The Sobol routine estimates first-order
and total-order indices using Saltelli pick-freeze samples. Both require
independent uniform inputs; these assumptions must not be silently transferred
to correlated survey observations. A dependence-preserving joint sampler is
needed for correlated-input Monte Carlo. Standard Sobol indices also require
care when inputs are dependent.

## 4. Validation and reporting

- Distinguish internal precision, positional accuracy against independent
  reference data, and compliance with a stated acceptance specification.
- State coordinate frame, units, epoch, vertical reference and the measurand.
- Preserve the joint covariance and its physical sources, not only marginal
  standard uncertainties.
- State whether the uncertainty is a first-order approximation or a
  simulation-based result.
- Report the exact RMSE definition, sample size, bias and validation design.
- Do not treat a requirement envelope as an estimator of achieved uncertainty.

## 5. References

- JCGM, [JCGM 100:2008 — Guide to the expression of uncertainty in measurement](https://www.bipm.org/en/doi/10.59161/jcgm100-2008), Sections 5.1–5.2.
- NIST, [TN 1297 Appendix A — Law of propagation of uncertainty](https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-appendix-law-propagation-uncertainty).
- Repository foundation: [Covariance, correlated observations and generalized least squares](../../foundations/measurement-science/covariance-correlated-observations-and-gls.md).
