# Whittaker-Eilers smoother

The Whittaker-Eilers smoother estimates a smooth sequence z from observations y by minimizing

\[
\sum_i w_i(y_i-z_i)^2 + \lambda\lVert D_d z\rVert_2^2,
\]

where W contains observation weights, D_d is the order-d finite-difference operator, and lambda controls smoothness. The solution satisfies

\[
(W+\lambda D_d^T D_d)z=Wy.
\]

Second-order differences penalize curvature and preserve linear sequences in the penalty's null space. Larger lambda produces smoother estimates. Missing observations can be represented with zero weights.

## Reference implementation

The [NumPy implementation](../../implementations/python/whittaker-smoother/README.md) uses a dense linear solve and supports missing values and caller-supplied nonnegative weights. It assumes uniform index spacing and does not estimate lambda automatically.

## Limits

This is a one-dimensional sequence smoother, not a full spatial surface interpolator. For irregular sample spacing, use a spacing-aware penalty. For large series, use sparse/banded linear algebra. Select lambda with a justified validation design; random splits can be inappropriate for temporally or spatially structured data.
