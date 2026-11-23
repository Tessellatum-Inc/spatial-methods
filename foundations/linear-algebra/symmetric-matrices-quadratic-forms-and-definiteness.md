# Symmetric matrices, quadratic forms and definiteness

**Subject identity:** `SM-FND-002` — Linear algebra and matrix methods  
**Module:** 07  
**Status:** Initial public teaching resource; independent technical review and learner testing outstanding.

## 1. Why this structure matters

Symmetric matrices appear throughout spatial science. Covariance matrices describe variances and covariances; least-squares objectives are quadratic forms; local curvature and optimisation are described by Hessian matrices; and many energy, distance and similarity measures use symmetric matrix structure.

This module explains what symmetry means, how a matrix defines a quadratic form, and how positive, negative and indefinite forms behave. It connects these ideas to uncertainty, estimation and spatial geometry without treating every symmetric matrix as a covariance matrix.

## 2. Symmetric matrices

A real square matrix (M) is symmetric when

$$
M^T=M,
$$

which means (M_{ij}=M_{ji}) for every pair of indices.

For example,

$$
M=\begin{bmatrix}4&1\\1&2\end{bmatrix}
$$

is symmetric. By contrast,

$$
N=\begin{bmatrix}4&1\\2&2\end{bmatrix}
$$

is not.

Symmetry is a structural property, not a statement that the matrix is positive, invertible, a covariance matrix or physically meaningful. A symmetric matrix may be positive definite, positive semidefinite, negative definite, indefinite or singular.

For real symmetric matrices, eigenvalues are real and the matrix admits an orthonormal eigenbasis. This spectral structure is developed further in [Module 08 — Eigenvalues, eigenvectors and spectral structure](eigenvalues-eigenvectors-and-spectral-structure.md).

## 3. Quadratic forms

Given a real symmetric matrix (M), a quadratic form is the scalar

$$
q(\mathbf{x})=\mathbf{x}^TM\mathbf{x}.
$$

For a two-dimensional vector,

$$
\mathbf{x}=\begin{bmatrix}x_1\\x_2\end{bmatrix},
\qquad
M=\begin{bmatrix}a&b\\b&c\end{bmatrix},
$$

the quadratic form is

$$
q(\mathbf{x})=ax_1^2+2bx_1x_2+cx_2^2.
$$

The cross-term coefficient is twice the off-diagonal matrix entry. This is a common source of factor-of-two mistakes.

A quadratic form assigns a scalar to each vector. Depending on (M), it may represent squared length, a variance, an objective function, energy, curvature or another model-specific quantity. Its interpretation comes from the problem, not from the algebra alone.

### Worked example 1 — evaluate a quadratic form

Let

$$
M=\begin{bmatrix}4&1\\1&2\end{bmatrix},
\qquad
\mathbf{x}=\begin{bmatrix}2\\-1\end{bmatrix}.
$$

Then

$$
M\mathbf{x}=\begin{bmatrix}7\\0\end{bmatrix},
\qquad
q(\mathbf{x})=\mathbf{x}^TM\mathbf{x}=14.
$$

The result is a scalar. It is not automatically a squared distance or a variance; that depends on how (M) was defined.

## 4. Positive and negative definiteness

The sign of a quadratic form over nonzero vectors classifies its definiteness.

- **Positive definite (PD):** (\mathbf{x}^TM\mathbf{x}>0) for every nonzero (\mathbf{x}).
- **Positive semidefinite (PSD):** (\mathbf{x}^TM\mathbf{x}\geq0) for every (\mathbf{x}).
- **Negative definite:** (\mathbf{x}^TM\mathbf{x}<0) for every nonzero (\mathbf{x}).
- **Negative semidefinite:** (\mathbf{x}^TM\mathbf{x}\leq0) for every (\mathbf{x}).
- **Indefinite:** the form takes both positive and negative values.

The zero vector always gives zero. For a semidefinite matrix, nonzero vectors may also give zero; these directions form its null space.

For a real symmetric matrix, definiteness is equivalent to the signs of its eigenvalues:

| Type | Eigenvalue condition |
|---|---|
| Positive definite | All eigenvalues strictly positive |
| Positive semidefinite | All eigenvalues nonnegative |
| Negative definite | All eigenvalues strictly negative |
| Negative semidefinite | All eigenvalues nonpositive |
| Indefinite | At least one positive and one negative eigenvalue |

