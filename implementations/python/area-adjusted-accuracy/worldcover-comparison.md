# Comparing a land-cover map with a reference sample stratified by a different map

**Status:** Executed comparison published. All 834 points were sampled from five ESA WorldCover 2021 v200 COG tiles; design-adjusted accuracy and paired comparison outputs are available. The crosswalk remains provisional, and remote raster files were not downloaded or byte-hashed.

## Why this matters

A reference sample is often selected using one map's classes, then reused to evaluate another map. The sampling strata and the evaluated map classes are different variables:

- **Sampling stratum:** the class used to select the sample and define its design weight.
- **Evaluated map class:** the class predicted by the map being assessed at each sampled location.
- **Reference class:** the independently interpreted label for the sampled location.

The sampling strata do not need to equal the evaluated map classes. They must, however, define the probability sample and have valid population area proportions for the same target domain.

The estimator in [\`stratified_accuracy.py\`](stratified_accuracy.py) estimates each cell of the map/reference area-proportion error matrix as

\[
\hat p_{ij}=\sum_{h=1}^{H} W_h
\frac{n_{hij}}{n_h},
\]

where \(h\) indexes the original sampling strata, \(W_h\) is the population area proportion of sampling stratum \(h\), and \(n_{hij}\) is the sample count in stratum \(h\) whose evaluated map class is \(i\) and reference class is \(j\).

Overall accuracy is the sum of the diagonal cells. Mapped-class and reference-class area proportions are estimated from row and column totals. User's and producer's accuracy are ratios of the appropriate diagonal cell to the estimated row or column marginal, with delta-method uncertainty approximations.

For each indicator estimated from stratum \(h\), the variance contribution uses the within-stratum sample variance and, when population size is supplied, the finite-population correction \(1-n_h/N_h\).

## Fiji–WorldCover comparison

This workflow reuses the 834-point Fiji 2021 LULC test sample, but evaluates ESA WorldCover 2021 v200 at the same sample locations.

### Data and target population

- Reference sample: John Duncan's Fiji Land Use Land Cover Test Dataset.
- Sampling design: stratified random sample within the eight original Fiji 2021 mapped classes.
- Sampling frame: the eligible Tikinas after excluding Tikinas used to generate training samples.
- Sampling weights: the original Fiji map's eligible stratum pixel counts, not WorldCover's class proportions.
- Evaluated product: ESA WorldCover 2021 v200, 10 m land-cover map.
- Reference labels: the supplied Fiji test sample interpretations.
- Spatial support: one WorldCover raster cell containing each sample point.

The target is the same eligible sampling domain represented by the Fiji sample and supplied stratum counts. Do not describe the result as a complete national Fiji estimate if the excluded training Tikinas are not in the target frame.

### First executed results

The first successful GitHub Actions run sampled all 834 points from the five listed ESA COG tiles. Each source opened as a 36,000 × 36,000, one-band `uint8` GeoTIFF in EPSG:4326, with 10 m product resolution and zero as nodata. All 834 points were assigned to exactly one tile and returned a valid class value. The run used remote COG range reads; it did not download or hash complete raster files.

**Area-adjusted WorldCover overall accuracy: 74.12%** (standard error 2.37 percentage points; approximate 95% Wald interval 69.47%–78.76%).

The same 834 reference points give an estimated 82.51% overall accuracy for the original Fiji map. A paired, design-based comparison of point-level correctness gives:

- WorldCover overall accuracy: 74.12%.
- Original Fiji map overall accuracy: 82.51%.
- WorldCover minus original map: **−8.39 percentage points**.
- Paired standard error: 1.50 percentage points.
- Approximate 95% Wald interval for the difference: **−11.32 to −5.45 percentage points**.

The paired estimator uses the within-stratum sample variance of the difference between the two maps' correctness indicators, so it preserves the covariance created by evaluating both maps at the same sampled points. The interval is conditional on the stated stratified-SRS design, source population weights, target frame and class crosswalk; it is not a universal ranking of the two products.

WorldCover classes observed at the 834 sample locations were:

| Evaluated WorldCover class | Sample points | Estimated eligible-domain area |
|---|---:|---:|
| Tree | 383 | 81.46% |
| Grassland | 190 | 11.33% |
| Water | 110 | 2.31% |
| Mangrove | 102 | 1.98% |
| Herbaceous wetland | 12 | 2.49% |
| Urban / built-up | 28 | 0.21% |
| Bare / sparse vegetation | 7 | 0.03% |
| Cropland / agriculture | 2 | 0.18% |

These are design-weighted estimates from the sample, not direct measurements of WorldCover's total mapped area. No sample point received WorldCover codes 20 (shrubland), 70 (snow and ice) or 100 (moss and lichen). Their absence in this sample is not proof that those classes are absent from the target domain; class-specific accuracy for them cannot be estimated from these observations.

**Class-level caution:** the agriculture estimate is based on two sample points, bare/sparse vegetation on seven, and urban/built-up on 28. The herbaceous-wetland observations all disagree with the eight-class Fiji reference legend, producing a zero point estimate for user's accuracy and a degenerate zero estimated variance. Such boundary estimates must not be interpreted as certainty. The paired overall comparison is more stable than these sparse class-specific ratios, but it remains dependent on the provisional crosswalk below.

The source dataset's eligible domain excludes Tikinas used for training. Its stratum population pixel counts are accepted as supplied; the source raster and exclusion mask were not independently reconstructed. Reference labels remain the dataset's visual interpretations. No positional-tolerance or mixed-pixel rule was applied: each point was assigned the class of its containing raster cell.

The [successful automated rehearsal and downloadable outputs](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/44695806784) contain the sampled CSV, source/raster metadata, accuracy report and paired comparison report.

### ESA WorldCover class legend and provisional harmonisation

The extraction script maps WorldCover class codes to working labels:

| WorldCover code | ESA class | Working label | Fiji reference correspondence |
|---:|---|---|---|
| 10 | Tree cover | tree | tree |
| 20 | Shrubland | shrubland | shrubland |
| 30 | Grassland | grassland | grassland |
| 40 | Cropland | agriculture | agriculture |
| 50 | Built-up | urban | urban |
| 60 | Bare / sparse vegetation | bare_soil_rock | bare soil / rock |
| 70 | Snow and ice | snow_ice | no direct reference class |
| 80 | Permanent water bodies | water | water |
| 90 | Herbaceous wetland | herbaceous_wetland | no direct reference class |
| 95 | Mangroves | mangrove | mangrove |
| 100 | Moss and lichen | moss_lichen | no direct reference class |

This is a **provisional analyst-defined crosswalk**, not an authoritative equivalence between two land-cover ontologies. Cropland/agriculture, built-up/urban and bare/sparse vegetation/bare soil-rock are broad correspondences. Review the source class definitions and the study's target legend before treating these as semantically equivalent. Codes 70, 90 and 100 have no direct class in the eight-class Fiji reference legend; if any occur at sample points, they remain distinct evaluated-map classes and contribute as errors to overall accuracy rather than being silently forced into a different reference category.

A custom code-to-label mapping can be supplied to the extraction script. Any alternative must be documented and applied consistently.

### Prepare the raster

ESA WorldCover 2021 v200 is distributed as 10 m Cloud Optimized GeoTIFF tiles in EPSG:4326. Download the tiles covering every Fiji sample point from the official data access page. For multiple tiles, build a virtual raster (VRT) or mosaic that covers the entire sample. Do not sample a rendered WMS/WMTS image: those services are intended for display, not analytical class extraction.

The 834 sample coordinates cross the antimeridian and fall in **five** 3° × 3° tiles: `S18E174`, `S18E177`, `S18W180`, `S21E177` and `S21W180`. This was derived from all 834 coordinates in the pinned GeoJSON; do not assume one Fiji tile covers the sample. This coordinate audit found 1 point in S18E174, 602 in S18E177, 44 in S18W180, 172 in S21E177 and 15 in S21W180. The script accepts repeated `--raster` arguments and checks that each point falls in exactly one supplied tile. It transforms the GeoJSON EPSG:4326 coordinates to each raster CRS before sampling. It fails on missing coverage, nodata, overlapping supplied tiles or unrecognised class codes; it does not silently drop points.

The official tile naming convention encodes the lower-left latitude and longitude of each 3° tile. The five source URLs are:

```text
https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/ESA_WorldCover_10m_2021_v200_S18E174_Map.tif
https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/ESA_WorldCover_10m_2021_v200_S18E177_Map.tif
https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/ESA_WorldCover_10m_2021_v200_S18W180_Map.tif
https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/ESA_WorldCover_10m_2021_v200_S21E177_Map.tif
https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/ESA_WorldCover_10m_2021_v200_S21W180_Map.tif
```

The script can now read HTTPS COG URLs directly through GDAL's `/vsicurl/` virtual filesystem. This can use HTTP range requests to read only the raster blocks needed around the sample points rather than downloading every full tile. The AWS objects have not been byte-verified in this repository; a successful extraction must still confirm that every URL resolves, every point is covered exactly once and no sampled cell is nodata. Remote reads record source URLs and raster metadata but cannot provide a local whole-file SHA-256. For a byte-level audit, download the tiles locally and use local file paths instead.

### Install the optional extraction dependency

\`\`\`bash
python -m pip install -r requirements-worldcover.txt
\`\`\`

### Extract WorldCover classes at the reference points

\`\`\`bash
python sample_worldcover.py \\
  --geojson /path/to/fiji-lulc-2021-test-data.geojson \\
  --raster https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/ESA_WorldCover_10m_2021_v200_S18E174_Map.tif \\
  --raster https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/ESA_WorldCover_10m_2021_v200_S18E177_Map.tif \\
  --raster https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/ESA_WorldCover_10m_2021_v200_S18W180_Map.tif \\
  --raster https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/ESA_WorldCover_10m_2021_v200_S21E177_Map.tif \\
  --raster https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/ESA_WorldCover_10m_2021_v200_S21W180_Map.tif \\
  --output worldcover-fiji-sample.csv
\`\`\`

The script verifies the pinned Fiji GeoJSON Git blob SHA-1 and 834-feature count. It assigns stable IDs based on feature order in that pinned file, retains the original sampling stratum and reference label, samples WorldCover band 1, and writes a sidecar JSON containing raster metadata and file fingerprints. Stable sample IDs are local identifiers created for this workflow; they are not supplied by the source dataset.

The extraction is a single-pixel point sample. It does not apply a majority window, buffer, positional tolerance, or mixed-pixel rule. Those choices would change the response protocol and must be justified before use.

### Automated rehearsal

The repository includes [`.github/workflows/fiji-worldcover-rehearsal.yml`](../../../.github/workflows/fiji-worldcover-rehearsal.yml). It runs on a targeted change to the extraction/estimator files or by manual `workflow_dispatch`. The job retrieves the pinned Fiji GeoJSON, reads the five public COG URLs through GDAL range requests, samples the points, runs the independent-strata estimator and uploads the CSV, provenance sidecar and accuracy JSON as a 30-day workflow artifact. It does not commit source imagery or generated outputs to the repository.

A successful workflow is the first gate for claiming a WorldCover result. Inspect the artifact's sample count, per-tile coverage, raster CRS/resolution/nodata metadata and the class distribution before interpreting the accuracy report. A failed workflow is not a result; inspect the failed step and update the documented source status.

### Run the design-based comparison

The original eligible stratum pixel counts sum to 157,057,276. Use those as the sampling-stratum population sizes:

\`\`\`bash
python stratified_accuracy.py worldcover-fiji-sample.csv \\
  --stratum-area-weights '{"water":0.011331967836,"mangrove":0.022598921173,"bare_soil_rock":0.003445902118,"urban":0.004378396325,"agriculture":0.090917519797,"grassland":0.096242589869,"shrubland":0.031660519822,"tree":0.739424183060}' \\
  --stratum-population-sizes '{"water":1779768,"mangrove":3549325,"bare_soil_rock":541204,"urban":687659,"agriculture":14279258,"grassland":15115599,"shrubland":4972515,"tree":116131948}' \\
  --json-out worldcover-fiji-accuracy.json
\`\`\`

The area weights are calculated from the population counts; the displayed decimals are rounded to 12 decimal places. The implementation validates that the weights sum to one within tolerance.

For a paired comparison with the original Fiji map, run:

```bash
python paired_map_comparison.py worldcover-fiji-sample.csv \
  --stratum-area-weights '{"water":0.011331967836,"mangrove":0.022598921173,"bare_soil_rock":0.003445902118,"urban":0.004378396325,"agriculture":0.090917519797,"grassland":0.096242589869,"shrubland":0.031660519822,"tree":0.739424183060}' \
  --stratum-population-sizes '{"water":1779768,"mangrove":3549325,"bare_soil_rock":541204,"urban":687659,"agriculture":14279258,"grassland":15115599,"shrubland":4972515,"tree":116131948}' \
  --json-out worldcover-fiji-paired-comparison.json
```

The default baseline column is `sampling_stratum`, valid here because the original Fiji map classes defined the sampling strata. For another baseline map, supply its actual sampled class column using `--baseline-map-column`.

### What the output means

- Matrix rows: harmonised ESA WorldCover classes at sample points.
- Matrix columns: Fiji reference classes.
- Matrix cell: estimated proportion of the eligible target area in that map/reference combination, weighted by the **original Fiji sampling strata**.
- Overall accuracy: sum of diagonal cells after class harmonisation.
- User's accuracy: diagonal cell divided by estimated area mapped to that class.
- Producer's accuracy: diagonal cell divided by estimated reference area for that class.
- Mapped-class area estimates: row totals.
- Reference-class area estimates: column totals.

The sample allocation discrepancy remains: source text describes 133 tree-stratum samples, while the pinned GeoJSON contains 134. This workflow uses the actual 834 records and retains that discrepancy in the provenance.

## Comparing two or more evaluated maps

The same sample may be reused to evaluate another map if its class values can be extracted at exactly the same sample points and the map's legend can be harmonised to the same reference legend. Each map should have its own evaluated-map class column and its own results. Keep the sample IDs, reference labels, original sampling strata, population weights, target domain and reference protocol fixed.

Do not compare maps using separate convenience samples and then attribute differences solely to map quality. If maps are sampled on different supports, dates, masks or target domains, document those differences.

## Design assumptions and limitations

1. Independent SRS without replacement is assumed within each of the eight original sampling strata.
2. The supplied stratum pixel counts are accepted as population sizes; the original raster and eligible-Tikina mask are not independently reconstructed here.
3. No arbitrary unequal-probability, cluster, systematic or spatially balanced design is supported.
4. Reference labels are treated as correct; interpreter and reference-image uncertainty are not propagated.
5. The sample's target domain excludes training Tikinas.
6. Class harmonisation is a substantive analytical decision, not a cosmetic renaming exercise.
7. One-pixel sampling does not resolve positional mismatch, mixed pixels or ambiguity at class boundaries.
8. Wald intervals and delta-method ratio intervals are approximations, especially fragile for rare classes and small denominators.
9. The 2021 product's independent global validation statistics are not directly comparable with a Fiji-domain estimate from this sample. They use a different validation design and target population.

## Current execution status

- Fiji GeoJSON: retrieved by the successful workflow and verified against its pinned Git blob SHA-1; SHA-256 is recorded in the provenance sidecar.
- WorldCover raster: all five official COG objects opened successfully over HTTPS; dimensions, bounds, CRS, resolution, nodata and source URLs were recorded. Full raster files were not downloaded or SHA-256 hashed.
- Extraction: all 834 reference points were sampled successfully, with no missing coverage, overlap or nodata failures.
- WorldCover design-adjusted overall accuracy: 74.12% (SE 2.37 percentage points; approximate 95% Wald interval 69.47%–78.76%).
- Paired comparison against the original Fiji map: −8.39 percentage points (paired SE 1.50; approximate 95% Wald interval −11.32 to −5.45).
- Reproducibility outputs: [successful GitHub Actions run and 30-day artifact](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/44695806784).

## Sources

- ESA WorldCover data access and licence: https://esa-worldcover.org/en/data-access


Required attribution for the WorldCover product: **© ESA WorldCover project 2021 / Contains modified Copernicus Sentinel data (2021) processed by ESA WorldCover consortium.** The product is provided under CC BY 4.0. Citation: Zanaga et al. (2022), *ESA WorldCover 10 m 2021 v200*, https://doi.org/10.5281/zenodo.7254221.
- ESA WorldCover 2021 v200 Product User Manual: https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/docs/WorldCover_PUM_V2.0.pdf
- ESA WorldCover Product Validation Report v2.0: https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/docs/WorldCover_PVR_V2.0.pdf
- Fiji Land Use Land Cover Test Dataset: https://pacific-data.sprep.org/dataset/fiji-land-use-land-cover-test-dataset
- Olofsson et al. (2014), Good practices for estimating area and assessing accuracy of land change, *Remote Sensing of Environment*, 148, 42–57. https://doi.org/10.1016/j.rse.2014.02.015
