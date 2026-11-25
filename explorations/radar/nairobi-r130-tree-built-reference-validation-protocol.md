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


## 9A. Initial public-source feasibility inventory (desk review, 2026-11-25)

This is a source-screening inventory, not evidence that any imagery covers the R130 sample frame. Exact footprint intersections, per-scene acquisition dates, positional accuracy and reuse rights remain to be verified.

| Candidate | What is currently documented | Assessment for the five 2026 target dates |
|---|---|---|
| OpenAerialMap / HOT Nairobi Open Drone Imagery (SDI RIA project) | A Nairobi project map is publicly listed and links to a downloadable GeoTIFF/TMS. The map page identifies a collaboration and project creation in April 2026, but the accessible metadata does not establish the imagery acquisition date, exact footprint overlap with R130, ground resolution or licence. | **First candidate to inspect.** Could provide independent aerial/drone reference if acquisition dates, footprint, resolution and licence pass the protocol. Not yet admissible. |
| Kenya Space Agency high-resolution imagery request | KSA provides a formal request route for high-resolution satellite/aerial imagery and asks for area, time period and resolution. The form does not guarantee availability. | **Potential direct route.** Request coverage for the five exact dates and the R130 mask; confirm provenance, GSD, acquisition timestamps, positional accuracy and research/commercial-use terms before acceptance. |
| Planet NICFI basemaps | Planet NICFI offers 4.77 m mosaics, but the program closure notice says no new monthly basemaps after December 2024; historical imagery remains. The current Earth Engine publisher-catalog metadata also displays a later availability endpoint, so actual asset timestamps and current access terms need reconciliation. | **Not a primary candidate for 2026 date matching.** At best historical context; do not treat an older mosaic as contemporaneous reference. Verify exact asset dates and terms if considered. |
| Ramani Geosystems Citi Data | Advertises orthorectified aerial imagery at 10–20 cm and historical Nairobi imagery, with the published collection described as extending through 2017. | **Not date-matched to 2026.** Could help with stable context or positional checks, not primary validation for these acquisitions. Confirm area coverage and licence before any use. |
| ESA WorldCover / other land-cover products | Published products can provide comparison context, but they are classified land-cover maps rather than independent visual reference observations for the exact R130 dates. | **Comparison only.** Do not score DW against these products as if they were ground truth. |

### Desk-review decision

No source is yet verified as both (a) spatially covering the actual R130 analysis mask and (b) temporally suitable for any of the five 2026 target dates with acceptable rights and resolution. **Gate A remains not passed.** The highest-value next actions are to inspect the Nairobi OpenAerialMap GeoTIFF metadata and request exact-date coverage from Kenya Space Agency. If neither yields qualifying evidence, the honest outcome is that date-specific empirical validation cannot currently be completed with accessible evidence.

