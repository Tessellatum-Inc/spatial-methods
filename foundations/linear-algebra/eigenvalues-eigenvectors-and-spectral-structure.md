# Eigenvalues, eigenvectors and spectral structure

**Subject identity:** `SM-FND-002` — Linear algebra and matrix methods  
**Module:** 08  
**Status:** Initial public teaching resource; independent technical review and learner testing outstanding.

## 1. Why spectral structure matters

Eigenvalues and eigenvectors reveal directions along which a linear transformation acts by simple scaling. For real symmetric matrices, this structure is especially useful: the eigenvalues are real and the eigenvectors can be chosen orthonormal.

Spatial applications include:

- principal component analysis (PCA) and multivariate variation;
- principal directions of coordinate uncertainty;
- local geometric orientation and shape analysis;
- stability and modes of linear systems;
- spectral descriptions of networks and spatial operators.

The same algebra appears in each case, but the meaning of an eigenvalue depends on the matrix being analysed. A covariance eigenvalue is a variance; an adjacency-matrix eigenvalue is not a variance; an eigenvalue of a physical dynamical operator may describe growth, decay or oscillation.

## 2. Eigenvalues and eigenvectors

For a square matrix (A), a nonzero vector (mathbf{v}) is an eigenvector with eigenvalue (lambda) when

$$
A\mathbf{v}=\lambda\mathbf{v}.
$$

The transformation maps this direction onto itself, scaling it by \(\lambda\). A positive eigenvalue preserves direction, a negative eigenvalue reverses direction, and a zero eigenvalue maps the eigenvector to zero.

Eigenvectors must be nonzero. The zero vector satisfies the equation for every scalar but is not an eigenvector.

Rearranging gives

$$
(A-\lambda I)\mathbf{v}=\mathbf{0}.
$$

A nonzero solution exists only when

$$
\det(A-\lambda I)=0.
$$

This is the characteristic equation. Its roots are the eigenvalues; solving the corresponding homogeneous system gives each eigenspace.

## 3. Worked example — a two-dimensional transformation

Let

$$
A=\begin{bmatrix}2&1\\1&2\end{bmatrix}.
$$

The characteristic equation is

$$
\det(A-\lambda I)
=(2-\lambda)^2-1=0.
$$

Thus the eigenvalues are \(\lambda_1=3\) and \(\lambda_2=1\).

For \(\lambda_1=3\), an eigenvector is \((1,1)^T\). For \(\lambda_2=1\), an eigenvector is \((1,-1)^T\). Normalising them gives

$$
\mathbf{q}_1=\frac{1}{\sqrt2}\begin{bmatrix}1\\1\end{bmatrix},
\qquad
\mathbf{q}_2=\frac{1}{\sqrt2}\begin{bmatrix}1\\-1\end{bmatrix}.
$$

The first direction is stretched by a factor of three; the second by a factor of one. The eigenvectors are perpendicular.

The same matrix can be reconstructed from its spectral components:

$$
A=Q\Lambda Q^T,
\qquad
Q=\begin{bmatrix}\mathbf{q}_1&\mathbf{q}_2\end{bmatrix},
\quad
\Lambda=\begin{bmatrix}3&0\\0&1\end{bmatrix}.
$$

This is an orthogonal diagonalisation.

## 4. The spectral theorem for real symmetric matrices

If (A) is a real symmetric matrix, then there exists an orthogonal matrix (Q) and a real diagonal matrix \(\Lambda\) such that

$$
A=Q\Lambda Q^T.
$$

The columns of (Q) are an orthonormal set of eigenvectors, and the diagonal entries of \(\Lambda\) are the corresponding real eigenvalues.

Orthogonal means

$$
Q^TQ=QQ^T=I.
$$

This result is especially powerful because it gives a coordinate system aligned with the matrix's principal directions. In that basis, the transformation acts independently along each eigenvector direction.

### What if eigenvalues repeat?

If an eigenvalue is repeated, its individual eigenvectors are not uniquely determined. Any orthonormal basis of its eigenspace is valid. The eigenspace itself is the invariant object; a particular set of basis vectors may vary between software libraries or runs.

Eigenvector signs are also arbitrary: if \(\mathbf{v}\) is an eigenvector, then \(-\mathbf{v}\) is equally valid. Do not interpret a sign flip as a different principal direction.

