# Numeric map classification

Classification converts a continuous numeric attribute into ordered classes.
The algorithm and boundary convention affect the resulting map; class labels
should not imply natural discontinuities where none exist.

- **Equal interval** divides the observed range into k intervals of equal width.
- **Quantile** places approximately equal numbers of observations in each class
  using empirical quantile boundaries. Ties can produce repeated boundaries
  and empty classes.
- **Fisher-Jenks natural breaks** chooses contiguous classes that minimize the
  sum of within-class squared deviations. The exact dynamic program is
  O(k n²), so it is a small-to-medium teaching baseline rather than a
  large-data implementation.

The companion implementation uses finite values, returns k+1 boundaries and
assigns a value equal to an interior upper boundary to the lower class. These
choices must be stated when comparing maps. The code does not choose k, account
for spatial autocorrelation, optimize perceptual color ramps or create
bivariate classifications.

See the tested [Python implementation](../../implementations/python/map-classification/README.md).
