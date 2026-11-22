# Spatial point processes and spatial sampling design

**Subject:** `SM-FND-005` — Spatial statistics and stochastic processes  
**Module status:** Initial teaching module; technical review and learner testing pending

## 1. Two different questions about spatial data

Spatial point-process theory and spatial sampling theory are related, but they answer different questions.

- A **point process** models the locations (and possibly times, marks or types) of events or objects in a region. Its questions include: how many events occur, where are they concentrated, and how do events depend on one another?
- A **sampling design** specifies how a finite or continuous target is observed. Its questions include: which locations or units are selected, with what probabilities, and which population quantities can be estimated from the resulting observations?

A point pattern is not automatically a probability sample. A sample of locations is not automatically a realization of a point process. Confusing these objects leads to incorrect uncertainty statements and invalid inference.

## 2. Spatial point processes

Let \(W\subset\mathbb R^2\) be an observation window and let \(X\) be a random, locally finite set of event locations. Local finiteness means that bounded regions contain finitely many events with probability one. The count in a measurable region \(B\subseteq W\) is

\[
N(B)=\#(X\cap B).
\]

A point process is characterized by the joint probability behaviour of counts in collections of regions, not just by one observed map.

### 2.1 First-order structure: intensity

The intensity measure is

\[
\Lambda(B)=\mathbb E[N(B)].
\]

When it has a density with respect to area, the first-order intensity function \(\lambda(s)\) satisfies

\[
\Lambda(B)=\int_B\lambda(s)\,ds.
\]

Intensity is an expected event count per unit area, not a probability that a location contains an event. For a sufficiently small region \(A\) around \(s\), \(\lambda(s)|A|\) approximates its expected count when intensity varies little over \(A\).

A homogeneous process has constant intensity. An inhomogeneous process has intensity that varies with location, potentially because of covariates, exposure, habitat, observation effort or other first-order structure. A spatially varying observed count surface does not by itself reveal which of these mechanisms generated it.

### 2.2 Second-order structure: interaction and clustering

For a process with a second-order product density \(\rho^{(2)}(s,t)\), the pair-correlation function is

\[
g(s,t)=\frac{\rho^{(2)}(s,t)}{\lambda(s)\lambda(t)}
\]

where the denominator is positive. Under suitable stationarity and isotropy assumptions, this can be expressed as a function \(g(r)\) of separation distance \(r=\|s-t\|\).

Informally:

- \(g(r)>1\) indicates more pairs at separation \(r\) than expected under the corresponding independent-location reference;
- \(g(r)<1\) indicates fewer such pairs;
- \(g(r)=1\) is the Poisson second-order reference.

These are statements about pair structure after accounting for first-order intensity. Raw clustering can be caused by inhomogeneous intensity even when events are conditionally independent given that intensity.

For a stationary isotropic process with intensity \(\lambda\), Ripley's K-function is

\[
K(r)=\frac{1}{\lambda}
\mathbb E\!\left[
\text{number of further events within distance }r
\text{ of a typical event}
\right].
\]

When the pair-correlation function exists,

\[
K(r)=2\pi\int_0^r u\,g(u)\,du.
\]

For a homogeneous Poisson process, \(g(r)=1\) and \(K(r)=\pi r^2\). This reference is often called complete spatial randomness (CSR), but it is a particular null model—not a universal definition of randomness. Estimation of K in a finite window requires edge correction and careful treatment of the observation window.

### 2.3 Canonical model families

**Poisson process.** Counts in disjoint sets are independent Poisson random variables. Conditional on a fixed count in a bounded region, locations are independent with density proportional to the intensity. The homogeneous case is a useful baseline; an inhomogeneous Poisson process accommodates a specified spatial intensity surface but has no residual interaction after conditioning on that surface.

**Cox process.** A Cox process is a Poisson process conditional on a random intensity field. Random variation in the intensity induces dependence and can represent aggregation at scales encoded by the field. A log-Gaussian Cox process uses a Gaussian random field for log-intensity. It is not interchangeable with an inhomogeneous Poisson model whose intensity is fixed.

**Cluster process.** Neyman–Scott models, including the Thomas and Matérn cluster processes, generate latent parent locations and offspring around them. They encode a particular mechanism for aggregation. A cluster-process fit does not prove that latent parents physically exist.

**Interaction or Gibbs process.** A Gibbs model assigns probability according to interactions among configurations. Repulsive models such as the Strauss process can represent inhibition, spacing or competition. Their simulation and inference may require MCMC; finite chains require convergence and mixing assessment.

**Space-time and marked processes.** Events may carry time, magnitude, category, sensor type or other marks. A space-time process models temporal triggering and spatial dependence jointly; a marked process models how attributes vary with event location and with one another. Projecting away time or marks can conceal important structure.

