# Legend and reference-protocol adjudication: Fiji 2021 versus ESA WorldCover v200

**Status: desk-based legend review completed; point-level imagery adjudication not yet performed.** This note examines whether the dominant transitions may arise partly from different class definitions and reference protocols. It does not relabel any sample point, change the accuracy estimates, or establish the cause of an individual disagreement.

## Why this review is necessary

The 834-point Fiji test sample was stratified using the original Fiji map classes. Its reference labels were manually assigned using 2021 annual-median Sentinel-2 and Planet NICFI RGB composites and high-resolution Google Satellite basemaps. The sample documentation describes the label categories but does not provide a full operational definition for every class on the test-dataset page.

A related Fiji land-cover labels dataset documents operational visual definitions for cropland/agriculture, grassland, scrubland and trees. Those definitions are useful evidence about the Fiji labelling scheme, but the repository has not established that every detail of that companion dataset's protocol was applied identically to every point in this test sample. Treat them as a closely related definition source, not proof of the exact decision made at each test point.

ESA WorldCover 2021 v200 uses the FAO Land Cover Classification System (LCCS), with explicit vegetation-cover thresholds and land-cover concepts. Similar class names therefore do not guarantee equivalent labels.

## Definition comparison

| Topic | Fiji reference-label guidance in the related Fiji labels dataset | ESA WorldCover 2021 v200 | Adjudication implication |
|---|---|---|---|
| Tree / tree cover | Trees are vegetation greater than head height forming a clear canopy. | Tree cover is an area dominated by trees with at least 10% tree cover. Shrubs and herbs may occur below the canopy, even at higher density than trees. Tree plantations are included. | Not equivalent thresholds. A visually clear canopy/height rule and a cover-percentage/dominance rule can classify open woodland and mixed woody vegetation differently. |
| Shrubland / scrubland | The related Fiji labels page calls this “scrubland”: vegetation below head height, not forming a closed canopy, with visible bush, shrub or woody structure. | Natural shrubs dominate with at least 10% cover; shrubs are woody perennials with persistent woody stems and no defined main stem, under 5 m. Scattered trees are allowed below 10% tree cover; herbs may occur at any density. | Strong boundary mismatch risk. Fiji's height and visible-structure rule differs from WorldCover's shrub growth-form and cover threshold. “Scrubland” and “shrubland” also need a controlled vocabulary decision. |
| Grassland | Low vegetation, e.g. below knee height, without bush, shrub or woody structure. | Natural herbaceous vegetation dominates with at least 10% cover. Trees/shrubs may occur if their cover is below 10%. Includes pastures and savannahs, regardless of grazing/fire management; may include uncultivated cropland without a harvest/bare-soil period in the reference year. | Fiji's low-height/no-woody-structure rule is not the same as WorldCover's herbaceous-dominance/cover rule. Savannah, pasture and mixed vegetation are particularly sensitive. |
| Agriculture / cropland | Cropping or livestock-management activity visible in high-resolution imagery; recently fallow land can remain agriculture where evidence of cropping or grazing is visible. | Annual cropland that is sown/planted and harvestable at least once within 12 months after sowing/planting. Perennial woody crops are classified as tree cover or shrubland; greenhouses are built-up. | This is the clearest semantic mismatch. Fiji includes visible livestock/grazing management and evidenced fallow; WorldCover's cropland class is annual-crop focused. Pasture can be WorldCover grassland, and woody perennial crops can be tree/shrub. |
| Herbaceous wetland / tree | Fiji reference legend has no dedicated wetland class; a point is assigned to one of its eight classes. | Herbaceous wetland is natural herbaceous vegetation with at least 10% cover, permanently or regularly flooded. Swamp forests are explicitly classified as tree cover; mangroves are separate. | WorldCover wetland predicted at a Fiji tree reference point is not automatically a contradiction: swamp forest is explicitly tree cover in WorldCover. The reverse interpretation still needs point-level evidence. |

