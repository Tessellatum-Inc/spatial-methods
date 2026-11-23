# Verification — numeric map classification

- Source: Section 9, page 19, classification row.
- Methods: equal interval, empirical quantile interpolation, exact Fisher-Jenks
  dynamic programming and explicit interval assignment.
- Tests: known equal-width boundaries, interpolated quantiles, a separated
  two-cluster Jenks example, duplicate values, one-class case and invalid input.
- Complexity: Jenks O(k n²) time and O(k n) memory.
- Open: Jenks algorithm identity/bibliography audit, optimal class-count
  selection, perceptual color scales, bivariate choropleths and spatially
  constrained classification.
- Status: partial contribution to grouped source entry.
