# Least squares and constrained systems

**Subject identity:** `SM-FND-002` — Linear algebra and matrix methods  
**Module:** 06  
**Status:** Initial public teaching resource; independent technical review and learner testing outstanding.

## 1. Why least squares is needed

Many spatial problems provide more observations than unknown parameters. A survey network may contain repeated height differences, a terrain model may be fitted to many sampled points, and a spatial regression may estimate a small number of coefficients from a large dataset.

When observations are inconsistent with one exact parameter vector—because of measurement noise, model mismatch or both—we need a principled way to choose an estimate.

**Least squares** chooses parameters that minimise a sum of squared residuals. Its geometry is the projection developed in Module 05. Its algebra is a system of linear equations. Its statistical interpretation depends on the observation model and covariance assumptions.

This module develops:

- the observation/design matrix model;
- residuals and the least-squares objective;
- normal equations and their geometric meaning;
- overdetermined, underdetermined and rank-deficient cases;
- weighted least squares and generalized least squares;
- exact linear constraints and the KKT system;
- the distinction between an exact constraint and an observation;
- practical interpretation and limits.

## 2. The linear observation model

A linear model can be written

$$
\mathbf{y}=A\mathbf{x}+\boldsymbol{\varepsilon},
$$

where:

- \(\mathbf{y}\) is the vector of observed values;
- \(A\) is the design or coefficient matrix;
- \(\mathbf{x}\) is the unknown parameter vector;
- \(\boldsymbol{\varepsilon}\) is the observation-error or model-discrepancy vector.

The model is linear in the unknown parameters. It does not have to describe a physically linear process in every respect; nonlinear physical models can sometimes be linearised around approximate parameters, a topic beyond this module.

The fitted observations are

$$
\widehat{\mathbf{y}}=A\widehat{\mathbf{x}},
$$

and, using the convention observation minus fitted value, the residual vector is

$$
\mathbf{r}=\mathbf{y}-A\widehat{\mathbf{x}}.
$$

Be consistent about the sign convention. Some disciplines define residuals with the opposite sign. The estimated parameters are unchanged if the residual convention is used consistently, but reported residual signs reverse.

### Dimensions matter

If there are \(m\) observations and \(n\) unknown parameters, then:

- \(\mathbf{y}\) and \(\mathbf{r}\) have \(m\) entries;
- \(A\) has \(m\) rows and \(n\) columns;
- \(\mathbf{x}\) has \(n\) entries.

A row represents an observation equation; a column represents the way one unknown parameter contributes to the observations.

## 3. Ordinary least squares

Ordinary least squares (OLS) selects the parameter vector that minimises the sum of squared residuals:

$$
\widehat{\mathbf{x}}
=\underset{\mathbf{x}}{\operatorname{argmin}}
\;\mathbf{r}^T\mathbf{r}
=\underset{\mathbf{x}}{\operatorname{argmin}}
\;(\mathbf{y}-A\mathbf{x})^T(\mathbf{y}-A\mathbf{x}).
$$

Squaring makes positive and negative residuals contribute positively and penalises large residuals more heavily than small ones. This objective is a mathematical choice, not a guarantee that the errors are independent, Gaussian, unbiased or free of gross mistakes.

If the columns of \(A\) are linearly independent, the minimiser is unique. If they are not, there may be multiple parameter vectors producing the same fitted observations.

### Worked example 1 — fitting a straight line

Suppose three measured values are observed at positions \(t=0,1,2\):

| \(t\) | Observed \(y\) |
|---:|---:|
| 0 | 1 |
| 1 | 2 |
| 2 | 2 |

Fit the model

$$
y_i=a+bt_i+\varepsilon_i.
$$

The design matrix, observations and parameters are

$$
A=\begin{bmatrix}1&0\\1&1\\1&2\end{bmatrix},
\qquad
\mathbf{y}=\begin{bmatrix}1\\2\\2\end{bmatrix},
\qquad
\mathbf{x}=\begin{bmatrix}a\\b\end{bmatrix}.
$$

The least-squares estimate is

$$
\widehat{a}=\frac{7}{6},
\qquad
\widehat{b}=\frac{1}{2}.
$$

The fitted values are

$$
\widehat{\mathbf{y}}
=\begin{bmatrix}7/6\\5/3\\13/6\end{bmatrix},
$$

and the residuals are

