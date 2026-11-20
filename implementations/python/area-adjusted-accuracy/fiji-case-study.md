# Fiji 2021 land-cover map accuracy: a reproducible stratified-sample case

**Status:** Real public reference-sample data inspected and analysed from a pinned source revision. This is a secondary analysis of the supplied test dataset, not a new field validation campaign.

## Case question

What do the published Fiji 2021 land-use/land-cover test sample and its documented mapped-class stratification imply for overall and class-specific accuracy when sample counts are converted to mapped-area proportions?

This case uses the Fiji LULC test dataset created by John Duncan and published through the Pacific Data Hub and the public `livelihoods-and-landscapes/ccai-data` repository. The dataset is described as an independent test sample for map evaluation, with 834 sample points selected by stratified random sampling within eight classes. The test areas exclude Tikinas used to generate training samples. The dataset is licensed under ODbL; consult the licence before redistributing derived database contents.

## Provenance and acquisition

| Item | Recorded value |
|---|---|
| Dataset | Fiji Land Use Land Cover Test Dataset |
| Publisher | Pacific Data Hub / Pacific Community |
| Author | John Duncan |
| Reference year | 2021 |
| Geography | Fiji, excluding Tikinas used for training data |
| Licence | Open Data Commons Open Database License (ODbL) |
| Source repository | https://github.com/livelihoods-and-landscapes/ccai-data |
| Pinned repository revision | `050021d57c99abaaa6f2c511e4f718a402c7ca2a` |
| File | `fiji-lulc-test-data/fiji-lulc-2021-test-data.geojson` |
| Git blob SHA-1 | `d07afda85d40b2eb6b13d2c17089e5b061a577c9` |
| Format / CRS | GeoJSON FeatureCollection / CRS84 |
| Features | 834 point features |
| Unique coordinates | 834 |
| Invalid point geometries | 0 |

The reproducibility script downloads the pinned GeoJSON from the GitHub raw URL, verifies its Git blob identity, computes a SHA-256 fingerprint and runs the analysis. The source dataset itself is not copied into this repository.

## Sampling and response design

The published dataset description states:
- A stratified random sample was drawn within eight 2021 mapped-class strata.
- The sample frame excludes Tikinas used to generate training data.
- The 2021 map was used to estimate class area proportions and define the strata.
- Reference labels were manually interpreted using 2021 annual median RGB composites from Sentinel-2 and Planet NICFI and high-resolution Google Satellite Basemaps.
- The class populations supplied for weighting are the counts of pixels available to be sampled in each stratum.

The eight strata are water, mangrove, bare soil/rock, urban/impervious, agriculture, grassland, shrubland and tree. The sample's `strata` property is used as the 2021 map class, and `ref_class` is used as the interpreted reference class.

### Documentation discrepancy retained

The dataset page says the total sample is 834, with 100 samples allocated to each of seven minority classes and 133 to the tree class. Those stated allocations sum to 833. The pinned GeoJSON actually contains 834 features: 100 in each of the seven minority strata and **134** in the tree stratum. This analysis uses the observed file counts and preserves the documentation discrepancy in its report; it does not silently alter or discard a record.

## Population weights and observed sample allocation

The source supplies the eligible population pixel counts below. The proportions are calculated by dividing each count by the total of 157,057,276 pixels.

| Mapped stratum | Eligible pixels | Area weight | Observed sample |
|---|---:|---:|---:|
| Water | 1,779,768 | 1.1332% | 100 |
| Mangrove | 3,549,325 | 2.2599% | 100 |
| Bare soil / rock | 541,204 | 0.3446% | 100 |
| Urban / impervious | 687,659 | 0.4378% | 100 |
| Agriculture | 14,279,258 | 9.0918% | 100 |
| Grassland | 15,115,599 | 9.6243% | 100 |
| Shrubland | 4,972,515 | 3.1661% | 100 |
| Tree | 116,131,948 | 73.9424% | 134 |
| **Total** | **157,057,276** | **100.0000%** | **834** |

The sample deliberately gives every minority class 100 observations while the tree class receives 134. This is a disproportionate allocation relative to mapped area. Raw sample-count proportions therefore do not represent the map-area proportions.

## Results

### Raw count accuracy versus area-adjusted accuracy

- Raw count-based overall accuracy: **68.35%** (570/834).
- Area-adjusted overall accuracy: **82.51%**.
- Estimated standard error with finite-population correction: **2.13 percentage points**.
- Approximate 95% Wald interval: **78.34%–86.67%**.

The gap is expected under disproportionate stratification. The raw sample gives each minority class far more influence than its share of the mapped area. The area-proportion error matrix weights each mapped stratum by its known mapped-area proportion before calculating overall accuracy.

