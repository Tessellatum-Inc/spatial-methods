# Bivariate Moran's I: how does one variable relate to its neighbours' values of another?

Stable ID: `SA-STAT-BIVARIATE-MORANS-I` · Draft 0.1 · Source compendium section 2, pages 2–3

## The question

Suppose each district has both a median income and a health outcome. Do districts with higher income tend to be surrounded by districts with higher (or lower) health outcomes? Bivariate Moran's I measures a global cross-variable spatial association.

This is not the same as univariate Moran's I. It relates a variable at each location to the spatial lag of a second variable.

## Definition

Let x and y be two numeric variables observed for the same n spatial units, in exactly the same order. Let z_x and z_y be their sample-standardized values, and let W be a spatial weights matrix.

The bivariate statistic used in the accompanying implementation is:

```
I_xy = (z_x' W z_y) / (n - 1)
```

Equivalently, it is the slope of the regression of z_x on the spatial lag W z_y when the variables are sample-standardized. The order matters: I_xy is not generally equal to I_yx.

The implementation row-standardizes W, requires non-negative weights and a zero diagonal, and leaves zero rows as islands. Other weight transformations define different statistics and should be reported explicitly.

## Conditional permutation inference

The reference implementation optionally holds x and W fixed and permutes y across spatial units. It recalculates I_xy for each permutation and reports a two-sided pseudo-p-value based on absolute deviations from the simulated mean, with the +1 correction:

```
p = (1 + count(|I_sim - mean(I_sim)| >= |I_obs - mean(I_sim)|)) / (M + 1)
```

This is one explicit conditional-randomization convention, not a universal default. Other libraries expose different alternative/tail conventions. Choose and state the null hypothesis before interpreting the result. A small p-value does not establish causation or remove confounding between x and y.

## Worked two-unit check

For two units linked only to each other, with x = y = [0, 1], each standardized vector is [-1/sqrt(2), 1/sqrt(2)]. The spatial lag reverses the two values, so the statistic is -1. This tiny example is useful for checking the sign and normalization.

## Assumptions and limitations

- Both variables describe the same spatial units and are aligned to the same row/column order.
- The weights matrix represents a defensible spatial relationship; row standardization does not make a poor weights design valid.
- The statistic is global and can hide local variation.
- Results depend on the chosen weights, study area, spatial units and permutation design.
- The teaching implementation uses a dense matrix and is intended for small examples, not large sparse spatial graphs.
- The conditional permutation procedure is not a block bootstrap and does not account automatically for temporal dependence or covariates.

For local bivariate clusters, use a separately specified local statistic and inference procedure; do not infer local patterns from this global value.

## Runnable material

- [Interactive Jupyter lab](../../notebooks/bivariate-morans-i-lab.ipynb)
- [Python implementation](../../implementations/python/bivariate-morans-i/README.md)
- [Implementation walkthrough](../../implementations/python/bivariate-morans-i/implementation-walkthrough.md)
- [Tests](../../implementations/python/bivariate-morans-i/test_bivariate_morans.py)

## References

- Anselin, L. (1995). Local Indicators of Spatial Association—LISA. *Geographical Analysis*, 27(2), 93–115. https://doi.org/10.1111/j.1538-4632.1995.tb00338.x
- PySAL, [esda.Moran_BV reference](https://pysal.org/esda/stable/generated/esda.Moran_BV.html), including variable standardization, weights transformations and conditional permutation inference.
