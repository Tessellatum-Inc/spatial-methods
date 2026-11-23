# Exercise A — repeated distance and horizontal-angle observations

**Version:** 0.1  
**Status:** Reproducible synthetic worked experiment; not field evidence  
**Primary subjects:** SM-FND-011, SM-COL-001, SM-COL-003  
**Connected subjects:** SM-ALG-018, SM-REC-008  
**Dataset:** [Synthetic observations](../../data/measurement/exercise-a-synthetic-observations.csv)  
**Analysis:** [Reproducible Python analysis](../../scripts/measurement/analyze_exercise_a.py)  
**Foundational context:** [Measurement principles and field verification](../../foundations/measurement-science/measurement-principles-and-field-verification.md)

## 1. Purpose

This exercise demonstrates how repeated terrestrial-survey observations become estimates, repeatability statistics, uncertainty statements and documented checks. It deliberately uses synthetic observations. No instrument was operated and no field performance is claimed.

The exercise has two parallel observation series:

1. Eight repeated EDM distance readings to one fixed target.
2. Eight repeated horizontal-angle readings between two fixed targets from one fixed station.

The dataset is intentionally small enough to inspect manually and structured so that a future field dataset can replace it without changing the analysis logic.

## 2. Measurands and scope

### Distance

The measurand is the horizontal-independent line-of-sight distance indicated for the fixed instrument-to-prism line, after the hypothetical field procedure's atmospheric and prism corrections have already been applied. Values are recorded in metres to 0.001 m.

For this simplified exercise, the observation model is:

\[
d_i = D + \varepsilon_i
\]

where D is the estimated distance under the stated setup and correction assumptions, and epsilon represents the remaining reading-to-reading variation.

This is not a full EDM physical model. A real procedure must document slope versus horizontal distance, atmospheric correction inputs, prism constant, instrument and reflector heights where relevant, instrument serial number, calibration information and the reference/traceability chain.

### Horizontal angle

The measurand is the horizontal angle from target A to target B at one fixed station, observed under unchanged setup conditions. The recorded values are in decimal degrees.

\[
\theta_i = \theta + \eta_i
\]

The example observations do not cross 0°/360°. The analysis nevertheless computes a circular mean and wrapped angular residuals so the method behaves correctly near the wrap boundary.

This is a repeated-angle demonstration, not an ISO 17123-3 theodolite field test. The full standard procedure and acceptance criteria must be obtained and followed before making any standards-based instrument-verification claim.

## 3. Synthetic observation record

All rows in the CSV are simulated. The eight readings are divided into two sequential blocks of four to make a simple drift/block comparison possible. They are not independent instrument setups: the same notional station and target setup is held fixed.

| Observation | Distance (m) | Horizontal angle (decimal degrees) | Block |
|---:|---:|---:|---|
| 1 | 50.002 | 63.40422222 | A |
| 2 | 49.999 | 63.40411111 | A |
| 3 | 50.001 | 63.40419444 | A |
| 4 | 50.000 | 63.40416667 | A |
| 5 | 49.998 | 63.40413889 | B |
| 6 | 50.001 | 63.40425000 | B |
| 7 | 50.000 | 63.40408333 | B |
| 8 | 49.999 | 63.40416667 | B |

The CSV is the machine-readable source of truth. The displayed angle values are rounded for readability; the CSV preserves the full values used by the analysis.

## 4. Estimation and repeatability

For n repeated scalar observations, the arithmetic mean is:

\[
\bar{x}=\frac{1}{n}\sum_{i=1}^{n}x_i
\]

The sample standard deviation is:

\[
s=\sqrt{\frac{\sum_{i=1}^{n}(x_i-\bar{x})^2}{n-1}}
\]

When the observations are suitably independent and represent the same measurement conditions, the standard uncertainty of the mean from this Type A evaluation is:

\[
u_A(\bar{x})=\frac{s}{\sqrt{n}}
\]

This standard error is not the spread of individual readings. It quantifies the statistical uncertainty of the estimated mean under the model and assumptions. Correlation, drift or changing conditions can make the simple formula inappropriate.

### Distance result

- Number of readings: 8
- Mean distance: 50.000000 m
- Sample standard deviation: 0.001309 m (1.309 mm)
- Standard uncertainty of the mean, Type A: 0.000463 m (0.463 mm)
- Observed range: 49.998 m to 50.002 m (4.000 mm)

### Horizontal-angle result

- Number of readings: 8
- Circular mean: 63° 24′ 15.000″
- Sample standard deviation: 0.200″
- Standard uncertainty of the mean, Type A: 0.071″
- The angle residuals are calculated using a wrapped difference in the interval around zero, not by naïvely subtracting decimal degrees.

The values above are reproducible from the CSV with the accompanying script.

## 5. Illustrative distance uncertainty budget

The following Type B inputs are explicitly assumed for this synthetic worked example. They are not specifications for any real EDM or prism.

