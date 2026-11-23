# Exercise G — Reliability, detectability and network design

**Status:** Reproducible synthetic network-design study  
**Dataset:** Reuses [Exercise C synthetic vertical-control network](../../data/measurement/exercise-c-synthetic-control-network.csv)  
**Implementation:** [analyze_exercise_g.py](../../scripts/measurement/analyze_exercise_g.py)  
**Scope:** Redundancy numbers, internal reliability, minimal detectable bias (MDB), external reliability and comparison of design interventions.

> **All observations and proposed additions are synthetic.** The B–E observation is a hypothetical design addition, not a field measurement. The exact A datum and independent-observation model are simplifying assumptions. This is not a survey specification or a guarantee of field performance.

## 1. From diagnosing errors to designing for them

Exercise F asked whether an existing network was statistically consistent and which observations deserved investigation. Exercise G asks whether the network was designed to expose errors in the first place.

A network can produce precise coordinates yet have weak ability to detect a gross error in a particular observation. Conversely, high redundancy does not automatically guarantee the best coordinate precision. Network design must consider at least:

- **Precision:** uncertainty of estimated heights or height differences.
- **Internal reliability:** ability to detect gross errors in observations.
- **External reliability:** effect on estimated parameters of gross errors that remain undetected at the selected detection threshold.
- **Cost and feasibility:** field time, access, equipment, crew, monumentation, safety and operational constraints.

Reliability depends on the design matrix and observation covariance, not on the numerical observed height differences. This is why it can be evaluated before the field campaign.

## 2. Network and design assumptions

The baseline is the nine-observation, four-unknown network from Exercise C:

- Fixed point A, treated as exact.
- Unknown heights B, C, D and E.
- Nine directed height-difference observations: AB, BC, CA, BD, DA, CD, DE, EA and CE.
- Five degrees of freedom.
- The supplied a-priori standard uncertainties are retained.
- Observations are assumed independent, so the observation covariance is diagonal.

The baseline network is not claimed to be optimally designed. It is a compact teaching network with enough redundancy to demonstrate reliability measures.

## 3. Redundancy numbers

For the linear model with design matrix (A), weight matrix (P), and parameter cofactor matrix:

[
Q_{xx}=(A^T P A)^{-1}
]

the residual-forming matrix is:

[
R=I-A(A^T P A)^{-1}A^T P
]

The diagonal element (r_i=R_{ii}) is the redundancy number of observation (i), under the stated model.

- A value near zero means little of that observation's error is exposed in the residuals; it is weakly controlled by the rest of the network.
- A larger value means a greater share of its error is reflected in residual space.
- The sum of redundancy numbers equals the network redundancy, (n-u=5), for this full-rank model.

Redundancy numbers are not probabilities that an observation is wrong. They are design diagnostics. They also depend on the covariance model; with correlated observations, the full covariance formulation must be used rather than treating each row as independent.

## 4. Minimal detectable bias (MDB)

For a single-observation alternative, a conventional normal-theory approximation is:

[
MDB_i=delta_0rac{sigma_i}{sqrt{r_i}}
]

where (sigma_i) is the a-priori standard uncertainty and (delta_0) is the selected noncentrality parameter.

This exercise uses (delta_0=4.13), approximately corresponding to a two-sided single-test false-alarm probability (alpha=0.001) and power (1-eta=0.80) under a standard normal approximation. It is a **per-observation design criterion**, not a simultaneous family-wise 0.1% guarantee across all nine observations. If the project requires simultaneous testing, the multiple-testing strategy and corresponding critical values must be designed explicitly.

A smaller MDB means smaller gross errors are detectable under the stated test design. Lower observation uncertainty and higher redundancy both reduce MDB.

## 5. External reliability

An undetected gross error can still bias the estimated heights. For an MDB-sized bias in observation (i), the parameter displacement is:

[
Delta hat{x}_i = Q_{xx}a_i^T p_i,MDB_i
]

for the independent-observation model, where (a_i) is the observation's design row and (p_i=1/sigma_i^2).

This exercise reports the largest absolute coordinate component of that displacement for each observation. It is a simple external-effect indicator; project-specific effects should instead be evaluated on the height differences, elevations, derived quantities or decisions that matter to the application.

Internal and external reliability answer different questions:
- Can the error be detected?
- If it is not detected, how much can it distort the result?

A good design needs both.

## 6. Three design scenarios

The script compares:

A. **Existing network:** the nine original synthetic observations.

B. **Add a B–E link:** one additional independent B-to-E height difference, with an assumed standard uncertainty of 1.6 mm. Its synthetic observed value is included only to make the record complete; design metrics do not depend on the observed value.

C. **Improve precision:** reduce every original observation's standard uncertainty by 20%, leaving network geometry unchanged.

### Reproduced design metrics

