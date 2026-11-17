# Spatial block split conformal prediction intervals

## Purpose

Split conformal prediction converts a held-out calibration sample into finite-sample prediction intervals without assuming a parametric residual distribution. For spatial data, treating nearby observations as independent calibration units can overstate the effective sample size. A block-level construction instead makes a caller-defined spatial block the calibration unit.

## Calibration score

For calibration observation i, let y_i be the observed response, \hat{y}_i its prediction, and s_i a strictly positive scale. The scale is one for ordinary absolute-residual calibration, or a supplied estimate of local error magnitude for a normalised, locally adaptive interval.

Within block b, define the maximum score

\[
S_b = \max_{i \in b} \frac{|y_i-\hat{y}_i|}{s_i}.
\]

For B calibration blocks and target miscoverage alpha, sort the B block scores and select the order statistic with rank

\[
k = \left\lceil (B+1)(1-\alpha) \right\rceil.
\]

If k exceeds B, the finite-sample conformal quantile is positive infinity. This is intentional: a finite interval cannot claim the requested coverage with too few exchangeable calibration units.

For a new prediction with scale s, the interval is

\[
[\hat{y}-q s,\;\hat{y}+q s],
\]

where q is the selected block-score quantile.

## What the block construction targets

If calibration blocks and the future block are exchangeable as units, the rank of the future block's maximum score among the B+1 block scores is uniform up to ties. The resulting interval therefore targets simultaneous coverage of all observations in that future block. It is not merely a pointwise guarantee.

## Spatial assumptions and limits

- The user defines block labels and should choose spatial separation and block dimensions using the sampling design and dependence scale.
- Comparable block extent and observation density matter because a maximum score tends to increase with block size.
- Spatial blocking reduces leakage from nearby observations but does not prove block exchangeability or independence. Residual dependence between blocks, nonstationarity, covariate shift and deployment mismatch can invalidate nominal coverage.
- The regression and optional scale models must be trained without the calibration outcomes used to compute scores.
- The method does not provide conditional coverage at every location or under arbitrary spatial dependence.

## Reference implementation

The NumPy baseline is in `implementations/python/spatial-block-conformal/spatial_block_conformal.py`. It returns the calibrated quantile and block-level diagnostics, then applies that quantile to predictions and optional positive local scales.
