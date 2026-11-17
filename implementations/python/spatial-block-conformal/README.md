# Spatial block split conformal intervals

This small NumPy package implements a block-level split conformal baseline for regression prediction intervals. The caller supplies calibration observations, their predictions, and spatial block labels. Each block contributes one score: the maximum absolute residual among observations in that block. A finite-sample upper order statistic of those block scores calibrates a two-sided interval.

An optional positive scale vector supports locally adaptive, normalised residuals. Supply calibration scales to `calibrate_spatial_blocks` and corresponding prediction scales to `spatial_block_interval`; the resulting half-width is the calibrated score quantile multiplied by the new observation's scale.

## Run

    python -m pytest -q

## Interpretation and limits

The calibration unit is the block, not the individual point. Under exchangeability of the calibration blocks and a future block, the maximum-score construction targets simultaneous coverage of all observations in a future block. This is stronger and more conservative than pointwise marginal coverage. The finite-sample quantile is infinite when there are too few calibration blocks for the requested alpha; the implementation does not silently substitute a lower order statistic.

Spatial block labels do not themselves establish exchangeability. Blocks should be designed to reduce dependence leakage and should have comparable spatial extent and sampling density. Residual dependence between blocks, nonstationarity, covariate shift, or a mismatch between calibration and deployment blocks can invalidate nominal coverage. This is not a guarantee under arbitrary spatial dependence.

The package does not fit the prediction model or scale model, choose block geometry, estimate spatial dependence ranges, perform cross-conformal inference, or provide conditional coverage guarantees. Predictions and scales must come from models trained without using the corresponding calibration outcomes.
