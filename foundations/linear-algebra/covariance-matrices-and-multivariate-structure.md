# Covariance matrices and multivariate structure

**Subject identity:** `SM-FND-002` — Linear algebra and matrix methods  
**Module:** 10  
**Status:** Initial public teaching resource; independent technical review and learner testing outstanding.

## 1. Why multivariate structure matters

Spatial observations and derived quantities rarely exist in isolation. A point position has multiple coordinate components. A survey network contains many related observations and unknowns. A multispectral pixel contains several bands. A terrain model contains neighbouring cells. A time series contains repeated measurements.

A vector of quantities therefore needs more than a list of individual variances. It needs a description of how the quantities vary together.

The covariance matrix is the central linear-algebra object for this purpose. It connects:

- uncertainty in individual quantities and uncertainty in combinations;
- correlated measurement observations and generalized least squares;
- coordinate uncertainty and error ellipses or ellipsoids;
- multiband data and principal component analysis;
- multivariate distance and anomaly screening;
- spatially indexed random variables and spatial covariance models.

This module develops the matrix structure. Probability and statistical inference own the distributional assumptions, estimation theory and inferential procedures in depth. Spatial statistics owns spatial dependence models, variograms and geostatistical inference.

## 2. Random vectors and covariance matrices

Let a random vector be

$$
\mathbf{X}=\begin{bmatrix}X_1&X_2&\cdots&X_p\end{bmatrix}^T
$$

with finite second moments and expectation vector

$$
\boldsymbol\mu=E[\mathbf{X}].
$$

Its covariance matrix is

$$
\Sigma=\operatorname{Cov}(\mathbf{X})
=E[(\mathbf{X}-\boldsymbol\mu)(\mathbf{X}-\boldsymbol\mu)^T].
$$

The entries are

$$
\Sigma_{ij}=\operatorname{cov}(X_i,X_j).
$$

The diagonal entries are variances; off-diagonal entries are covariances. The covariance between quantities has the product of their units. The variance of a quantity has squared units.

A covariance matrix is:

- square and symmetric;
- positive semidefinite, so \(\mathbf{a}^T\Sigma\mathbf{a}\geq0\) for every vector \(\mathbf{a}\);
- positive definite only when every nonzero linear combination has strictly positive variance.

A valid covariance matrix can be singular. For example, if \(X_2=2X_1\) exactly, the two-component vector has a zero-variance linear combination even though each component may have nonzero variance.

Positive definiteness is needed for some operations, such as an ordinary inverse and standard Cholesky factorization. It is not a universal validity requirement for covariance matrices.

## 3. Variance of a linear combination

For a fixed coefficient vector \(\mathbf{a}\), define

$$
Y=\mathbf{a}^T\mathbf{X}.
$$

Then

$$
\operatorname{Var}(Y)=\mathbf{a}^T\Sigma\mathbf{a}.
$$

For two variables,

$$
\operatorname{Var}(aX+bY)
=a^2\operatorname{Var}(X)+b^2\operatorname{Var}(Y)
+2ab\operatorname{cov}(X,Y).
$$

The covariance term matters. Adding independent variances when the quantities are correlated gives the wrong result.

### Worked example 1 — uncertainty in a coordinate difference

Suppose two one-dimensional positions have standard uncertainties 3 cm and 4 cm, with correlation coefficient 0.5. Their covariance is

$$
\operatorname{cov}(X_1,X_2)
=0.5(3)(4)=6\;\text{cm}^2.
$$

The covariance matrix is

$$
\Sigma=\begin{bmatrix}9&6\\6&16\end{bmatrix}\;\text{cm}^2.
$$

For the difference \(D=X_2-X_1\), use \(\mathbf{a}=(-1,1)^T\):

$$
\operatorname{Var}(D)
=\mathbf{a}^T\Sigma\mathbf{a}
=9+16-2(6)=13\;\text{cm}^2.
$$

Thus the standard uncertainty of the difference is \(\sqrt{13}\approx3.61\) cm. If the covariance were incorrectly set to zero, the result would be \(5\) cm. Positive correlation reduces the uncertainty of this difference because the shared movement partly cancels.

For the sum, the same positive covariance would increase uncertainty. The effect of correlation depends on the linear combination being considered.

## 4. Correlation matrices and standardisation

The correlation matrix standardises covariance by the marginal standard deviations. Let

$$
D=\operatorname{diag}(u_1,\ldots,u_p),
$$

where each \(u_i\) is the standard deviation of component (i). If all are nonzero,

$$
R=D^{-1}\Sigma D^{-1}.
$$

