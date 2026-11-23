# Local Moran's I with conditional permutation inference

## Purpose

Local Moran statistics identify where a global spatial pattern is concentrated: high values surrounded by high values (HH), low surrounded by low (LL), and spatial outliers (HL or LH). These labels are descriptive quadrant classifications; significance must be assessed separately.

## Statistic

Let \(z_i=x_i-\bar{x}\), \(m_2=n^{-1}\sum_i z_i^2\), and let \(w_{ij}\) be the supplied spatial weights. The local statistic is

\[
I_i=\frac{z_i}{m_2}\sum_j w_{ij}z_j.
\]

Under conditional randomization, the focal value \(z_i\) is held fixed and the remaining values are permuted over all other locations. For a zero-diagonal weights matrix, the conditional expectation is

\[
E[I_i\mid z_i]= -\frac{z_i^2}{(n-1)m_2}\sum_jw_{ij}.
\]

This expression accommodates non-row-standardized weights. An island (a zero-sum row) has no local statistic test and receives a NaN p-value.

## Inference and multiplicity

For each non-island location, the implementation holds the focal observation and weights row fixed, permutes all other centred observations, and recomputes \(I_i\). The Monte Carlo p-value uses \((b+1)/(B+1)\). The two-sided test measures absolute deviation from the conditional expectation; one-sided alternatives compare simulated statistics directly with the observed statistic.

By default, Benjamini–Hochberg adjusted p-values control the false discovery rate under their usual dependence conditions. The family comprises non-island locations with valid permutation tests. Set `adjustment="none"` to retain raw Monte Carlo p-values. HH/LL/HL/LH labels are emitted only when the adjusted p-value is at most the chosen alpha.

## Implementation

Runnable reference: [local_morans_i_permutation.py](../../implementations/python/spatial-econometrics/local_morans_i_permutation.py).

## Assumptions and limits

- Conditional randomization assumes the non-focal observations are exchangeable across the remaining locations under the null. This is not automatically suitable for trends, covariate-adjusted nulls, clustered sampling or unequal measurement precision.
- Local tests are dependent because neighbourhoods overlap. BH has formal guarantees under independence and certain positive-dependence structures; its interpretation under arbitrary spatial dependence requires care. Consider the more conservative Benjamini–Yekutieli procedure where arbitrary dependence control is required.
- The implementation does not compute a Benjamini–Yekutieli correction, local pseudo-z scores, or analytic normal approximations.
- The supplied weights are not symmetrised or row-standardised. Their construction, direction and scaling affect local statistics.
- Local significance is not a causal explanation, and the four quadrant labels are not evidence of a mechanism.
- The dense reference implementation is intended for teaching-scale matrices; runtime grows approximately with the number of locations squared times the number of permutations.

## Validation

Tests independently reconstruct the local statistics, conditional permutation distribution, and BH adjustment; cover islands and asymmetric weights; and reject invalid inputs. Run `python -m pytest -q`.

## References

- Anselin, L. (1995). Local indicators of spatial association—LISA. *Geographical Analysis*, 27(2), 93–115.
- Sokal, R. R., Oden, N. L., & Thomson, B. A. (1998). Local spatial autocorrelation in biological variables. *Biological Journal of the Linnean Society*, 65(3), 239–261.
