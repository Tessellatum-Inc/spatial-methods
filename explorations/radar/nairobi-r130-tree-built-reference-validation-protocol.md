# Nairobi R130 tree/built reference-validation protocol

## Status

**Protocol only — no reference sample has yet been collected or scored.** This document defines the evidence required before making an empirical statement about Dynamic World (DW) tree/built label quality in the Nairobi R130 analysis. It does not report accuracy results.

## 1. Question and scope

For the five R130 acquisition dates (2026-10-06, 2026-10-18, 2026-10-30, 2026-11-11 and 2026-11-23), how often do DW tree and built labels agree with an independently interpreted reference at the same ground footprint and a temporally defensible date?

The primary scope is the binary tree-versus-built comparison used by the residual analysis. The reference protocol must also preserve mixed, other, obscured and indeterminate cases rather than forcing every pixel into one of the two classes.

This is a local validation of the selected Nairobi study footprint and dates. It cannot be generalized to all Nairobi, Kenya, other seasons, or the global DW product.

## 2. Independence and admissible reference evidence

DW is derived from Sentinel-2 imagery. A second classification product derived from the same Sentinel-2 observations is not independent reference evidence, even if its map differs from DW. Agreement between two model-derived maps is a separate diagnostic and must be reported as such.

A reference observation is admissible only when all of the following are documented:

1. **Independent visual evidence:** preferably orthorectified aerial or satellite imagery with ground sampling distance of 3 m or finer. Imagery at coarser resolution may be used only if it clearly resolves the 10 m footprint and is flagged for sensitivity analysis.
2. **Temporal proximity:** imagery acquired within 30 days of the target date is preferred. A 31–90 day gap is conditional: accept only if interpreters can rule out relevant land-cover change using available time series and record the justification. Beyond 90 days is not admissible for primary-date scoring.
3. **Spatial registration:** source CRS, georeferencing, pixel footprint overlay and any visible offset must be recorded. If positional uncertainty could change the class assignment, mark the sample indeterminate.
4. **Provenance and rights:** provider, acquisition date, resolution, access URL or asset ID, licence/terms and retrieval date must be recorded. Do not redistribute imagery where licence terms prohibit it.
5. **No circularity:** do not use DW labels/probabilities, the residual outcome, or another model's prediction to decide the reference class.

Candidate reference sources must pass this audit before sample scoring begins. Publicly accessible imagery is not automatically independent, sufficiently resolved, temporally matched, or licensed for reuse.

## 3. Sampling frame and design

Freeze and checksum the exact R130 study mask, the 30 residual-map footprints, the DW image identifiers and the DW label/probability rasters used by the analysis before drawing samples.

Use a probability sample from the eligible 10 m pixel footprints in the analysis mask. Stratify the frame by:

- DW predicted class: trees or built;
- DW top-class probability: <0.50, 0.50–<0.70, 0.70–<0.85, >=0.85;
- acquisition date.

Retain an explicit sampling-frame count for every date × predicted-class × probability stratum. If some strata are too small, sample all units in that stratum and record the inclusion probability. Do not silently omit low-confidence pixels.

To limit spatial dependence and fieldwork/review burden, draw spatially balanced primary sampling units (for example, 1 km grid cells) and then randomly sample pixels within selected units and strata. Record both stages' inclusion probabilities. The final per-pixel inclusion probability is the product of the applicable stage probabilities; analysis weights are its inverse. If a two-stage design is not implemented, use a documented spatially balanced probability design with known inclusion probabilities instead.

Avoid selecting only visually interesting or easily interpreted sites. Any purposive supplement for rare edge cases must be labelled exploratory and excluded from design-based accuracy estimates unless its inclusion probabilities are known.

### Sample size

Do not choose a convenient round number and call it representative. Run a small blinded pilot across all major strata, estimate class-specific agreement and design effect, then calculate the final sample allocation for a predeclared precision target. Oversample low-frequency predicted classes and low-confidence strata where necessary, while retaining weights. Report the achieved effective sample size and precision; do not claim the nominal point count is the independent sample size.

## 4. Reference response design

Each sampled 10 m pixel is interpreted using the exact ground footprint, not a point-only visual impression. Interpreters are blinded to the DW label, probability values, residual values and the study's expected direction.

Record continuous fractions where feasible:

- tree canopy fraction;
- built/artificial surface fraction;
- other visible cover fraction;
- obscured or unobservable fraction.

Fractions should sum to approximately 1.0, with a documented tolerance; if the image cannot support reliable fractional interpretation, record a categorical label and reason instead of inventing precision.

Primary categorical response:

- tree_dominant: tree canopy fraction > 0.50;
- built_dominant: built/artificial fraction > 0.50;
- mixed: neither tree nor built exceeds 0.50, or both are materially present without a clear dominant class;
- other: another land-cover type dominates;
- indeterminate: imagery, timing, registration or interpretation does not support a defensible call.

The threshold is a study operational definition, not a claim that DW's semantic class definitions are identical. Preserve the fractions so alternative thresholds can be evaluated transparently. Mixed, other and indeterminate are not to be silently dropped from the sample ledger.

