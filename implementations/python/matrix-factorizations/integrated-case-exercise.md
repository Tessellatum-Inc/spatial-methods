# Practical exercise: from local control to a covariance-aware terrain model

**Level:** intermediate undergraduate to postgraduate  
**Estimated time:** 2–3 hours  
**Prerequisites:** matrix multiplication, linear systems, least squares, covariance matrices and basic Python/NumPy  
**Data:** entirely synthetic and dimensionless

This exercise uses the [integrated case implementation](integrated_case.py). Work through the learner tasks before opening the worked interpretation. The objective is not just to obtain coefficients: it is to justify the solver, inspect the assumptions and explain what the diagnostics do—and do not—establish.

## Scenario

A small hypothetical mapping team has three local control points with corresponding mapped coordinates. It also has twelve synthetic elevation observations over the same local area. You are asked to:

- derive the local-to-map affine transformation;
- fit a planar terrain approximation;
- examine how an assumed correlated-error model changes the estimate;
- assess whether the fitted design is numerically estimable.

No actual survey, CRS, instrument or site is represented.

## Learner tasks

### Part A — Control transformation and LU

The local control coordinates are:

| Point | Local x | Local y | Map X | Map Y |
|---|---:|---:|---:|---:|
| C1 | 0 | 0 | 500.0 | 1000.0 |
| C2 | 10 | 0 | 510.2 | 1001.0 |
| C3 | 0 | 8 | 499.2 | 1008.4 |

1. Write the affine equations for (X) and (Y), including translation terms.
2. Construct the (3\times3) design matrix and the two right-hand-side vectors.
3. Solve each square system using pivoted LU. State why LU is appropriate here.
4. Recover the six affine parameters and transform at least two sample points from the implementation.
5. Explain why three non-collinear control pairs determine the six parameters but provide no redundancy for checking the transformation.
6. Inspect the control-design condition number. What does it tell you, and why is it not a universal accuracy score?

### Part B — Terrain plane and QR

The transformed sample coordinates are used in the model

[
z_i = a + bX_i + cY_i + \varepsilon_i.
]

1. Identify the design matrix columns and the unknown parameter vector.
2. Solve the ordinary least-squares problem using QR. Do not form (A^TA) or explicitly invert a matrix.
3. Report the intercept and two gradients.
4. Explain the geometric meaning of the OLS residual orthogonality condition (A^T r=0).
5. Compare the fitted coefficients with the generating plane ([80, 0.12, -0.07]^T). Why should the estimated values not be expected to match exactly?

### Part C — Correlated errors and Cholesky/GLS

The example assumes an observation covariance

[
\Sigma_{ij}=\sigma^2\rho^{|i-j|},
\qquad \sigma=0.03,\quad \rho=0.45.
]

1. Explain what the diagonal and off-diagonal entries represent.
2. Why is Cholesky factorization suitable for this covariance matrix?
3. Show how solving (L\widetilde A=A) and (L\widetilde z=z), where (LL^T=\Sigma), converts GLS into an OLS problem in whitened coordinates.
4. Report the GLS coefficients and compare them with the OLS coefficients.
5. Compare raw residual RMS values. Explain why a smaller raw RMS is not, by itself, proof that one estimator is better.
6. Critique the covariance assumption. In particular, what is questionable about defining correlation by sample order rather than spatial separation?

### Part D — SVD and numerical diagnostics

1. Inspect the singular values of the whitened design matrix.
2. Calculate its numerical rank using the tolerance stated in the implementation.
3. Calculate the 2-norm condition number from the largest and smallest singular values.
4. Explain the difference between full numerical rank, identifiability and parameter precision.
5. Explain why changing coordinate units or centring/scaling columns can change the condition number without changing the underlying physical problem.
6. Name at least three additional checks needed before treating a real terrain or survey solution as trustworthy.

## Submission checklist

- [ ] Affine equations and control design matrix.
- [ ] LU solution and control-geometry interpretation.
- [ ] QR plane estimate and residual orthogonality explanation.
- [ ] GLS derivation and covariance critique.
- [ ] SVD singular values, rank tolerance and condition number.
- [ ] A short paragraph separating mathematical output from real-world validity.

## Worked solution and interpretation

### A. Affine model

Use

[
X_i=t_x+a_xx_i+b_xy_i,\qquad
Y_i=t_y+a_yx_i+b_yy_i.
]

With columns ([x_i,y_i,1]), the common design matrix is

[
C=\begin{bmatrix}
0&0&1\\
10&0&1\\
0&8&1
\end{bmatrix}.
]

