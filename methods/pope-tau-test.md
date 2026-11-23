# Pope's tau test for geodetic outlier detection

## Purpose

Baarda-style data snooping standardises residuals using an a-priori variance factor. When that variance factor is not known reliably, Pope's tau test estimates it from the same least-squares adjustment and uses the resulting internally studentized residuals.

For the linear Gauss–Markov model

\[
\mathbf l=\mathbf A\mathbf x+\mathbf e,\qquad
\operatorname{Cov}(\mathbf e)=\sigma_0^2\mathbf Q_{ll},
\]

let \(\mathbf v=\mathbf l-\mathbf A\hat{\mathbf x}\), \(\mathbf Q_{vv}\) be the residual cofactor matrix, and \(r=m-\operatorname{rank}(\mathbf A)\) the residual degrees of freedom. Estimate the variance factor by

\[
\hat\sigma_0^2=\frac{\mathbf v^T\mathbf Q_{ll}^{-1}\mathbf v}{r}.
\]

The individual internally studentized residual is

\[
T_i=\frac{|v_i|}{\hat\sigma_0\sqrt{q_{vv,ii}}}.
\]

The tau distribution is related to Student's t. For a Student critical value \(t\) with \(r-1\) degrees of freedom,

\[
\tau_{crit}=\frac{\sqrt r\,t}{\sqrt{r-1+t^2}}.
\]

## Implemented scope

The NumPy/SciPy implementation reuses the weighted linear adjustment and accepts a full positive-definite observation cofactor/covariance matrix. It uses a two-sided Bonferroni allocation \(\alpha/(2m)\) across the \(m\) tested residuals, giving a conservative family-wise threshold. It reports every flagged index, the maximum absolute tau statistic, estimated variance factor and critical values.

The function requires at least two residual degrees of freedom. A perfect fit with effectively zero estimated variance is returned as zero_residual_variance; it is not misreported as a successful outlier test. Observations with zero residual redundancy have undefined individual statistics and are returned as NaN.

This is a single-adjustment test. It does not automatically remove observations, iterate after deletion, resolve multiple-outlier masking/swamping, or establish the physical cause of an outlier. Inspect flagged observations and the model before any re-adjustment.

## Reproduction

Run from implementations/python/helmert-7-parameter:

~~~bash
python -m pip install -r requirements.txt
python -m pytest -q
~~~

## References

- Pope, A. J. (1976). *The Statistics of Residuals and the Detection of Outliers*. NOAA Technical Report NOS NGS 65-1. https://repository.library.noaa.gov/view/noaa/30811.
- U.S. Army Corps of Engineers (2018). *EM 1110-2-1009: Structural Deformation Surveying*, section 9-14, equations 9-6 and 9-7. https://www.publications.usace.army.mil/portals/76/publications/engineermanuals/em_1110-2-1009.pdf.
- Deakin, R. E. & Hunter, M. N. (2018, corrected 2021). *Tau Distribution and Testing Residuals*. https://www.mygeodesy.id.au/documents/Tau%20distribution.pdf.

The implementation is original and uses synthetic test data; no source code, figures or observation data are reproduced.
