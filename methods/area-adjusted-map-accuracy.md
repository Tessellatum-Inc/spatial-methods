# Design-based, area-adjusted map accuracy and class-area estimation

**Kind:** Method  
**Status:** Researched synthesis; supported implementation is a bounded stratified estimator.  
**Scope:** Probability samples with independent simple random sampling within known strata. The original mapped-class-stratified estimator is a special case; a second estimator supports evaluating a map whose classes differ from the sample's original strata.

## Why the ordinary confusion matrix can mislead

A confusion matrix of sample counts describes the realised sample. If sampling is disproportionate across mapped classes, those counts do not represent the mapped area proportions. An unweighted overall accuracy or class-area estimate can therefore answer the wrong question.

For a map divided into mapped-class strata, let (W_i) be the proportion of total map area in mapped class (i), (n_i) the sample size in that stratum and (n_{ij}) the number of sampled units mapped as class (i) and interpreted as reference class (j).

The area-proportion error matrix estimator is

[
hat p_{ij}=W_irac{n_{ij}}{n_i}.
]

Rows are mapped classes; columns are reference classes. The estimated overall accuracy is

[
widehat{OA}=sum_ihat p_{ii}.
]

The user's accuracy for mapped class (i) is the within-stratum diagonal proportion,

[
widehat{UA}_i=rac{n_{ii}}{n_i},
]

while the producer's accuracy for reference class (j) is

[
widehat{PA}_j=
rac{hat p_{jj}}{sum_ihat p_{ij}}.
]

The estimated reference area proportion for class (j) is the column total

[
hat P_j=sum_ihat p_{ij}.
]

For total mapped area (A), the estimated reference-class area is (Ahat P_j). This adjusts the mapped area using the reference sample rather than assuming the map's class totals are correct.

## Uncertainty under the supported design

For independent simple random samples without replacement within mapped-class strata, let \(N_i\) be the number of eligible population units in stratum \(i\). When these population sizes are known, the finite-population correction is \(f_i=1-n_i/N_i\). An estimator of overall-accuracy variance is

\[
\widehat{\operatorname{Var}}(\widehat{OA})=
\sum_i W_i^2\frac{\hat U_i(1-\hat U_i)}{n_i-1}f_i,
\qquad \hat U_i=n_{ii}/n_i.
\]

For a reference-class area proportion, the estimated variance is the sum of the independent stratum contributions,

\[
\widehat{\operatorname{Var}}(\hat P_j)=
\sum_i W_i^2\frac{\hat p_{ij}^{(s)}(1-\hat p_{ij}^{(s)})}{n_i-1}f_i,
\qquad \hat p_{ij}^{(s)}=n_{ij}/n_i.
\]

When population sizes \(N_i\) are unavailable, the implementation uses \(f_i=1\), i.e. no finite-population correction. When valid stratum population sizes are supplied, it applies the correction to the within-stratum variance contributions. The implementation uses a delta-method approximation for producer's-accuracy uncertainty and normal-approximation Wald intervals. These are teaching baselines; small samples and estimates near zero or one require more careful interval methods.

## When the evaluated map differs from the sampling strata

A reference sample may be selected using an existing map, then reused to evaluate a different map at the same locations. In that case, distinguish three labels:

- \(h\): the **sampling stratum** used to select observations;
- \(i\): the **evaluated map class** observed at each sampled location;
- \(j\): the **reference class** assigned under the response protocol.

Let \(W_h\) be the eligible population area proportion in sampling stratum \(h\), \(n_h\) its sample size and \(n_{hij}\) the count with evaluated map class \(i\) and reference class \(j\). The design-based area-proportion error matrix is

\[
\hat p_{ij}=\sum_{h=1}^{H} W_h\frac{n_{hij}}{n_h}.
\]

The evaluated map's estimated class-area proportions are the row totals; estimated reference-class area proportions are the column totals. Overall accuracy is the diagonal sum. User's and producer's accuracy are ratios of the corresponding diagonal cell to its estimated row and column marginal, respectively.

For a cell indicator within sampling stratum \(h\), let \(\hat q_{hij}=n_{hij}/n_h\). Under independent SRS without replacement within strata, its variance contribution is

\[
\widehat{\operatorname{Var}}(\hat p_{ij})=
\sum_{h=1}^{H}W_h^2
\frac{\hat q_{hij}(1-\hat q_{hij})}{n_h-1}
\left(1-\frac{n_h}{N_h}\right),
\]

where \(N_h\) is the eligible population size in sampling stratum \(h\). Set the finite-population correction to one when \(N_h\) is unavailable. Variances for overall accuracy and the row/column marginals use the corresponding within-stratum indicator proportions. The ratio accuracy measures require covariance-aware delta-method approximations.

