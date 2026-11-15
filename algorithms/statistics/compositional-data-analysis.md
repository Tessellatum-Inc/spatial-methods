# Compositional data analysis: closure and log-ratio transforms

Compositions describe relative parts of a whole. Their natural sample space is the simplex, not unconstrained Euclidean space. This lesson covers closure, centered log-ratio (CLR), additive log-ratio (ALR), isometric log-ratio (ILR) and Aitchison distance.

## Core transforms

- **Closure:** divide each part by the total.
- **CLR:** subtract the mean log part from every log part; the resulting coordinates sum to zero.
- **ALR:** express each non-denominator part as a log ratio to one selected denominator.
- **ILR:** project log parts onto an orthonormal basis of the zero-sum subspace, producing D−1 Euclidean coordinates.
- **Aitchison distance:** Euclidean distance in ILR coordinates (equivalently, the norm of a CLR difference).

The [implementation](../../implementations/python/compositional-data/README.md) uses a Helmert orthonormal basis and checks round trips and isometry.

## Zero handling

Log-ratio transforms cannot accept zeros. Structural zeros, rounded zeros and below-detection-limit observations require different treatments. The implementation refuses zeros in log-ratio transforms instead of inserting an arbitrary pseudocount. Closure itself accepts nonnegative values with a positive total.

## Limits

The package implements transformations and distance only. Compositional kriging, spatial dependence, regression, missing-part imputation and zero replacement remain open.
