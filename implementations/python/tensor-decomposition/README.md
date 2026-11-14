# Three-way CP/PARAFAC decomposition

A dense NumPy implementation of canonical polyadic (CP/PARAFAC) decomposition using alternating least squares (ALS). It approximates a fully observed 3D tensor as a sum of rank-one outer products.

Run with `python -m pytest -q` from this directory.

## Scope and caveats

This is a small, dense, unconstrained teaching baseline. It uses pseudoinverse updates of the Hadamard product of factor Gram matrices. It does not support missing entries, sparse tensors, nonnegativity, regularization, streaming updates, automatic rank selection, robust losses, or Tucker/tensor-train formats. CP-ALS can be sensitive to initialization, ill-conditioning and local minima; a low reconstruction error does not establish that factors are scientifically identifiable or unique. Large arrays can exceed memory because dense unfoldings and reconstruction tensors are materialized.
