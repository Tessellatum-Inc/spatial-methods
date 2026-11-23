# Matrix factorizations: LU, QR, Cholesky and singular-value decomposition

**Subject identity:** `SM-FND-002` — Linear algebra and matrix methods  
**Module:** 09  
**Status:** Initial public teaching resource; independent technical review and learner testing outstanding.

## 1. Why factorization matters

A matrix factorization rewrites a matrix as a product of structured matrices. The purpose is not merely algebraic elegance. It can make repeated solves efficient, expose rank and geometry, preserve useful structure, and avoid forming an inverse explicitly.

Spatial computation uses these ideas in many places:

- coordinate and parameter systems;
- least-squares adjustment and regression;
- covariance and generalized least squares;
- principal component analysis;
- raster and image transformations;
- network and inverse problems;
- numerical optimisation and scientific models.

The factorization should match the matrix structure and the question being asked. A method that is appropriate for a small, well-conditioned square system may be a poor choice for a large, rank-deficient least-squares problem.

## 2. Factorization is not the same as inversion

To solve

$$
A\mathbf{x}=\mathbf{b},
$$

one could write \(\mathbf{x}=A^{-1}\mathbf{b}\) when an inverse exists. In computation, explicitly forming \(A^{-1}\) is usually unnecessary and can be less accurate and more expensive than solving the system directly.

A factorization expresses \(A\) in a form that supports structured substitution or orthogonal transformations. For example, if

$$
A=LU,
$$

then solving \(A\mathbf{x}=\mathbf{b}\) becomes two triangular solves:

$$
L\mathbf{z}=\mathbf{b},
\qquad
U\mathbf{x}=\mathbf{z}.
$$

If the same matrix is used for many right-hand sides, its factorization can be reused. The factorization itself does not make an ill-conditioned problem well-conditioned; it provides a computational route to the solution.

## 3. LU factorization

For a suitable square matrix, LU factorization writes

$$
A=LU,
$$

where (L) is lower triangular and (U) is upper triangular. In practical numerical linear algebra, row pivoting is commonly used:

$$
PA=LU,
$$

where (P) is a permutation matrix recording row exchanges.

Pivoting is important because a zero or very small pivot can make unpivoted elimination fail or amplify rounding error. Partial pivoting selects a large available entry in the current column as the pivot. It is widely used, although it is not a universal guarantee against every form of numerical difficulty.

### Worked example 1 — a small LU factorization

Let

$$
A=\begin{bmatrix}2&1\\4&3\end{bmatrix}.
$$

Eliminating the entry below the first pivot uses multiplier 2. The factorization is

$$
L=\begin{bmatrix}1&0\\2&1\end{bmatrix},
\qquad
U=\begin{bmatrix}2&1\\0&1\end{bmatrix},
$$

and direct multiplication confirms (LU=A).

To solve \(A\mathbf{x}=(5,11)^T\), first solve

$$
L\mathbf{z}=\begin{bmatrix}5\\11\end{bmatrix},
$$

giving \(\mathbf{z}=(5,1)^T\). Then solve \(U\mathbf{x}=\mathbf{z}\), giving \(x_2=1\), \(x_1=2\). The solution is \((2,1)^T\).

This example is small and exact. Real computations use finite precision, pivoting, scaling and diagnostic checks as appropriate.

### When LU is useful

- Square nonsingular systems.
- Multiple right-hand sides with the same coefficient matrix.
- General-purpose direct solution where matrix structure does not suggest a more specialised factorization.

LU is not the default least-squares method for a rectangular design matrix. Forming normal equations and applying LU to them can square the condition number; QR or SVD is generally preferable for least squares.

## 4. QR factorization

QR factorization writes a matrix as

$$
A=QR,
$$

where (Q) has orthonormal columns (or is a full orthogonal matrix in a square formulation) and (R) is upper triangular or upper trapezoidal. For a matrix with full column rank and (m\geq n), the thin QR form has

$$
Q\in\mathbb{R}^{m\times n},
\quad Q^TQ=I,
\quad R\in\mathbb{R}^{n\times n}.
$$

Orthogonal transformations preserve Euclidean lengths:

$$
\|Q\mathbf{z}\|_2=\|\mathbf{z}\|_2.
$$

This is why QR is central to stable least-squares computation.

### Least squares using QR

For an overdetermined model

$$
A\mathbf{x}\approx\mathbf{y},
$$

