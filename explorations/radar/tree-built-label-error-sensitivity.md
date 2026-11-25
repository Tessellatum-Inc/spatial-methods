# Tree/built class-label error sensitivity

## Purpose

The Nairobi R130 contrast uses Dynamic World-derived tree and built labels. Those labels are model predictions, not ground truth. This experiment asks how class-conditional label flips could alter a trees-minus-built mean absolute residual error contrast.

## Explicit target and estimator

Within each spatial block, calculate trees MAE minus built MAE separately in each pre-defined matched stratum. Average stratum contrasts equally within block, then average eligible blocks equally. The target uses latent true labels. The observed-label estimator uses noisy T/B labels and retains only blocks for which every stratum has both true and observed class support.

This experiment is deliberately about label contamination, not the spatial interval method. It does not estimate a corrected contrast.

## Synthetic design

- 20 × 20 blocks, 3 strata per block, 80 pixels per stratum.
- Tree prevalence varies over rows and is bounded to preserve both classes.
- Absolute residuals are exponential with class-specific means (trees 0.82, built 0.52) plus a small spatial block effect.
- Confusion scenarios: perfect labels; symmetric 5%; asymmetric tree-to-built 15% / built-to-tree 5%; spatially varying 10% base rates; symmetric 20%.
- 200 Monte Carlo replications per scenario.
- Fixed seed: 20261205.

## Interpretation guardrails

- This is a sensitivity experiment with assumed confusion rates, not an estimate of Dynamic World accuracy.
- Label error may vary by geography, season, class mixture, object size, sensor conditions and spatial context. A single confusion matrix is unlikely to capture all of that.
- Common-support filtering is explicit and can itself change the retained block population. Read support counts with the contrast shifts.
- No confidence intervals, spatial coverage claims, correction estimator, or Nairobi-specific conclusion are produced.
- Do not retroactively tune the Nairobi study using this synthetic design.

## Results

Pending GitHub Actions completion and artifact inspection.