### Class-specific estimates

| Class | User's accuracy | Area-adjusted producer's accuracy | Raw count producer's accuracy | Estimated reference-area proportion |
|---|---:|---:|---:|---:|
| Water | 84.00% | 94.50% | 84.85% | 1.0073% |
| Mangrove | 90.00% | 76.25% | 89.11% | 2.6675% |
| Bare soil / rock | 53.00% | 28.06% | 61.63% | 0.6509% |
| Urban / impervious | 44.00% | 40.18% | 91.67% | 0.4795% |
| Agriculture | 55.00% | 88.70% | 79.71% | 5.6374% |
| Grassland | 70.00% | 66.02% | 51.85% | 10.2037% |
| Shrubland | 55.00% | 15.22% | 50.46% | 11.4376% |
| Tree | 88.81% | 96.69% | 63.64% | 67.9161% |

User's accuracy is the within-mapped-stratum diagonal proportion, so it is unchanged by row area weighting. Producer's accuracy uses the estimated reference-class column total and can change sharply when the sample allocation is disproportionate. The urban class is a particularly clear example: raw count producer's accuracy is 91.67%, while the area-adjusted estimate is 40.18%.

Reference-area proportions are estimates for the eligible sampling domain, not the entire Fiji land area without qualification. No hectare estimates are given because the case uses the supplied pixel counts as design weights and does not independently establish an area conversion for every pixel in the study grid.

### Uncertainty and finite-population correction

The population pixel counts are supplied for each stratum, so the estimator applies the finite-population correction (FPC) for SRS without replacement. Because the sample fractions are tiny, the FPC changes the overall standard error only negligibly (from approximately 0.02126493 without FPC to 0.02126491 with FPC).

The reported Wald interval is a normal approximation. The standard errors quantify sampling variation under the documented stratified random design; they do not quantify uncertainty in visual reference interpretation, temporal matching, geolocation, map-class definitions, or the representativeness of the excluded training Tikinas.

## Interpretation and boundaries

This is a genuine data analysis using a public reference sample and the source-provided stratum population counts. It is not a fully independent replication of the original mapping team's validation protocol.

Important limits:
1. **Target geography:** estimates concern the eligible map domain after excluding Tikinas used for training samples. They should not be reported as unqualified national estimates for all of Fiji.
2. **Reference evidence:** labels are quality-checked visual interpretations. The analysis does not re-interpret imagery, audit inter-interpreter agreement or independently verify every reference label.
3. **Map identity:** the `strata` field is the 2021 map class. This case therefore assesses the 2021 map that defined the strata. Comparing another map product requires extracting that product's mapped class at each sample point and using a method that supports sampling strata different from map classes.
4. **Design scope:** the estimator assumes independent SRS within each mapped-class stratum. It is not a generic solution for clustered, unequal-probability or spatially balanced designs.
5. **Population weights:** the pixel counts and sample frame are accepted from the published dataset description; the map raster and eligible-Tikina mask were not independently reconstructed here.
6. **Temporal and spatial support:** the interpretation protocol uses 2021 imagery and 10 m mapping context. Mixed pixels, geolocation error, class ambiguity and temporal mismatch remain possible.
7. **Allocation metadata:** the source's 133-versus-134 tree-sample discrepancy remains open.

## Reproduce

From this directory:

```bash
python fiji_case_study.py --json-out fiji-case-report.json
```

Or provide an already downloaded copy of the exact pinned GeoJSON:

```bash
python fiji_case_study.py --geojson /path/to/fiji-lulc-2021-test-data.geojson
```

The script uses only the Python standard library plus the sibling `area_adjusted_accuracy.py` module. It verifies the pinned Git blob SHA-1 before analysis.

## Sources

- John Duncan. *Fiji Land Use Land Cover Test Dataset*. Pacific Data Hub, modified 15 September 2023. ODbL. Dataset description, sampling design, population counts and data format: https://pacific-data.sprep.org/dataset/fiji-land-use-land-cover-test-dataset
- Source repository and pinned GeoJSON: https://github.com/livelihoods-and-landscapes/ccai-data/tree/050021d57c99abaaa6f2c511e4f718a402c7ca2a/fiji-lulc-test-data
- Olofsson, P., Foody, G. M., Herold, M., Stehman, S. V., Woodcock, C. E., & Wulder, M. A. (2014). Good practices for estimating area and assessing accuracy of land change. *Remote Sensing of Environment*, 148, 42–57. https://doi.org/10.1016/j.rse.2014.02.015

The dataset is external and retains its ODbL terms. The repository stores the reproducibility code and analysis, not a redistributed copy of the GeoJSON.
