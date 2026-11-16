# Iterative proportional fitting for spatial microsimulation

This package implements two-dimensional iterative proportional fitting
(IPF), also called raking. A nonnegative seed table is alternately scaled
to match target row and column totals. Structural zeros remain zero.

## Install and test

    python -m pip install -r requirements.txt
    python -m pytest -q

## Minimal example

    from ipf import iterative_proportional_fit
    result = iterative_proportional_fit(
        [[10, 20], [30, 40]],
        {0: [40, 60], 1: [50, 50]},
    )
    print(result["fitted"])

## Limits

This is the marginal-fitting core only. It does not create synthetic
individuals, perform simulated annealing, resolve incompatible structural
zeros, estimate uncertainty, or implement full spatial microsimulation.
Convergence is returned explicitly; callers must inspect the flag and error.
