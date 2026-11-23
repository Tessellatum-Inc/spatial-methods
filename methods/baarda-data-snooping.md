# Baarda-style data snooping for geodetic least-squares adjustment

## Model and adjustment

For a linear Gauss–Markov observation model

\[
l=A x+e,\qquad \operatorname{Cov}(e)=\sigma_0^2 Q_{ll},
\]

the weighted least-squares estimate is

\[
\hat x=(A^TQ_{ll}^{-1}A)^{-1}A^TQ_{ll}^{-1}l.
\]

The residual vector and its cofactor matrix are

\[
v=l-A\hat x,\qquad Q_{vv}=Q_{ll}-A(A^TQ_{ll}^{-1}A)^{-1}A^T.
\]

The global quadratic statistic is

\[
T=\frac{v^TQ_{ll}^{-1}v}{\sigma_0^2},
\]

with \(m-n\) degrees of freedom when the design has full column rank. A formal global test compares this statistic with a chi-square critical value at a stated significance level.

## Local data snooping

For known a-priori variance factor, the Baarda-style standardized residual is

\[
w_i=\frac{v_i}{\sigma_0\sqrt{q_{vv,ii}}}.
\]

The implementation returns all local w statistics, residual redundancy numbers, the largest absolute statistic, and indices exceeding a caller-supplied critical value. The critical value is deliberately supplied by the user: a family-wise or other multiple-testing policy should be chosen explicitly rather than hidden in the library. The module also supports a full positive-definite observation covariance/cofactor matrix, not just independent equal-variance observations.

## Important interpretation

The global test detects overall model inconsistency; local data snooping attempts to identify a suspect observation after an overall rejection. A large standardized residual is evidence for investigation, not proof of a blunder. Classical single-outlier data snooping can be weakened by multiple simultaneous outliers, masking, swamping, low redundancy and model misspecification. Re-estimate only after an explicit decision about an observation; automatic deletion is not implemented here.

The current code is a transparent single-adjustment baseline. Pope's internally studentized residual test for an estimated variance factor is implemented separately in the Pope tau lesson. Baarda's full alternative-hypothesis/reliability design, iterative data snooping, robust M-estimation, RANSAC, free-network datum constraints and nonlinear adjustment remain outside this package.

## Reproduction

Run from implementations/python/helmert-7-parameter:

~~~bash
python -m pip install -r requirements.txt
python -m pytest -q
~~~

## References

- Baarda, W. (1968). *A Testing Procedure for Use in Geodetic Networks*. Netherlands Geodetic Commission, Publications on Geodesy, New Series, Vol. 2, No. 5.
- Kok, J. J. (1982). *On Data Snooping and Multiple Outlier Testing*. NOAA Technical Report NOS NGS 30.
- Schwarz, C. R., & Kok, J. J. (1993). Blunder Detection and Data Snooping in LS and Robust Adjustments. *Journal of Surveying Engineering*, 119(4), 127–135. DOI: 10.1061/(ASCE)0733-9453(1993)119:4(127).

This lesson paraphrases the statistical procedure; it reproduces no source code, figures, tables or observation data.