## 5. Eigenvalues and quadratic forms

For a real symmetric matrix,

$$
A=Q\Lambda Q^T.
$$

Writing \(\mathbf{x}=Q\mathbf{z}\), the quadratic form becomes

$$
\mathbf{x}^TA\mathbf{x}
=\mathbf{z}^T\Lambda\mathbf{z}
=\sum_i\lambda_i z_i^2.
$$

The quadratic form is therefore a weighted sum of squared coordinates in the eigenvector basis.

This gives a direct connection to Module 07:

- all eigenvalues positive: positive definite;
- all eigenvalues nonnegative: positive semidefinite;
- mixed positive and negative eigenvalues: indefinite;
- zero eigenvalues: nonzero directions with zero quadratic contribution.

For a symmetric matrix, the trace is the sum of eigenvalues and the determinant is their product:

$$
\operatorname{tr}(A)=\sum_i\lambda_i,
\qquad
\det(A)=\prod_i\lambda_i.
$$

These identities are useful checks, but trace and determinant alone do not reveal the full eigenstructure.

## 6. Rayleigh quotient and directional behaviour

For nonzero \(\mathbf{x}\), the Rayleigh quotient of a real symmetric matrix is

$$
R(\mathbf{x})=
\frac{\mathbf{x}^TA\mathbf{x}}
{\mathbf{x}^T\mathbf{x}}.
$$

It measures the quadratic form per unit squared vector length. Its minimum and maximum over unit vectors are the smallest and largest eigenvalues:

$$
\lambda_{\min}\leq R(\mathbf{x})\leq\lambda_{\max}.
$$

Equality occurs for eigenvectors associated with the corresponding extreme eigenvalues.

This helps interpret principal directions: they are directions where the quadratic form reaches an extreme value under a unit-length constraint.

## 7. Covariance eigenstructure and uncertainty ellipses

A covariance matrix is symmetric and positive semidefinite. For a two-dimensional coordinate vector,

$$
\Sigma=Q\Lambda Q^T,
\qquad
\Lambda=\begin{bmatrix}\lambda_1&0\\0&\lambda_2\end{bmatrix}.
$$

The eigenvectors give the principal directions of coordinate variation. The eigenvalues are the variances along those directions, so the corresponding standard deviations are \(\sqrt{\lambda_1}\) and \(\sqrt{\lambda_2}\).

For a positive-definite covariance matrix, constant Mahalanobis-distance contours are ellipses aligned with these eigenvectors. Their semi-axis lengths for a fixed squared-distance value \(c\) are proportional to \(\sqrt{c\lambda_i}\).

If an eigenvalue is zero, the covariance is singular and the distribution is confined to a lower-dimensional subspace under the model. Ordinary inverse-covariance Mahalanobis distance is then not defined; a specialised treatment is required.

The eigenvalues are in squared coordinate units. The eigenvectors describe directions in the coordinate basis. Changing units or coordinate basis changes the numerical covariance matrix and may change the interpretation of its axes.

## 8. Principal component analysis

PCA uses the eigenstructure of a covariance or correlation matrix to find orthogonal directions of variation in multivariate data.

Suppose a centred data matrix (X) has observations in rows and variables in columns. Its sample covariance matrix is

$$
S=\frac{1}{n-1}X^TX.
$$

Since (S) is symmetric and PSD, it can be orthogonally diagonalised:

$$
S=Q\Lambda Q^T.
$$

The eigenvectors (columns of (Q)) are principal component directions. The eigenvalues quantify the sample variance along those directions. Projecting centred observations onto selected eigenvectors gives component scores.

### Worked example — two perfectly related spatial attributes

Consider three centred observations for two attributes, perhaps two standardised measurements sampled at the same locations:

$$
X=\begin{bmatrix}
-1&-1\\
0&0\\
1&1
\end{bmatrix}.
$$

The sample covariance matrix is

$$
S=\frac{1}{2}X^TX
=\begin{bmatrix}1&1\\1&1\end{bmatrix}.
$$

Its eigenvalues are 2 and 0. The first principal direction is proportional to \((1,1)^T\); the second is proportional to \((1,-1)^T\).

All observed variation lies along the first direction. The second direction has zero sample variance because the two columns are identical in this deliberately simple dataset.

