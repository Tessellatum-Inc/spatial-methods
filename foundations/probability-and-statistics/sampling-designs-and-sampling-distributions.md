# Sampling designs and sampling distributions

**Subject:** SM-FND-004 — Probability and statistical inference  
**Module:** 04  
**Status:** Initial researched teaching resource; independent technical review and learner testing pending.

## 1. From a spatial question to a sample

Spatial inference begins before a point is selected. A defensible design makes explicit:

- **Target population:** the complete set of units about which a conclusion is intended.
- **Sampling frame:** the operational list, map, network or spatial domain from which units can actually be selected.
- **Sampling unit:** the entity selected, such as a parcel, pixel, road segment, waterbody, plot, household or site.
- **Observation unit:** the entity on which a measurement is made; it may differ from the sampling unit.
- **Variable:** the characteristic measured or classified.
- **Estimand:** the population quantity to estimate, such as a mean, total, proportion, rate or spatial distribution.
- **Estimator:** the rule used to calculate an estimate from the realised sample.

A map of accessible sites is not automatically a complete sampling frame. If remote, unsafe, privately held or poorly mapped locations are missing, the frame may systematically exclude parts of the target population. A probability sample from an incomplete frame does not automatically represent the omitted units.

A useful design statement identifies the target population, spatial and temporal extent, unit, frame, variable, estimand, selection procedure, expected nonresponse and analysis method.

## 2. Probability sampling and inclusion probabilities

A probability sample is selected using a defined random mechanism. Each eligible unit has a known, non-zero probability of selection under the design.

For unit \(i\), the first-order inclusion probability is

\[
\pi_i=P(i\text{ is included in the sample}).
\]

For two distinct units \(i,j\), the joint inclusion probability is

\[
\pi_{ij}=P(i\text{ and }j\text{ are both included}).
\]

Inclusion probabilities are properties of the design, not observed values. They are central to design-based inference, where finite population values are treated as fixed and randomness comes from sample selection.

For a fixed-size simple random sample without replacement of \(n\) units from \(N\),

\[
\pi_i=\frac{n}{N},\qquad
\pi_{ij}=\frac{n(n-1)}{N(N-1)}.
\]

The base design weight is

\[
w_i=\frac{1}{\pi_i}.
\]

For equal-probability simple random sampling this is \(N/n\). Unequal-probability designs require unit-specific weights and an estimator appropriate to the design. A weight is not a measure of a unit's importance or data quality.

Convenience, volunteer and purposive samples do not acquire known inclusion probabilities merely because they are numerous or geographically dispersed. They can be useful for exploration, rapid response, case studies and model development, but conventional design-based population estimates require additional assumptions or a different inferential framework.

## 3. Core sampling designs

### 3.1 Simple random sampling

Every possible sample of a specified size has the same selection probability. Under equal-probability sampling, each unit has the same first-order inclusion probability.

Useful when the frame is credible and there is little reliable prior information for improving the design. It is conceptually straightforward and provides a baseline for comparison. Limitations in spatial work include uneven geographic spread, travel inefficiency and the possibility that rare or geographically concentrated subgroups receive few observations.

### 3.2 Stratified random sampling

Partition the population into non-overlapping strata before selection. Draw a probability sample independently within each stratum.

Strata may represent ecological zones, land-cover classes, administrative areas, elevation bands, urban/rural contexts or other known subpopulations. Categories must be defined consistently and every target unit assigned appropriately.

For stratum \(h\), let \(N_h\) be its population size, \(n_h\) its sample size, and \(W_h=N_h/N\). The stratified mean estimator is

\[
\bar{y}_{st}=\sum_{h=1}^{H}W_h\bar{y}_h.
\]

Under independent simple random sampling without replacement within strata, its estimated variance is

\[
\widehat{\operatorname{Var}}(\bar{y}_{st})
=\sum_{h=1}^{H}W_h^2
\left(1-\frac{n_h}{N_h}\right)\frac{s_h^2}{n_h}.
\]

Stratification can improve precision when units within strata are relatively homogeneous for the target variable, and it ensures coverage of specified subgroups. It can also support separate estimates for each stratum.

Proportional allocation makes \(n_h\) proportional to \(N_h\). Equal allocation gives the same sample size to each stratum. Neyman allocation, under equal per-unit costs and a fixed total sample size, allocates approximately in proportion to \(N_hS_h\), where \(S_h\) is the within-stratum standard deviation. Costs, minimum reporting requirements and unequal variances may justify other allocations.

