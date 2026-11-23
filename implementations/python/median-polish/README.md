# Tukey median polish

Dependency-free robust additive decomposition of a two-way table into an overall effect, row effects, column effects and residuals.

## Quick start

~~~python
from median_polish import median_polish
deaths = [
    [14, 15, 14],
    [7, 4, 7],
    [8, 2, 10],
    [15, 9, 10],
    [0, 2, 0],
]
result = median_polish(deaths)
print(result["overall"])
print(result["row_effects"])
print(result["column_effects"])
print(result["residuals"])
~~~

## Method

Median polish fits an additive model y_ij = overall + row_i + column_j + residual_ij. It alternately subtracts row and column medians from the residual table, accumulates the effects, and recentres row and column effects by their medians. Convergence follows the proportional reduction in the sum of absolute residuals, matching the documented R stats::medpolish criterion.

Missing cells are rejected by default. With na_rm=True, they are ignored when computing medians and remain None in the residual matrix. All-missing rows or columns receive zero effect.

## Scope

This is a robust two-way additive decomposition, not a spatial smoother that uses coordinates or neighbourhoods. It does not include interactions, weights, multiway arrays, inference, uncertainty or a spatial covariance model.