The diagonal of (R) contains ones; off-diagonal entries are correlation coefficients between -1 and +1.

Correlation is dimensionless and can make dependence patterns easier to compare when variables have different units or scales. But standardising is not neutral: it changes the geometry and relative influence of variables. A covariance analysis and a correlation analysis answer different questions.

Zero covariance does not generally imply independence. Independence implies zero covariance when the relevant moments exist, but the converse needs additional distributional assumptions.

## 5. Linear transformations and uncertainty propagation

If a random vector \(\mathbf{X}\) is transformed by a fixed matrix (B),

$$
\mathbf{Y}=B\mathbf{X}+\mathbf{c},
$$

then

$$
E[\mathbf{Y}]=B\boldsymbol\mu+\mathbf{c},
\qquad
\Sigma_Y=B\Sigma_XB^T.
$$

The constant translation \(\mathbf{c}\) changes the expectation but not the covariance. The transformation changes how uncertainty is oriented, scaled and correlated.

### Worked example 2 — sum and difference

For two quantities with covariance matrix

$$
\Sigma_X=\begin{bmatrix}4&1\\1&9\end{bmatrix},
$$

form the sum and difference:

$$
\mathbf{Y}=B\mathbf{X},
\qquad
B=\begin{bmatrix}1&1\\1&-1\end{bmatrix}.
$$

Then

$$
\Sigma_Y=B\Sigma_XB^T
=\begin{bmatrix}15&-5\\-5&11\end{bmatrix}.
$$

The variance of the sum is 15, the variance of the difference is 11, and their covariance is -5. The transformed quantities are not independent merely because they are expressed as sum and difference.

For a differentiable nonlinear function \(\mathbf{y}=f(\mathbf{x})\), first-order propagation uses the Jacobian (J) evaluated at the chosen expansion point:

$$
\Sigma_y\approx J\Sigma_xJ^T.
$$

This is a local linear approximation. Its adequacy depends on nonlinearity, uncertainty magnitude and distribution shape. Strong nonlinearity or non-Gaussian inputs may require simulation or a more complete treatment.

## 6. Covariance of estimated parameters and observations

In a linear model,

$$
\mathbf{y}=A\mathbf{x}+\boldsymbol\varepsilon,
$$

the observation covariance describes the stochastic structure of \(\boldsymbol\varepsilon\). If the covariance is \(\Sigma_y\), generalized least squares uses it to weight the residual vector:

$$
\hat{\mathbf{x}}
=(A^T\Sigma_y^{-1}A)^{-1}A^T\Sigma_y^{-1}\mathbf{y},
$$

under the required full-rank and positive-definiteness assumptions.

For a fixed linear model with known covariance and no exact constraints, the formal covariance of the GLS estimate is

$$
\Sigma_{\hat x}=(A^T\Sigma_y^{-1}A)^{-1}.
$$

This expression is not a universal uncertainty guarantee. It depends on the model, covariance specification, rank conditions and treatment of estimated variance components. Constraints change the parameter covariance structure; robust or misspecified models require additional care.

If \(\Sigma_y=LL^T\), Cholesky-based whitening can transform the problem to ordinary least squares without explicitly forming \(\Sigma_y^{-1}\). Module 09 explains the factorization; the repository's GLS implementation documents its positive-definite covariance requirement.

Covariance must be justified by an acquisition or processing mechanism. Shared instrument setup, common atmospheric effects, calibration, image geolocation, processing batches or repeated sessions may create dependence, but the mechanism and magnitude must be investigated rather than assumed from labels alone.

## 7. Spatial uncertainty geometry

For a two-dimensional coordinate vector \(\mathbf{x}=(E,N)^T\), its covariance matrix can be written

$$
\Sigma=\begin{bmatrix}
\sigma_E^2&\sigma_{EN}\\
\sigma_{EN}&\sigma_N^2
\end{bmatrix}.
$$

The eigenvectors give the principal directions of the covariance ellipse; the eigenvalues give the variances along those directions. The square roots of the eigenvalues are standard deviations along the principal axes.

A plotted ellipse requires a scale or probability convention. Under a bivariate normal model, contours of constant Mahalanobis distance are ellipses, but the multiplier used for a stated coverage probability is not automatically the one-dimensional value (k=2). The appropriate chi-square quantile and degrees of freedom must be used for the stated probability region.

Coordinate covariance also depends on coordinate representation, units, reference frame and the transformations applied. A covariance ellipse is not a boundary of guaranteed error and does not establish positional accuracy against an external truth source.

## 8. Multivariate structure and PCA

For a centred data matrix (X) with rows representing observations and columns representing variables, the sample covariance matrix is