Disproportionate allocation must be reflected in weights when producing population-wide estimates. An unweighted average of stratum means is not generally the population mean.

### 3.3 Systematic and grid sampling

Choose a random start and then select units according to a regular interval or spatial pattern. Examples include every kth record in an ordered frame, a regularly spaced grid, or transects at fixed intervals.

Systematic designs can give useful spatial coverage and operational simplicity. However, a periodic pattern in the phenomenon that aligns with the sampling interval can produce misleading results. Variance estimation for a single systematic sample can also require additional assumptions or a design with replication.

A grid is a layout, not a complete sampling design by itself. State how the origin, orientation, spacing, boundary treatment and randomisation were chosen.

### 3.4 Cluster and multistage sampling

In cluster sampling, groups of units are sampled first. All units or a subsample within selected clusters are then observed. Examples include selecting villages and then households, catchments and then sites, or image tiles and then pixels.

Cluster sampling can reduce travel and listing costs. But observations within a cluster may be similar, reducing the effective information gained from each additional observation. Treating all within-cluster measurements as independent usually understates uncertainty.

Multistage sampling selects units at multiple levels, such as counties, then communities, then households. Each stage has its own selection probabilities; the final unit's inclusion probability is the product of the relevant conditional stage probabilities when the design is structured accordingly.

### 3.5 Adaptive cluster sampling

Begin with a probability sample. If a sampled unit meets a pre-specified condition, expand observation to neighbouring units according to a defined rule. This can be useful when a rare characteristic is clustered, such as a sparse invasive species, localised contamination or a rare habitat.

The adaptive rule changes the selection mechanism. Valid estimation requires an estimator that accounts for the adaptive design; simply treating all observed units as an ordinary random sample is generally invalid.

### 3.6 Spatially balanced probability sampling

Spatially balanced designs aim to distribute a probability sample across a spatial sampling frame while retaining a known random selection mechanism and inclusion probabilities. Generalized Random Tessellation Stratified (GRTS) sampling is one established approach.

GRTS is designed for point, linear and areal resources and can accommodate stratification, unequal inclusion probabilities, legacy sites and replacement sites. The EPA spsurvey package implements GRTS and related design and analysis methods.

Spatial balance is not synonymous with equal spacing. Nor does a visually regular sample automatically have design-based inclusion probabilities. Distinguish balance with respect to the sampling frame from a layout that merely looks geographically even.

A spatially balanced sample can be efficient for natural-resource monitoring, but the design still depends on a defensible frame, estimand, selection probabilities and analysis. It does not eliminate nonresponse, measurement error, confounding or temporal mismatch.

## 4. Sampling distributions

A statistic calculated from a sample changes from one possible sample to another. Its **sampling distribution** is the probability distribution of that statistic under repeated application of the sampling design. This differs from the distribution of individual population values and from the distribution of observed measurements.

For simple random sampling, the sample mean is

\[
\bar{Y}=\frac{1}{n}\sum_{i\in s}Y_i.
\]

Under simple random sampling without replacement from a finite population of size \(N\), with population mean \(\bar{Y}_N\) and finite-population variance

\[
S^2=\frac{1}{N-1}\sum_{i=1}^{N}(Y_i-\bar{Y}_N)^2,
\]

the design expectation and variance of the sample mean are

\[
E_d(\bar{Y})=\bar{Y}_N,
\qquad
\operatorname{Var}_d(\bar{Y})=
\left(1-\frac{n}{N}\right)\frac{S^2}{n}.
\]

The subscript \(d\) emphasises that expectation and variance are over the sampling design. The factor \(1-n/N\) is the finite population correction in the variance expression. It matters when a substantial fraction of a finite population is sampled. For a negligible sampling fraction, it is close to one.

An estimated standard error is the square root of an estimated sampling variance. It describes the variability of an estimator under the assumed design and analysis. It is not the standard deviation of individual observations, nor does it include every possible source of uncertainty.

### Central limit theorem: useful, not automatic

Under suitable conditions, appropriately standardised sample means approach a normal distribution as sample size increases. This helps motivate confidence intervals and tests.

But “large n” is not a universal guarantee. The approximation depends on the population distribution, sample design, dependence, weights, influential observations and estimand. Strong clustering, heavy tails, rare events, highly unequal weights or spatial dependence may require different approximations or specialised variance estimators.

