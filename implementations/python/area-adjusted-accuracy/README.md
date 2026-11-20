# Design-based, area-adjusted map accuracy

This Python companion contains two design-based estimators for map accuracy and reference-class area: one for a sample stratified by the evaluated map, and one for a sample stratified independently of the evaluated map.

It fills a deliberately separate gap in the shared [accuracy-assessment metrics package](../accuracy-assessment/README.md). That package provides count-based classification metrics; this companion accounts for mapped-class area proportions and the stated sampling design.

## Supported designs

**Original estimator — `area_adjusted_accuracy.py`**
- The evaluated map classes are also the sampling strata.
- Within each mapped-class stratum, units are selected by simple random sampling.
- Mapped-class area proportions are known and sum to one.

**Independent-strata estimator — `stratified_accuracy.py`**
- The sample is selected within supplied sampling strata that may differ from the evaluated map classes.
- The eligible population area proportions of the sampling strata are known and sum to one.
- Each sampled unit has both an evaluated map class and a reference class.

Both estimators assume independent simple random sampling without replacement within strata. Neither is a generic engine for cluster, arbitrary unequal-probability, adaptive, general systematic or spatially balanced samples. The target population and response protocol must remain appropriate for the map being evaluated.

## When sampling strata differ from the evaluated map

Use this when a reference sample was selected using one map, but you want to evaluate another map at the same sample locations. The input columns are `sampling_stratum`, `map_class` and `reference_class`. Sampling-stratum weights must describe the target population; they are not the evaluated map's class proportions.

```csv
sample_id,sampling_stratum,map_class,reference_class
p01,original_forest,tree,tree
p02,original_forest,grassland,grassland
p03,original_water,water,water
```

Run the general estimator with weights and, optionally, eligible population sizes keyed by sampling stratum:

```bash
python stratified_accuracy.py comparison.csv \
  --stratum-area-weights '{"original_forest":0.7,"original_water":0.3}' \
  --stratum-population-sizes '{"original_forest":7000,"original_water":3000}' \
  --json-out comparison-report.json
```

The general estimator constructs each map/reference cell by weighting its within-sampling-stratum joint proportion. It then estimates overall accuracy, mapped-class and reference-class area marginals, user's accuracy and producer's accuracy. Map and reference labels must be harmonised to a defensible common legend. If a map has classes with no reference counterpart, those labels remain distinct and are counted as disagreement; do not force them into a convenient class without a documented crosswalk.

### Fiji sample and ESA WorldCover 2021 v200

The repository now includes an extraction workflow for evaluating ESA WorldCover against the Fiji reference sample without pretending that WorldCover classes were the sampling strata.

1. Download the five official WorldCover 2021 v200 10 m COG tiles covering the Fiji sample points. You can pass all five as repeated `--raster` arguments or build a VRT. Use analytical raster data, not a rendered WMS/WMTS.
2. Install the optional `rasterio` dependency: `python -m pip install -r requirements-worldcover.txt`.
3. Sample the WorldCover raster at the pinned 834 Fiji reference points:

```bash
python sample_worldcover.py \
  --geojson /path/to/fiji-lulc-2021-test-data.geojson \
  --raster /path/to/worldcover-2021-fiji.vrt \
  --output worldcover-fiji-sample.csv
```

4. Run `stratified_accuracy.py` using the original Fiji sampling-stratum weights and pixel counts. The full command and class harmonisation discussion are in [the Fiji–WorldCover comparison guide](worldcover-comparison.md).

The extraction script preserves the original Fiji sample strata, reference labels and point order, assigns stable local sample IDs, transforms point coordinates to the raster CRS and fails on nodata or missing coverage. It writes a provenance sidecar with raster metadata and file fingerprints. Its default WorldCover-to-reference label mapping is provisional and must be reviewed for the intended legend before interpreting accuracy.

**No WorldCover raster has yet been sampled and no WorldCover comparison result is claimed.**

## Input

CSV with one row per sampled unit:

```csv
sample_id,map_class,reference_class
s01,forest,forest
s02,forest,other
s03,other,other
```

The script requires `map_class` and `reference_class`. `sample_id` is retained for the user's audit trail but is not used in calculations.

## Run

From this directory:

```bash
python area_adjusted_accuracy.py sample.csv --area-weights '{"forest":0.6,"other":0.4}' --total-area 125000 --json-out report.json
python area_adjusted_accuracy.py sample.csv --area-weights '{"forest":0.6,"other":0.4}' --stratum-population-sizes '{"forest":10000,"other":20000}'
python fiji_case_study.py --json-out fiji-case-report.json
python -m unittest -v
```