$$
\mathbf{r}
=\begin{bmatrix}-1/6\\1/3\\-1/6\end{bmatrix}.
$$

The residuals sum to zero, and their position-weighted sum is also zero:

$$
A^T\mathbf{r}=\mathbf{0}.
$$

This is not a coincidence. It is the orthogonality condition for the least-squares solution.

## 4. The normal equations

Expanding the OLS objective gives

$$
\Phi(\mathbf{x})
=\mathbf{y}^T\mathbf{y}
-2\mathbf{x}^TA^T\mathbf{y}
+\mathbf{x}^TA^TA\mathbf{x}.
$$

Setting its gradient to zero yields the **normal equations**:

$$
A^TA\widehat{\mathbf{x}}=A^T\mathbf{y}.
$$

If \(A\) has full column rank, \(A^TA\) is invertible and the formal solution is

$$
\widehat{\mathbf{x}}
=(A^TA)^{-1}A^T\mathbf{y}.
$$

This expression is useful for understanding the mathematics. It is not generally the preferred numerical implementation: explicitly forming \(A^TA\) can worsen conditioning, and explicitly computing an inverse is usually unnecessary. QR or SVD-based methods are generally preferred for numerical work; those methods are developed in the matrix-factorization and numerical-analysis material.

### Geometric meaning

At the least-squares solution,

$$
A^T\mathbf{r}=\mathbf{0}.
$$

The residual is orthogonal to every column of \(A\), and therefore to the entire column space of the model. The fitted vector is the orthogonal projection of \(\mathbf{y}\) onto that column space.

If a constant column is present in \(A\), the residuals sum to zero. If a linear trend column is present, residuals are also orthogonal to that trend column. These are consequences of the model's columns, not universal rules that every residual set must satisfy.

## 5. Observation count, rank and identifiability

The number of observations alone does not determine whether the unknown parameters are identifiable. The rank and structure of \(A\) matter.

- **Overdetermined:** \(m>n\). There are more observation equations than parameters. If \(A\) has full column rank, OLS has a unique solution, even if no exact solution to \(A\mathbf{x}=\mathbf{y}\) exists.
- **Exactly determined:** \(m=n\). A unique exact solution exists only if \(A\) is nonsingular.
- **Underdetermined:** \(m<n\). There are fewer equations than unknowns. A unique solution cannot be identified from these equations alone.
- **Rank deficient:** columns of \(A\) are dependent. Some parameter combinations cannot be distinguished by the observations, regardless of the observation count.

If \(A\) has rank \(r\), the nullity is \(n-r\). Every vector in the null space can be added to a solution without changing the fitted observations:

$$
A(\mathbf{x}+\mathbf{z})=A\mathbf{x}
\quad\text{when}\quad
A\mathbf{z}=\mathbf{0}.
$$

This is the algebraic origin of datum defects in free networks and other unidentifiable parameter combinations. A least-squares objective does not magically supply information missing from the model.

## 6. Weighted least squares

Not all observations need have equal uncertainty. If observations are uncorrelated but have different variances, weighted least squares (WLS) uses a diagonal weight matrix:

$$
W=\operatorname{diag}
\left(\frac{1}{\sigma_1^2},\ldots,\frac{1}{\sigma_m^2}\right).
$$

The objective is

$$
\widehat{\mathbf{x}}
=\underset{\mathbf{x}}{\operatorname{argmin}}
\;(\mathbf{y}-A\mathbf{x})^T
W(\mathbf{y}-A\mathbf{x}).
$$

An observation with smaller variance receives greater weight. The weights must represent a defensible relative precision model; they should not be chosen simply to make a desired answer dominate.

The normal equations become

$$
A^TWA\widehat{\mathbf{x}}=A^TW\mathbf{y}.
$$

When \(W\) is positive definite and \(A\) has full column rank, the solution is unique.

## 7. Generalized least squares and correlated observations

If observations are correlated, a diagonal weight matrix discards their covariance structure. Generalized least squares (GLS) uses the full observation covariance matrix \(Q\):

$$
\operatorname{Cov}(\boldsymbol{\varepsilon})=Q.
$$

For a positive-definite \(Q\), the GLS objective is

$$
\widehat{\mathbf{x}}
=\underset{\mathbf{x}}{\operatorname{argmin}}
\;(\mathbf{y}-A\mathbf{x})^T
Q^{-1}(\mathbf{y}-A\mathbf{x}).
$$

