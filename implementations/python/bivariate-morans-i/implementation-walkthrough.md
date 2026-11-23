# Bivariate Moran's I: implementation walkthrough

The implementation makes the asymmetric relationship between a variable and the spatial lag of another variable explicit.

## 1. Validate the observations

Both vectors are converted to finite floats. They must have equal length, contain at least two values and have non-zero sample variance. The vectors must be aligned to the same spatial-unit order as the rows and columns of W.

## 2. Standardize each variable

For each vector, subtract its mean and divide by its sample standard deviation. With this convention, the sum of squared standardized values is n - 1.

## 3. Validate and row-standardize W

The weights matrix must be square, finite and non-negative. Self-weights are rejected. Each nonzero row is divided by its sum; an island remains a zero row. Row standardization is part of this implementation's declared model, not a universal requirement for every bivariate Moran analysis.

## 4. Form the spatial lag of y

For each unit i:

```
(W z_y)_i = sum_j w_ij z_y_j
```

This is the weighted neighbourhood average of the second variable's standardized values.

## 5. Calculate the statistic

```
I_xy = sum_i z_x_i (W z_y)_i / (n - 1)
```

The denominator follows from sample standardization of x. The statistic is directional: I_xy and I_yx need not be equal, especially for asymmetric weights.

## 6. Conditional randomization

When permutations are requested, x and W remain fixed and the standardized y values are shuffled across locations. Each shuffled statistic is recalculated. The package reports the simulated mean, variance, standard deviation, z-score and a two-sided pseudo-p-value centred on the simulated mean, using the +1 correction.

This is a conditional randomization scheme. It is not a spatial block permutation, a model-based bootstrap or a causal test. Spatial dependence and the substantive null hypothesis must be considered before interpreting the p-value.

## 7. Test coverage

The tests include:
- a hand-checkable two-unit case;
- row standardization and islands;
- directional asymmetry;
- seeded permutation reproducibility and p-value bounds;
- invalid dimensions, constant variables, self-weights, empty weights and non-finite values;
- the no-permutation return contract.

Run `python -m pytest -q` from this directory. The tests verify this declared implementation contract, not the suitability of a real study's spatial weights or null model.