$$
S=\frac{1}{n-1}X^TX.
$$

PCA finds orthogonal directions that successively explain the variance in the data. For a symmetric covariance matrix,

$$
S=Q\Lambda Q^T,
$$

where the eigenvectors in (Q) are principal directions and the eigenvalues in (Lambda) are the variances along those directions.

The proportion of total sample variance associated with component (i) is

$$
p_i=\frac{\lambda_i}{\sum_j\lambda_j},
$$

provided the total variance is nonzero.

### Covariance PCA versus correlation PCA

- **Covariance PCA** uses variables in their original units and scales. Variables with larger numerical variance can dominate.
- **Correlation PCA** standardises each variable to unit variance before decomposition. This gives variables equal marginal variance but may amplify low-variance or noisy variables.

For multiband imagery, band units, scaling, radiometric calibration, masks, atmospheric effects, noise and sample design matter. PCA is a linear transformation of the supplied data; it does not automatically separate signal from noise or produce physically meaningful thematic classes.

Eigenvector signs are arbitrary. If eigenvalues are repeated or nearly repeated, individual eigenvectors can also be unstable even when the subspace they span is stable.

See the repository's [PCA method](../../algorithms/statistics/pca.md), [PCA implementation](../../implementations/python/pca-transform/README.md), and Module 08.

## 9. Mahalanobis distance and multivariate comparison

For a vector \(\mathbf{x}\), mean \(\boldsymbol\mu\) and positive-definite covariance matrix \(\Sigma\), squared Mahalanobis distance is

$$
d_M^2=(\mathbf{x}-\boldsymbol\mu)^T
\Sigma^{-1}
(\mathbf{x}-\boldsymbol\mu).
$$

It scales deviations according to covariance, accounting for variable scales and linear correlations. A point far from the mean in a low-variance direction can have a large Mahalanobis distance even if its raw coordinate difference is modest.

The distance depends on a defensible mean and covariance estimate. It is not automatically a probability, an anomaly verdict or a robust outlier test. Thresholds require distributional assumptions and attention to sample size, parameter estimation, multiple testing and model misspecification.

For singular covariance, the ordinary inverse does not exist. A generalised inverse or dimension-reduced treatment may be mathematically possible, but the null space and support of the distribution must be handled explicitly.

## 10. Spatial covariance is not simply a covariance matrix

A covariance matrix can describe dependence among a finite collection of variables. Spatial statistics often models a random field indexed by location:

$$
Z(\mathbf{s}),\qquad \mathbf{s}\in\mathcal{D}.
$$

A covariance function describes dependence between locations:

$$
C(\mathbf{s}_i,\mathbf{s}_j)
=\operatorname{cov}(Z(\mathbf{s}_i),Z(\mathbf{s}_j)).
$$

For a finite set of locations, evaluating the covariance function produces a covariance matrix. A valid spatial covariance model must generate positive-semidefinite matrices for all admissible finite location sets.

Stationarity, isotropy, anisotropy, trends, barriers, non-Euclidean distance, support effects and nonstationarity all influence model choice. A distance-decay formula that looks plausible is not automatically a valid covariance function.

This module establishes the matrix side of the relationship. Variograms, covariance-function families, spatial prediction, kriging, neighbourhood definitions and spatial cross-validation belong to spatial statistics and geostatistics.

## 11. Worked spatial synthesis — a two-component position

Suppose a local position estimate has covariance

$$
\Sigma=\begin{bmatrix}0.0004&0.00012\\0.00012&0.0009\end{bmatrix}\;\text{m}^2.
$$

The marginal standard uncertainties are 0.020 m and 0.030 m. Their correlation is

$$
\rho=\frac{0.00012}{0.020\times0.030}=0.20.
$$

The covariance matrix is symmetric and positive definite because its leading principal minors are positive: 0.0004 and

$$
0.0004(0.0009)-(0.00012)^2>0.
$$