This equivalence depends on symmetry (or, more generally, on the symmetric part of a real quadratic form). Do not apply the symmetric-matrix eigenvalue test blindly to a nonsymmetric matrix.

### Worked example 2 — three different behaviours

Consider:

$$
M_1=\begin{bmatrix}2&0\\0&3\end{bmatrix},
\quad
M_2=\begin{bmatrix}1&0\\0&0\end{bmatrix},
\quad
M_3=\begin{bmatrix}1&0\\0&-1\end{bmatrix}.
$$

Their quadratic forms are:

$$
q_1=x_1^2\,2+3x_2^2,
\qquad
q_2=x_1^2,
\qquad
q_3=x_1^2-x_2^2.
$$

- (M_1) is positive definite: every nonzero vector gives a positive value.
- (M_2) is positive semidefinite but not positive definite: vectors on the (x_2)-axis give zero.
- (M_3) is indefinite: ((1,0)^T) gives (+1), while ((0,1)^T) gives (-1).

## 5. How to test definiteness

For a real symmetric matrix, several equivalent tests are useful.

### Eigenvalue test

Inspect the eigenvalues. All strictly positive means positive definite; all nonnegative means positive semidefinite. Numerical computation requires tolerances: an eigenvalue close to zero should not be casually classified from a rounded display.

### Principal-minor test for positive definiteness

Sylvester's criterion states that a real symmetric matrix is positive definite if and only if all its leading principal minors are positive.

For a symmetric two-by-two matrix,

$$
M=\begin{bmatrix}a&b\\b&c\end{bmatrix},
$$

positive definiteness is equivalent to

$$
a>0,
\qquad
ac-b^2>0.
$$

For positive semidefiniteness, all principal minors (not merely the leading ones) must be nonnegative. In larger dimensions, checking principal minors directly is often inconvenient and numerically fragile; eigenvalue or factorization-based methods are more practical.

### Cholesky factorisation

A real symmetric positive-definite matrix admits a Cholesky factorisation

$$
M=LL^T,
$$

where (L) is lower triangular with positive diagonal entries.

Then

$$
\mathbf{x}^TM\mathbf{x}
=\mathbf{x}^TLL^T\mathbf{x}
=\|L^T\mathbf{x}\|^2>0
$$

for every nonzero vector. Cholesky therefore provides both a computational factorisation and a structural test for positive definiteness, subject to numerical tolerances and implementation details.

A PSD matrix may be singular and does not in general admit an ordinary Cholesky factor with strictly positive diagonal entries. Pivoted or eigenvalue-based methods may be needed.

## 6. Covariance matrices

A covariance matrix for a random vector \(\mathbf{X}\) is

$$
\Sigma=\operatorname{Cov}(\mathbf{X})
=E\left[(\mathbf{X}-E\mathbf{X})(\mathbf{X}-E\mathbf{X})^T\right].
$$

It is symmetric because covariance is symmetric:

$$
\operatorname{Cov}(X_i,X_j)
=\operatorname{Cov}(X_j,X_i).
$$

It is positive semidefinite because, for every fixed vector \(\mathbf{a}\),

$$
\mathbf{a}^T\Sigma\mathbf{a}
=\operatorname{Var}(\mathbf{a}^T\mathbf{X})\geq0.
$$

This is a fundamental result: the quadratic form gives the variance of a linear combination of random variables.

The diagonal entries are variances; off-diagonal entries are covariances. Correlation coefficients are dimensionless standardised covariances, not interchangeable with covariance values.

### Worked example 3 — variance of a linear combination

Suppose two coordinate errors have covariance matrix

$$
\Sigma=\begin{bmatrix}4&1.5\\1.5&9\end{bmatrix}
$$

in squared coordinate units. For the linear combination \(Z=X_1+X_2\), let \(\mathbf{a}=(1,1)^T\). Then

$$
\operatorname{Var}(Z)
=\mathbf{a}^T\Sigma\mathbf{a}
=4+1.5+1.5+9=16.
$$

The standard deviation is 4 coordinate units. If the covariance had been incorrectly set to zero, the variance would have been 13, underestimating the variance of this particular sum. For a difference, the same positive covariance would reduce the variance instead:

$$
\operatorname{Var}(X_1-X_2)=4-1.5-1.5+9=10.
$$

The effect of correlation depends on the linear combination being considered.

A covariance matrix can be PSD but singular. For example, if one variable is an exact linear combination of others, some nonzero combination has zero variance. This is mathematically valid, although it can make inverse-covariance calculations impossible without a specialised formulation.

