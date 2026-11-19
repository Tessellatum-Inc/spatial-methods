# Covariance and generalized least squares

A small, dependency-free Python implementation supporting the Spatial Methods measurement-science modules.

## Contents

- `covariance_gls.py` — covariance validation, session-common covariance construction, diagonal comparison and Cholesky-based generalized least squares.
- `test_covariance_gls.py` — unit tests for covariance validity, singular positive-semidefinite matrices, shared-session structure and GLS behaviour.
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

The GLS solver requires a symmetric positive-definite observation covariance matrix and a full-column-rank design matrix. It whitens the observations and design matrix using Cholesky factorisation, then solves the normal equations. It does not silently regularize singular covariance matrices, impose datum constraints, estimate variance components, apply robust estimators, or rescale formal covariance by an estimated variance factor. Singular or rank-deficient problems require an appropriate constrained or generalized-inverse formulation.

The session-common model is only one possible covariance structure. It must be supported by the acquisition and processing process; a session label alone does not establish the magnitude or existence of a shared random effect.

The example reuses synthetic observations, control values and assumptions from Exercises D and K. It is not field evidence, a survey specification or a recommendation for any particular instrument or project. The diagonal WLS output is a deliberately misspecified comparison when shared session effects are present.

## Relationship to the knowledge base

See [Covariance, correlated observations and generalized least squares](../../../foundations/measurement-science/covariance-correlated-observations-and-gls.md) and [Exercise K](../../../experiments/measurement/exercise-k-correlated-errors-and-generalized-least-squares.md).
