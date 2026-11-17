# Local quadratic modified Shepard interpolation

The original Shepard method is a global inverse-distance weighted average.
The modified local-quadratic family replaces each observation value with a
local polynomial q_i(x), constrained so q_i(x_i)=z_i, then blends these
local models:

```
z_hat(x) = sum_i W_i(x) q_i(x) / sum_i W_i(x)
W_i(x) = [ (R_i - d_i(x))_+ / (R_i d_i(x)) ]²
```

Here d_i is planar Euclidean distance and R_i is a local influence radius.
The implementation chooses R_i from the nw-th nearest sample and fits each
local quadratic using the nq-nearest neighbours. A rank-deficient quadratic
fit falls back to a linear local model, then a constant local model. Exact
sample queries return the observed value; points outside all supports return
None.

## Scope

This is a documented Franke–Nielson-style teaching variant, not a claim to
reproduce Renka's QSHEP2D coefficients, NAG's default choices or acceleration
structures. It uses brute-force neighbourhood searches and local weighted
least squares. It does not provide derivatives, robust fitting, 3D support,
anisotropy, barriers, network distances or prediction uncertainty.

## References

- Shepard, D. (1968). A two-dimensional interpolation function for
  irregularly-spaced data. *Proceedings of the 23rd ACM National Conference*,
  517–523. https://doi.org/10.1145/800186.806877.
- Franke, R., & Nielson, G. (1980). Smooth interpolation of large sets of
  scattered data. *International Journal for Numerical Methods in
  Engineering*, 15, 1691–1704. https://doi.org/10.1002/nme.1620151110.
- Renka, R. J. (1988). Multivariate interpolation of large sets of scattered
  data. *ACM Transactions on Mathematical Software*, 14, 139–148.
  https://doi.org/10.1145/42288.42291.