## 5. Standard errors under common designs

For simple random sampling without replacement, an estimated standard error of the sample mean is

\[
\widehat{SE}(\bar{y})=
\sqrt{\left(1-\frac{n}{N}\right)\frac{s^2}{n}}.
\]

For stratified sampling, use the stratified variance estimator in Section 3.2. For unequal-probability or spatially balanced designs, use variance estimation methods compatible with the actual design and its inclusion probabilities.

Do not apply the simple random sample formula merely because a dataset contains n rows. A convenience sample, clustered sample, weighted sample or systematic design may have a different sampling distribution.

### Design effect

The design effect compares variance under a complex design with variance under a specified reference design, commonly simple random sampling of the same nominal size:

\[
DEFF=\frac{\operatorname{Var}_{design}(\hat{\theta})}
{\operatorname{Var}_{reference}(\hat{\theta})}.
\]

A design effect greater than one means the estimator is less precise than the reference under that comparison; below one means more precise. It depends on the estimand, outcome, design, weights and reference assumptions. There is no single universal design effect for a survey.

## 6. Sample size and precision

Sample size should follow from the estimand, desired precision, confidence or coverage convention, variability, design, nonresponse and available resources—not from a universal rule such as “30 samples is enough.”

For a simple random sample from a large population, a rough planning expression for estimating a mean with target margin \(d\) is

\[
n\approx\left(\frac{z_{1-\alpha/2}\sigma}{d}\right)^2,
\]

where \(\sigma\) is a planning value for the population standard deviation and \(z_{1-\alpha/2}\) is a normal quantile for the chosen two-sided confidence level.

For a finite population, a common adjustment is

\[
n_{finite}=\frac{n_0}{1+(n_0-1)/N},
\]

where \(n_0\) is the large-population result. Complex designs may require inflation for design effect, nonresponse and subgroup reporting. Estimating a proportion requires a planning value for the proportion; when unknown, a conservative value may be used, with assumptions stated.

A sample-size calculation cannot repair a biased frame, invalid measurement protocol, nonresponse bias or a poorly defined target population.

## 7. Worked example: stratified estimate of mean travel time

Suppose a hypothetical city study defines two strata: central districts and outer districts. The target is mean travel time for all eligible trips in a specified reference week. Assume the frame contains 600 central-district trips and 400 outer-district trips.

A stratified probability sample selects 30 central trips and 20 outer trips. Observed sample means and standard deviations are:

| Stratum | \(N_h\) | \(n_h\) | \(\bar y_h\) | \(s_h\) |
|---|---:|---:|---:|---:|
| Central | 600 | 30 | 12 min | 4 min |
| Outer | 400 | 20 | 18 min | 5 min |

The population weights are \(W_1=0.6\) and \(W_2=0.4\). The estimated overall mean is

\[
\bar y_{st}=0.6(12)+0.4(18)=14.4\text{ minutes}.
\]

The estimated variance is

\[
\begin{aligned}
\widehat{\operatorname{Var}}(\bar y_{st})
&=0.6^2(1-30/600)\frac{4^2}{30}\\
&\quad+0.4^2(1-20/400)\frac{5^2}{20}\\
&=0.3724\text{ min}^2.
\end{aligned}
\]

Therefore,

\[
\widehat{SE}(\bar y_{st})=\sqrt{0.3724}\approx0.610\text{ minutes}.
\]

This estimate uses known population stratum sizes and the stated within-stratum simple random sampling assumptions. It is not a result from actual travel records. A confidence interval would additionally require a suitable reference distribution and degrees-of-freedom or variance-estimation procedure consistent with the design.

## 8. Spatial sampling problems that need explicit treatment

### Incomplete frames and coverage error

A frame may omit informal settlements, unregistered businesses, unmapped roads, seasonal water bodies, small parcels or recently changed land cover. Record exclusions and their likely consequences. A probability sample from an incomplete frame does not automatically represent omitted parts of the target population.

### Nonresponse and inaccessible locations

A selected location that cannot be reached is not permission to choose the nearest convenient substitute. Record the outcome and reason. Pre-specify replacement rules and use design-compatible adjustment where justified. Replacements can change inclusion probabilities and should be documented.

### Spatial and temporal support

A point, pixel, plot, road segment and administrative area represent different supports. Their measurements are not interchangeable. Define spatial resolution, footprint, time window, aggregation and boundary treatment before selecting a sample.

### Positional and measurement error

