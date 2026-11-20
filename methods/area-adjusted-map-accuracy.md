# Design-based, area-adjusted map accuracy and class-area estimation

**Kind:** Method  
**Status:** Researched synthesis; supported implementation is a bounded stratified estimator.  
**Scope:** Probability samples stratified by mapped class, with simple random sampling within each stratum.

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

For independent simple random samples without replacement within mapped-class strata, let (N_i) be the number of eligible population units in stratum (i). When these population sizes are known, the finite-population correction is (f_i=1-n_i/N_i). An estimator of overall-accuracy variance is

[
widehat{operatorname{Var}}(widehat{OA})=
sum_i W_i^2rac{hat U_i(1-hat U_i)}{n_i-1},
qquad hat U_i=n_{ii}/n_i.
]

For a reference-class area proportion, the estimated variance is the sum of the independent stratum contributions,

[
widehat{operatorname{Var}}(hat P_j)=
sum_i W_i^2rac{hat p_{ij}^{(s)}(1-hat p_{ij}^{(s)})}{n_i-1},
qquad hat p_{ij}^{(s)}=n_{ij}/n_i.
]

When population sizes (N_i) are unavailable, the implementation uses (f_i=1), i.e. no finite-population correction. When valid stratum population sizes are supplied, it applies the correction to the within-stratum variance contributions. The implementation uses a delta-method approximation for producer's-accuracy uncertainty and normal-approximation Wald intervals. These are teaching baselines; small samples and estimates near zero or one require more careful interval methods.

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

The [Python implementation](../implementations/python/area-adjusted-accuracy/README.md) supports this mapped-class-stratified SRS design and reports the area-proportion matrix, overall accuracy, user's and producer's accuracy, reference-class area and uncertainty summaries. It optionally applies the finite-population correction when the eligible stratum population sizes are supplied. A real-data example using the public [Fiji 2021 land-cover test sample](../implementations/python/area-adjusted-accuracy/fiji-case-study.md) demonstrates the workflow and explicitly records a sample-allocation discrepancy in the source documentation.

It does not support arbitrary unequal-probability, cluster, adaptive or general systematic/spatially balanced designs. It does not propagate uncertainty in map-area weights or reference interpretation, apply nonresponse adjustments, or certify a map.

## References

- Olofsson, P., Foody, G. M., Herold, M., Stehman, S. V., Woodcock, C. E., & Wulder, M. A. (2014). Good practices for estimating area and assessing accuracy of land change. *Remote Sensing of Environment*, 148, 42–57. https://doi.org/10.1016/j.rse.2014.02.015
- Olofsson, P., Foody, G. M., Stehman, S. V., & Woodcock, C. E. (2013). Making better use of accuracy data in land change studies: Estimating accuracy and area and quantifying uncertainty using stratified estimation. *Remote Sensing of Environment*, 129, 122–131. https://doi.org/10.1016/j.rse.2012.10.031

The Fiji case is a secondary analysis of a public reference sample; it is not a new field campaign or independent re-interpretation. The method page is an initial synthesis, not an independent technical review or a universal prescription for all sampling designs.