Source notes:
- [Nairobi Open Drone Imagery project map](https://umap.hotosm.org/ar/map/nairobi-open-drone-imagery-sdi-ria-project_2646) (metadata currently exposed by the map page is incomplete).
- [Kenya Space Agency imagery request](https://ksaforms.ksa.go.ke/request_imagery/).
- [NICFI program notice](https://openforis.org/fileadmin/planet.html) and [Planet NICFI catalog entry](https://developers.google.com/earth-engine/datasets/catalog/projects_planet-nicfi_assets_basemaps_africa).
- [Ramani Citi Data](https://ramani.co.ke/citidata).
- [ESA WorldCover validation context](https://esa-worldcover.org/en/data-access).

## 9. Current status and next action

Current status: **Gate A not yet passed.** No qualifying local reference imagery inventory or interpreted sample has been established in this repository. The next operational task is a source-feasibility inventory for the five dates and study footprint, recording candidate imagery coverage, date, resolution, registration, licence and access. Only after that inventory should a sample be drawn.

## 10. Method references

- Dynamic World documentation describes the nine class-probability bands, per-image predictions from Sentinel-2 and the recommendation to threshold top-class probability for selecting confident predictions: [Google Earth Engine Data Catalog](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_DYNAMICWORLD_V1).
- The Dynamic World paper describes expert reference annotations and its test dataset; those global test data are useful methodological context but are not automatically a local Nairobi reference sample: [Brown et al. (2022), Scientific Data](https://doi.org/10.1038/s41597-022-01307-4).
- Independent validation requires higher-resolution reference data not used in map production, as summarized by the Copernicus Land Monitoring Service: [How are European CLC data validated?](https://land.copernicus.eu/en/faq/products/corine-land-cover/how-are-european-clc-data-validated).
- Probability sampling, response design and design-aware accuracy assessment are core components of rigorous land-cover validation: [CEOS WGCV LPV Land Cover Validation Protocol (2025)](https://lpvs.gsfc.nasa.gov/PDF/CEOS_WGCV_LPV_Land_Cover_protocol_Sept2025_V1.pdf).


## 9B. OpenAerialMap metadata follow-up (desk review, 2026-11-25)

The first candidate was traced one step further, but it still does not pass Gate A.

- The Nairobi uMap page points to a legacy OpenAerialMap image/TIFF identifier `69ed845c45781de300a01b25` and a TMS view. The page says the imagery was produced through HOT and SDI Kenya's Resilience Initiative Africa collaboration.
- The page's own user-content credit block says **“No licence has been set.”** This is a material reuse-rights gap. General OpenAerialMap descriptions of the platform's licensing do not override the item-specific metadata shown for this candidate.
- The map page's April 27–28, 2026 dates are the project-map creation/modification dates, not verified image acquisition dates. They cannot be used as the capture date.
- OpenAerialMap's current imagery service documents a STAC-native catalogue and exposes a STAC API. The public documentation says item metadata/assets should be inspected through the catalogue and that per-image tile endpoints use a STAC item ID. The legacy identifier in the uMap URL has not been verified as a current STAC item ID; do not assume the two identifier systems are interchangeable.
- A direct catalogue lookup for the legacy identifier was not successfully resolved in this desk review. Therefore no claim is made about the asset's capture date, GSD, footprint, CRS, positional accuracy or downloadable source metadata.

**Decision:** keep this asset as a lead, not a reference source. Before using it, obtain the underlying item record/GeoTIFF and verify: (1) acquisition start/end time, (2) polygon footprint intersection with the frozen R130 mask, (3) pixel size/GSD and CRS, (4) georeferencing/positional accuracy, (5) explicit licence and attribution terms. If the licence remains unset, obtain written permission or exclude the imagery from any reproducible validation dataset.

The current OAM documentation also describes a newer STAC catalogue/API, so future source audits should search that catalogue by Nairobi bbox and date rather than relying only on legacy map URLs.


## 9C. Additional Nairobi drone-imagery lead (desk review, 2026-11-25)

A second, potentially more date-relevant lead was found: [Dandora, Nairobi Drone Imagery](https://umap.hotosm.org/ar/map/dandora-nairobi-drone-imagery_7933), published as a uMap map by a named contributor on 2026-10-23. The page describes it as drone imagery and links to OpenAerialMap. This is closer in calendar time to the 2026-10-18 and 2026-10-30 R130 dates than the April map listing, but **the map publication date is not the drone acquisition date**.

HOT's project page describes drone acquisition across 33 Nairobi villages (approximately 2.7 km²) under its SDI Kenya partnership and says imagery is to be published on OpenAerialMap. That supports the existence of a broader Nairobi drone-imagery programme, but does not establish that the Dandora asset overlaps the R130 mask or was captured near any particular R130 date.

**Decision:** add Dandora as a higher-priority retrieval lead, not as admissible reference evidence. The same checks remain mandatory: actual capture timestamp, image footprint, GSD, CRS/georeferencing, positional accuracy and item-specific licence. Its local footprint may cover only a small part of the study frame; any resulting validation would need to report the covered subpopulation and must not imply citywide representativeness.

Sources:
- [Dandora, Nairobi Drone Imagery uMap listing](https://umap.hotosm.org/ar/map/dandora-nairobi-drone-imagery_7933) (published 2026-10-23; capture metadata not exposed in the indexed page).
- [HOT KYC Nairobi project description](https://www.hotosm.org/en/projects/building-resilience-through-risk-informed-community-led-urban-development-kyc-nairobi/) (describes the 33-village drone mapping programme; does not provide per-asset capture metadata).


## 9D. Date-resolved OpenAerialMap leads (desk review, 2026-11-25)

The catalogue search surfaced a correction to the earlier Dandora lead and one additional October acquisition.

### Dandora UAV imagery — not temporally admissible for primary scoring

The OrionGIS catalogue record identifies the HOTOSM East and Southern Africa Hub Dandora UAV asset as acquired **2026-04-01**, at **5.0 cm/pixel**, with **CC BY 4.0** stated on the catalogue record. A second Dandora Mar–Apr asset is dated **2026-03-26 to 2026-04-03**, at **7.7 cm/pixel**, also listed as CC BY 4.0. These are useful high-resolution historical context, but they are more than 90 days before all five October–November R130 dates. They therefore fail the protocol's temporal rule for primary-date reference scoring. The earlier uMap publication date must not be mistaken for acquisition date.

### Limuru–Kwambira aviation training-ground imagery — promising date, unproven footprint

An SDI Kenya–Muungano wa Wanavijiji catalogue record reports acquisition **2026-10-13 to 2026-10-14**, **4.0 cm/pixel**, GeoTIFF/COG, 17 MB, and **CC BY 4.0**. This is temporally close to the 2026-10-18 R130 date (4–5 days) and potentially useful if the footprint intersects the frozen R130 mask. However:
- The record names Limuru–Kwambira / an aviation training ground, not the R130 study area.
- The record reports “Platform satellite” while naming a DJI Mini 4 Pro sensor; this metadata inconsistency must be resolved with the provider.
- The page gives only country-level coverage in its summary; exact geometry, CRS, positional accuracy and asset acquisition metadata still require inspection.
- A separate set of similarly named catalogue entries appears to describe the same or overlapping project; deduplicate by source item ID and footprint before counting assets.

**Decision:** Dandora is excluded from primary date-specific validation on temporal grounds. Limuru–Kwambira becomes a conditional retrieval lead for the 2026-10-18 date only; do not infer coverage of Nairobi R130 from its Kenya catalogue listing. Even if it intersects the frame, the resulting reference subset may be geographically selective and must be reported as such. It cannot validate the other four dates without separate admissible evidence.

Sources:
- [Dandora UAV imagery record](https://orionterrametrics.com/data/kenya/imagery-land-cover/dandora-uav-imagery-q2sw) — acquisition 2026-04-01, 5.0 cm/pixel, CC BY 4.0 as listed.
- [Dandora Mar–Apr 2026 record](https://orionterrametrics.com/data/kenya/imagery-land-cover/dandora-mar-apr-2026-ufur) — acquisition 2026-03-26 to 2026-04-03, 7.7 cm/pixel, CC BY 4.0 as listed.
- [Limuru–Kwambira record](https://orionterrametrics.com/data/kenya/imagery-land-cover/limuru-kwambira-customized-aviation-training-ground-znt5) — acquisition 2026-10-13 to 2026-10-14, 4.0 cm/pixel, CC BY 4.0 as listed; provider metadata needs reconciliation.
- [Kenya imagery catalogue listing](https://orionterrametrics.com/data/kenya/imagery-land-cover) — additional similarly named Limuru entries, not yet deduplicated.

### Updated source-feasibility decision

Gate A remains **not passed**. We now have one temporally close October lead, but its study-mask intersection and platform metadata are unresolved, and it cannot cover the full five-date design. The next efficient action is to obtain the frozen R130 mask geometry and compare it against the STAC item geometry for the Limuru asset. If the intersection is empty, stop pursuing it for this study. If non-empty, inspect the original COG metadata and confirm the acquisition/platform details directly with the provider before sampling.


## 9E. Study-footprint screening against the acquisition configuration (2026-11-25)

The current Dynamic World acquisition script records the R130 working extent as CRS84 bounding box **[36.65, -1.45, 37.05, -1.15]**. This is a rectangular acquisition extent, not a substitute for the exact valid-pixel/study mask; it is nevertheless a useful first-pass spatial screen.

The Limuru–Kwambira asset is explicitly named for a Limuru aviation training ground. Its catalogue page provides a thumbnail but no machine-readable geometry in the page text reviewed here. Limuru lies north-west of the Nairobi study area, so the item is not assumed to intersect the R130 extent. It must be checked by its authoritative STAC geometry or COG geotransform before any further work. If its footprint does not intersect the bounding box above, it is out of scope and should be dropped immediately.

The OAM STAC landing page is reachable and advertises a GET/POST search endpoint. The current documentation supports filtering by spatial bbox and datetime; however, the web inspection path used in this desk review did not return a usable search response for the R130 bounding box. This is a tooling/retrieval limitation, not evidence that the catalogue contains no matching imagery. A reproducible local STAC query should be run against the endpoint with the exact R130 bbox and date interval, then each returned item's full geometry and properties should be retained.

**Operational conclusion:** we have narrowed the search, but have not demonstrated that any October OAM item intersects the R130 frame. Do not describe the Limuru asset as coverage of Nairobi. The next gate is a geometry-first STAC query using the acquisition script's bbox, followed by exact intersection with the frozen valid-pixel mask if one is available.


## 9D. Limuru–Kwambira imagery metadata reconciliation (desk review, 2026-11-25)

A better metadata record was located for the Limuru–Kwambira UAV imagery. The previously noted variant that described the platform as satellite should not be used as the canonical record. The more detailed OrionGIS index entry reports:

- acquisition interval: **2026-10-12 to 2026-10-13**;
- platform: **UAV**;
- sensor: **DJI Mini 4 Pro**;
- reported ground resolution: **4.0 cm/pixel**;
- provider/publisher: **SDI Kenya–Muungano Wa Wanavijiji**;
- source platform: OpenAerialMap;
- reported licence: **CC BY 4.0**;
- format: GeoTIFF Cloud Optimized GeoTIFF; reported size 16 MB.

This is a material improvement over the earlier ambiguous metadata and is temporally close to the 2026-10-18 R130 acquisition (5–6 days earlier). The indexed record is a third-party discovery/index page, however, not the authoritative STAC Item or source GeoTIFF metadata. Its displayed thumbnail is not georeferenced evidence and cannot establish footprint overlap or positional accuracy.

**Spatial decision remains unresolved.** The R130 search rectangle is [36.65, -1.45, 37.05, -1.15] in CRS84, but the index page reports only country-level coverage (KEN), not a machine-readable footprint. The dataset name suggests a Limuru/Kwambira locality; do not infer intersection or non-intersection from the place name. Retrieve the exact OpenAerialMap STAC Item and inspect its geometry, bbox, acquisition datetime or start/end fields, GSD, platform metadata, asset hrefs and licence. Then compute polygon intersection against the frozen R130 mask, not just the broad discovery rectangle.

The OAM STAC documentation specifies gsd, oam:platform_type, oam:producer_name, item geometry and bbox as core imagery metadata. The public STAC API is documented at https://api.imagery.hotosm.org/stac; search by the R130 bbox and acquisition window, then fetch individual item records. A successful bbox search is only a candidate screen: retain the exact item geometry and test actual overlap.

**Gate A update:** the Limuru–Kwambira record is now a *high-priority, temporally admissible candidate for 2026-10-18 only*, subject to authoritative item-level confirmation. It does not yet establish coverage for the other four dates, nor does it justify any empirical accuracy claim. Its licence is reported as CC BY 4.0 by the index, but confirm the item-specific source licence and attribution in the authoritative record before redistribution.

Sources:
- [OrionGIS Limuru–Kwambira dataset record](https://orionterrametrics.com/data/kenya/imagery-land-cover/limuru-kwambira-customised-aviation-training-ground-9gf6) (acquisition, platform, sensor, GSD and licence as indexed; not authoritative geometry).
- [OpenAerialMap STAC API documentation](https://docs.imagery.hotosm.org/dev/backend/stac-api/).
- [OpenAerialMap STAC schema](https://docs.imagery.hotosm.org/dev/ingest/schema/) (required imagery metadata fields).


## 9E. OpenAerialMap STAC endpoint and reproducible candidate query (2026-11-25)

The OpenAerialMap STAC service root was directly inspected and returned a valid STAC Catalog with a declared `/search` endpoint (GET and POST). This confirms the catalogue route is live; it does **not** confirm that the Limuru–Kwambira item is present in that catalogue or that it overlaps the R130 study area.

A reproducible discovery client has been added at `query_oam_reference_candidates.py`. From the repository root, run:

```bash
python -m pip install requests shapely
python explorations/radar/query_oam_reference_candidates.py
```

The client searches the R130 discovery rectangle and the October–November 2026 date interval, follows STAC `rel=next` pagination, and writes a JSON audit containing item IDs, acquisition datetime fields, platform/GSD metadata, item licence field, geometry/bbox, and asset-key availability. It does not download imagery. The client reports only a boolean geometry-intersection screen against the broad R130 discovery rectangle; it does not calculate an area fraction. A positive result is not proof of overlap with the frozen analysis mask. Retrieve the authoritative item geometry and perform the final intersection in a suitable projected CRS against the exact analysis mask. The client records no item as validated merely because it appears in the search results.

**Execution status:** the STAC root request was verified during this review. The live `/search` request could not be executed from the available review runtime, so no item count, item ID, geometry overlap, or asset availability is claimed. The OrionGIS index entry continues to report 12–13 October acquisition, 4 cm GSD, DJI Mini 4 Pro, and CC BY 4.0, but its own displayed coverage is country-level and is not a substitute for item geometry. Treat all those attributes as indexed metadata pending confirmation in the authoritative STAC Item and source GeoTIFF.

**Next gate:** run the committed query in repository Actions or a network-enabled environment, inspect the exact Limuru item and any overlapping candidates, then perform geometry intersection against the frozen R130 analysis mask. Only after that should the source COG be downloaded and inspected for CRS, affine transform, pixel size, nodata, footprint, acquisition provenance, visual interpretability, and positional alignment.

Sources:
- [OpenAerialMap STAC catalogue root](https://api.imagery.hotosm.org/stac) (live root and advertised search endpoint).
- [OrionGIS Limuru–Kwambira indexed record](https://orionterrametrics.com/data/kenya/imagery-land-cover/limuru-kwambira-customised-aviation-training-ground-9gf6) (secondary metadata record; no item geometry exposed in the page text).
- [STAC API Item Search standard](https://docs.ogc.org/cs/25-005/25-005.html) (bbox, datetime and pagination semantics).

## 9F. First live OpenAerialMap STAC audit result (2026-11-25)

The manually dispatched catalogue audit completed successfully (workflow run [45673737646](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45673737646)). It queried the R130 discovery rectangle and 2026-10-01 through 2026-11-24 interval, and returned **one** candidate item:

- STAC collection: `openaerialmap`
- Item ID: `6aec5e73b093219a6d913430`
- Producer metadata: `Kenya Flying Labs`
- Platform type: `uav`
- Reported GSD: `0.02379` m (approximately 2.38 cm)
- Item licence field: `CC-BY-4.0`
- Acquisition interval: `2026-11-04T21:00:00Z` to `2026-11-05T08:30:51.775Z`
- Item bbox (CRS84): `[36.864017, -1.321417, 36.885078, -1.308559]`
- Geometry: present; intersects the **broad discovery rectangle**.

The acquisition interval is approximately six days before the 2026-11-11 R130 date and is therefore a promising temporal candidate for that date only. It does not provide evidence for the other four R130 dates.

**Important limitations:** this is one catalogue item, not yet an admissible reference source. The audit did not download or inspect the source COG, verify the reported licence with the provider, assess georeferencing/positional accuracy, or intersect the item geometry with the frozen valid-pixel R130 mask. The broad rectangle intersection is only a discovery screen. The item has three catalogue asset keys (`metadata`, `thumbnail`, `visual`); asset presence alone does not establish that a usable full-resolution source asset is available.

**Gate A remains open.** Next steps are to preserve the full STAC item geometry and asset metadata in the audit output, intersect the candidate with the exact R130 mask, retrieve and inspect the source metadata/COG, and confirm acquisition provenance and reuse rights. If the item covers only a small subset of the R130 mask, any eventual reference sample must be explicitly restricted to that supported subset; it cannot be represented as validation of the full study footprint.

## 9G. Full geometry and source-asset inventory (2026-11-25)

The rerun after preserving STAC geometry and asset metadata confirms the same single candidate, item `6aec5e73b093219a6d913430`. The item record identifies the visual asset title as **“Informal settlements Mapping, Nairobi Kenya”**, with a Cloud Optimized GeoTIFF media type and a catalogue-reported size of **870,378,149 bytes** (approximately 830 MiB). The item also advertises a small JSON metadata asset and a PNG thumbnail. The audit preserves the item geometry and the asset descriptors; it does not download the large visual COG.

The catalogue polygon, projected to UTM zone 37S (EPSG:32737), has an approximate footprint area of **3.33 km²** and dimensions of about **2.34 km by 1.42 km**. This is a geometric calculation from the catalogue coordinates, not a measurement of usable valid imagery pixels. The footprint is fully within the broad acquisition rectangle, but exact overlap with the R130 valid-pixel mask remains untested.

**Source retrieval discipline:** inspect the small metadata JSON first, then assess the COG using HTTP range / cloud-optimized access only after the metadata, licence and spatial scope are acceptable. Do not download an 830 MiB image just to discover its acquisition date or CRS. The source metadata fetcher has been added with a 1 MB response cap, an explicit host allowlist, redirect refusal, and no path to the visual COG; its tests cover successful metadata retrieval and untrusted-host rejection.

**Current decision:** the asset is now a strong retrieval candidate for the 2026-11-11 date because its catalogue interval is 2026-11-04 21:00 UTC to 2026-11-05 08:30:51 UTC, its reported GSD is 2.379 cm, and its advertised licence is CC-BY-4.0. These remain catalogue assertions pending metadata/provider verification. Its geographic footprint is small relative to the R130 acquisition rectangle and must not be treated as representative of all bursts, dates or the full study area.