| Metric | Existing | Add B–E | Improve precision 20% |
|---|---:|---:|---:|
| Observations | 9 | 10 | 9 |
| Minimum redundancy number | 0.437 | 0.508 | 0.437 |
| Maximum MDB | 10.132 mm | 9.606 mm | 8.106 mm |
| Mean MDB | 9.099 mm | 8.720 mm | 7.279 mm |
| Maximum absolute coordinate effect at MDB | 4.341 mm | 3.745 mm | 3.472 mm |
| Trace of parameter covariance | 4.667 mm² | 4.277 mm² | 2.987 mm² |

These are results under the chosen synthetic model and design criterion. They are not field performance claims.

### Interpretation

**Adding a B–E observation** improves the weakest redundancy number from 0.437 to 0.508, lowers the maximum MDB, and reduces the maximum coordinate effect at the MDB threshold. It also improves formal parameter precision. It adds an observation and therefore field cost, but it creates a new independent geometric relationship rather than simply repeating the same route.

**Improving all observation precisions by 20%** leaves redundancy numbers unchanged because the relative network geometry is unchanged and every weight is scaled equally. It reduces MDB and parameter covariance. Better instruments or procedures can improve precision, but they do not repair weak network geometry or create new independent checks.

Neither intervention is universally best. Their relative value depends on the project's tolerance, field access, costs, error sources and required reliability.

## 7. Design lessons

1. **Redundancy must be useful, not merely numerous.** Repeating an observation with the same setup, instrument, operator, systematic error or environmental exposure may add less independent control than its count suggests.
2. **Geometry matters.** New links should create alternative routes and constrain weak parts of the network.
3. **Precision and reliability are distinct.** Reducing all standard uncertainties improves MDB and coordinate precision but leaves redundancy numbers unchanged.
4. **External effects matter.** A design should limit the consequences of errors that escape detection, not only maximise the chance of flagging them.
5. **Control points need their own quality assessment.** Treating a benchmark as exact can make the network appear stronger than it is. Exercise D and E explored uncertain and minimally constrained control; a real design must carry datum uncertainty appropriately.
6. **Correlation can reduce effective redundancy.** Two measurements sharing a common error source are not necessarily two independent checks.
7. **Field feasibility is part of optimal design.** An ideal mathematical network that cannot be occupied safely or economically is not an optimal field design.

## 8. Reproduction

From the repository root:

```bash
python scripts/measurement/analyze_exercise_g.py
```

The implementation uses only the Python standard library. It reads the Exercise C CSV, builds the design matrix, computes the parameter cofactor matrix, redundancy numbers, MDBs and external parameter effects, then compares the two hypothetical design interventions.

## 9. Limitations and next work

This is a small vertical network with one exact datum and independent observations. It does not optimise monument locations, route lengths, session schedules, crew time or a full cost function. It does not model correlated observations, uncertain control, multiple simultaneous gross errors, nonlinear observations or the full family-wise multiple-testing problem.

A more advanced design study should:
- evaluate all candidate links and repeated sessions;
- introduce realistic correlation groups for common setups and instruments;
- compute reliability for project-critical height differences, not just individual heights;
- compare single and multiple gross-error detection power;
- include control uncertainty and alternative datum realisations;
- optimise cost subject to precision, MDB and external-effect constraints;
- validate the design using simulation and, ultimately, independently collected field observations.

## 10. References

1. Baarda, W. (1968), *A Testing Procedure for Use in Geodetic Networks*, Netherlands Geodetic Commission, Publications on Geodesy, New Series, Vol. 2, No. 5. Foundational work on testing and internal/external reliability. [Reference chapter](https://www.ncgeo.nl/wp-content/uploads/2024/06/09Baarda.pdf).
2. TU Delft OPEN Publishing (2024), *Network Quality Control*, an open textbook covering network design, precision, reliability, MDB, adjustment and testing. [Publisher record](https://research.tudelft.nl/en/publications/network-quality-control-2nd-edition/), [DOI](https://doi.org/10.59490/tb.100).
3. Nowak, E. and Odziemczyk, W. (2018), “Impact analysis of observation coupling on reliability indices in a geodetic network,” *Reports on Geodesy and Geoinformatics*, 106, 1–7. [Open article](https://doi.org/10.2478/rgg-2018-0008).
4. Bonimani, M. L. and Lehmann, R. (2019), “A half-century of Baarda’s concept of reliability: a review, new perspectives, and applications,” *Survey Review*, 51(367), 261–277. [DOI](https://doi.org/10.1080/00396265.2018.1548118).
5. Amiri-Simkooei, A. R. et al. (2012), “Basic Concepts of Optimization and Design of Geodetic Networks,” *Journal of Surveying Engineering*. [DOI](https://doi.org/10.1061/(ASCE)SU.1943-5428.0000081).

The implementation is an original teaching model informed by these references. It is not a complete production network-optimisation package or a substitute for project-specific survey design.
