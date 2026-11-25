# Matched-strata equal-block contrast validation

## Status

A synthetic matched-strata simulation and dedicated GitHub Actions workflow have been added. Numerical results are pending a completed workflow run and artifact inspection.

## Estimand

Each spatial block contains between two and five shared strata. Within every stratum, target and reference observations are sampled with unequal sample sizes and used to estimate a target-minus-reference contrast. The stratum contrasts are averaged equally within each block. Eligible block contrasts are then averaged equally across blocks.

The coverage target is the finite-population mean of the latent equal-stratum block contrasts among baseline-eligible blocks (those with common matched support), before any subsequent informative selection.

This is deliberately not a pooled pixel-weighted contrast.

## Data-generating design

- Grid: 24 × 24 candidate blocks.
- Replications: 100 per condition.
- Spatial dependence: separable Gaussian AR(1), correlations 0.3, 0.6 and 0.8.
- Pixel-level target/reference sample sizes: independently varied from 8 to 79 per stratum.
- Strata per block: 2–5, equally weighted within block.
- Stratum heterogeneity: zero-mean within block, so the latent equal-stratum block contrast equals the spatial block effect.
- Baseline common-support loss: 8% of candidate blocks, independent of the latent contrast.
- Informative-selection stress condition: blocks above the 80th percentile of latent contrast are additionally excluded, after the target population is defined.
- Methods: moving-window percentile bootstrap and product-Bartlett spatial HAC.
- Candidate window widths / HAC bandwidths: 3, 5 and 7 blocks.
- Moving-window replicates: 250 per realization.
- Monte Carlo uncertainty: 95% Wilson intervals.

## Why this experiment matters

The earlier experiments treated block values as directly observed means. This design adds a layer closer to the actual study: within-block matched-stratum contrasts are estimated from unequal pixel samples, strata are equally weighted within blocks, and blocks are equally weighted in the final estimand.

The independent eligibility condition tests the estimator under ordinary common-support loss. The informative-selection condition deliberately violates that assumption and assesses intervals against the pre-selection target population. Neither method includes a missingness correction, so bias and undercoverage are expected possibilities.

## Guardrails

- The synthetic process is not the Nairobi R130 data-generating process.
- Pixel noise is Gaussian and independent within strata; more realistic heteroskedasticity, heavy tails, class-label error and spatially varying support remain open.
- The informative-selection condition is a stress test, not a proposed model of Dynamic World or raster missingness.
- A 100-replication simulation and three tuning values cannot establish 95% calibration.
- Do not select a method or bandwidth by the best observed coverage.
- Do not use these results to retroactively tune the Nairobi study.

## Reproducibility

- Script: [simulate_matched_strata_equal_block_contrast.py](simulate_matched_strata_equal_block_contrast.py)
- Workflow: [matched-strata-equal-block-contrast-validation.yml](../../.github/workflows/matched-strata-equal-block-contrast-validation.yml)
- Expected artifact: `matched-strata-equal-block-contrast`

## Results

Pending workflow completion. Append artifact-backed coverage, Wilson intervals, interval widths, estimate bias and eligible-block counts here.
