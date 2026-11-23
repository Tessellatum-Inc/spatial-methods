# Low-rank matrix completion with Soft-Impute

This package implements a nuclear-norm-regularized matrix completion
baseline. Missing cells are initialized with the observed global mean;
each iteration computes an SVD, soft-thresholds singular values, optionally
caps the rank, and restores observed cells exactly.

## Install and test

    python -m pip install -r requirements.txt
    python -m pytest -q

## Minimal example

    import numpy as np
    from soft_impute import soft_impute

    data = np.array([[1., 2., 3.], [2., np.nan, 6.], [3., 6., 9.]])
    result = soft_impute(data, regularization=0.01, max_rank=1)

## Limits

This is a dense, small/medium matrix baseline. It does not implement
spatiotemporal tensor completion, spatial regularization, covariates,
uncertainty estimates, deep inpainting or distributed/large-scale solvers.
The observed global-mean initialization and regularization parameter affect
the result; tune them using a validation design that masks known values.