Two trained interpreters independently label each sample. They record class, fractions, confidence (high/medium/low), evidence date, evidence source and a short rationale. Disagreements and low-confidence cases go to a third adjudicator, who remains blind to DW and residual results. Preserve both initial interpretations and the adjudicated response.

## 5. Temporal handling

Match reference evidence to each target date separately. A single static reference image must not be reused across all five dates without evidence that the land cover remained stable.

Record the exact DW Sentinel-2 source asset and timestamp used for each target date. If DW has no matching acquisition, document the nearest valid DW acquisition and its time offset; do not silently substitute a composite. A composite can conceal change and is not equivalent to a single-date label.

For every sample, record whether visible construction, demolition, vegetation clearing, planting, seasonal change, shadow, cloud or other transient condition occurred between the reference acquisition and target date. Apply the admissibility rules before examining the DW prediction.

## 6. Primary analysis

Report a weighted confusion matrix for the DW binary tree/built predictions against adjudicated reference labels, separately by target date. Use the known inclusion probabilities to estimate:

- user's accuracy / precision for predicted trees and predicted built;
- producer's accuracy / recall for reference tree-dominant and built-dominant classes;
- class-specific omission and commission error;
- weighted prevalence and the share of mixed, other and indeterminate cases;
- confidence intervals that respect the actual spatial sampling design (primary sampling units / clusters and strata).

Do not calculate a single binary accuracy by dropping mixed/other/indeterminate cases without also reporting their weighted share and a clearly labelled conditional estimate. Primary binary estimates should state the exact reference definition and temporal window.

The original residual estimand is an equal-stratum then equal-eligible-block mean of trees-minus-built MAE. A conventional pixel-level confusion matrix does not by itself quantify bias in that estimand. Any propagation of label uncertainty into the residual contrast must preserve the original matched strata, block eligibility and equal weighting. Report the reference-supported subset and the changed target population explicitly; do not apply a global confusion-matrix correction as if errors were spatially uniform.

## 7. Quality controls and audit trail

- Freeze the sample draw and publish a sample manifest before interpretation.
- Store immutable sample IDs; keep coordinates in a controlled file if public release would expose sensitive locations.
- Record source imagery IDs, acquisition dates, resolutions, licences, interpretation versions and adjudication history.
- Conduct a blinded duplicate review on at least 10% of samples, distributed across dates and strata.
- Report raw agreement and class-specific disagreement between interpreters; do not rely on a single kappa statistic.
- Track indeterminate rate and reasons. If it is high or differs by predicted class/confidence stratum, investigate possible verification bias.
- Keep training/calibration samples separate from final validation samples. If reference labels are used to tune thresholds or rules, reserve a new untouched holdout sample for final evaluation.
- Publish code, sampling seed, frame counts, inclusion probabilities, schema and aggregate results; protect restricted imagery and sensitive coordinates.

## 8. Stop/go gates

**Gate A — source feasibility:** at least one admissible, independent, temporally matched source is identified for the target footprint and dates, with usable licence/terms and provenance. If not, stop: report that empirical validation is currently infeasible; do not substitute agreement with another model.

**Gate B — frame integrity:** exact masks, DW assets, labels/probabilities and date joins are frozen and reproducible; frame counts reconcile to the analysis population.

**Gate C — sampling integrity:** all selected units have known inclusion probabilities; pilot informs a documented precision-based sample size; low-confidence strata are represented.

**Gate D — reference quality:** blind double interpretation and adjudication are complete; temporal and registration exclusions are logged; duplicate review is reported.

**Gate E — analysis:** weighted date-specific metrics and design-aware uncertainty are produced; mixed/other/indeterminate shares are visible; implications for the matched-strata residual estimand are assessed without changing the original Nairobi analysis.

No empirical accuracy claim is permitted until Gates A–E are passed.

## 9. Current status and next action

Current status: **Gate A not yet passed.** No qualifying local reference imagery inventory or interpreted sample has been established in this repository. The next operational task is a source-feasibility inventory for the five dates and study footprint, recording candidate imagery coverage, date, resolution, registration, licence and access. Only after that inventory should a sample be drawn.

## 10. Method references

- Dynamic World documentation describes the nine class-probability bands, per-image predictions from Sentinel-2 and the recommendation to threshold top-class probability for selecting confident predictions: [Google Earth Engine Data Catalog](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_DYNAMICWORLD_V1).
- The Dynamic World paper describes expert reference annotations and its test dataset; those global test data are useful methodological context but are not automatically a local Nairobi reference sample: [Brown et al. (2022), Scientific Data](https://doi.org/10.1038/s41597-022-01307-4).
- Independent validation requires higher-resolution reference data not used in map production, as summarized by the Copernicus Land Monitoring Service: [How are European CLC data validated?](https://land.copernicus.eu/en/faq/products/corine-land-cover/how-are-european-clc-data-validated).
- Probability sampling, response design and design-aware accuracy assessment are core components of rigorous land-cover validation: [CEOS WGCV LPV Land Cover Validation Protocol (2025)](https://lpvs.gsfc.nasa.gov/PDF/CEOS_WGCV_LPV_Land_Cover_protocol_Sept2025_V1.pdf).