least squares minimises \(\|A\mathbf{x}-\mathbf{y}\|_2\). If \(A=QR\) with full column rank, then

$$
\|A\mathbf{x}-\mathbf{y}\|_2
=\|Q^T\mathbf{y}-R\mathbf{x}\|_2
$$

up to the orthogonal residual component. The minimiser is obtained by solving

$$
R\mathbf{x}=Q^T\mathbf{y}.
$$

The residual component perpendicular to the column space does not affect the parameter solution.

Householder reflections are a common way to compute QR robustly. Modified Gram–Schmidt can be useful in some settings but may lose orthogonality in finite precision; classical Gram–Schmidt is especially vulnerable without reorthogonalisation. The detailed numerical comparison belongs to numerical analysis.

### Worked example 2 — fit a line with QR-equivalent least squares

Fit \(y=a+bt\) to the three synthetic observations

| (t) | (y) |
|---:|---:|
| 0 | 1 |
| 1 | 2 |
| 2 | 2 |

The design matrix and observation vector are

$$
A=\begin{bmatrix}1&0\\1&1\\1&2\end{bmatrix},
\qquad
\mathbf{y}=\begin{bmatrix}1\\2\\2\end{bmatrix}.
$$

The least-squares line is

$$
\hat y=\frac76+\frac12t.
$$

The fitted values are \((7/6,5/3,13/6)^T\), and the residuals \(\mathbf{r}=\mathbf{y}-A\hat{\mathbf{x}}\) are

$$
\mathbf{r}=\begin{bmatrix}-1/6\\1/3\\-1/6\end{bmatrix}.
$$

They sum to zero and have zero dot product with the centred time column, so the residual is orthogonal to the two columns of the design matrix. QR obtains this solution without explicitly forming \(A^TA\).

The observations are invented teaching values; this is not a trend claim about a real spatial process.

## 5. Cholesky factorization

For a real symmetric positive-definite matrix (S), Cholesky factorization writes

$$
S=LL^T,
$$

where (L) is lower triangular with positive diagonal entries. Equivalently, one may use an upper-triangular factor (R) such that (S=R^TR).

Cholesky exploits symmetry and positive definiteness. It is generally more economical than a general LU factorization for this matrix class.

### Worked example 3 — Cholesky factor

Let

$$
S=\begin{bmatrix}4&2\\2&3\end{bmatrix}.
$$

A Cholesky factor is

$$
L=\begin{bmatrix}2&0\\1&\sqrt2\end{bmatrix},
$$

because multiplication gives (LL^T=S).

To solve \(S\mathbf{x}=\mathbf{b}\), solve \(L\mathbf{z}=\mathbf{b}\) and then \(L^T\mathbf{x}=\mathbf{z}\).

### Connection to GLS

If an observation covariance matrix \(\Sigma\) is symmetric positive definite, Cholesky gives \(\Sigma=LL^T\). GLS minimises

$$
(\mathbf{y}-A\mathbf{x})^T\Sigma^{-1}(\mathbf{y}-A\mathbf{x}).
$$

Rather than explicitly computing \(\Sigma^{-1}\), one can whiten the observations and design by triangular solves involving (L), then solve the resulting least-squares problem. The repository's covariance-GLS implementation follows a Cholesky-based route and documents its SPD requirement.

A positive-semidefinite singular covariance matrix does not have an ordinary Cholesky factor with strictly positive diagonal entries. A failed Cholesky factorization may indicate non-positive-definiteness, singularity, poor scaling or numerical tolerance issues. It is not permission to add arbitrary diagonal noise.

## 6. Singular-value decomposition (SVD)

Every real matrix (A\in\mathbb{R}^{m\times n}) has a singular-value decomposition

$$
A=U\Sigma V^T,
$$

where (U) and (V) are orthogonal (or have orthonormal columns in a thin form), and \(\Sigma\) contains nonnegative singular values on its diagonal.

The singular values are ordered by convention:

$$
\sigma_1\geq\sigma_2\geq\cdots\geq0.
$$

The right singular vectors (columns of (V)) describe parameter-space directions; the left singular vectors (columns of (U)) describe corresponding directions in the output space. A singular value tells how strongly the transformation scales its associated direction.

The number of nonzero singular values is the exact algebraic rank. In floating-point computation, rank is numerical: values below a chosen tolerance are treated as negligible. The tolerance should be considered relative to matrix scale, dimensions, noise and the modelling question.

### Worked example 4 — a rank-deficient design

