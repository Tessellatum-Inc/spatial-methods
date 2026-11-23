# Fiji–WorldCover spatial disagreement analysis

**Status:** Executed on the 834-point sample extracted in the WorldCover rehearsal. Four outcome proportions use the original Fiji sampling strata, supplied eligible-domain area weights and finite-population corrections. Point-level spatial output is provided as GeoJSON. Nearest-neighbour summaries are exploratory descriptions, not tests of spatial clustering.

## What is being compared

At each sampled location, the original Fiji map class is represented by the original sampling-stratum label, because that map defined the sample. The WorldCover class is the value extracted from the single 10 m raster cell containing the same point. Both are compared with the supplied reference interpretation.

The four mutually exclusive outcomes are:

1. **Both correct:** both mapped classes equal the reference class.
2. **Fiji only correct:** the original Fiji map equals the reference; WorldCover does not.
3. **WorldCover only correct:** WorldCover equals the reference; the original Fiji map does not.
4. **Both wrong:** neither map equals the reference.

This is not identical to direct map-label disagreement. Both maps can be wrong but still predict the same wrong class. The report therefore also calculates whether the two maps' class labels differ and separates same-wrong-class from different-wrong-class cases.

## Design-based estimates

For outcome \(k\), the estimated eligible-domain proportion is

\[
\hat P_k=\sum_h W_h\hat p_{hk},
\]

where \(h\) indexes the eight original Fiji sampling strata, \(W_h\) is the supplied eligible-domain area proportion, and \(\hat p_{hk}\) is the observed outcome proportion within stratum \(h\).

The variance estimator is the stratified SRS-without-replacement indicator variance, with the supplied finite-population correction \(1-n_h/N_h\). Wald intervals are approximate. The four outcome proportions sum to one, but their estimates are correlated; their individual confidence intervals should not be added or interpreted independently.

### Results

| Outcome | Sample points | Design-weighted estimate | SE | Approx. 95% Wald interval |
|---|---:|---:|---:|---:|
| Both correct | 337 | 70.88% | 2.34 pp | 66.29%–75.47% |
| Fiji only correct | 233 | 11.63% | 1.36 pp | 8.96%–14.29% |
| WorldCover only correct | 96 | 3.24% | 0.43 pp | 2.40%–4.08% |
| Both wrong | 168 | 14.25% | 2.11 pp | 10.12%–18.39% |

The design-weighted estimate of direct map-label disagreement is **19.87%** (455 of 834 points; SE 1.41 pp; approximate 95% Wald interval 17.10%–22.63%). Within the both-wrong group, the maps assigned the same wrong class at 42 points and different wrong classes at 126 points.

The weighted outcome split is more informative than raw point counts alone because the original sample intentionally oversampled minority mapped classes. The large tree stratum also carries most of the eligible-domain area weight. Per-stratum sample counts, within-stratum outcome proportions, weighted contributions and FPC values are retained in the JSON report.

## Spatial inspection

The spatial_disagreement.py script writes a GeoJSON FeatureCollection containing all 834 points. Each feature retains the sample ID, original sampling stratum, original Fiji map class, WorldCover class, reference class, four-way outcome, direct map-label disagreement flag, WorldCover code and source tile. Coordinates remain longitude/latitude (CRS84 / EPSG:4326).

The script also reports great-circle nearest-neighbour distances separately for the direct map-label-disagreement points and map-label-agreement points. Longitude differences are wrapped across the antimeridian, which matters for this Fiji sample. The observed nearest-neighbour median is 2.53 km for map-label-disagreement points and 3.18 km for map-label-agreement points. These are descriptions of sampled-point geometry only. They are not Moran's I, a scan statistic, a point-process test or a design-adjusted spatial-clustering test. The sample is stratified by the original map, and its spatial intensity is not uniform; nearest-neighbour contrasts must not be interpreted as inferential evidence of clustering.

The source GeoJSON attributes contain only the reference class and sampling stratum. No administrative-region field is available in this sample, so this analysis does not assign points to provinces, islands or other named regions.

## Reproduction

From this directory, using the CSV produced by the successful WorldCover rehearsal:

\`\`\`bash
python -m unittest -v test_spatial_disagreement.py
python spatial_disagreement.py worldcover-fiji-sample.csv \\
  --stratum-area-weights '{"water":0.011331967836,"mangrove":0.022598921173,"bare_soil_rock":0.003445902118,"urban":0.004378396325,"agriculture":0.090917519797,"grassland":0.096242589869,"shrubland":0.031660519822,"tree":0.739424183060}' \\
  --stratum-population-sizes '{"water":1779768,"mangrove":3549325,"bare_soil_rock":541204,"urban":687659,"agriculture":14279258,"grassland":15115599,"shrubland":4972515,"tree":116131948}' \\
  --json-out fiji-worldcover-spatial-disagreement.json \\
  --geojson-out fiji-worldcover-spatial-disagreement.geojson
\`\`\`

The JSON records the input CSV SHA-256, all stratum-level estimates, weighted four-outcome proportions, direct map-label disagreement and exploratory distance summaries. The GeoJSON preserves all point-level outcome labels for mapping in GIS.

## Interpretation limits

- Estimates apply to the eligible Fiji sample frame, excluding Tikinas used for training samples; they are not an unqualified estimate for all Fiji.
- The original map class is taken from sampling_stratum, which is justified only because the original Fiji map defined those strata.
- Reference labels are supplied visual interpretations, not independently field-verified labels.
- WorldCover uses the single pixel containing each point; positional tolerance and mixed-pixel effects are not modelled.
- The strict eight-class working crosswalk remains provisional. Crosswalk sensitivity is reported separately.
- Sampling uncertainty intervals do not include uncertainty in reference labels, crosswalk choices, positional support, temporal alignment or supplied area weights.
- Nearest-neighbour distances are descriptive and are not adjusted for the stratified design. No spatial-clustering significance claim is made.
- No administrative geography was inferred from coordinates.