## 7. Quadratic forms in least squares

The weighted least-squares objective is

$$
\Phi(\mathbf{x})
=(\mathbf{y}-A\mathbf{x})^TW(\mathbf{y}-A\mathbf{x}).
$$

If (W) is symmetric positive definite, this objective is nonnegative and measures a weighted squared residual magnitude. Its Hessian with respect to the parameters is

$$
\nabla^2\Phi(\mathbf{x})=2A^TWA.
$$

The matrix (A^TWA) is PSD. It is positive definite if (A) has full column rank (assuming (W) is PD). If it is singular, some parameter directions are not distinguished by the observations.

For GLS, (W=\Sigma^{-1}) when the observation covariance \(\Sigma\) is positive definite. If the covariance is only semidefinite, the ordinary inverse does not exist; a different model and solution method are required.

The quadratic form therefore links:
- the residual metric chosen for estimation;
- the rank and identifiability of the design;
- the curvature of the objective;
- the existence and uniqueness of an unconstrained minimiser.

## 8. Spatial interpretation — uncertainty ellipses

For a two-dimensional coordinate error vector with zero mean and positive-definite covariance

$$
\Sigma=\begin{bmatrix}\sigma_x^2&\sigma_{xy}\\\sigma_{xy}&\sigma_y^2\end{bmatrix},
$$

the squared Mahalanobis distance is

$$
d^2=\mathbf{e}^T\Sigma^{-1}\mathbf{e}.
$$

Contours of constant (d^2) are ellipses. Their orientation and axis lengths are determined by the eigenvectors and eigenvalues of the covariance matrix: eigenvectors give principal directions, and eigenvalues give variances along those directions.

This is a statistical description under the assumed coordinate-error model. It is not automatically a 95% confidence ellipse; the probability content depends on the distribution, dimensionality, confidence convention and whether covariance parameters are known or estimated.

Coordinate units and reference frame matter. A covariance matrix in metres squared cannot be combined uncritically with one in degrees squared or with coordinates expressed in a different frame.

## 9. Quadratic forms and optimisation

For a quadratic objective

$$
f(\mathbf{x})=\frac12\mathbf{x}^TH\mathbf{x}
+\mathbf{g}^T\mathbf{x}+c,
$$

where (H) is symmetric, the gradient and Hessian are

$$
\nabla f=H\mathbf{x}+\mathbf{g},
\qquad
\nabla^2 f=H.
$$

- If (H) is positive definite, the function is strictly convex and has a unique global minimiser.
- If (H) is positive semidefinite, the function is convex, but a minimiser may not be unique or may not exist without further conditions.
- If (H) is indefinite, a stationary point may be a saddle point rather than a minimum.
- If (H) is negative definite, the function is strictly concave and has a unique global maximum, not a minimum.

This classification is local and global for an unconstrained quadratic function because its Hessian is constant. Constrained optimisation adds further conditions.

In spatial applications, quadratic objectives appear in parameter estimation, smoothing, interpolation, energy-based models and some network optimisation formulations. The matrix's physical meaning and units must be established for each application.

## 10. Common mistakes and limits

- **Assuming symmetric means positive definite:** symmetry alone says nothing about the sign of the quadratic form.
- **Confusing PSD with PD:** PSD matrices may be singular; their nonzero null directions matter.
- **Treating every symmetric matrix as a covariance:** a covariance matrix must be PSD and its entries must have valid variance/covariance meaning and units.
- **Ignoring covariance off-diagonal terms:** they affect the variance of linear combinations and the GLS objective.
- **Using covariance where inverse covariance is required:** distinguish the covariance matrix from the weight/precision matrix.
- **Calling a Mahalanobis contour a confidence region without assumptions:** distribution and probability calibration matter.
- **Testing a nonsymmetric matrix as if it were symmetric:** first establish the relevant structure.
- **Ignoring numerical scale and tolerance:** near-zero eigenvalues and near-singular matrices require careful numerical treatment.
- **Assuming a positive-semidefinite covariance can always be inverted:** singular covariance requires a specialised approach.

This module introduces real symmetric matrices and quadratic forms. Complex Hermitian matrices, indefinite inner-product spaces, advanced matrix inequalities, semidefinite programming and numerical eigenvalue algorithms are outside its scope.

## 11. Exercises

### Exercise 1 — identify symmetry

Is \(M=\begin{bmatrix}3&-2\\-2&5\end{bmatrix}\) symmetric?