The first component accounts for all observed sample variance. This does not establish a causal relationship between the attributes, nor does it prove that the same relationship holds outside this tiny synthetic dataset.

### Covariance PCA versus correlation PCA

Covariance PCA uses variables in their original units and scales. Variables with larger numerical variances can dominate.

Correlation PCA standardises variables before analysis, so each nonconstant variable has unit variance. This changes the analysis and can be preferable when variables have different units or scales, but it is not automatically the correct choice. Standardisation can amplify noisy or low-variance variables.

The choice should follow the scientific question, measurement scales and intended interpretation. PCA is sensitive to outliers and missing-data treatment, and its components are not automatically meaningful physical processes.

The repository's [PCA method page](../../algorithms/statistics/pca.md) and [Python implementation](../../implementations/python/pca-transform/README.md) provide the applied counterpart. The implementation's tests and stated limitations should be consulted before relying on it.

## 9. Spatial and network operators

Eigenanalysis also appears in spatial weights and graph-based methods. For example, eigenvectors of a graph Laplacian can describe broad patterns of connectivity and graph smoothness. The multiplicity of the zero eigenvalue of an undirected graph Laplacian is related to the number of connected components.

However, the matrix definition matters:

- an undirected graph adjacency matrix is symmetric when edges are represented symmetrically;
- a directed adjacency matrix is generally nonsymmetric;
- row-standardised spatial weights need not be symmetric, even if the underlying neighbour relation is undirected;
- a graph Laplacian has its own sign and normalisation conventions.

Do not transfer the symmetric spectral theorem or covariance interpretation to every spatial weights matrix. Nonsymmetric matrices may have complex eigenvalues and different spectral properties. Directed networks and non-normal operators require separate treatment.

In spatial analysis, the meaning of an eigenvector is determined by the operator, its construction, its normalisation and the spatial support. It is not automatically a geographic region, process or causal factor.

## 10. Stability and repeated transformations

If a linear transformation is repeatedly applied,

$$
\mathbf{x}_{k+1}=A\mathbf{x}_k,
$$

then, when (A) is diagonalisable, each eigencomponent is scaled by its eigenvalue at each step. For a symmetric matrix, the orthogonal eigenbasis makes this interpretation especially clear.

Eigenvalue magnitudes can indicate whether components grow, decay or remain unchanged under repeated application:

- \(|\lambda|<1\): the component decays;
- \(|\lambda|>1\): the component grows in magnitude;
- \(|\lambda|=1\): the component's magnitude is preserved, though a negative eigenvalue alternates sign.

This is a simplified discrete linear system. Stability of a real spatial or physical process depends on the actual dynamics, time step, forcing, nonlinearities and model structure. Eigenvalues alone do not validate a model.

## 11. Common mistakes and limitations

- **Treating eigenvectors as unique:** signs are arbitrary and repeated eigenspaces admit multiple valid bases.
- **Interpreting eigenvalues without matrix context:** a covariance eigenvalue is a variance; another operator has another meaning.
- **Assuming every matrix has real eigenvalues:** this is guaranteed for real symmetric matrices, not arbitrary real matrices.
- **Confusing PCA with factor analysis:** PCA decomposes total variance; factor analysis models common variance under a different statistical model.
- **Ignoring variable scaling:** covariance PCA and correlation PCA answer different questions.
- **Treating explained variance as causal explanation:** PCA is descriptive and depends on the selected data and variables.
- **Assuming spatial weights are symmetric:** row standardisation and directed relationships can break symmetry.
- **Ignoring units and coordinate basis:** covariance eigenvalues and directions depend on variable scaling and representation.
- **Overinterpreting small eigenvalues:** they may reflect a real near-dependency, sampling noise, numerical error or a modelling choice.

This module introduces the spectral theorem for real symmetric matrices and selected spatial applications. General eigenanalysis of nonsymmetric matrices, Jordan forms, complex spectral theory, iterative eigensolvers, perturbation bounds and numerical conditioning are deferred to specialist numerical analysis.

## 12. Exercises

### Exercise 1 — verify an eigenpair

For \(A=\begin{bmatrix}2&1\\1&2\end{bmatrix}\), verify that \((1,1)^T\) is an eigenvector and find its eigenvalue.

**Worked guidance:** Multiplication gives \((3,3)^T=3(1,1)^T\), so the eigenvalue is 3.

