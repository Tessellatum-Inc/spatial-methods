# Covariance and generalized least squares

A small, dependency-free Python implementation supporting the Spatial Methods measurement-science modules.

## Contents

- `covariance_gls.py` — covariance validation, session-common covariance construction, diagonal comparison and Cholesky-based unconstrained GLS.
- `constrained_gls.py` — exact-constraint GLS using a Lagrange-multiplier KKT system; supports rank-deficient design matrices when constraints remove all datum defects.
- `test_covariance_gls.py` — tests for covariance validity, shared-session structure and unconstrained GLS.
- `test_constrained_gls.py` — tests for inner constraints, non-zero exact constraints, unresolved datum defects and singular observation covariance.
- `example_exercise_k.py` — applies the reusable solver to the repository's synthetic Exercise D network used in Exercise K.

## Run

From this directory:

```bash
python -m unittest -v
python example_exercise_k.py
```

No third-party packages are required.

## Numerical and statistical scope

The covariance validator checks symmetry and positive semidefiniteness using a Jacobi eigenvalue iteration. Its tolerance is absolute relative to a scale floor of one; users working with very large or very small units should inspect scaling and choose tolerances appropriate to their problem.

The unconstrained GLS solver requires a symmetric positive-definite observation covariance matrix and a full-column-rank design matrix. It whitens observations and design using Cholesky factorisation. The constrained solver also requires positive-definite observation covariance, but permits a rank-deficient design when the exact constraints remove every datum defect and the resulting KKT system is nonsingular. It returns the constrained parameter covariance as the upper-left block of the inverse KKT matrix for fixed Q and exact constraints.

These routines do not silently regularize singular observation covariance matrices. A singular covariance model is a separate problem requiring a justified generalized-inverse or null-space formulation; datum constraints alone do not solve it. Neither solver estimates variance components, applies robust estimators, or rescales formal covariance by an estimated variance factor.

The session-common model is only one possible covariance structure. It must be supported by the acquisition and processing process; a session label alone does not establish the magnitude or existence of a shared random effect.

Exercise E demonstrates one vertical-translation datum defect and a sum-to-zero inner constraint. It is a synthetic educational example, not a universal treatment for horizontal or three-dimensional geodetic networks. The example's control value and uncertainty are invented and are not Kenyan benchmark data. Exercise K likewise uses synthetic observations and assumptions, not field evidence or an instrument specification.

## Relationship to the knowledge base

See [Covariance, correlated observations and generalized least squares](../../../foundations/measurement-science/covariance-correlated-observations-and-gls.md), [Exercise E](../../../experiments/measurement/exercise-e-minimally-constrained-vertical-network.md), and [Exercise K](../../../experiments/measurement/exercise-k-correlated-errors-and-generalized-least-squares.md).
