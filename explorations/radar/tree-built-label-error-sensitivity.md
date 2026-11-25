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
- Confusion scenarios: perfect labels; symmetric 5%; asymmetric tree-to-built 15% / built-to-tree 5%; spatially varying 10% base rates; symmetric 20%; a joint ambiguity scenario; an ambiguity-only label-flip scenario; and an ambiguity-only residual-inflation scenario.
- 200 Monte Carlo replications per scenario.
- Fixed seed: 20261205.

## Interpretation guardrails

- This is a sensitivity experiment with assumed confusion rates, not an estimate of Dynamic World accuracy.
- Label error may vary by geography, season, class mixture, object size, sensor conditions and spatial context. A single confusion matrix is unlikely to capture all of that.
- Common-support filtering is explicit and can itself change the retained block population. Read support counts with the contrast shifts.
- No confidence intervals, spatial coverage claims, correction estimator, or Nairobi-specific conclusion are produced.
- Do not retroactively tune the Nairobi study using this synthetic design.

## Results (artifact-backed)

The GitHub Actions workflow completed successfully on 2026-11-25 (latest run 45667688603; commit 7de5840). Unit tests passed and the 200-replication simulation artifact was generated.

| Scenario | Mean observed contrast | Mean shift from latent-label target | 2.5th–97.5th percentiles of replicate shifts |
|---|---:|---:|---:|
| Perfect labels | 0.3000 | 0.0000 | 0.0000 to 0.0000 |
| Symmetric 5% flips | 0.2683 | -0.0317 | -0.0371 to -0.0279 |
| Asymmetric 15% T→B, 5% B→T | 0.2417 | -0.0584 | -0.0643 to -0.0523 |
| Spatially varying 10% base rates | 0.2345 | -0.0656 | -0.0723 to -0.0602 |
| Symmetric 20% flips | 0.1763 | -0.1238 | -0.1314 to -0.1161 |

The latent-label target averaged 0.30003 in every scenario because the scenarios share the same generated latent data stream. All 400 blocks retained common true/observed support in this design.

### Interpretation

Under this particular generator, label contamination attenuated the positive trees-minus-built contrast toward zero. The shift increased with the assumed flip rates and was larger under the spatially varying confusion scenario than under symmetric 10% base rates would be expected to be, given the row-dependent class prevalence and class-conditional flip pattern.

The percentile ranges above describe variation across simulated replicate shifts; they are not confidence intervals for a real-world effect or estimates of uncertainty in Dynamic World accuracy. These results demonstrate sensitivity to assumed label error, not the actual direction or magnitude of bias in Nairobi.

The initial scenarios assume label flips are conditionally random within each class (apart from the specified row gradient). A follow-on scenario now uses a beta-distributed ambiguity proxy: ambiguous pixels have larger residual magnitudes and a higher flip probability. This is a deliberately stylized mixed-pixel/boundary stress test, not a measured ambiguity score. Its results will be appended after workflow validation.


## Factorial follow-up: separating ambiguity mechanisms (validated 2026-11-25)

The follow-up isolates two mechanisms using a paired 2 × 2 design:

| Cell | Ambiguity-linked label flips | Ambiguity-linked residual inflation |
|---|---|---|
| Neutral baseline | Off | Off |
| Label only | On | Off |
| Residual only | Off | On |
| Joint | On | On |

All four cells use the same latent labels, ambiguity-proxy draws, base residual draws and random streams within each Monte Carlo replicate. Each cell's outcome is its label-induced shift (noisy-label estimate minus that cell's latent-label target). The interaction is calculated per replicate as:

`joint - label\_only - residual\_only + neutral`

This difference-in-differences isolates non-additivity between the two mechanisms in this generator. It does not estimate a real-world causal effect.

### Validated results

- GitHub Actions run: [45669390116](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45669390116)
- Commit: `d0c9c5db7a39cbf4b68117741717134931fcbfc1`
- Unit tests: passed.
- Simulation: passed; artifact uploaded.
- Replications: 200 per scenario; seed `20261205`.
- Paired interaction mean: **−0.01474**.
- 2.5th–97.5th percentiles across the 200 replicate interaction values: **−0.01660 to −0.01321**. These are Monte Carlo replicate percentiles, not a confidence interval.

| Factorial cell | Mean latent-label contrast | Mean label-induced shift |
|---|---:|---:|
| Neutral baseline | 0.30055 | −0.06324 |
| Label-error only | 0.30055 | −0.11544 |
| Residual inflation only | 0.36933 | −0.07773 |
| Joint | 0.36933 | −0.14467 |

The residual-inflation cells have a different latent-label contrast because residual inflation changes the underlying residual magnitudes. The factorial comparison therefore uses label-induced shifts (observed minus latent target), not raw observed contrasts. This distinction is essential to the interaction calculation.

### Interpretation and limits

The negative interaction indicates that, in this synthetic setup, combining ambiguity-linked label flips with ambiguity-linked residual inflation produces an additional negative shift beyond the sum of their separate shifts. The magnitude is small relative to the main label-error shifts in these scenarios.

The earlier joint-only ambiguity scenario is not a clean mechanism-isolation result; the paired factorial cells supersede it for that purpose. The generator still uses assumed flip probabilities and a beta-distributed ambiguity proxy. It does not estimate Dynamic World confusion, model actual boundary pixels, assess spatial confidence-interval coverage, or establish a Nairobi R130 bias correction. The replicate percentiles describe this simulation's paired outcomes only.
