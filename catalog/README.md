# Spatial analysis catalogue

This directory is the structured index of the project's knowledge inventory. It includes algorithms, operations, data structures, models, statistics, standards, workflows, systems and applied methods. Full technical explanations belong in canonical records in their relevant directories.

## Subject navigation

- [Geoinformatics master subject index](master-subject-index.md) — the canonical map of subject areas, stable IDs, priorities and cross-pillar relationships.
- [Subject-to-repository alignment register](subject-alignment-register.md) — connects the subject map to existing algorithms, methods, verification records, implementations, notebooks, learning paths and source sections. Its current mappings are structural, not technical verification.
- [First curation cluster: reference, positioning and measurement](first-curation-cluster-reference-positioning-measurement.md) — maps existing geodesy, GNSS and uncertainty assets, identifies field-survey and standards gaps, and defines an applied capstone.

- [Surveying and field measurement source map](surveying-field-measurement-source-map.md) — an initial authority-ranked source register for measurement science, instrument verification, GNSS practice, control/topographic surveying and levelling, with subject-ID links and open research streams.
- [Measurement principles and field verification](../foundations/measurement-science/measurement-principles-and-field-verification.md) — the first foundational synthesis, covering the measurement chain, uncertainty, error sources, redundancy and procedure-specific field verification.
- [Exercise A: repeated distance and horizontal-angle observations](../experiments/measurement/exercise-a-repeated-distance-and-angle.md) — a reproducible synthetic worked experiment with a machine-readable dataset and Python analysis; explicitly not field evidence.
- [Exercise B: differential levelling and loop adjustment](../experiments/measurement/exercise-b-differential-levelling-loop.md) — a synthetic levelling loop with forward/reverse observations, weighted closure adjustment, elevation covariance and a reproducible analysis.
- [Exercise C: weighted least-squares adjustment of a vertical control network](../experiments/measurement/exercise-c-weighted-control-network.md) — a synthetic multi-route network with observation equations, weighted adjustment, residual diagnostics and parameter covariance.
- [Exercise D: stochastic control and correlated observations](../experiments/measurement/exercise-d-stochastic-control-and-correlation.md) — compares fixed and uncertain datum control and introduces a non-diagonal observation covariance model.\n- [Exercise E: minimally constrained vertical network](../experiments/measurement/exercise-e-minimally-constrained-vertical-network.md) — demonstrates the vertical datum defect, inner constraints, free-network covariance and transfer onto an external control datum.

- [Exercise F: network quality, statistical testing and blunder detection](../experiments/measurement/exercise-f-network-quality-and-blunder-detection.md) — compares global chi-square and local standardized-residual diagnostics, injects a synthetic gross error, examines multiple testing and withholding sensitivity, and includes an independent synthetic check.

- [Exercise G: reliability, detectability and network design](../experiments/measurement/exercise-g-reliability-and-network-design.md) — computes redundancy numbers, minimal detectable biases and external effects, then compares an added independent B–E link with a uniform precision improvement.\n- [Exercise H: Monte Carlo reliability and design simulation](../experiments/measurement/exercise-h-monte-carlo-reliability-and-design.md) — simulates correlated standardised-residual tests under single and multiple gross errors, compares the baseline and augmented networks, and reports empirical detection, false alarms, identification and masking.
- [Exercise I: robust estimation and iterative outlier identification](../experiments/measurement/exercise-i-robust-estimation-and-outlier-identification.md) — compares ordinary least squares, sequential data snooping and Huber IRLS under uncontaminated, single-error and multiple-error scenarios.\n- [Exercise J: Monte Carlo comparison of robust estimators](../experiments/measurement/exercise-j-monte-carlo-comparison-of-robust-estimators.md) — compares LS, iterative data snooping and Huber IRLS over repeated clean and contaminated simulations, including baseline and augmented network designs.\n- [Exercise K: correlated errors and generalized least-squares adjustment](../experiments/measurement/exercise-k-correlated-errors-and-generalized-least-squares.md) — compares covariance-aware GLS with a deliberately misspecified diagonal model and tests uncertainty calibration under shared session effects.
- [Exercise L: block-robust GLS with correlated observations](../experiments/measurement/exercise-l-block-robust-gls-with-correlated-observations.md) — compares covariance-aware GLS, diagonal WLS and an illustrative block-Huber estimator under single-observation and session-level contamination.
- [Exercise M: multi-session network adjustment and robustness](../experiments/measurement/exercise-m-multi-session-network-adjustment-and-robustness.md) — expands the correlated network to twelve independent repeated sessions and evaluates clean-data downweighting, single-row errors and multiple contaminated sessions.