This extension does **not** remove the need for a common, defensible class legend. If evaluated-map classes and reference classes are not harmonised, the diagonal does not represent meaningful agreement. Classes present only in one legend remain disagreements; do not silently collapse them.

The original estimator remains appropriate when the evaluated map classes are exactly the sampling strata. The independent-strata estimator supports reusing a probability sample to evaluate another map, provided the original stratum weights describe the same target population and the response protocol remains valid.

## Design and response protocol

A complete assessment needs three linked protocols:

1. **Sampling design:** define the target population and frame; select a probability sample; record mapped-class area weights, stratum sample sizes, inclusion probabilities and nonresponse.
2. **Response design:** define the sampling unit, reference data, temporal alignment, interpretation rules, class definitions, interpreter procedures and adjudication of ambiguous cases.
3. **Analysis:** use estimators and variance formulas consistent with the actual sampling design and response protocol.

Reference labels are not automatically error-free. Positional mismatch, mixed pixels, temporal mismatch, interpreter disagreement and inadequate reference imagery can affect the response labels and should be documented.

## Worked synthetic example

Suppose two mapped classes occupy 60% and 40% of a hypothetical map. Four units are sampled at random within each mapped-class stratum.

| Mapped class | Reference forest | Reference other | Sample n |
|---|---:|---:|---:|
| Forest | 3 | 1 | 4 |
| Other | 1 | 3 | 4 |

The estimated area-proportion matrix is:

| Mapped class | Reference forest | Reference other |
|---|---:|---:|
| Forest | 0.45 | 0.15 |
| Other | 0.10 | 0.30 |

Overall accuracy is (0.45+0.30=0.75), not the unweighted sample diagonal proportion unless the design weights happen to justify that calculation.

Estimated reference forest area proportion is (0.45+0.10=0.55). For a hypothetical mapped area of 1,000 ha, the estimated reference forest area is 550 ha. These values are synthetic and are included only to demonstrate the estimator.

## Implementation

The [Python implementation](../implementations/python/area-adjusted-accuracy/README.md) includes both the mapped-class-stratified estimator and a general independent-strata estimator. Both report area-proportion matrices, overall accuracy, user's and producer's accuracy, class-area marginals and uncertainty summaries, and optionally apply finite-population corrections. The public [Fiji 2021 land-cover sample](../implementations/python/area-adjusted-accuracy/fiji-case-study.md) demonstrates the first design. The [Fiji–WorldCover comparison](../implementations/python/area-adjusted-accuracy/worldcover-comparison.md) reuses the same 834 reference points to evaluate ESA WorldCover 2021 v200. It reports 74.12% area-adjusted overall accuracy and a paired difference of −8.39 percentage points versus the original Fiji map; these estimates remain conditional on the provisional class crosswalk and eligible sample frame. A [crosswalk sensitivity analysis](../implementations/python/area-adjusted-accuracy/crosswalk-sensitivity.md) shows the paired difference remains negative under two alternative legends.

Neither implementation supports arbitrary unequal-probability, cluster, adaptive or general systematic/spatially balanced designs. It does not propagate uncertainty in map-area weights or reference interpretation, apply nonresponse adjustments, or certify a map.

## References

- Olofsson, P., Foody, G. M., Herold, M., Stehman, S. V., Woodcock, C. E., & Wulder, M. A. (2014). Good practices for estimating area and assessing accuracy of land change. *Remote Sensing of Environment*, 148, 42–57. https://doi.org/10.1016/j.rse.2014.02.015
- Olofsson, P., Foody, G. M., Stehman, S. V., & Woodcock, C. E. (2013). Making better use of accuracy data in land change studies: Estimating accuracy and area and quantifying uncertainty using stratified estimation. *Remote Sensing of Environment*, 129, 122–131. https://doi.org/10.1016/j.rse.2012.10.031

The Fiji case is a secondary analysis of a public reference sample; it is not a new field campaign or independent re-interpretation. The method page is an initial synthesis, not an independent technical review or a universal prescription for all sampling designs.


## Class-specific diagnostics for samples stratified by a different map

When the probability sample was stratified by a source map rather than the evaluated map, class-specific accuracy must be derived from the design-weighted error matrix, not from unweighted row or column counts. For each evaluated map class, user's accuracy is the diagonal cell divided by its estimated mapped area. For each reference class, producer's accuracy is the diagonal cell divided by its estimated reference area. These ratios can be unstable for rare or empty mapped classes; a 100% user's accuracy based on a handful of predictions should be reported with its sample count and not treated as strong evidence.

The [Fiji–WorldCover class-specific error investigation](../implementations/python/area-adjusted-accuracy/class-specific-error-analysis.md) demonstrates this decomposition and distinguishes error patterns from causal explanations.