The corresponding normal equations are

$$
A^TQ^{-1}A\widehat{\mathbf{x}}
=A^TQ^{-1}\mathbf{y}.
$$

WLS is a special case of GLS when \(Q\) is diagonal and the weights are its inverse diagonal elements.

The covariance matrix must be connected to plausible error-generating mechanisms: shared instrument setup, common atmospheric effects, session processing, repeated use of control, or other defensible sources. A correlation matrix should not be invented merely because software accepts one.

Under the linear model with zero-mean errors and correctly specified covariance, the GLS estimator has formal covariance

$$
\operatorname{Cov}(\widehat{\mathbf{x}})
=(A^TQ^{-1}A)^{-1}
$$

when the design has full column rank and \(Q\) is positive definite. This expression is conditional on the stated model and fixed covariance; it is not automatically a complete uncertainty statement.

## 8. Exact constraints

Some parameter relationships are imposed exactly by definition or by the chosen mathematical formulation. They can be written

$$
C\mathbf{x}=\mathbf{d},
$$

where \(C\) is the constraint matrix and \(\mathbf{d}\) is the constraint vector.

A constrained least-squares problem minimises the chosen residual objective subject to those exact equations:

$$
\min_{\mathbf{x}}
\;(\mathbf{y}-A\mathbf{x})^T
W(\mathbf{y}-A\mathbf{x})
\quad\text{subject to}\quad
C\mathbf{x}=\mathbf{d}.
$$

For GLS, replace \(W\) with \(Q^{-1}\).

An exact constraint is not an observation with a very small variance. It has no stochastic observation uncertainty within the mathematical model. If a control coordinate is uncertain, it should normally be represented as an observation with an appropriate stochastic model, not silently fixed as exact.

### Inner constraints and datum selection

A free network may determine relative geometry while leaving a datum freedom. In a simple two-point height-difference example,

$$
h_B-h_A=2.
$$

The solutions are \((h_A,h_B)=(t,t+2)\) for any real \(t\). A sum-to-zero inner constraint,

$$
h_A+h_B=0,
$$

selects \(h_A=-1\), \(h_B=1\). This fixes a mathematical origin for the relative network; it does not connect the heights to an external benchmark or national vertical datum.

A constraint should reflect a declared datum convention or genuine exact relationship. Adding arbitrary constraints to make a matrix invertible can produce a unique answer without making it physically meaningful.

## 9. The KKT system for exact constraints

For the weighted quadratic objective, define

$$
N=A^TWA,
\qquad
\mathbf{g}=A^TW\mathbf{y}.
$$

Using Lagrange multipliers, the constrained solution satisfies the Karush–Kuhn–Tucker (KKT) system

$$
\begin{bmatrix}
N&C^T\\
C&0
\end{bmatrix}
\begin{bmatrix}
\widehat{\mathbf{x}}\\
\boldsymbol{\lambda}
\end{bmatrix}
=
\begin{bmatrix}
\mathbf{g}\\
\mathbf{d}
\end{bmatrix}.
$$

The first block row expresses the stationarity condition; the second enforces the exact constraints.

The KKT matrix is not an ordinary positive-definite normal matrix. Under suitable conditions—such as independent constraints and a positive-definite objective on directions not removed by the constraints—the constrained solution is unique. If a datum defect remains, or the constraints are redundant or inconsistent, the system may be singular or infeasible.

For a rank-deficient design, exact constraints can remove the null-space freedom if they constrain every unidentifiable parameter direction. They cannot repair an invalid observation model or create external information that was never observed.

### Worked example 2 — a two-height inner constraint

Suppose the single relative observation is

$$
y=2,
\qquad
A=\begin{bmatrix}-1&1\end{bmatrix},
\qquad
\mathbf{x}=\begin{bmatrix}h_A\\h_B\end{bmatrix}.
$$

The observation equation is \(-h_A+h_B=2\). The design matrix has rank one and a one-dimensional null space spanned by \((1,1)^T\): translating both heights by the same amount leaves the observation unchanged.

Impose the inner constraint

$$
C=\begin{bmatrix}1&1\end{bmatrix},
\qquad d=0.
$$

The exact equations are now

$$
-h_A+h_B=2,
\qquad
h_A+h_B=0.
$$

Solving gives

$$
\widehat{h}_A=-1,
\qquad
\widehat{h}_B=1.
$$

