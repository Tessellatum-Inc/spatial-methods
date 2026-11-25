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
- Pixel-level target/reference sample sizes: independently varied from 8 to 79 before a spatial support factor is applied; a minimum of 5 is retained.
- Strata per block: 2–5 before a row-dependent support factor is applied; at least 2 are retained and equally weighted within block.
- Pixel noise: independent Student-t draws with 4 degrees of freedom, standardized to unit variance and multiplied by a row-varying scale (0.65–1.55).
- Spatially varying support: the number of matched strata and within-stratum sample sizes tend to decrease with row position.
- Stratum heterogeneity: zero-mean within block, so the latent equal-stratum block contrast equals the spatial block effect.
- Baseline common-support loss: 8% of candidate blocks, independent of the latent contrast.
- Informative-selection stress condition: blocks above the 80th percentile of latent contrast are additionally excluded, after the target population is defined.
- Methods: moving-window percentile bootstrap and product-Bartlett spatial HAC.
- Candidate window widths / HAC bandwidths: 3, 5 and 7 blocks.
- Moving-window replicates: 250 per realization.
- Monte Carlo uncertainty: 95% Wilson intervals.

## Estimand-preservation invariant

For every simulated realization, the committed experiment now computes the direct arithmetic mean of the observed eligible block contrasts and checks that both the moving-window and spatial-HAC procedures return exactly that point estimate (within floating-point tolerance). This is an implementation invariant, not evidence that either interval has correct coverage. A mismatch stops the experiment rather than allowing an interval comparison under a silently altered estimand.

## Why this experiment matters

The earlier experiments treated block values as directly observed means. This design adds a layer closer to the actual study: within-block matched-stratum contrasts are estimated from unequal pixel samples, strata are equally weighted within blocks, and blocks are equally weighted in the final estimand. The latest version adds heavy-tailed pixel noise, spatially varying noise scale, and spatially varying matched-support quantity. These are deliberately separate stress dimensions from informative selection.

The independent eligibility condition tests the estimator under ordinary common-support loss. The informative-selection condition deliberately violates that assumption and assesses intervals against the pre-selection target population. Neither method includes a missingness correction, so bias and undercoverage are expected possibilities.

## Guardrails

- The synthetic process is not the Nairobi R130 data-generating process.
- Pixel noise is heavy-tailed and heteroskedastic but independent within strata; dependence across scenes, bursts and polarizations and class-label error remain open.
- The informative-selection condition is a stress test, not a proposed model of Dynamic World or raster missingness.
- A 100-replication simulation and three tuning values cannot establish 95% calibration.
- Do not select a method or bandwidth by the best observed coverage.
- Do not use these results to retroactively tune the Nairobi study.

## Reproducibility

- Script: [simulate_matched_strata_equal_block_contrast.py](simulate_matched_strata_equal_block_contrast.py)
- Workflow: [matched-strata-equal-block-contrast-validation.yml](../../.github/workflows/matched-strata-equal-block-contrast-validation.yml)
- Expected artifact: `matched-strata-equal-block-contrast`

## Results (artifact-backed)

The heavy-tailed, spatially varying-support workflow completed successfully on 2026-11-25 (run 45666402622; commit d16f78f). Its artifact contains 100 replications per condition, 18 interval configurations per eligibility condition, and no unsupported intervals.

### Independent common-support loss

All 18 configurations achieved 100/100 empirical coverage in each dependence setting (rho = 0.3, 0.6, 0.8). The Wilson 95% interval for 100/100 is approximately [0.963, 1.000]. Mean interval-width ranges across methods and tuning values were:

| Spatial rho | Mean interval width range | Mean estimate bias |
|---:|---:|---:|
| 0.3 | 0.168–0.184 | -0.00045 |
| 0.6 | 0.221–0.301 | -0.00070 |
| 0.8 | 0.259–0.411 | +0.00052 |

This is evidence only for this specified generator and tuning grid. The perfect observed coverage, paired with widening intervals as dependence strengthens, is not a general calibration result. One hundred replications leave substantial Monte Carlo uncertainty, and the intervals can be conservative.

### Informative high-contrast exclusion

Coverage was assessed against the pre-selection baseline-eligible population target, while the estimator saw only the selected blocks.

| Spatial rho | Moving-window coverage (widths 3 / 5 / 7) | Spatial-HAC coverage (bandwidths 3 / 5 / 7) | Mean estimate bias |
|---:|---:|---:|---:|
| 0.3 | 0 / 0 / 0% | 0 / 0 / 0% | -0.245 |
| 0.6 | 0 / 0 / 0% | 0 / 0 / 0% | -0.239 |
| 0.8 | 0 / 2 / 6% | 0 / 0 / 0% | -0.229 |

Mean eligible blocks fell from about 529 under independent common-support loss to about 424 under informative exclusion. The intervals remained comparatively narrow relative to the roughly 0.23–0.25 downward bias. This is the expected failure mode when selection changes the observed population but the interval procedure has no selection model or correction.

### Interpretation

The simulation separates two issues that must not be conflated:

1. Under independent support loss, the point estimator remained nearly unbiased for the defined baseline-eligible target, and all tested intervals covered it in this finite experiment.
2. Under value-dependent exclusion, both methods estimated the selected population while being judged against the pre-selection target. Their poor coverage is a target-population/selection problem, not evidence that a different spatial bandwidth alone would solve it.

No method or bandwidth is selected as a winner. Do not generalize these results to the Nairobi R130 study or claim 95% calibration from 100 replications.


## Generator sanity check (not interval validation)

An independent local smoke-check of the specified generator found near-zero average estimation bias under independent common-support loss (absolute mean bias below 0.001 across the tested dependence settings). Under the deliberately informative high-contrast exclusion, the observed equal-block estimate shifted downward by approximately 0.24 in the tested settings. This confirms that the selection stress condition creates a material target/observed-population gap. It is not a run of the committed coverage script, does not test interval coverage, and is not a workflow artifact.
