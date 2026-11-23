# Spatial block split conformal calibration

The spatial block split conformal baseline calibrates prediction intervals at the block level rather than treating every nearby observation as an independent calibration unit.

Given observed calibration responses y_i, held-out predictions \hat{y}_i, optional positive local scales s_i, and caller-defined block labels b(i), each block contributes one score:

\[
S_b=\max_{i:b(i)=b}\frac{|y_i-\hat{y}_i|}{s_i}.
\]

The ordinary absolute-residual version uses s_i=1. A supplied scale produces a locally adaptive width, but the scale model must be fitted without using the calibration outcomes.

For B blocks and miscoverage alpha, the implementation selects the sorted block score at rank ceil((B+1)(1-alpha)). If the rank exceeds B, the quantile is infinite. New predictions receive symmetric intervals with half-width equal to this quantile times their optional local scale.

This is a conservative block-level construction: under exchangeability of calibration blocks and a future block, it targets simultaneous coverage of every observation in the future block. The construction does not make arbitrary spatial blocks exchangeable. Block dimensions, separation, sampling density and the deployment regime remain substantive design choices. Comparable block sizes matter because block maxima increase with the number of observations.