### 2.4 Observation is part of the model

The observed point pattern may differ from the underlying event process because of incomplete detection, variable effort, reporting delays, censoring, positional error or a restricted observation window. If detection probability varies spatially, an apparent intensity gradient may reflect the observation system rather than the phenomenon.

Record the observation window, event definition, temporal interval, detection mechanism, effort or exposure, coordinate system, positional uncertainty and any exclusions. A model of event locations does not automatically correct for an imperfect observation process.

## 3. Spatial sampling: design before selection

Let a finite target population contain units \(U=\{1,\ldots,N\}\), with values \(y_i\). A sample \(s\subseteq U\) is selected under a probability design. Define the first-order inclusion probability

\[
\pi_i=P(i\in s)
\]

and the second-order inclusion probability

\[
\pi_{ij}=P(i\in s,\ j\in s).
\]

These probabilities describe the selection mechanism. They are distinct from a model's predicted probability or posterior uncertainty.

If every unit has a known, positive inclusion probability, the Horvitz–Thompson estimator of the finite-population total is

\[
\widehat{T}_{HT}=\sum_{i\in s}\frac{y_i}{\pi_i}.
\]

Under the stated probability design, this estimator is design-unbiased for \(T=\sum_{i\in U}y_i\). Its design variance depends on joint inclusion probabilities:

\[
\operatorname{Var}_p(\widehat T_{HT})
=\sum_{i\in U}\sum_{j\in U}
(\pi_{ij}-\pi_i\pi_j)
\frac{y_i}{\pi_i}\frac{y_j}{\pi_j},
\]

with the appropriate convention for diagonal terms. An estimator of that variance requires the design's joint inclusion structure and conditions on which pairs can be observed. Knowing only the selected coordinates is not enough.

For a mean, one may divide a total estimator by the known population size for a finite-population mean, or use a ratio estimator where the denominator is estimated. Ratio estimators are not generally exactly design-unbiased.

## 4. Common spatial sampling designs

### 4.1 Simple random and stratified sampling

In simple random sampling without replacement, all samples of a fixed size have equal probability. It gives a transparent baseline but may leave large spatial gaps or undersample rare subpopulations by chance.

In stratified sampling, the target is partitioned into non-overlapping strata before selection. Samples are drawn within each stratum. Stratification can guarantee coverage of important classes or regions and improve precision when strata are internally homogeneous for the estimand. Allocation may be proportional, equal or cost/variance informed; the estimator must use the actual inclusion probabilities and weights.

### 4.2 Systematic and spatially balanced sampling

Systematic designs select units using a random start and a fixed interval or spatial pattern. They can distribute observations efficiently, but periodic structure in the target can interact with the sampling interval. A design's randomization and variance properties must be specified rather than inferred from the visual regularity of its points.

Spatially balanced probability designs aim to spread selected units across the domain while retaining known inclusion probabilities. Balance can improve coverage, but a visually even pattern alone does not establish probability-sampling validity. Use a documented design and preserve its selection probabilities and randomization record.

### 4.3 Cluster, multistage and adaptive sampling

Cluster sampling selects groups of units, often to reduce travel or access cost. It can increase variance when units within clusters are similar. Multistage designs select primary units and then secondary units, requiring the inclusion probabilities across stages.

Adaptive cluster sampling begins with an initial probability sample and expands around units satisfying a predeclared condition. It can be efficient for rare, clustered phenomena, but the expansion rule changes the sample structure. Valid estimation requires an estimator and variance procedure that match the actual adaptive design; the mean of all visited units is not generally design-unbiased.

### 4.4 Model-based and sequential designs

Model-based design selects observations to improve prediction, reduce posterior uncertainty or optimise an expensive response. Adaptive sampling and active learning can use uncertainty and spatial diversity to choose the next location. Bayesian optimisation instead targets an objective such as a maximum or minimum.

These are not automatically probability samples. They can be appropriate for prediction, optimisation and discovery, but a query-selected dataset should not be used as if it were a representative probability sample for design-based population accuracy or area estimation. If population inference is also required, reserve an independent probability sample or use a valid inferential framework for the actual selection process.

## 5. Continuous spatial domains and support

For a continuous domain, the sampling unit may be a point, plot, transect, pixel footprint, volume, route segment or time interval. The support of an observation determines what quantity it represents. A point measurement, an areal average and a remotely sensed pixel retrieval are not interchangeable even when they share a variable name and units.

A spatial design must define:

