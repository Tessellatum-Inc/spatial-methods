# Tukey median polish

Robustly decompose a two-way table into an overall effect, row effects, column effects and residuals. Median polish alternately removes row and column medians, recentres effects, and iterates until the proportional reduction in absolute residual sum is below a tolerance.

The [Python implementation](../../implementations/python/median-polish/README.md) supports missing values when explicitly requested and reports convergence history.

This is a two-way additive table method, not a coordinate-based spatial smoother. It does not include weights, interactions, multiway arrays or inference.

## Reference

Tukey (1977), *Exploratory Data Analysis*; R stats::medpolish documentation.