There is no residual in this one-observation example because the relative observation is exactly satisfied. The constraint selects the vertical origin; it is not a second measured height difference and does not provide an external datum.

## 10. Exact constraints versus stochastic control

Consider three different modelling choices:

1. **Exact datum convention:** impose a declared inner constraint, such as a sum-to-zero condition, to select one representative from a family of equivalent free-network solutions.
2. **Fixed external control:** treat a parameter as exact only if the modelling purpose and evidence justify that assumption.
3. **Uncertain external control:** include the control as an observation with its uncertainty and any relevant covariance.

These choices answer different questions. A datum convention removes mathematical freedom. Exact control fixes a parameter by assumption. Stochastic control contributes information with finite uncertainty.

The distinction matters in survey adjustment, georeferencing, calibration, registration and any inverse problem with gauge freedoms.

## 11. Spatial application — from height differences to an adjusted network

A levelling or vertical-control network can be written as a system of observation equations. Each measured height difference contributes a row to the design matrix. Unknown station heights form the parameter vector.

For an observation from station A to station B,

$$
\Delta h_{AB}=h_B-h_A+\varepsilon_{AB}.
$$

The corresponding design row has −1 in the A column, +1 in the B column and zeros elsewhere.

A network with loops and redundant paths is generally overdetermined. Adjustment finds a set of station heights that best fits the observations under the chosen stochastic model. The residuals describe discrepancies between observations and fitted differences.

If the network has no external vertical control, all heights may be shifted by a common amount without changing any height difference. A datum constraint can select a unique relative solution. To report heights in an external reference system, appropriate external control and its uncertainty must be introduced.

The repository's synthetic Exercise C, Exercise E and Exercises K–O explore progressively richer versions of these ideas. They are teaching simulations, not field measurements or proof that a particular field network is adequate.

## 12. Formal covariance and interpretation

For full-column-rank OLS with independent, equal-variance errors of variance \(\sigma^2\),

$$
\operatorname{Cov}(\widehat{\mathbf{x}})
=\sigma^2(A^TA)^{-1}.
$$

For WLS/GLS with known covariance \(Q\), the corresponding full-rank expression is

$$
\operatorname{Cov}(\widehat{\mathbf{x}})
=(A^TQ^{-1}A)^{-1}.
$$

These expressions are conditional on a correct linear model, the stated covariance and the relevant rank assumptions. If a variance factor is estimated from residuals, its estimation and degrees of freedom must be handled explicitly. If exact constraints are imposed, the constrained parameter covariance differs from the unconstrained expression; it can be obtained from the appropriate constrained system under its assumptions.

A small residual does not prove that the model is correct. A low formal parameter variance does not prove that the observations are unbiased, the datum is appropriate, the covariance is realistic, or the network is reliable against gross errors.

## 13. Common mistakes and limits

- **Treating least squares as a universal truth criterion:** it minimises a stated objective under a stated model; it does not validate the model.
- **Using equal weights without justification:** unequal precision and correlation may matter.
- **Ignoring rank:** more observations do not guarantee identifiable parameters.
- **Confusing residuals with errors:** residuals are computed from the fitted model; the true observation errors are not directly known.
- **Treating a datum constraint as an observation:** an inner constraint selects a representation; it does not create external control.
- **Treating uncertain control as exact:** this understates uncertainty and can distort the result.
- **Forming normal equations blindly:** this may worsen numerical conditioning; use stable factorizations.
- **Inverting covariance matrices explicitly:** implementations should generally use factorization and solves.
- **Assuming a covariance model is known because it is coded:** its structure and parameters need evidence from the observation process.
- **Deleting large residuals automatically:** residual magnitude alone is not proof of a blunder.

This module introduces linear estimation and exact linear constraints. Nonlinear least squares, robust estimators, variance-component estimation, full numerical conditioning analysis, singular observation covariance and generalized-inverse methods are outside its scope.

## 14. Exercises

### Exercise 1 — write a design matrix

A line model is \(y_i=a+bt_i+\varepsilon_i\), with observations at \(t=0,2,4\). Write the design matrix.

**Worked guidance:** \(A=\begin{bmatrix}1&0\\1&2\\1&4\end{bmatrix}\). The first column represents the intercept and the second the slope contribution.

### Exercise 2 — calculate fitted values and residuals

For the fitted line in Worked example 1, calculate the residual sum.

