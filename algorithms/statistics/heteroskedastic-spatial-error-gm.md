# Heteroskedastic spatial-error generalized moments

## Model and scope

Consider a spatial autoregressive disturbance process

\[
u=\lambda Wu+\varepsilon,
\]

where the innovations are mutually independent, have zero means, and may have unknown observation-specific variances. A caller supplies a consistent predictor \(\tilde u\) of the regression disturbance. This record covers the disturbance-parameter moment stage only; it does not claim to be a complete SARAR estimator.

The homoskedastic Kelejian–Prucha (1999) estimator uses three moments involving the innovation variance. Those restrictions cannot simply be reused when innovation variances differ across observations. Kelejian and Prucha (2010) instead construct two quadratic restrictions whose inner matrices have zero diagonal, eliminating the unknown diagonal variance contribution.

## Heteroskedasticity-robust moment restrictions

Write \(\varepsilon=(I-\lambda W)u\) and \(\bar\varepsilon=W\varepsilon\). Under independent innovations with diagonal covariance \(\Sigma\),

\[
\frac{1}{n}E(\bar\varepsilon'\bar\varepsilon)
=\frac{1}{n}\operatorname{tr}(W\Sigma W'),
\qquad
\frac{1}{n}E(\bar\varepsilon'\varepsilon)=0.
\]

The first restriction subtracts the diagonal variance contribution. Define

\[
A_1=W'W-\operatorname{diag}(\operatorname{diag}(W'W)),
\qquad A_2=W.
\]

Both matrices have zero diagonal. The two moments can be written as

\[
\frac{1}{n}E
\begin{bmatrix}
\varepsilon'A_1\varepsilon\\
\varepsilon'A_2\varepsilon
\end{bmatrix}=0.
\]

For a residual predictor \(\tilde u\), set \(v=W\tilde u\), \(w=Wv\), and \(d_i=\sum_j w_{ji}^2\). Expanding the sample moments in \(\lambda\) gives

\[
\tilde\gamma-\tilde\Gamma
\begin{bmatrix}\lambda\\\lambda^2\end{bmatrix},
\]

where

\[
\tilde\gamma_1=n^{-1}\left(v'v-\sum_i d_i\tilde u_i^2\right),
\qquad
\tilde\gamma_2=n^{-1}v'\tilde u,
\]

and

\[
\tilde\Gamma=\frac{1}{n}
\begin{bmatrix}
2(v'w-\sum_i d_i\tilde u_i v_i)
&
-(w'w-\sum_i d_i v_i^2)\\
v'v+w'\tilde u
&
-w'v
\end{bmatrix}.
\]

The implementation minimises the squared Euclidean norm of these two residual moments over a caller-supplied admissible interval. Identity weighting is a simple consistent starting choice; it is not the optimally weighted estimator.

## Interpretation and limitations

- The zero-diagonal construction removes the unknown innovation-variance contribution from the expectations of the quadratic moments, provided innovations are independent and the maintained spatial-process regularity conditions hold.
- The moment matrix must identify \(\lambda\); a numerical rank check is necessary but does not establish the full asymptotic identification conditions.
- The input must be a sufficiently accurate predictor of the structural disturbance. Supplying ordinary OLS residuals is not automatically appropriate when the regression includes an endogenous spatial lag; a consistent IV-based predictor may be needed.
- This reference implementation estimates the disturbance coefficient only. It does not estimate regression coefficients, implement feasible generalized 2SLS, calculate the full joint asymptotic covariance, or provide standard errors and tests.
- The optimization interval must lie strictly inside a conservative nonsingularity interval for \(I-\lambda W\). Dense eigenvalue calculations and grid-plus-golden-section optimisation target small teaching examples.

## Implementation

The NumPy implementation is `implementations/python/spatial-econometrics/heteroskedastic_spatial_error_gm.py`. It returns the moment-based estimate, objective, two residual moments and the estimated moment coefficients.

## References

- Kelejian, H. H., & Prucha, I. R. (2010). Specification and estimation of spatial autoregressive models with autoregressive and heteroskedastic disturbances. *Journal of Econometrics*, 157(1), 53–67. https://doi.org/10.1016/j.jeconom.2009.10.025.
- Kelejian, H. H., & Prucha, I. R. (1999). A generalized moments estimator for the autoregressive parameter in a spatial model. *International Economic Review*, 40(2), 509–533.
