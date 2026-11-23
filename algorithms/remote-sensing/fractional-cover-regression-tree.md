# Fractional-cover estimation with a regression tree

Fractional cover represents the proportion of a pixel occupied by a specified
surface component (for example green vegetation, non-photosynthetic vegetation
or bare soil). It is a continuous response, not a hard land-cover class.

## CART regression baseline

Given labelled samples (x_i, y_i), with predictor vector x_i and fractional
response y_i in [0,1], a regression tree recursively partitions feature space.
At a candidate split j,t its squared-error gain is

    delta_SSE = SSE(parent) - SSE(left) - SSE(right).

The implementation chooses the best positive-gain split subject to a maximum
depth and minimum leaf sample count. Each terminal leaf predicts the mean
training fraction in that leaf. Ties are resolved by feature order and
ascending threshold, making the result deterministic.

## Implementation

See the Python package at
../../implementations/python/fractional-cover/README.md. It complements,
rather than replaces, the separate FCLS spectral unmixing implementation.

## Assumptions and validation

Training labels must be finite fractions in [0,1], and predictors must be
finite and consistently scaled. Random pixel splits can leak spatial
autocorrelation; use spatially blocked or geographically separated validation.
Report held-out RMSE, MAE, bias, sample design, sensor/season and domain of
applicability. Do not interpret a fitted tree as a published operational
vegetation-continuous-fields product or as a physically constrained spectral
mixture model.
