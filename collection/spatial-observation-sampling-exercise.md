# Practical exercise: design a spatial sampling campaign

> **Level:** Intermediate undergraduate to postgraduate  
> **Estimated time:** 2–3 hours  
> **Companion:** [Spatial observation and sampling design](spatial-observation-and-sampling-design.md)  
> **Evidence status:** Entirely hypothetical; all values are synthetic and do not describe a real place or field campaign.

## Scenario

A regional environmental team needs to estimate the total seasonal load of a measured substance across a 10,000-unit study frame. The units are small, non-overlapping sampling areas. A complete candidate frame is available, and a preliminary map divides it into three broad environmental strata.

The team has a budget for 200 field samples. Each sample has approximately equal collection and laboratory cost. A small pilot study provides approximate within-stratum standard deviations. The team wants a probability sample, not a set of convenient sites near accessible roads.

### Synthetic frame and pilot information

| Stratum | Frame units (N_h) | Pilot standard deviation (S_h) |
|---|---:|---:|
| Urban | 4,000 | 12 |
| Peri-urban | 3,500 | 20 |
| Rural | 2,500 | 8 |
| **Total** | **10,000** | — |

Assume the measured variable is expressed in a consistent unit per sampling unit. The standard deviations are planning inputs only; they are not field results.

## Part A — Define the design before the sample

1. State the target population, observation unit, measurand, spatial support and time window.
2. Explain what the sampling frame must contain for these strata to define the target population.
3. Identify two ways the frame could exclude part of the target population.
4. Explain why selecting 200 sites near roads would not preserve the intended probability design.
5. Define a field protocol for recording inaccessible, unsafe, missing or rejected sites without silently replacing them with convenient alternatives.

## Part B — Allocate the sample

For equal per-unit costs, Neyman allocation assigns sample effort in proportion to stratum population size and within-stratum standard deviation:

\[
n_h=n\frac{N_hS_h}{\sum_{k=1}^{H}N_kS_k}
\]

where (n=200), (N_h) is the number of frame units in stratum (h), and (S_h) is the pilot standard deviation.

Calculate (n_h) for each stratum and round to integer sample counts while preserving the total of 200.

### Worked allocation

The allocation weights are:

- Urban: (4{,}000\times12=48{,}000)
- Peri-urban: (3{,}500\times20=70{,}000)
- Rural: (2{,}500\times8=20{,}000)

Their sum is (138{,}000). The unrounded allocations are approximately 69.57, 101.45 and 28.99. One valid integer allocation is:

| Stratum | Allocated sample (n_h) | Sampling fraction (n_h/N_h) | Base design weight (N_h/n_h) |
|---|---:|---:|---:|
| Urban | 70 | 0.0175 | 57.14 |
| Peri-urban | 101 | 0.0289 | 34.65 |
| Rural | 29 | 0.0116 | 86.21 |
| **Total** | **200** | — | — |

The design oversamples the more variable peri-urban stratum relative to proportional allocation. This can improve precision for a total when the pilot variability is informative and per-unit costs are similar. The unequal sampling fractions mean the raw sample should not be treated as self-weighting.

For comparison, proportional allocation would assign 80, 70 and 50 observations. Discuss the trade-off between proportional representation and variance-efficient allocation.

## Part C — Estimate a population total

Suppose a synthetic completed sample produces these stratum means:

| Stratum | Synthetic sample mean (ar y_h) |
|---|---:|
| Urban | 36 |
| Peri-urban | 57 |
| Rural | 23 |

For stratified random sampling, estimate the population total using:

\[
\widehat{T}_{st}=\sum_{h=1}^{H}N_h\bar y_h
\]

Substituting the synthetic means:

\[
\widehat{T}_{st}
=4{,}000(36)+3{,}500(57)+2{,}500(23)
=401{,}000
\]

The estimated population mean is:

\[
\widehat{\bar Y}_{st}=\frac{\widehat{T}_{st}}{N}
=\frac{401{,}000}{10{,}000}=40.1
\]

1. Explain why the unweighted average of the three stratum means is not the correct overall population mean for this frame.
2. Explain how the unequal sample allocations affect the design weights.
3. State what additional information is required to estimate sampling variance from the completed sample.
4. Explain why a correct sampling estimator cannot correct a biased measurement instrument or a systematically incomplete frame.

## Part D — Make the design spatial and operational

Prepare a one-page field plan covering:

- how the frame and stratum boundaries will be versioned;
- how random selections will be generated reproducibly within each stratum;
- how coordinates and site access instructions will be prepared;
- what happens when a selected site is inaccessible;
- sample containers, labels, time records and chain of custody where relevant;
- instrument calibration, field blanks, duplicates or other method-specific quality controls;
- how raw observations and laboratory results will be linked;
- how independent checks and missingness will be reported.

Do not use the sampling weights as a substitute for a spatial access plan. The selected sites must be visited or their non-observation documented under a predefined protocol.

## Part E — Challenge the assumptions

For each change below, explain whether the design or estimator needs to change.

1. Peri-urban sites cost twice as much to reach as urban sites.
2. Several selected sites are clustered within the same neighbourhood.
3. The frame excludes remote rural areas with poor road access.
4. The team adds a fourth stratum after seeing preliminary sample results.
5. The substance varies sharply near rivers and industrial outfalls.
6. Some laboratory measurements are below the detection limit.
7. The final map is intended to predict values at unsampled locations, not only estimate a regional total.

## Submission checklist

- [ ] Target population, measurand, support and frame defined
- [ ] Sampling design and selection procedure stated
- [ ] Neyman allocation calculated with integer counts summing to 200
- [ ] Design weights and stratified estimator interpreted correctly
- [ ] Field access, nonresponse and quality-control rules specified
- [ ] Spatial dependence and frame limitations discussed
- [ ] Uncertainty and validation requirements stated
- [ ] Synthetic values clearly distinguished from real observations

## Instructor notes

Reward explicit assumptions, correct weighting and critical treatment of coverage and measurement bias. The worked values are synthetic and serve only to demonstrate stratified allocation and estimation. Neyman allocation is appropriate here only under the stated equal-cost, fixed-budget assumptions and a usable pilot estimate of within-stratum variability. For unequal costs, multistage selection, adaptive sampling, spatially constrained designs or model-based prediction, the allocation and inference need to be derived for the actual design.

This exercise is not a field sampling specification, environmental compliance protocol or laboratory method. A real campaign requires domain-specific measurands, safety and access review, applicable standards, validated instruments and laboratory procedures, and an independently reviewed quality plan.
