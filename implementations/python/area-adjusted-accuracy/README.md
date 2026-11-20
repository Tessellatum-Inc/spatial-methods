# Design-based, area-adjusted map accuracy

This small Python companion estimates map accuracy and reference-class area from a probability sample stratified by mapped class.

It fills a deliberately separate gap in the shared [accuracy-assessment metrics package](../accuracy-assessment/README.md). That package provides count-based classification metrics; this companion accounts for mapped-class area proportions and the stated sampling design.

## Supported design

- The map classes are the sampling strata.
- Within each mapped-class stratum, units are selected by simple random sampling.
- Each sampled unit receives a reference class under a documented response protocol.
- The mapped-class area proportions are known and sum to one.
- Samples from different strata are treated as independent.

The estimator is not a generic design-based engine. Do not use it unchanged for cluster, unequal-probability, adaptive, general systematic or spatially balanced samples.

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

A real public-data example is documented in [Fiji 2021 land-cover map accuracy](fiji-case-study.md). The case script downloads a pinned GeoJSON snapshot, verifies its Git blob identity and applies the supported estimator. The raw dataset is not redistributed in this repository.

## Learning materials

- [Introductory learner exercise and worked solution](exercise.md)
- [Advanced three-class disproportionate-sampling exercise](advanced-exercise.md)
- [Advanced exercise sample CSV](advanced-sample.csv)
- [Assessment report template](report-template.md)
- [Fiji 2021 real-data case study](fiji-case-study.md)
- [Fiji case reproduction script](fiji_case_study.py)
- [Fiji case script tests](test_fiji_case_study.py)
- [Introductory synthetic sample CSV](sample.csv)

The test suite includes synthetic regression cases, finite-population correction checks and a structural fixture for the Fiji case script. The Fiji script itself analyses the pinned public dataset when run with network access; its test fixture does not substitute for a live download. Passing tests does not establish support for other sampling designs.