Let

$$
A=\begin{bmatrix}1&1\\2&2\\3&3\end{bmatrix}.
$$

The columns are identical, so the rank is one, not two. The parameter direction \((1,-1)^T\) is in the null space because

$$
A\begin{bmatrix}1\\-1\end{bmatrix}=\mathbf{0}.
$$

No observation can distinguish an increase in the first parameter from an equal decrease in the second. The model identifies only their sum.

SVD exposes this weak or unobservable direction through a zero singular value. If a singular value is merely very small rather than exactly zero, the parameters may be technically identifiable but highly sensitive to small data or rounding changes.

## 7. Pseudoinverse and minimum-norm solutions

The Moore–Penrose pseudoinverse is defined using the SVD. If

$$
A=U\Sigma V^T,
$$

then, for nonzero singular values,

$$
A^+=V\Sigma^+U^T,
$$

where \(\Sigma^+\) reciprocates retained nonzero singular values and transposes the rectangular diagonal structure.

The vector

$$
\hat{\mathbf{x}}=A^+\mathbf{y}
$$

is a least-squares solution with minimum Euclidean norm among all least-squares solutions. This is a mathematically precise selection rule, not a physical justification for preferring small parameter values.

For rank-deficient systems, many parameter vectors may produce the same fitted observations. The pseudoinverse selects one representative. If parameters have physical meaning, the minimum-norm convention must be justified or replaced by meaningful constraints, prior information or a different model.

Truncating small singular values is sometimes used for regularisation. It changes the effective model and trades variance against bias. A threshold is a modelling decision, not a neutral software default.

## 8. Choosing among the factorizations

| Problem structure | Common approach | Main reason |
|---|---|---|
| General square nonsingular system | Pivoted LU | Direct triangular solves |
| Full-column-rank overdetermined least squares | Householder QR | Avoids normal-equation conditioning penalty |
| Symmetric positive-definite system | Cholesky | Exploits symmetry and positive definiteness |
| Rank diagnosis or rank-deficient least squares | SVD | Reveals weak/null directions and supports minimum-norm solution |
| PCA of symmetric covariance matrix | Symmetric eigensolver or SVD of centred data | Computes principal directions |
| GLS with SPD observation covariance | Cholesky whitening plus least squares | Uses covariance structure without explicitly inverting it |

This is a guide, not a universal solver-selection algorithm. Sparse structure, matrix size, conditioning, accuracy requirements, constraints, hardware and available libraries also matter.

## 9. Spatial application — measurement network and datum defect

Consider a relative-height network with unknown heights \(h_A,h_B\) and one observed height difference:

$$
-h_A+h_B=2.
$$

Its design matrix has one row, \(A=[-1\;1]\), and rank one. There are two unknowns, so one parameter direction is unobservable: adding the same constant to both heights does not change the observed difference.

A factorization such as SVD can reveal this rank defect and null direction. It cannot decide what the heights should be relative to an external vertical datum.

A justified exact datum constraint, such as fixing one point or imposing a clearly declared inner constraint, changes the mathematical problem. An external control observation with uncertainty instead belongs in a stochastic observation model. These are different modelling choices; a factorization does not choose between them.

## 10. Numerical and modelling cautions

- **Do not form an inverse just to solve a system.** Use factorization and solves.
- **Do not assume normal equations are harmless.** Their condition number is approximately the square of the design matrix condition number in the full-rank 2-norm setting.
- **Do not use unpivoted LU indiscriminately.** Pivoting and scaling may be essential.
- **Do not assume Cholesky works for every symmetric matrix.** It requires positive definiteness in its ordinary form.
- **Do not treat a tiny singular value as a universal rank threshold.** Scale, units, noise and purpose matter.
- **Do not confuse numerical rank with scientific identifiability.** The model and measurement design determine what can be learned.
- **Do not treat the pseudoinverse as a substitute for modelling.** Minimum norm is a mathematical convention.
- **Do not assume a successful factorization validates the data.** It does not establish correct CRS, units, observation independence, covariance structure or field quality.

Detailed backward error, condition estimation, iterative refinement, sparse factorization, preconditioning, rank-revealing pivoted QR and solver benchmarking belong to numerical analysis and scientific computing.

## 11. Exercises

### Exercise 1 — triangular solves

Why does (A=LU) make a square linear system easier to solve?

**Worked guidance:** It replaces one general system with two triangular systems, which can be solved efficiently by forward and backward substitution.