Solving the two right-hand sides gives

[
[a_x,b_x,t_x]^T=[1.02,-0.10,500]^T,
]
[
[a_y,b_y,t_y]^T=[0.10,1.05,1000]^T.
]

Thus (X=500+1.02x-0.10y) and (Y=1000+0.10x+1.05y). The matrix is nonsingular because the three local points are non-collinear. But three points for six affine parameters leave zero residual degrees of freedom: the transformation interpolates the controls exactly and cannot independently reveal a bad control point or model misspecification.

The control-design condition number is approximately **10.18** in the stated coordinate scale. It describes numerical sensitivity of this particular parameterisation; it does not measure map accuracy or control quality. Centring/scaling and coordinate units affect its value.

### B. QR plane fit

The implementation builds (A=[\mathbf{1},X,Y]) and solves (\min_\beta\|A\beta-z\|_2) by reduced QR. The fitted OLS coefficients are approximately

[
[81.5001263,;0.120285637,;-0.0716342167]^T.
]

The generating plane was ([80,0.12,-0.07]^T), but the observations include a fixed nonzero error pattern. Least squares estimates the best-fitting plane for those observations; it does not remove the errors or guarantee recovery of the generating parameters in one finite sample.

At the least-squares solution, each design column is orthogonal to the residual vector, so (A^Tr\approx0), up to floating-point error.

### C. GLS interpretation

The assumed covariance is positive definite for the selected (\sigma>0) and (|\rho|<1), so it admits a Cholesky factor (L). Since (\Sigma=LL^T),

[
(A\beta-z)^T\Sigma^{-1}(A\beta-z)
=\|L^{-1}(A\beta-z)\|_2^2.
]

Therefore QR can solve the whitened least-squares problem without explicitly forming (\Sigma^{-1}). The resulting GLS coefficients are approximately

[
[83.3850848,;0.119566374,;-0.0731478319]^T.
]

OLS raw residual RMS is approximately **0.01546**; GLS raw residual RMS is approximately **0.01612**. The GLS raw RMS is slightly larger, which is not a failure: GLS minimises a covariance-weighted quadratic criterion, not unweighted raw residual RMS. The whitened residual norm is approximately **2.6401**.

The AR(1)-style covariance here correlates observations by their row order. Unless row order represents a meaningful temporal or spatial sequence, that is an artificial teaching assumption. A real spatial covariance model would need defensible separation metrics, a justified covariance family, parameter estimation or external support, and diagnostic validation.

### D. SVD and numerical rank

The whitened-design singular values are approximately

[
[8.52293\times10^4,;3.60686\times10^2,;2.11403\times10^{-1}].
]

With tolerance

[
\tau=\epsilon_{machine}\max(m,n)\sigma_{max},
]

the tolerance is approximately (2.27\times10^{-10}), and the computed numerical rank is **3**. The 2-norm condition number is approximately **403,161**. The matrix is full rank under this threshold, yet its columns are substantially differently scaled and the model is numerically sensitive in the stated parameterisation.

Full rank says the columns are independent under a selected numerical threshold. Identifiability concerns whether parameters are uniquely determined by the model and data structure. Precision additionally depends on observation noise, covariance, design geometry, units and model validity. These are related but not interchangeable concepts.

Further checks for a real application would include redundant independent control/check points, CRS and datum validation, coordinate-unit and axis-order checks, residual maps and outlier investigation, covariance-model diagnostics, uncertainty propagation, and an appropriate terrain-model assessment.

## Suggested marking guide (20 points)

| Criterion | Points |
|---|---:|
| Correct affine model, LU setup and no-redundancy explanation | 4 |
| Correct QR formulation, estimate and residual geometry | 4 |
| Correct GLS whitening derivation and covariance critique | 5 |
| SVD rank/conditioning calculation and interpretation | 4 |
| Clear distinction between synthetic mathematical result and real-world validity | 3 |

**Instructor note:** accept equivalent numerical results within reasonable floating-point tolerances. Reward explicit assumptions and defensible interpretation more than matching rounded digits. The worked values are reference outputs from the deterministic implementation, not field tolerances or acceptance thresholds.

## Further reading

- [Integrated case implementation](integrated-case.md)
- [Runnable Python script](integrated_case.py)
- [Automated tests](test_integrated_case.py)
- [Matrix factorization foundation](../../../foundations/linear-algebra/matrix-factorizations-lu-qr-cholesky-svd.md)
- [Covariance and multivariate structure](../../../foundations/linear-algebra/covariance-matrices-and-multivariate-structure.md)
