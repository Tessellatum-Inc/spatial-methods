# Positional verification plan — survey-to-spatial-dataset capstone

**Status:** Method design only. No reference observations, field measurements or accuracy results exist.  
**Parent workflow:** [Survey-to-spatial-dataset](README.md)  
**Proposed application:** [Urban public-transport stop and roadside-asset inventory](pilot-project-definition.md)  
**Related foundation:** [Measurement principles and field verification](../../foundations/measurement-science/measurement-principles-and-field-verification.md)

## 1. Purpose and boundary

This plan defines how positional quality could be independently evaluated once the pilot's site, intended use, acquisition method, reference system and acceptance requirements are known.

It is not an accuracy specification, a field authorisation, a survey procedure for a particular instrument, or evidence that the proposed inventory meets any tolerance. The synthetic PostGIS rehearsal validates software behaviour only. It supplies no positional evidence.

The governing principle is:

**Define the requirement first; design independent checks second; acquire and process third; evaluate against the predeclared rule last.**

Do not select a convenient tolerance after looking at the results.

## 2. Define what position means for each feature

Before choosing equipment, state the measurand and representation.

For every feature class, decide:
- what physical point is being represented (for example, signpost centre, shelter reference point, kerb-ramp transition, or a defined stop-location reference);
- whether the geometry is a directly observed point, an offset-derived point, an image-derived point or a representative cartographic point;
- whether the required quantity is horizontal position, height, 3D position, or a combination;
- whether the feature is static and stable enough for the intended observation interval;
- whether the point definition can be repeated by another observer.

A coordinate can be precise but refer to the wrong physical point. Feature definition and positional measurement must therefore be evaluated together.

## 3. Establish the requirement and acceptance rule

Record the intended use and consequences of positional error. Identify any contractual, client, statutory or technical specification that actually applies. If no authoritative requirement exists, the project owner and competent reviewer must define and approve a project-specific requirement before collection.

The requirement record must specify:
- feature classes covered;
- horizontal, vertical or 3D component;
- coordinate reference system, reference-frame realisation and epoch where applicable;
- vertical datum/height type where applicable;
- required statistic or test (not just a vague phrase such as "accurate to X");
- confidence or coverage interpretation;
- treatment of systematic bias and gross errors;
- sample design and minimum evidence needed;
- decision rule, including any guard band for reference uncertainty;
- who approves the rule and when it was frozen.

Do not copy a numerical threshold from a different project or instrument manual and present it as a universal tolerance. If the user requirement is not known, leave acceptance as **unresolved** and do not issue a pass/fail accuracy claim.

## 4. Select an independent reference method

Choose the reference method only after reconnaissance and requirement definition. Candidate methods may include appropriately controlled total-station observations, suitable GNSS methods, levelling for height, calibrated dimensional measurement, or independently controlled image/point-cloud methods. These are alternatives, not interchangeable guarantees.

The reference method must have:
- a documented reference frame and coordinate operation;
- known provenance and traceability appropriate to the required decision;
- uncertainty materially suitable for evaluating the test data;
- a documented instrument/system verification status;
- a procedure appropriate to the feature and environment;
- an operator and reviewer with suitable competence.

A second reading from the same instrument, setup, control and processing chain is not automatically independent. Identify shared control, calibration, atmospheric, centring, operator, software and transformation effects. Where errors are correlated, account for covariance rather than assuming independence.

### Reference evidence register

Create one record per reference source or check observation with at least:

| Field | Meaning |
|---|---|
| reference_id | Stable identifier |
| feature_id | Feature being checked |
| reference_method | Actual method used |
| reference_instrument_id | Equipment register identifier |
| reference_operator | Operator/team code |
| observed_at | Timestamp with timezone |
| reference_crs | Full CRS/reference-frame identification |
| coordinate_epoch | Where applicable |
| height_reference | Where applicable |
| reference_coordinates | Coordinates and units |
| standard_uncertainty | Component-wise uncertainty and basis |
| covariance_information | Covariance/correlation where known |
| raw_record_ref | Immutable source record |
| independence_statement | What is independent and what is shared |
| verification_status | Evidence supporting the reference method |
| notes | Conditions, limitations and anomalies |

## 5. Design the check sample

The check sample must represent the population and the failure modes relevant to the intended use. Do not choose only convenient, open-sky or easy-to-access features.

Before fieldwork:
1. Define the population of features and the units to be checked.
2. Stratify where meaningful (feature class, corridor section, environment, acquisition method, obstruction, geometry or risk).
3. Select locations to cover the full study extent, including edges and clusters where relevant.
4. Include difficult conditions likely to degrade acquisition, not just ideal conditions.
5. Determine sample size from the required statistical decision, expected variability, confidence/coverage and practical risk. Document the rationale; do not invent a universal minimum number.
6. Randomise or otherwise document selection within strata to limit convenience bias.
7. Identify any repeat observations and changed setups needed to test repeatability or setup effects.
8. Reserve independent check observations from adjustment, calibration, tuning and parameter selection.