| Component | Assumed standard uncertainty | Basis |
|---|---:|---|
| Repeatability of mean | 0.463 mm | Type A from the eight synthetic readings |
| Display resolution | 0.289 mm | 1 mm increment, rectangular rounding interval ±0.5 mm divided by √3 |
| Prism-constant contribution | 0.500 mm | Illustrative standard uncertainty supplied as an assumed input |
| EDM scale contribution | 0.100 mm | Illustrative 2 ppm standard uncertainty at 50 m |
| Combined standard uncertainty | 0.747 mm | Root-sum-square, assuming components are uncorrelated |
| Expanded uncertainty | 1.493 mm | k = 2, illustrative approximation |

\[
u_c=\sqrt{u_A^2+u_{res}^2+u_{prism}^2+u_{scale}^2}
\]

\[
U=k u_c,\qquad k=2
\]

**Illustrative reported result:** 50.0000 m ± 0.0015 m (expanded uncertainty, k = 2).

This is a teaching calculation, not a traceable survey result. The assumed Type B inputs must be replaced with evidence from the actual instrument, prism, calibration information and procedure. The root-sum-square calculation is only justified if the components can reasonably be treated as uncorrelated and the linear uncertainty model is adequate.

The repeated observations share one setup. Setup-related effects do not become smaller merely because the same setup is observed repeatedly. They would need their own model and evidence if material.

## 6. Angle uncertainty boundary

Only the Type A repeatability of the mean is calculated for the angle series. A complete angle uncertainty budget would need, at minimum, a defined instrument and its angular calibration/verification information, display resolution, station and target centring, target definition, pointing/aiming procedure, face-left/face-right design, observation-set structure, environmental conditions and the geometry needed to translate centring offsets into angular effects.

Do not append a guessed instrument accuracy figure to the Type A result and call it a complete uncertainty budget.

## 7. Checks and interpretation

The reproducible script reports:
- observation count, mean, sample standard deviation and standard uncertainty of the mean;
- minimum, maximum and range for distance;
- angular circular mean and wrapped residuals;
- block means for A and B;
- the illustrative distance uncertainty budget.

The block means are a diagnostic, not a formal drift test. A difference between blocks may arise from random variation or a time-dependent effect. With only two blocks and four observations per block, this dataset cannot establish the absence of drift or other systematic effects.

A defensible real-world exercise should add independent checks, for example:
- re-observe after a fresh instrument and target setup;
- repeat on another day or with another operator;
- compare against a suitable reference distance or independently established angle;
- observe in both telescope faces where appropriate;
- document environmental and setup conditions;
- inspect residuals and time order rather than relying only on a single standard deviation.

An independent check must be genuinely independent of the observations used to estimate the result. Reprocessing the same observations is not an independent validation.

## 8. Field-compatible procedure

For a real exercise, adapt this sequence to the instrument manual, project specification and applicable standard:

1. Define the required distance and angle quantities, units, tolerances and reference conditions before observing.
2. Select stable, unambiguous station and target marks with suitable geometry and line of sight.
3. Record instrument, prism/target, serial numbers, operator, date/time, station and target identifiers, setup and environmental metadata.
4. Check tribrach, tripod, centring, levelling, target height, prism constant and instrument configuration.
5. Record raw readings in a field book or structured file. Do not overwrite raw observations with corrected or rounded values.
6. Collect a planned number of repeated observations, preserving observation order and face information.
7. Repeat after a fresh setup or under a separately specified condition for a meaningful reproducibility check.
8. Reduce observations using documented corrections and the declared measurement model.
9. Calculate estimates, residuals and uncertainty components; investigate outliers rather than deleting them automatically.
10. Compare against predeclared acceptance requirements and independent evidence. Report limitations and retain the raw record.

This is a planning template, not a substitute for the complete ISO 17123 procedure, an instrument manual or a project-specific survey specification.

## 9. What this exercise demonstrates — and does not

**Demonstrates:** the distinction between individual-reading scatter and uncertainty of the mean; Type A evaluation; an explicit illustrative Type B budget; circular treatment of angles; basic block diagnostics; and reproducible reporting.

**Does not demonstrate:** instrument calibration, traceability, accuracy against a known reference, compliance with a surveying standard, performance under different operators/days, or suitability for any engineering or cadastral tolerance.

## 10. Sources and further reading

- NIST, *TN 1297: Type A Evaluation of Standard Uncertainty* — statistical evaluation from observation series: https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-3-type-evaluation-standard-uncertainty
- NIST, *Guidelines for Evaluating and Expressing the Uncertainty of NIST Measurement Results*, Appendix A — mean and standard uncertainty of the mean: https://www.nist.gov/system/files/documents/2017/05/09/tn1297s.pdf
- ISO 17123-3:2001, *Field procedures for testing geodetic and surveying instruments — Part 3: Theodolites* — scope is field repeatability evaluation, not comprehensive acceptance/performance evaluation: https://www.iso.org/standard/30200.html
- BIPM/JCGM 100:2008, *Evaluation of measurement data — Guide to the expression of uncertainty in measurement*: https://www.bipm.org/documents/20126/2071204/JCGM_100_2008_E.pdf

## 11. Next experiment

Exercise B will use a levelling loop to connect repeated observations to misclosure, adjustment, uncertainty propagation, benchmark/reference assumptions and independent closure checks. It should reuse the measurement-model and reporting discipline established here.