**Sources and scope:** the Fiji test sample description documents its 2021 image interpretation inputs and eight labels. The detailed Fiji visual definitions above come from a related Fiji labels dataset page. WorldCover definitions are from Table 3 of its v200 Product User Manual (version 2.0, 24 October 2022). See the source register entries cited below.

## Reinterpreting the dominant transitions

### 1. WorldCover tree → Fiji reference shrubland (89 points; 10.13 weighted percentage points)

This is the largest observed error contribution, but the two definitions are not directly aligned.

- Fiji's related visual rule separates shrubland and trees using approximate height, canopy closure and visible woody structure.
- WorldCover's tree class uses tree dominance and a 10% cover threshold; shrubs and herbs can be abundant beneath tree canopy.
- WorldCover shrubland instead requires natural shrubs to dominate, with its own growth-form and cover rules.

**What can be concluded now:** a definition mismatch is plausible and material. It is not possible to conclude that all 89 points are genuine WorldCover tree-classification errors. The result should remain a disagreement under the strict working legend, with a flagged semantic-boundary interpretation.

**What imagery review must establish:** whether the sampled location is genuinely dominated by trees at the WorldCover support, whether the Fiji label was driven by low stature/open canopy, and whether the reference interpretation and map pixel represent the same land-cover patch.

### 2. WorldCover tree → Fiji reference grassland (52 points; 3.22 pp)

The Fiji grassland rule excludes visible bush, shrub or woody structure, while WorldCover permits woody plants where tree/shrub cover is below 10% and labels tree cover where trees dominate at 10% or more. The difference could reflect a genuine canopy-cover threshold disagreement, mixed pixels, local patch structure, or a reference-label error.

The imagery review should distinguish:
- isolated trees or sparse woody cover in an otherwise herbaceous patch;
- continuous or dominant tree canopy;
- a point close to a vegetation boundary;
- a scale mismatch between the visual interpretation footprint and the 10 m WorldCover cell.

### 3. WorldCover grassland → Fiji reference agriculture (38 points; 3.13 pp) and WorldCover tree → Fiji agriculture (25 points; 2.13 pp)

The Fiji agriculture definition includes visible livestock management and recently fallow land with evidence of cropping or grazing. WorldCover cropland is annual-crop focused; pastures are explicitly compatible with its grassland class, while perennial woody crops can be mapped as tree cover or shrubland.

This means that some of the large agriculture omission signal may be a **target-definition mismatch**, not simply a failure to recognise cultivated land. It does not explain every point: annual cropland should still be a plausible WorldCover cropland target when the annual-crop definition is met.

The review should record whether each location shows active annual cultivation, recently fallow fields, managed pasture/grazing, perennial woody crops, agroforestry, or natural vegetation. Do not infer agricultural use from green vegetation alone.

### 4. WorldCover herbaceous wetland → Fiji reference tree (7 points; 1.75 pp)

WorldCover's manual explicitly excludes swamp forests from herbaceous wetland and assigns them to tree cover. The observed transition may therefore indicate a genuine disagreement, but it could also represent mixed wetland vegetation, a flooded herbaceous patch interpreted as tree by the Fiji reference, or a local edge effect. The small count makes this a targeted review item, not a general conclusion.

## Revised interpretation of the accuracy findings

The strict eight-class results remain valid as a **literal comparison of the supplied labels under the stated analyst crosswalk**. They should not be described as a definitive ranking of two semantically harmonised products.

The most defensible current statements are:

1. The Fiji and WorldCover labels are not fully definition-equivalent for woody vegetation and agriculture.
2. The large tree-to-shrubland and agriculture-to-grassland/tree transitions coincide with documented differences in class rules.
3. WorldCover's annual-cropland definition is narrower than the related Fiji reference definition, which includes grazing and evidenced fallow.
4. WorldCover's tree definition can include mixed canopies with substantial shrub/herb understorey, whereas the related Fiji visual rule distinguishes classes partly by height and visible structure.
5. These mismatches plausibly contribute to the observed accuracy gap, but their contribution cannot be quantified without re-adjudicating the affected sample points under an explicitly harmonised protocol.

