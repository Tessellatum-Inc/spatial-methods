# Verification — spatial block split conformal intervals

**Status:** Partial implementation of the conformal-prediction subset of the source-listed uncertainty and probabilistic-mapping family.

## Implemented

- Two-sided split conformal calibration using one maximum absolute residual per caller-defined spatial block.
- Finite-sample order-statistic rank, including an infinite quantile when the requested rank exceeds the calibration-block count.
- Optional positive scale normalisation for locally adaptive interval widths.
- Prediction intervals and calibration diagnostics (block count, observation count, rank and block scores).

## Independent checks

- Hand-calculated block maxima and order-statistic fixtures.
- A separate fixture verifies that multiple observations in one block contribute one calibration score.
- Scale-normalised scores and prediction intervals are checked against exact arithmetic.
- Too-few-block behaviour is checked explicitly for an infinite interval.
- Invalid dimensions, non-finite values, invalid alpha, missing labels and non-positive scales are rejected.

Run from this package directory: python -m pytest -q.

## Not covered

Ordinary random-split conformal variants, cross-conformal methods, conformalised quantile regression, spatially varying calibration partitions, automatic block-size selection, dependence-aware confidence guarantees under arbitrary spatial processes, quantile regression forests, area-of-applicability diagnostics, fuzzy/possibilistic maps and other uncertainty representations in the broader source row.