### Exercise 2 — find the second eigenvalue

For the same matrix, show that \((1,-1)^T\) is an eigenvector.

**Worked guidance:** The product is \((1,-1)^T\), so the eigenvalue is 1.

### Exercise 3 — classify a symmetric matrix

A real symmetric matrix has eigenvalues 4, 1 and 0. What is its definiteness?

**Worked guidance:** It is positive semidefinite but not positive definite. The zero eigenvalue gives a nonzero null direction.

### Exercise 4 — interpret a covariance eigenvalue

A two-dimensional covariance matrix has eigenvalues 25 and 4, in squared metres. What are the standard deviations along the principal directions?

**Worked guidance:** They are 5 m and 2 m respectively. The eigenvectors determine the directions.

### Exercise 5 — identify PCA's leading direction

For the covariance matrix \(S=\begin{bmatrix}1&1\\1&1\end{bmatrix}\), what is the leading principal direction?

**Worked guidance:** It is proportional to \((1,1)^T\), with eigenvalue 2. The orthogonal direction has eigenvalue zero.

### Exercise 6 — explain eigenvector sign

A PCA software package reports a component loading vector \((0.6,0.8)^T\), while another reports \((-0.6,-0.8)^T\). Are these necessarily different results?

**Worked guidance:** No. They describe the same one-dimensional eigendirection. Eigenvector sign is arbitrary; component scores reverse sign at the same time.

### Exercise 7 — repeated eigenvalues

What is special about an eigenspace when an eigenvalue has multiplicity greater than one?

**Worked guidance:** The eigenspace has dimension greater than one, and any orthonormal basis spanning it is valid. Individual eigenvectors are not uniquely defined.

### Exercise 8 — covariance versus correlation PCA

Why might standardising variables change the PCA result?

**Worked guidance:** Standardisation rescales variables to unit variance before decomposition. This changes their relative contribution, particularly when variables have different units or variances.

### Exercise 9 — graph matrix caution

Can the real symmetric spectral theorem be applied automatically to a row-standardised spatial weights matrix?

**Worked guidance:** No. Row standardisation can make the matrix nonsymmetric. Its spectral properties require a method appropriate to that matrix structure.

### Exercise 10 — repeated transformation

A component of a symmetric linear system has eigenvalue 0.8. What happens to that component under repeated multiplication by the matrix?

**Worked guidance:** Its magnitude is multiplied by 0.8 at each iteration and decays geometrically, assuming the same fixed linear transformation is repeatedly applied.

## 13. Connections and next steps

- **Module 07 — Symmetric matrices, quadratic forms and definiteness:** establishes the matrix structure and definiteness conditions used here.
- **Module 09 — Matrix factorizations:** develops practical decompositions used to solve systems and compute spectral information.
- **Module 10 — Covariance matrices and multivariate structure:** develops covariance estimation and multivariate interpretation.
- [Principal component analysis](../../algorithms/statistics/pca.md) connects covariance eigenanalysis to a concrete spatial-analysis method.
- [PCA Python implementation](../../implementations/python/pca-transform/README.md) provides the repository's applied implementation.
- [Covariance and generalized least squares](../../implementations/python/covariance-gls/README.md) connects symmetric positive-definite covariance structures to estimation.

## References

- Massachusetts Institute of Technology, Department of Mathematics. [18.06 Linear Algebra — OpenCourseWare, Spring 2010](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/). Course scope includes eigenvalues, eigenvectors, symmetric matrices, positive definite matrices and applications.
- Strang, G. (2021). [Lecture Notes for Linear Algebra](https://www-math.mit.edu/~gs/LectureNotes/). MIT-hosted notes on eigenvalues, eigenvectors and matrix structure.

**Source note:** These references are linked for human study. The MIT course identity and topic coverage are recorded in the repository source register; individual lectures and notes have not been reviewed claim by claim. This module presents original explanations and synthetic examples rather than reproducing course text, figures or exercises.

**Scope:** eigenvalues and eigenvectors, characteristic equations, the spectral theorem for real symmetric matrices, Rayleigh quotient, covariance eigenstructure, PCA, selected graph spectral concepts and repeated linear transformations. General nonsymmetric spectral theory, numerical eigensolvers, perturbation theory and advanced statistical interpretation are deferred.
