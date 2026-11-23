# Local quadratic modified Shepard interpolation

This NumPy teaching implementation blends local polynomials centred at
sample locations. Each local polynomial is constrained to reproduce its
centre observation; weighted least squares fits a quadratic to nearby
observations, with a linear/constant fallback when a local design is rank
deficient. The local polynomials are blended using compact Franke–Nielson-
style weights:

```
W_i(x) = [ max(0, R_i - d_i) / (R_i d_i) ]²
```

The support radius R_i is set by the `nw`-th nearest neighbour; the local
fit uses the `nq`-nearest neighbourhood. Exact sample queries return the
observed value. Queries outside every local support return `None`.

## Install and test

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## Limits

This is an explicitly scoped Franke–Nielson-style local-quadratic variant,
not a claim of exact equivalence to Renka's QSHEP2D or NAG's implementation.
It uses brute-force neighbour searches and dense local least squares, does
not implement cell-based acceleration, derivatives, robust fitting or
higher-dimensional variants, and does not return uncertainty. The default
neighbour counts are practical starting points, not universally optimal.
