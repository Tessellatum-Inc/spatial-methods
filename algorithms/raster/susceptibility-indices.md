# Groundwater and landslide susceptibility index baselines

## DRASTIC

The DRASTIC function calculates the weighted sum of seven supplied rating layers: depth to water, net recharge, aquifer media, soil media, topography, impact of the vadose zone and hydraulic conductivity. Conventional weights are 5, 4, 3, 2, 1, 5 and 3. Ratings must be on the 1–10 scale. The function does not derive ratings from raw measurements or define locally appropriate class thresholds.

## Frequency ratio

The categorical frequency-ratio method estimates FR = P(class | event) / P(class) for each predictor category and maps the result back to cells. It requires a binary event inventory and a categorical predictor. FR above one indicates over-representation of events in that category relative to its area share. Inventory completeness, spatial sampling bias and class discretization strongly affect the result.

## Logistic susceptibility baseline

A binary logistic regression is fitted with an intercept and ridge-regularized slopes using Newton/IRLS updates. The companion prediction function returns event probabilities. This numerical baseline does not perform feature scaling/selection, spatially blocked validation, calibration assessment, class-imbalance correction, uncertainty estimation or causal interpretation. Avoid random train/test splits when spatial autocorrelation would leak nearby observations.

## Limits

These are methodological building blocks, not a validated groundwater or landslide hazard product. They do not replace hydrogeological field investigation, landslide inventory quality control, spatial cross-validation, independent validation or expert review.
