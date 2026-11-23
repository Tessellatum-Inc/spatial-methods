# Radial-basis-function interpolation in two dimensions

Radial-basis interpolation represents a surface as a weighted sum of radial
kernels centered at observations plus a polynomial tail:

```
f(x) = sum_i w_i phi(||x - x_i||) + p(x)
```

The reference implementation uses an affine tail
`p(x) = a0 + a1 x + a2 y` and supports:

- Thin plate: `phi(r) = r² log(r)`, with `phi(0) = 0`.
- Cubic: `phi(r) = r³`.
- Gaussian: `phi(r) = exp(-(epsilon r)²)`.

For zero smoothing, coefficients are obtained from the augmented system

```
[ Phi   P ] [w] = [z]
[ P^T   0 ] [a]   [0]
```

where `Phi[i,j] = phi(||x_i - x_j||)` and columns of `P` are
`1, x, y`. A non-negative diagonal smoothing value is added to `Phi`
before solving. With a nonsingular system and zero smoothing, training
values are interpolated; with positive smoothing, the solution is regularized
and need not pass through every observation.

Coordinates are centered and scaled internally. The model rejects duplicate
sites, collinear site configurations that cannot support the affine tail,
non-finite inputs, and singular solves.

## Scope and limits

This is a dense, global, planar 2D reference implementation. The solve is
O(n³) and prediction is O(mn). It is not universal kriging, does not estimate
a covariance model or prediction variance, and does not provide local,
anisotropic, barrier-aware or network-distance interpolation. It does not
cover all spline families or modified Shepard interpolation. Gaussian
epsilon and smoothing must be selected by the caller; no automatic tuning
or cross-validation is claimed.

## References

- Buhmann, M. D. (2003). *Radial Basis Functions: Theory and Implementations*.
  Cambridge University Press.
- Fasshauer, G. E. (2007). *Meshfree Approximation Methods with MATLAB*.
  World Scientific.
