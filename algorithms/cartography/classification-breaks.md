# Classification breaks for thematic mapping

Classification turns a continuous spatial attribute into discrete map classes. The method changes the visual story: equal-width, distribution-aware, quantile and variance-based breaks answer different questions. No classifier repairs poor data, chooses a meaningful number of classes automatically or makes an unsuitable variable suitable for choropleth mapping.

## Implemented methods

| Method | Principle | Important qualification |
|---|---|---|
| Geometric interval | Equal ratios between positive minimum and maximum | Requires strictly positive data; unsuitable for zero/negative values |
| Standard deviation | Mean plus/minus integer multiples of population standard deviation | Boundaries are clipped to observed minimum/maximum |
| Box plot | Quartiles, median and Tukey 1.5-IQR fences | Outlier-aware descriptive classes, not an optimisation objective |
| Head/tail breaks | Recursively split heavy-tailed values at the current mean | Meaningful only when a heavy-tailed pattern is present |
| Dalenius–Hodges | Equalise cumulative square-root histogram frequencies | Approximate; results depend on histogram binning |
| ckmeans | Dynamic programming minimises within-class squared deviations | Exact 1D partition for chosen k; O(km²) with m distinct values |

## ckmeans objective

For sorted unique values with multiplicities, the algorithm partitions the values into k contiguous groups and minimises the sum of within-class squared deviations. Prefix sums of counts, values and squared values make each candidate interval cost O(1). Dynamic programming evaluates all previous cut positions. The transparent implementation is O(km²), where m is the number of distinct observed values.

## Choosing responsibly

Use geometric intervals for positive multiplicative scales; standard-deviation classes when distance from the mean is meaningful; box-plot classes to expose quartiles and potential outliers; head/tail breaks only after inspecting for a heavy-tailed pattern; Dalenius–Hodges as a histogram-dependent approximation; and ckmeans when minimising within-class squared error is the explicit objective.

The source also lists “maximum breaks” and “pretty breaks”. These names require identity and specification review before implementation; they are not silently treated as synonyms for ckmeans or Jenks natural breaks.

## Verification

Tests cover positivity, observed-range clipping, quartiles/Tukey fences, recursive heavy-tail splits, Dalenius–Hodges ordering, constant data, validation and ckmeans partitions against an independent exhaustive partition oracle.

## References

- Dalenius, T. and Hodges, J. L. (1959). Minimum variance stratification. *Journal of the American Statistical Association*.
- Wang, H. and Song, M. (2011). Ckmeans.1d.dp: optimal k-means clustering in one dimension by dynamic programming. *The R Journal*.
- Jiang, B. (2013). Head/tail breaks: a new classification scheme for data with a heavy-tailed distribution. *The Professional Geographer*.

See the [tested Python implementation](../../implementations/python/classification-breaks/README.md).