**Worked guidance:** Yes. The off-diagonal entries match, so \(M^T=M\).

### Exercise 2 — expand a quadratic form

Expand \(\mathbf{x}^TM\mathbf{x}\) for \(M=\begin{bmatrix}a&b\\b&c\end{bmatrix}\).

**Worked guidance:** The result is \(ax_1^2+2bx_1x_2+cx_2^2\). Both off-diagonal contributions appear.

### Exercise 3 — classify a diagonal matrix

Classify \(M=\operatorname{diag}(5,2,0)\).

**Worked guidance:** It is positive semidefinite but not positive definite. The third coordinate direction is in its null space.

### Exercise 4 — test a two-by-two matrix

Is \(M=\begin{bmatrix}2&1\\1&3\end{bmatrix}\) positive definite?

**Worked guidance:** The first leading principal minor is 2, and the determinant is 5. Both are positive, so Sylvester's criterion establishes positive definiteness.

### Exercise 5 — covariance of a sum

For \(\Sigma=\begin{bmatrix}4&1.5\\1.5&9\end{bmatrix}\), calculate the variance of \(X_1+X_2\).

**Worked guidance:** Use \(\mathbf{a}=(1,1)^T\). The variance is \(4+1.5+1.5+9=16\).

### Exercise 6 — covariance of a difference

Using the same covariance matrix, calculate the variance of \(X_1-X_2\).

**Worked guidance:** Use \(\mathbf{a}=(1,-1)^T\). The variance is \(4-1.5-1.5+9=10\).

### Exercise 7 — interpret a singular covariance

What does a zero eigenvalue of a PSD covariance matrix indicate?

**Worked guidance:** There is a nonzero linear combination of variables with zero variance under the model. This may reflect an exact dependency or a degenerate model; it does not mean the associated individual variables necessarily have zero variance.

### Exercise 8 — least-squares curvature

When is \(A^TWA\) positive definite if \(W\) is positive definite?

**Worked guidance:** When the columns of \(A\) are linearly independent (full column rank). Otherwise the matrix is PSD and singular.

### Exercise 9 — identify a convex objective

A quadratic objective has a symmetric positive-semidefinite Hessian. What can be concluded?

**Worked guidance:** The objective is convex. Strict convexity and a unique minimiser do not follow unless stronger conditions hold.

### Exercise 10 — uncertainty ellipse

What determines the principal directions of a two-dimensional covariance ellipse?

**Worked guidance:** The eigenvectors of the covariance matrix. The corresponding eigenvalues are variances along those directions.

## 12. Connections and next steps

- **Module 06 — Least squares and constrained systems:** uses quadratic objectives and the matrix \(A^TWA\).
- **Module 08 — Eigenvalues, eigenvectors and spectral structure:** develops the spectral interpretation of symmetric matrices and covariance ellipses.
- **Module 09 — Matrix factorizations:** develops Cholesky and other factorizations used to solve systems involving positive-definite matrices.
- **Module 10 — Covariance matrices and multivariate structure:** develops covariance construction, interpretation and multivariate applications.
- [Covariance and generalized least squares implementation](../../implementations/python/covariance-gls/README.md) documents the repository's covariance validation and GLS routines.
- [Measurement science and survey adjustment learning path](../../learning-paths/measurement-science-and-survey-adjustment.md) connects covariance and estimation to synthetic network experiments.
- [Principal component analysis](../../algorithms/statistics/pca.md) uses covariance structure and eigenvectors to describe multivariate variation.

## References

- Massachusetts Institute of Technology, Department of Mathematics. [18.06 Linear Algebra — OpenCourseWare, Spring 2010](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/). Course scope includes symmetric matrices, positive definite matrices, least squares and eigenvalues.
- Strang, G. (2021). [Lecture Notes for Linear Algebra](https://www-math.mit.edu/~gs/LectureNotes/). MIT-hosted notes on linear algebra and matrix structure.

**Source note:** These references are linked for human study. The MIT course identity and topic coverage are recorded in the repository source register; individual lectures and notes have not been reviewed claim by claim. This module uses original explanations and synthetic numerical examples rather than reproducing course text, figures or exercises.

**Scope:** real symmetric matrices, quadratic forms, definiteness, covariance matrix properties, least-squares curvature, Mahalanobis distance and uncertainty ellipses, and quadratic optimisation. Detailed probability theory, eigenvalue algorithms, numerical conditioning, robust covariance estimation and semidefinite optimisation are deferred.