**Worked guidance:** The residuals are \((-1/6,1/3,-1/6)^T\). Their sum is zero because the design contains an intercept column and the residual is orthogonal to that column.

### Exercise 3 — interpret rank

A design matrix has 8 rows, 5 columns and rank 4. How many parameter-space null directions does it have?

**Worked guidance:** By rank–nullity, nullity is \(5-4=1\). One parameter combination is not identifiable from the design.

### Exercise 4 — identify a WLS weight

Two independent observations have standard uncertainties 2 units and 4 units. What are their relative inverse-variance weights?

**Worked guidance:** The variances are 4 and 16, so weights are 1/4 and 1/16. Their ratio is 4:1. A common multiplicative scaling does not change the estimate.

### Exercise 5 — distinguish WLS and GLS

When is diagonal WLS an appropriate special case of GLS?

**Worked guidance:** When the observation covariance is diagonal, so observations are uncorrelated under the model, and the weights are inverse variances (up to a common scale factor).

### Exercise 6 — diagnose a datum defect

A network observes only height differences among three stations and has no external vertical control. What parameter freedom remains?

**Worked guidance:** A common additive shift of all three heights leaves every difference unchanged. The network has one vertical translation datum defect. An inner constraint can select an origin, but does not establish an external datum.

### Exercise 7 — classify a constraint

A benchmark height has a documented uncertainty of 3 mm. Should it normally be represented as an exact constraint?

**Worked guidance:** No. Finite uncertainty is stochastic information. Represent it as an observation with a defensible variance and covariance structure, unless a specific approximation is explicitly justified and its consequences stated.

### Exercise 8 — interpret residual orthogonality

What does \(A^T\mathbf{r}=0\) express in ordinary least squares?

**Worked guidance:** The residual is orthogonal to the model's column space. It cannot be reduced by moving the fitted vector in a direction represented by the columns of A.

### Exercise 9 — exact versus stochastic information

A free network is assigned a sum-to-zero height constraint. Does this make the mean physical height of the network zero?

**Worked guidance:** No. It defines a convenient internal datum convention for the relative solution. It says nothing about the network's actual external elevation.

### Exercise 10 — choose the model

Repeated observations share a common session-level error source. Is a diagonal weight matrix sufficient by default?

**Worked guidance:** Not if the shared source induces material correlation. A covariance model that represents the shared component may be more appropriate, provided its structure and magnitude are supported by acquisition and processing evidence.

## 15. Connections and next steps

- **Module 03 — Linear systems, elimination, rank and null spaces:** provides consistency, rank and datum-defect concepts.
- **Module 05 — Inner products, norms, orthogonality and projections:** provides the geometric interpretation of least squares.
- **Module 07 — Symmetric matrices, quadratic forms and definiteness:** develops the matrix structure of the least-squares objective and covariance.
- **Module 09 — Matrix factorizations:** develops QR, Cholesky and SVD approaches used in stable computation.
- [Covariance and generalized least squares implementation](../../implementations/python/covariance-gls/README.md) provides dependency-free educational solvers and synthetic examples.
- [Measurement science and survey adjustment learning path](../../learning-paths/measurement-science-and-survey-adjustment.md) connects the mathematics to the repository's synthetic experiments.

The Python implementation's unconstrained GLS solver requires positive-definite observation covariance and full-column-rank design. Its exact-constraint solver can accommodate design rank defects only when the exact constraints remove them and the KKT system is nonsingular. Neither implementation silently regularises singular observation covariance.

## References

- Massachusetts Institute of Technology, Department of Mathematics. [18.06 Linear Algebra — OpenCourseWare, Spring 2010](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/). Course scope includes least squares, projections and constrained systems.
- Strang, G. (2021). [Lecture Notes for Linear Algebra](https://www-math.mit.edu/~gs/LectureNotes/). MIT-hosted notes on least squares and linear algebra.

**Source note:** These references are linked for human study. The MIT course identity and topic coverage are recorded in the repository source register; individual lectures and notes have not been reviewed claim by claim. This module presents original explanations and synthetic examples rather than reproducing course text, figures or exercises.

**Scope:** linear observation models, ordinary and weighted least squares, generalized least squares with positive-definite observation covariance, rank and identifiability, exact linear constraints, inner datum constraints, KKT formulation and conditional formal covariance. Nonlinear adjustment, robust estimation, variance-component estimation, singular covariance and numerical solver theory are deferred.