Area weights are proportions of the total mapped area, not sample proportions. `--total-area` is optional and must use a declared unit (for example hectares or square metres).

## Estimates

Rows of the estimated error matrix are mapped classes (sampling strata); columns are reference classes. Each cell is the estimated proportion of the total mapped area in that map/reference combination:

\[
\hat p_{ij}=W_i\frac{n_{ij}}{n_i}.
\]

The report includes:
- estimated area-proportion error matrix;
- overall accuracy and its estimated standard error;
- user's accuracy by mapped class;
- producer's accuracy by reference class;
- reference-class area proportions and standard errors;
- optional reference-class area estimates in the caller's area units;
- normal-approximation 95% Wald intervals.

For the supported stratified design, the variance of the overall accuracy estimate is estimated by

\[
\widehat{\operatorname{Var}}(\widehat{OA})=
\sum_i W_i^2\frac{\hat U_i(1-\hat U_i)}{n_i-1}f_i,
\]

where \(\hat U_i=n_{ii}/n_i\) and \(f_i=1-n_i/N_i\) when stratum population size \(N_i\) is supplied; otherwise \(f_i=1\). Reference-class area proportion estimates are column totals of the area-proportion error matrix. Their variance is estimated by summing the independent within-stratum proportion variances with the same stratum-specific correction. Producer's-accuracy uncertainty uses a delta-method approximation for its ratio estimator.

## Important interpretation

A raw count-based confusion matrix is not an area-proportion error matrix when the sample is stratified disproportionately. Do not calculate overall accuracy as the unweighted sum of diagonal sample proportions in that situation.

The reference labels are treated as correct for this estimator. If interpretation uncertainty, temporal mismatch, positional mismatch or ambiguous classes matter, they need an explicit response-design and uncertainty treatment.

The Wald intervals are simple normal approximations, not universally reliable small-sample intervals. If valid stratum population sizes are supplied, the implementation applies the SRS-without-replacement finite-population correction to the within-stratum variance contributions. If population sizes are not supplied, no correction is applied. Variance in the mapped-class area weights is not included.

This is an educational and analytical baseline, not a regulatory or certification tool. A defensible assessment still requires a complete sampling frame, a probability selection protocol, suitable reference data, documented interpretation rules, and an analysis consistent with the actual design.

## References

- Olofsson, P., Foody, G. M., Herold, M., Stehman, S. V., Woodcock, C. E., & Wulder, M. A. (2014). Good practices for estimating area and assessing accuracy of land change. *Remote Sensing of Environment*, 148, 42–57. https://doi.org/10.1016/j.rse.2014.02.015
- Olofsson, P., Foody, G. M., Stehman, S. V., & Woodcock, C. E. (2013). Making better use of accuracy data in land change studies: Estimating accuracy and area and quantifying uncertainty using stratified estimation. *Remote Sensing of Environment*, 129, 122–131. https://doi.org/10.1016/j.rse.2012.10.031

A real public-data analysis is documented in [Fiji 2021 land-cover map accuracy](fiji-case-study.md). The [Fiji–WorldCover comparison guide](worldcover-comparison.md) is a separate, prepared comparison workflow; its WorldCover extraction remains pending raster acquisition and execution.

## Learning materials

- [Introductory learner exercise and worked solution](exercise.md)
- [Advanced three-class disproportionate-sampling exercise](advanced-exercise.md)
- [Advanced exercise sample CSV](advanced-sample.csv)
- [Assessment report template](report-template.md)
- [Fiji 2021 real-data case study](fiji-case-study.md)
- [Fiji case reproduction script](fiji_case_study.py)
- [Fiji case script tests](test_fiji_case_study.py)
- [Estimator for independent sampling strata](stratified_accuracy.py)
- [Tests for the independent-strata estimator](test_stratified_accuracy.py)
- [ESA WorldCover point-sampling script](sample_worldcover.py)
- [WorldCover sampling tests](test_sample_worldcover.py)
- [WorldCover comparison guide](worldcover-comparison.md)
- [Optional rasterio requirements](requirements-worldcover.txt)
- [Introductory synthetic sample CSV](sample.csv)

The earlier mapped-class implementation's 10-test suite was run against a local mirror recreated from fetched repository sources. The new independent-strata estimator and pinned point-reader tests have not yet been executed; no GitHub Actions run has been triggered. Passing tests does not establish support for other sampling designs or validate the provisional class crosswalk.
