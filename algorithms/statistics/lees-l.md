# Lee's L: do two variables share the same spatial pattern?

Stable ID: SA-STAT-LEES-L · Draft 0.1 · Source compendium section 2, page 2

## The question

Pearson's correlation describes how two variables vary together at the same locations. It does not tell us whether their geographical patterns also correspond. Lee's L combines point-to-point association with the spatial structure of both variables.

For example, income and access to healthcare might be positively correlated across districts. But do their neighbourhood-smoothed maps also correspond, and do both variables retain meaningful spatial structure after smoothing?

## What Lee's L measures

Lee's L is a global bivariate spatial association statistic. Its construction combines spatial smoothing of the first variable, spatial smoothing of the second variable, and the Pearson correlation between the two spatially lagged variables.

This differs from bivariate Moran's I, which relates one variable at each location to the spatial lag of the other. Lee's L uses both spatial lags.

## Formula

Let x and y be finite variables observed at the same n spatial units. Let W be a row-standardized spatial weights matrix, and let the spatial lags be W x and W y.

The row-standardized form in Lee (2001), equations 13–14, is:

~~~text
L_xy = sum_i[(Wx_i - mean(x)) (Wy_i - mean(y))]
       / sqrt(sum_i(x_i - mean(x))^2 * sum_i(y_i - mean(y))^2)
~~~

The centring convention follows Lee's original derivation. For row-standardized weights with no islands, each row sums to one.

The spatial smoothing scalars are:

~~~text
SSS_x = sum_i(Wx_i - mean(x))^2 / sum_i(x_i - mean(x))^2
SSS_y = sum_i(Wy_i - mean(y))^2 / sum_i(y_i - mean(y))^2
~~~

Lee relates L to the product of the square roots of the two smoothing scalars and the correlation between the lagged variables. The decomposition has mean-alignment conditions; the direct formula above is the implementation target.

## Interpretation

- Positive L: the two spatially smoothed variables tend to co-vary in the same direction.
- Negative L: their smoothed patterns tend to vary in opposite directions.
- Near-zero L: little global co-patterning under the selected weights and study design.

Do not treat the sign or magnitude as a universal threshold for significance. Results depend on the variables, spatial units, neighbourhood definition and weights transformation. A global statistic can conceal local regimes.

## Why this is not bivariate Moran's I

Bivariate Moran's I uses a cross-product such as x'Wy. Lee's L uses the product of both spatial lags, (Wx)'(Wy), scaled by the original variables' sums of squares. Lee's construction therefore includes the smoothing behaviour of both variables. The two statistics answer related but different questions.

## Implementation contract

The accompanying Python implementation requires finite equal-length vectors with non-zero variance, and a finite non-negative square weights matrix aligned to the vectors. It rejects self-weights and islands, row-standardizes a copy of the input matrix, calculates the global statistic from Lee (2001), and reports both smoothing scalars as diagnostics.

It does not calculate a p-value or claim inferential significance. This is a transparent dense-matrix teaching implementation, not a replacement for a full spatial-statistics package.

## Runnable material

- [Interactive Jupyter lab](../../notebooks/lees-l-lab.ipynb)
- [Python implementation](../../implementations/python/lees-l/README.md)
- [Implementation walkthrough](../../implementations/python/lees-l/implementation-walkthrough.md)
- [Tests](../../implementations/python/lees-l/test_lees_l.py)

## References

- Lee, S.-I. (2001). Developing a bivariate spatial association measure: An integration of Pearson's r and Moran's I. Journal of Geographical Systems, 3, 369–385. https://doi.org/10.1007/S101090100064
- [Original paper PDF](https://sangillee.snu.ac.kr/papers/2001_02_JGS_Lee.pdf), especially equations 12–20.
- [spdep Lee statistic documentation](https://r-spatial.github.io/spdep/reference/lee.html), a maintained implementation with its own documented computational convention.
- [ArcGIS Pro: How Lee's L works](https://doc.esri.com/en/arcgis-pro/latest/tool-reference/spatial-statistics/how-bivariate-spatial-association-works.html), including a distinct global/local presentation.

## Scope note

Software packages document formulas and normalizations that are not always presented identically. This lesson names its precise equation and weights contract rather than implying byte-for-byte equivalence with every implementation. Local Lee's L, permutation inference, alternative kernels and general non-row-standardized weights remain separate work.

## Change history

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-11-15 | Initial source-grounded global statistic lesson and tested teaching implementation |