### Exercise 2 — pivoting

What problem does row pivoting address during Gaussian elimination?

**Worked guidance:** It avoids zero pivots and reduces the risk of large multipliers from very small pivots. It improves practical robustness but is not a universal guarantee of good conditioning.

### Exercise 3 — QR dimensions

For a full-column-rank matrix with 8 rows and 3 columns, what are the dimensions of thin (Q) and (R)?

**Worked guidance:** (Q) is (8\times3), with orthonormal columns; (R) is (3\times3) upper triangular.

### Exercise 4 — least-squares orthogonality

What property of the residual makes QR useful for least squares?

**Worked guidance:** At the least-squares solution, the residual is orthogonal to the column space of (A). Orthogonal transformations preserve Euclidean lengths and expose the triangular parameter system.

### Exercise 5 — Cholesky eligibility

Can ordinary Cholesky factorization be applied to a symmetric positive-semidefinite matrix with a zero eigenvalue?

**Worked guidance:** Not in its ordinary positive-diagonal form. The matrix is singular; a pivoted, eigenvalue-based or other specialised method may be appropriate.

### Exercise 6 — GLS whitening

If (Sigma=LL^T), what operation avoids explicitly calculating (Sigma^{-1}) in GLS?

**Worked guidance:** Use triangular solves with (L) to whiten the observation vector and design matrix, then solve the resulting least-squares problem.

### Exercise 7 — rank from singular values

A matrix has singular values 8, 2 and 0. What is its exact algebraic rank?

**Worked guidance:** Two. In numerical data, rank would be assessed using a scale-aware tolerance rather than exact equality to zero.

### Exercise 8 — interpret a null direction

For (A=[-1\;1]), explain why ((1,1)^T) is a null vector.

**Worked guidance:** The product is zero. A common translation of both heights leaves their difference unchanged, so the observation cannot determine absolute datum.

### Exercise 9 — pseudoinverse meaning

Does the minimum-norm pseudoinverse solution prove that the smallest parameter values are physically correct?

**Worked guidance:** No. It selects the solution with smallest Euclidean norm under the chosen parameter scaling. That convention needs scientific justification.

### Exercise 10 — choose a factorization

Which factorization is a common choice for a full-column-rank overdetermined least-squares problem, and why?

**Worked guidance:** Householder QR is a common choice because orthogonal transformations preserve lengths and avoid explicitly forming the normal equations.

## 12. Connections and next steps

- **Module 06 — Least squares and constrained systems:** provides the estimation problem solved using QR and related methods.
- **Module 07 — Symmetric matrices, quadratic forms and definiteness:** establishes the SPD structure needed for Cholesky.
- **Module 08 — Eigenvalues, eigenvectors and spectral structure:** connects to SVD, PCA and rank.
- **Module 10 — [Covariance matrices and multivariate structure](covariance-matrices-and-multivariate-structure.md):** develops covariance, correlation, propagation and multivariate models.
- [Covariance and generalized least squares implementation](../../implementations/python/covariance-gls/README.md) documents Cholesky-based covariance handling and solver assumptions.
- [PCA method](../../algorithms/statistics/pca.md) and [PCA implementation](../../implementations/python/pca-transform/README.md) connect spectral methods to multiband spatial data.
- [Measurement science and survey adjustment learning path](../../learning-paths/measurement-science-and-survey-adjustment.md) connects rank, datum and estimation to synthetic network exercises.

## References

- Massachusetts Institute of Technology, Department of Mathematics. [18.06 Linear Algebra — OpenCourseWare, Spring 2010](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/). Course scope includes LU, QR, least squares, positive definite matrices, eigenvalues and singular-value decomposition.
- Strang, G. (2021). [Lecture Notes for Linear Algebra](https://www-math.mit.edu/~gs/LectureNotes/). MIT-hosted notes on matrix factorizations and numerical linear algebra.

**Source note:** These references are linked for human study. The MIT course identity and topic coverage are recorded in the repository source register; individual lectures and notes have not been reviewed claim by claim. This module uses original explanations and synthetic numerical examples rather than reproducing course text, figures or exercises.

**Scope:** LU with pivoting, QR, Cholesky, SVD, pseudoinverse, numerical rank and selected spatial applications. Detailed numerical stability analysis, sparse methods, preconditioning, iterative solvers, factorization complexity and solver benchmarking are deferred to numerical analysis and scientific computing.