1. the target population or domain and its boundaries;
2. the estimand or decision, including spatial and temporal support;
3. the sampling frame and known coverage gaps;
4. the selection mechanism and inclusion probabilities, where probability inference is intended;
5. the measurement method, effort, detection and quality controls;
6. the coordinate reference, datum, epoch and distance metric;
7. the treatment of nonresponse, inaccessible sites, missingness and positional error;
8. the analysis and variance procedure before observations are collected.

Instrument accuracy, pixel size, point density and sample count are not substitutes for a defensible design.

## 6. Connecting theory to computational methods

The repository contains several distinct, bounded implementations. Their existence does not imply that every model has been fitted, validated for a particular application or proven optimal.

| Theory or design question | Repository route | What it currently demonstrates |
|---|---|---|
| Homogeneous and clustered point patterns | [Poisson and Thomas models](../../algorithms/statistics/poisson-and-thomas-processes.md) and [point-process package](../../implementations/python/point-process/README.md) | Reproducible generative baselines, not parameter estimation |
| Spatially varying first-order intensity | [Inhomogeneous Poisson simulation](../../algorithms/statistics/inhomogeneous-poisson-process.md) | Exact simulation for a supplied piecewise-constant intensity grid |
| Residual second-order structure under varying intensity | [Inhomogeneous K](../../algorithms/statistics/inhomogeneous-ripley-k.md) | Estimator using externally supplied positive intensities; intensity fitting and inferential corrections remain separate |
| Space-time triggering | [ETAS simulation](../../algorithms/statistics/etas-point-process.md) | Bounded marked branching simulator, not operational hazard inference |
| Bounded continuous space-filling designs | [Spatial sampling package](../../implementations/python/spatial-sampling-design/README.md) | Latin hypercube, maximin heuristic, thinning and k-means coverage |
| Adaptive site selection | [Adaptive spatial sampling](../../methods/adaptive-spatial-sampling.md) and [adaptive/Bayesian sampling](../../methods/adaptive-and-bayesian-spatial-sampling.md) | Greedy uncertainty-diversity and other bounded sequential-design methods |
| Observation frame, support and field acquisition | [Spatial observation and sampling design](../../collection/spatial-observation-and-sampling-design.md) | Cross-technology framework for defining the observation process before choosing an instrument |

For an applied route, begin with the estimand and observation design, choose a model that matches the phenomenon and observation mechanism, then use an implementation whose limitations are explicit. Keep simulation, parameter estimation, model checking and decision-making as separate stages.

## 7. Model criticism and design diagnostics

For point processes, inspect first-order intensity before interpreting second-order summaries. Compare observed statistics with simulations under an explicitly stated null or fitted model, using the same window and observation assumptions. Consider edge effects, intensity estimation, covariates, detection, spatial scale and parameter uncertainty. A rejection of CSR does not identify a unique alternative model.

For sampling, inspect frame coverage, inclusion probabilities, spatial balance, nonresponse, measurement error and whether the analysis matches the design. For adaptive or model-based selection, distinguish the optimisation objective from any population estimand. Validate predictive models with spatially appropriate holdouts; nearby training and test observations can make performance appear better than transfer to new regions.

## 8. Further reading

- Baddeley, A., Rubak, E., & Turner, R. (2015). *Spatial Point Patterns: Methodology and Applications with R*. CRC Press.
- Møller, J., & Waagepetersen, R. P. (2004). *Statistical Inference and Simulation for Spatial Point Processes*. Chapman & Hall/CRC.
- Diggle, P. J. (2013). *Statistical Analysis of Spatial and Spatio-Temporal Point Patterns* (3rd ed.). CRC Press.
- Cressie, N. (1993). *Statistics for Spatial Data* (rev. ed.). Wiley.
- Cochran, W. G. (1977). *Sampling Techniques* (3rd ed.). Wiley.
- Thompson, S. K. (2012). *Sampling* (3rd ed.). Wiley.
- Stevens, D. L., Jr., & Olsen, A. R. (2004). Spatially balanced sampling of natural resources. *Journal of the American Statistical Association*, 99(465), 262–278.

## 9. Check your understanding

1. Why is intensity not a probability that a point exists at a location?
2. How can an inhomogeneous Poisson process produce apparent clustering in a raw map without residual pair interaction?
3. What additional structure does a Cox process introduce compared with an inhomogeneous Poisson process?
4. Why does rejecting CSR not establish that a Thomas process generated the observed pattern?
5. What is the difference between a first-order inclusion probability and a model-based prediction probability?
6. Under what conditions is the Horvitz–Thompson total design-unbiased?
7. Why can a spatially balanced-looking sample still fail to support design-based inference?
8. Why should a model-driven active-learning sample not be reported as a probability sample for map accuracy?
9. How can variable detection effort confound interpretation of an observed intensity surface?
10. Which sampling and observation assumptions would need to be recorded before applying a point-process model to field-collected events?
