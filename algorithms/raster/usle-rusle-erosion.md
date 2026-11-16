# USLE and RUSLE soil-loss factor calculations

## Factor product

The Universal Soil Loss Equation and Revised USLE estimate long-term average sheet and rill erosion as A = R × K × LS × C × P. The factor-product function multiplies supplied rainfall erosivity, soil erodibility, slope-length/steepness, cover-management and support-practice factors with NumPy broadcasting. The output unit follows the units used for R and K.

## Slope-length and steepness

The LS helper accepts slope in degrees and horizontal slope length in metres. It calculates the length factor relative to 22.13 m using either a supplied exponent m or a conventional slope-dependent beta approximation. The steepness factor uses a common two-branch percent-slope equation. This is a compact empirical formulation, not a flow-accumulation-aware LS algorithm for convergent terrain.

## Limitations

The routines do not derive R, K, C or P from local observations, model gully/channel erosion, sediment delivery, deposition, conservation practice design, event-scale erosion or sediment transport. RUSLE is not a process-based hillslope simulation and its calibration/validity is regional. Do not interpret output as total catchment sediment yield without a separate delivery model and validation.