## Coverage

See the [source-to-repository coverage matrix](coverage-matrix.md) for an honest view of what is captured, what has been researched and where work remains. The matrix deliberately does not count a source transcription as verified coverage. See the [source review dashboard](review-dashboard.md) for a dated count of all 695 source-entry rows and their current review labels.

## Intake source

The initial 47-page *Spatial Analysis Algorithms: Complete Compendium* has been imported page-by-page under [source-inventory](../source-inventory/README.md). That is the preserved intake record.

The transcription preserves original page boundaries and extracted wording. It is not an independently verified reference work. The next task is a separate, auditable catalogue pass. A source entry is not automatically an algorithm or a verified canonical record.

## Intake and normalisation rules

For every source entry, preserve:

- original section numbering and headings;
- original category groupings;
- source wording for each listed method, variant, named algorithm and implementation family;
- source page or page range;
- ambiguities, caveats and possible duplicates.

Normalisation is a second pass. Do not silently delete, rename or merge source entries because they appear redundant. Preserve the original source label and record a canonical label or relationship separately. The source explicitly marks some later additions as remembered and requiring verification; keep those entries flagged.

Use the [source-entry verification protocol](verification-protocol.md) to record identity, bibliography, technical claims, implementation and rights as separate dimensions. Do not use one blanket “verified” status. The [selected verification notes](selected-verification-notes.md) demonstrate the level of evidence recorded for a small number of bibliography checks. The structural alias reconciliations are recorded in [Catalogue crosswalk Batch 1](catalogue-crosswalk-batch-1.md), [Batch 2](catalogue-crosswalk-batch-2.md), [Batch 3](catalogue-crosswalk-batch-3.md), and [Batch 4](catalogue-crosswalk-batch-4.md); these inventories do not upgrade technical verification statuses.

## Stable IDs

Proposed format: `SA-<DOMAIN>-<SLUG>`.

Initial domain codes (provisional):

- `GEO` — geometry and vector operations;
- `IDX` — indexing and query processing;
- `NET` — networks and routing;
- `STA` — spatial statistics and geostatistics;
- `RAS` — raster and image analysis;
- `RS` — remote sensing and Earth observation;
- `3D` — 3D, terrain and point clouds;
- `SIM` — simulation and modelling;
- `AI` — machine learning and GeoAI;
- `DB` — spatial databases and distributed systems;
- `APP` — applied/domain methods;
- `CART` — cartography and visualisation.

Codes may be extended as the inventory is fully audited. Once assigned to a published record, an ID is stable. See the [record-type taxonomy](record-types.md) before creating or classifying a canonical record.

## Suggested inventory fields

| Field | Meaning |
|---|---|
| `source_section` | Original compendium section |
| `source_heading` | Original category heading |
| `source_label` | Exact source wording |
| `source_page` | Original page |
| `canonical_name` | Normalised name, if established |
| `record_id` | Stable ID, once assigned |
| `kind` | Algorithm, operation, data structure, model, statistic, metric, method, workflow, system, standard, implementation, dataset or application |
| `domain` | Main domain |
| `relationships` | Prerequisites, variants, alternatives and applications |
| `identity_status` | Whether the named item has been resolved |
| `bibliography_status` | Whether citation metadata has been checked |
| `claim_status` | Whether specific technical claims have been checked |
| `implementation_status` | Whether a reproducible implementation exists and has been tested |
| `rights_status` | Whether reuse rights have been checked for the intended use |
| `evidence` | Primary or authoritative evidence and review date |
| `notes` | Ambiguity, duplicate candidate or scope note |

## Item-level section indexes

The [section index](sections/README.md) links to source entries extracted and provisionally classified section by section. [Section 1](sections/01-core-gis.md) is the first completed intake pass; it is not yet a fully verified technical catalogue.

## Canonical records already developed

The repository contains a growing set of scoped canonical records, including geometry algorithms and operations, spatial statistics, raster and hydrology methods, geostatistics, geodesy, decision-support methods and location-science models. Each record should state its own evidence and implementation scope. The existence of a canonical page does not automatically verify every grouped source entry that mentions the same family.

The full source catalogue has not yet been normalised record-by-record. Do not infer completion from the page transcription or the presence of related learning materials alone.
