# Matrix factorizations: computational companion

A compact, reproducible comparison of LU, QR, Cholesky and singular-value decomposition (SVD), using small spatial-science examples.

This companion demonstrates established library routines; it does **not** reimplement production-grade factorization algorithms.

## Requirements and run

- Python 3.10+
- NumPy 1.26+
- SciPy 1.11+

From this directory:

```bash
python -m pip install -r requirements.txt
python examples.py
python -m unittest -v
```

## Experiments

1. **LU with partial pivoting** — solve a small coordinate/parameter system and inspect the permutation and triangular factors.
2. **QR least squares** — fit a plane to synthetic elevation observations without forming the normal equations.
3. **Cholesky and GLS whitening** — factor a positive-definite observation covariance, whiten the design and observations, then solve by QR. The example makes explicit that the Cholesky factor is a computational device, not evidence that the assumed covariance model is appropriate.
4. **SVD and near-dependence** — inspect singular values and numerical rank for nearly dependent parameter directions. Rank depends on a tolerance; it is not an absolute property of floating-point data.
5. **SVD-based PCA** — decompose a centred synthetic point cloud and recover principal directions. Eigenvector/sign orientation is arbitrary.

## Method selection

| Method | Typical task | Key condition or caution |
|---|---|---|
| LU | Square linear systems | Pivoting matters; singular or ill-conditioned systems need diagnosis |
| QR | Least squares | Orthogonal transformations avoid explicitly forming normal equations |
| Cholesky | SPD covariance/normal systems | Fails for indefinite or singular matrices in ordinary form |
| SVD | Rank diagnosis, pseudoinverse, low-rank structure | More informative but generally more expensive; tolerance/truncation is a modelling choice |

Do not explicitly compute a matrix inverse merely to solve a system. Normal equations square the 2-norm condition number for full-column-rank problems. A successful factorization does not establish good conditioning, correct units, valid observations, an appropriate CRS, or a defensible stochastic model.

## Scope and reproducibility

All observations and coordinates are synthetic, dimensionless teaching values. They are not Nairobi measurements, survey control, instrument specifications or evidence of field accuracy. The examples do not implement geodetic network adjustment, robust estimation, sparse/distributed solvers, mixed precision, rank-revealing pivoted QR, or a production numerical diagnostics framework. NumPy and SciPy select their own low-level LAPACK implementations, so last-bit output can vary by platform.

The GLS illustration uses a symmetric positive-definite covariance matrix and Cholesky whitening. It is conceptually related to, but does not replace, the dependency-free implementation in [covariance-gls](../covariance-gls/README.md). PCA complements the existing [PCA transform](../pca-transform/README.md).

## Learning links

- [Matrix factorizations foundation module](../../../foundations/linear-algebra/matrix-factorizations-lu-qr-cholesky-svd.md)
- [Covariance matrices and multivariate structure](../../../foundations/linear-algebra/covariance-matrices-and-multivariate-structure.md)
- [Linear algebra sequence audit](../../../foundations/linear-algebra/sequence-audit.md)

## Integrated workflow

The [integrated synthetic spatial case](integrated-case.md) connects affine control transformation, terrain-plane fitting, covariance-aware GLS and SVD diagnostics in one reproducible workflow. It includes a separate script and tests; its assumptions and limits are documented explicitly.

The [learner exercise and worked solution](integrated-case-exercise.md) provides staged tasks, a submission checklist and a 20-point marking guide.
