# Numerical analysis and scientific computing

**Subject identity:** `SM-FND-016` — Numerical analysis and scientific computing.

Numerical analysis studies how mathematical problems are represented and solved with finite-precision computation. It asks whether a problem is sensitive to small changes in its inputs, whether an algorithm controls the errors it introduces, whether an iterative method converges, and whether a computed result is accurate enough for its intended use.

Spatial methods rely on numerical computation at almost every stage: coordinate transformations, geodetic calculations, least-squares adjustment, raster resampling, geometric predicates, interpolation, terrain derivatives, optimisation and statistical estimation. A formula can be mathematically correct while a particular numerical implementation is inaccurate, unstable or inappropriate.

This collection explains the numerical principles. It does not replace the mathematical foundations of the problem, domain-specific measurement theory, or the documentation of a particular solver.

## Scope and boundaries

The domain will cover:

- finite-precision number systems and floating-point arithmetic;
- representation, rounding, cancellation, overflow, underflow and exceptional values;
- absolute, relative, forward and backward error;
- conditioning of mathematical problems;
- stability of numerical algorithms;
- error propagation and sensitivity;
- root finding and nonlinear equation solving;
- direct and iterative methods for linear systems;
- numerical differentiation and integration;
- interpolation, approximation and discretisation error;
- convergence, stopping criteria and tolerance selection;
- reproducibility, numerical testing and reporting.

**Boundaries:** Linear algebra explains vector spaces, matrix structure and exact algebraic relationships. This domain explains the finite-precision consequences of computing with them. Measurement science explains uncertainty in observations and measurands; floating-point error is a computational effect and must not be silently added to, or confused with, observational uncertainty. Domain foundations explain what the computed quantities mean physically.

## Learning modules

| Module | Topic | Spatial connections | Status |
|---|---|---|---|
| 01 | [Floating-point numbers, rounding and computational error](floating-point-numbers-rounding-and-computational-error.md) | Coordinate arithmetic, distance calculations, raster values, geodetic computation and reproducibility | Initial public teaching resource |
| 02 | [Sensitivity and perturbation analysis](sensitivity-and-perturbation-analysis.md) | Coordinate differences, distance sensitivity, affine transformations and error propagation | Initial public teaching resource |
| 03 | [Numerical stability and backward error](numerical-stability-and-backward-error.md) | Residuals, stable summation, least-squares factorisation and robust geometric predicates | Initial public teaching resource |
| 04 | [Convergence, iterative methods and stopping criteria](convergence-iterative-methods-and-stopping-criteria.md) | Sparse raster models, iterative estimation, solver diagnostics and tolerance selection | Initial public teaching resource |
| 05 | [Root finding and nonlinear equation solving](root-finding-and-nonlinear-equation-solving.md) | Threshold crossings, implicit spatial models, root conditioning and safeguarded solvers | Initial public teaching resource |
| 06 | [Numerical differentiation](numerical-differentiation.md) | Terrain gradients, raster derivatives, local sensitivity and sampled spatial fields | Initial public teaching resource |
| 07 | [Numerical integration and quadrature](numerical-integration-and-quadrature.md) | Spatial totals, terrain and water volumes, raster aggregation, area measures and numerical quadrature | Initial public teaching resource |
| 08 | [Interpolation and approximation](interpolation-and-approximation.md) | Surface construction, raster resampling, spatial prediction, model validation and support | Initial public teaching resource |

The first eight modules establish a working numerical core, not a complete numerical-analysis curriculum. Further modules should be added when their prerequisites, examples and validation requirements are clear.

## Application anchors

- [Coordinate transformation and CRS axis order](../../algorithms/geodesy/crs-transformation.md)
- [Ellipsoidal geodesic operations](../../algorithms/geodesy/ellipsoidal-geodesic-operations.md)
- [Precision models and snap rounding](../../algorithms/geometry/precision-models.md)
- [Least squares and constrained systems](../linear-algebra/least-squares-and-constrained-systems.md)
- [Survey-to-spatial-dataset recipe](../../recipes/survey-to-spatial-dataset/README.md)
- [Application dependency audit](../application-dependency-audit.md)

These are application anchors for numerical reasoning, not claims that each linked implementation has been independently certified.

## Development and review standard

Each module should define its numerical model and notation, distinguish mathematical and computational error, include reproducible examples, explain assumptions and failure modes, and connect the theory to real spatial computations. Numerical examples should state precision, units, tolerances and relevant software or library versions. Tests should include boundary cases and should avoid treating agreement between two implementations as independent proof of correctness.

## Sequence audit

The [numerical-analysis sequence audit](sequence-audit.md) records the module dependencies, shared error vocabulary, repository checks, technical-review priorities and remaining scope gaps. It is a desk audit, not independent technical certification.

## Review status

Modules 01–08 are initial teaching resources. They have not received independent numerical-analysis review or learner testing. The subject collection is not complete, and publication does not constitute technical certification.