The eigenvectors give the principal axes of the uncertainty ellipse; the eigenvalues give squared standard uncertainties along those axes. A rotation into another local orthonormal frame uses \(\Sigma'=R\Sigma R^T\). The ellipse rotates with the coordinate frame, while the underlying uncertainty description is transformed consistently.

This example is illustrative only. It does not specify a real instrument, control network, CRS, confidence region or acceptance tolerance.

## 12. Exercises

### Exercise 1 — covariance matrix entries

What do the diagonal and off-diagonal entries of a covariance matrix represent?

**Worked guidance:** Diagonal entries are variances; off-diagonal entries are covariances between pairs of variables.

### Exercise 2 — valid covariance structure

Why must a covariance matrix be positive semidefinite?

**Worked guidance:** Every linear combination has a variance \(\mathbf{a}^T\Sigma\mathbf{a}\), which cannot be negative.

### Exercise 3 — difference uncertainty

Two measurements each have variance 25 and covariance 10. Find the variance of their difference.

**Worked guidance:** \(25+25-2(10)=30\). The covariance term reduces the difference variance.

### Exercise 4 — correlation conversion

Two quantities have standard deviations 2 m and 3 s, and covariance 1.2 m·s. Find their correlation.

**Worked guidance:** \(1.2/(2\times3)=0.2\). The units cancel.

### Exercise 5 — transformation

If \(\mathbf{Y}=B\mathbf{X}+\mathbf{c}\), what is the covariance of \(\mathbf{Y}\)?

**Worked guidance:** \(B\Sigma_XB^T\). A fixed translation does not affect covariance.

### Exercise 6 — covariance versus correlation PCA

When might correlation PCA be preferable, and what is its trade-off?

**Worked guidance:** It is useful when variables with different units or scales should contribute on a standardised basis. It can amplify low-variance noisy variables and changes the question being analysed.

### Exercise 7 — singular covariance

Can a singular matrix still be a valid covariance matrix?

**Worked guidance:** Yes. Positive semidefinite is sufficient for covariance validity. Singularity indicates an exact zero-variance linear combination or redundant representation.

### Exercise 8 — error ellipse interpretation

Do the eigenvalues of a coordinate covariance matrix directly give the semi-axis lengths of a 95% confidence ellipse?

**Worked guidance:** No. Their square roots are principal standard deviations. A probability ellipse requires an appropriate multiplier under a stated distributional model.

### Exercise 9 — Mahalanobis distance

Why can a small raw deviation be unusual in one direction but not another?

**Worked guidance:** Mahalanobis distance scales the deviation using covariance. A deviation along a low-variance direction can be more surprising under the model than a larger deviation along a high-variance direction.

### Exercise 10 — spatial covariance

What additional validity requirement applies to a proposed spatial covariance function?

**Worked guidance:** It must produce positive-semidefinite covariance matrices for every admissible finite set of locations, not merely plausible pairwise values.

## 13. Connections and scope boundaries

- **Module 07 — Symmetric matrices, quadratic forms and definiteness:** explains why covariance matrices are positive semidefinite and how quadratic forms encode variance.
- **Module 08 — Eigenvalues, eigenvectors and spectral structure:** explains principal directions and spectral decomposition.
- **Module 09 — Matrix factorizations:** explains Cholesky, QR and SVD computational routes.
- [Covariance, correlated observations and generalized least squares](../measurement-science/covariance-correlated-observations-and-gls.md) develops the measurement-science and estimation interpretation.
- [Covariance GLS implementation](../../implementations/python/covariance-gls/README.md) demonstrates selected covariance-aware computations and its explicit SPD limitations.
- [PCA method](../../algorithms/statistics/pca.md) and [PCA implementation](../../implementations/python/pca-transform/README.md) connect covariance structure to multiband data.
- [Measurement science and survey adjustment learning path](../../learning-paths/measurement-science-and-survey-adjustment.md) connects covariance to synthetic network adjustment exercises.

This module does not provide a complete probability course, statistical covariance estimation, robust covariance estimation, spatial covariance model catalogue, variogram fitting, kriging, random-field simulation, uncertainty budgets or a universal error-ellipse procedure. Those require their own domain-specific assumptions and validation.

## References

- BIPM / Joint Committee for Guides in Metrology. [JCGM 100:2008 — Evaluation of measurement data: Guide to the expression of uncertainty in measurement](https://www.bipm.org/en/web/guest/publications/guides). The source register notes that this legacy core must be read alongside the current GUM suite and 2026 Amendment 1; it is not the entire current guidance set.
- Massachusetts Institute of Technology, Department of Mathematics. [18.06 Linear Algebra — OpenCourseWare, Spring 2010](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/).
- Strang, G. [Lecture Notes for Linear Algebra](https://www-math.mit.edu/~gs/LectureNotes/).

**Source note:** These links support further study. The source register records the review scope and limitations for the metrology guide and MIT course. This module's explanations and numerical examples are original; individual MIT lectures and notes have not been reviewed claim by claim.

**Scope:** Covariance and correlation matrices, linear transformations, first-order covariance propagation, GLS covariance structure, uncertainty geometry, PCA, Mahalanobis distance and the finite-matrix connection to spatial covariance functions. Statistical inference, detailed spatial covariance modelling and geostatistical prediction are deferred to their respective foundation domains.