If the population is too small for a defensible statistical sample, consider checking all features and state the limits of inference. A small sample cannot support broad claims about unsampled conditions.

## 6. Preserve independence

Independent check coordinates must not be used to:
- constrain or adjust the coordinates being tested;
- tune transformation parameters;
- select processing settings after inspecting check residuals;
- remove observations until the check statistics pass.

If check results lead to a correction or model change, record the change and acquire a new independent check set, or clearly label the original checks as no longer independent for the revised result.

Document shared sources of error. "Different instrument" alone does not prove independence if both methods rely on the same control coordinates or transformation.

## 7. Compute discrepancies and uncertainty

For a matched test feature (i), use a consistent coordinate order and units.

Horizontal components:
- (dE_i = E_{test,i} - E_{ref,i})
- (dN_i = N_{test,i} - N_{ref,i})
- horizontal radial discrepancy: (r_i = \sqrt{dE_i^2+dN_i^2})

Vertical component, where relevant:
- (dH_i = H_{test,i} - H_{ref,i})

Report horizontal and vertical results separately. Do not combine them into one number unless the specification explicitly defines a 3D metric.

At minimum, consider reporting:
- number of planned, observed, valid and excluded checks;
- mean component discrepancies (bias);
- component standard deviations;
- RMSE by component;
- horizontal radial discrepancy distribution;
- a percentile or confidence statistic only when its definition and sample basis are stated;
- maximum discrepancy with investigation status;
- results by feature class and relevant environmental stratum;
- confidence intervals or uncertainty bounds appropriate to the design.

For component (j), the conventional sample RMSE is:
\[
RMSE_j = \sqrt{\frac{1}{n}\sum_{i=1}^{n}d_{ij}^{2}}
\]
This statistic combines systematic and random effects; report bias as well so the two are not hidden.

### Reference uncertainty

The reference is not exact. For a test-minus-reference difference, the component variance is:
\[
u^2(d)=u^2(test)+u^2(ref)-2\,cov(test,ref)
\]
For independent test and reference errors, the covariance term is zero. If common control, calibration or processing sources exist, do not assume it is zero without justification.

Use uncertainty estimates that match the coordinate component and confidence interpretation. Explain whether reported values are standard uncertainties, expanded uncertainties, confidence intervals or empirical discrepancies. Do not subtract reference uncertainty mechanically from observed errors or claim a corrected accuracy statistic without a justified statistical model.

## 8. Investigate failures without hiding them

For every failed or unusual check:
- preserve the original observation and reference record;
- inspect feature identification and point definition;
- inspect raw measurements, setup and instrument metadata;
- check CRS, epoch, units, axis order and coordinate transformations;
- examine control, geometry, multipath/obstruction, centring, height entry and environmental conditions as relevant;
- identify whether the issue is isolated, systematic, clustered or class-specific;
- document any correction, re-observation or exclusion and its reason.

Do not delete a point solely because it worsens the statistics. Any exclusion must have a defensible, recorded reason independent of the desired result. Report both the original check outcome and the disposition.

## 9. Pre-field decision sheet

Complete and approve this sheet before acquisition. "TBD" means the gate remains open.

| Decision | Approved value / evidence |
|---|---|
| Intended use and decision supported | TBD |
| Feature classes and point definitions | TBD |
| Study boundary and population | TBD |
| Required positional component(s) | TBD |
| CRS, frame, epoch and height reference | TBD |
| Applicable specification or approved project requirement | TBD |
| Acceptance statistic and decision rule | TBD |
| Reference method and traceability | TBD |
| Reference uncertainty budget | TBD |
| Independence and shared-error assessment | TBD |
| Sampling/stratification rationale | TBD |
| Planned number and distribution of checks | TBD |
| Repeat/setup-change design | TBD |
| Failure investigation and recheck process | TBD |
| Competent reviewer and approval date | TBD |

## 10. Verification report template

A final report should include:
1. Executive decision: pass, fail, conditional, or not evaluated against a defined requirement.
2. Intended use, scope, feature definitions and exclusions.
3. Acquisition and reference methods, equipment and operators.
4. CRS/reference-frame/epoch/height details and transformations.
5. Sample design, selection, coverage and independence statement.
6. Reference uncertainty and shared-error analysis.
7. Predeclared acceptance rule and approval evidence.
8. Component discrepancies, bias, RMSE and justified distribution statistics.
9. Results by feature class and relevant conditions.
10. Failed checks, investigations, exclusions and corrective actions.
11. Limitations, unsampled conditions and fitness-for-use statement.
12. Raw data references, processing versions, hashes and reviewer sign-off.

A report must not imply that one small pilot validates all instruments, operators, environments or feature classes.

## 11. Release gate

The positional-verification gate remains **NOT READY** until the site, intended use, feature definitions, method, reference, competent supervision, access/safety conditions and predeclared acceptance rule are established.

The current synthetic PostGIS run demonstrates schema ingestion, programmed spatial checks and GeoPackage export only. It contains no independent reference coordinates and cannot populate this verification report with accuracy results.