Do not silently recode the existing sample. Keep the strict results, the earlier crosswalk sensitivity scenarios, and any future harmonised re-labelling as separate estimands.

## Point-level imagery adjudication protocol

The present repository analysis artifact contains sample coordinates/labels and extracted WorldCover class values; it does not contain the original reference imagery chips or a saved, point-centred multi-date image stack. No representative points have been visually inspected in this review. Therefore no image-based cause is claimed.

For a defensible next pass:

1. Recover the pinned Fiji GeoJSON and its sample IDs; retain the original `sampling_stratum`, `reference_class` and WorldCover class without overwriting them.
2. Select a documented review subset: all 89 tree→shrubland points if practical, all 63 agriculture→grassland/tree points, and all 7 wetland→tree points. If reviewing fewer, use a reproducible selection rule and retain inclusion probabilities; do not hand-pick only visually striking examples.
3. Assemble imagery close to the 2021 reference period: the cited 2021 annual-median Sentinel-2 and Planet NICFI composites where access permits, plus high-resolution basemap imagery only where its date and licence are known. Record acquisition/composite dates, provider, resolution, projection, URL or asset ID, and licence.
4. Display the WorldCover 10 m cell, sample point, neighbouring cells and a fixed context window. A single pixel is not sufficient to judge a heterogeneous landscape.
5. Have at least two interpreters independently assign a harmonised land-cover label using a written decision tree. Keep land use (cropping/grazing) separate from land cover (herbaceous/woody structure) where possible.
6. Record evidence, confidence, ambiguity, interpreter, date, and adjudication rationale. Resolve disagreements without looking at the map being evaluated where feasible, to reduce confirmation bias.
7. Recompute accuracy only after freezing the revised reference labels and crosswalk. Preserve the original labels and publish the revised results as a separate analysis.
8. If the re-review changes the target concept from land cover to land use, do not compare the resulting metrics as if they estimate the same classification task.

Suggested review worksheet fields:

`sample_id, sampling_stratum, original_reference_class, worldcover_code, image_source, image_date, visible_tree_cover, visible_shrub_structure, herbaceous_cover, annual_crop_evidence, grazing_evidence, fallow_evidence, wetness_evidence, boundary_or_mixed_pixel, harmonised_reference_class, confidence, interpreter, adjudication_note`

## Evidence boundary

- This is a desk-based comparison of published definitions and sample documentation.
- No original image chips, point-level image stacks or field observations were inspected here.
- The related Fiji labels page is supplementary definition evidence; the exact operational rubric used for every point in the 834-point test sample remains incompletely documented.
- No point has been relabelled; no accuracy metric or crosswalk sensitivity result has changed.
- WorldCover's 10 m grid is not a guarantee that the Fiji reference interpretation has identical spatial support.
- Temporal coincidence at the year level does not guarantee that every image composite represents the same season or date.
- Any new reference interpretation should be independently reviewed and preserve the original data and provenance.

## References

- John Duncan / Pacific Data Hub, [Fiji Land Use Land Cover Test Dataset](https://pacific-data.sprep.org/dataset/fiji-land-use-land-cover-test-dataset) (834-point stratified sample and 2021 reference-image protocol; ODbL).
- John Duncan / Pacific Data Hub, [Fiji Land Use Land Cover Labels](https://pacificdata.org/data/dataset/fiji-land-use-land-cover-labels) (related dataset's operational visual class definitions; ODbL).
- Van De Kerchove, R., Zanaga, D., Xu, P., Tsendbazar, N. E., & Lesiv, M. (2022). [Product User Manual WorldCover, v2.0](https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/docs/WorldCover_PUM_V2.0.pdf), especially Table 3 and known limitations. ESA.
- Zanaga et al. (2022). [ESA WorldCover 10 m 2021 v200](https://doi.org/10.5281/zenodo.7254221).