Sampling uncertainty is only one part of total uncertainty. Geolocation error, sensor error, observer effects, classification error and temporal mismatch may remain even with a well-designed probability sample.

### Field feasibility

Safety, access, permissions, cost, weather and logistics are real design constraints. Incorporate them before selection where possible. If field implementation departs from the original design, preserve planned and realised sample records and explain the effect on inference.

## 9. Exercises

**A — Define the population.** A team wants to estimate the proportion of buildings in a city that have rooftop solar. State a target population, frame, sampling unit, observation unit, variable and estimand. Identify two likely coverage problems.

*Worked guidance:* define the date and city boundary; a building footprint register may be a frame but can omit informal or recently constructed buildings. The sampling unit may be a building; the observation may be an inspected roof or image interpretation. The estimand is the proportion of eligible buildings with solar under a clear operational definition.

**B — Inclusion probability and weight.** A simple random sample without replacement selects 80 units from a frame of 2,000. Find each unit's inclusion probability and base weight.

*Worked guidance:* \(\pi_i=80/2000=0.04\); \(w_i=1/0.04=25\).

**C — Stratified allocation.** A population contains 70% urban and 30% rural units. Explain why an equal sample of 50 from each stratum should not be averaged without weights to estimate the population mean.

*Worked guidance:* equal allocation oversamples the smaller rural stratum. Use population weights 0.7 and 0.3 for the overall mean, while retaining stratum-specific estimates if useful.

**D — Sampling distribution.** A finite population has \(N=500\), and a simple random sample without replacement has \(n=100\). What is the finite population correction factor in the variance expression?

*Worked guidance:* \(1-n/N=1-100/500=0.8\). The standard-error multiplier is \(\sqrt{0.8}\).

**E — Design choice.** A rare invasive plant occurs in spatial clusters. Compare a simple random sample, stratified sample and adaptive cluster sample. What extra design information is needed before making valid population estimates?

*Worked guidance:* discuss prior maps or strata, initial random selection, the adaptive expansion rule, inclusion probabilities, field detection and an estimator compatible with the design.

**F — Critique a claim.** A report says “we collected 100 points across the region, so the sample is representative.” List at least five missing pieces of evidence.

*Worked guidance:* target population and frame, random selection procedure, inclusion probabilities, spatial/temporal coverage, nonresponse and replacement records, measurement protocol, subgroup coverage, weights and analysis method.

## 10. Connections and next steps

- Previous: [Joint distributions, covariance and dependence](joint-distributions-covariance-and-dependence.md).
- [Measurement principles and field verification](../measurement-science/measurement-principles-and-field-verification.md): measurement error is distinct from sampling error.
- Spatial data collection: design a frame and field protocol that match the target population and observation support.
- Spatial statistics: spatial dependence affects precision and variance estimation; spatial balance does not mean observations are independent.
- Next: likelihood and statistical estimation, connecting sampling models to parameter estimation and fitted spatial models.

## References

- U.S. Environmental Protection Agency. [Selecting a Sampling Design](https://www.epa.gov/quality/selecting-sampling-design). Used for a practical comparison of simple random, stratified, systematic/grid, ranked-set and adaptive cluster designs. This guidance is not a substitute for a study-specific statistical design.
- Dumelle, M., Kincaid, T., Olsen, A. R., and Weber, M. (2023). “spsurvey: Spatial Sampling Design and Analysis in R.” *Journal of Statistical Software*, 105(3), 1–29. [https://doi.org/10.18637/jss.v105.i03](https://doi.org/10.18637/jss.v105.i03). Used for design-based spatial probability sampling, GRTS and inclusion-probability concepts.
- [EPA spsurvey spatially balanced sampling vignette](https://usepa.github.io/spsurvey/articles/sampling.html). Used for GRTS design features, stratification and spatial sampling-frame concepts.

The examples and calculations in this module are original synthetic teaching illustrations. No real survey has been designed, selected or validated here.

## Evidence and review boundary

The EPA sampling-design guidance was inspected for its descriptions and use cases for common designs. The 2023 spsurvey paper and official vignette were inspected for GRTS, design-based inference and spatial balance relative to the sampling frame. This is an introductory synthesis, not a complete survey-design manual. Variance estimators for unequal-probability, clustered, adaptive and spatially balanced samples require design-specific treatment beyond the simple formulas shown here. A real project should be designed and reviewed by a competent statistician and domain specialist.
