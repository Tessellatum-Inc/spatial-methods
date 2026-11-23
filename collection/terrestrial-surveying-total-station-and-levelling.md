# Terrestrial surveying: total station and differential levelling

> **Pillar:** Spatial Data Collection  
> **Subject:** SM-COL-001 — Geodetic and engineering surveying  
> **Status:** Initial field-method synthesis; detailed instrument-specific procedures and local standards review remain necessary  
> **Connected pillars:** Measurement science, survey adjustment, coordinate geometry, control-network design and survey-to-spatial-dataset workflows

## 1. Purpose and method choice

Terrestrial surveying determines positions, directions, distances and height differences from observations made at or near the Earth's surface. Two core instrument families are:

- **Total stations**, which combine angular measurement and electronic distance measurement (EDM) to determine relative point positions and, with a reference orientation and control, coordinates.
- **Levels and graduated staffs**, which determine height differences from horizontal lines of sight. Differential levelling is often the preferred method when vertical control is the primary measurand.

These methods are complementary, not interchangeable. A total station can derive height differences by trigonometric levelling, but its vertical result is sensitive to vertical-angle, distance, instrument-height, target-height, refraction and setup effects. Differential levelling directly transfers height through a sequence of staff readings and is generally preferred when high-quality vertical control is required.

Choose the method from the defined measurand, required uncertainty, terrain, visibility, access, control geometry, instrument capability and governing specification. Do not choose a method solely because an instrument is available.

## 2. Define the measurand and reference

Before occupation, define exactly what point or surface is being observed. A coordinate may refer to a monument centre, prism centre, pole tip, kerb edge, pavement breakline, structure corner or another physical feature. These are not interchangeable.

Record the feature identity and physical definition; coordinate reference system, datum/reference-frame realisation and epoch; horizontal projection, units and axis conventions; vertical datum and whether heights are orthometric, normal or ellipsoidal; control-point provenance, coordinates and uncertainty; required horizontal and vertical quality and acceptance criteria; instrument and target configuration; independent checks and failed-check handling.

A local engineering grid may be appropriate for a project, but its origin, orientation, scale and relationship to any external CRS must be explicit. Do not silently mix grid distances with ground distances or coordinates from different datums.

## 3. Total-station observation model

A total station observes horizontal direction, vertical direction (or zenith angle), and slope distance to a prism or, in some instruments, a reflectorless target. The instrument does not directly measure an absolute map coordinate. Coordinates are computed from observations, station coordinates, orientation, instrument height and target height.

Let \(S\) be corrected slope distance; \(z\) be zenith angle measured from the upward vertical; \(\alpha\) be horizontal direction clockwise from the chosen north reference; \(HI\) be instrument height above the occupied station mark; \(HT\) be target/prism height above the target point; and \((E_0,N_0,H_0)\) be occupied station coordinates.

For a zenith-angle convention:

\[
D_h = S\sin z
\]

\[
\Delta h_{IT}=S\cos z
\]

\[
E_T=E_0+D_h\sin\alpha
\]

\[
N_T=N_0+D_h\cos\alpha
\]

\[
H_T=H_0+HI+\Delta h_{IT}-HT
\]

These equations assume a local Cartesian grid, a horizontal direction measured clockwise from grid north, and a zenith angle measured from the upward vertical. If the instrument reports a vertical angle \(v\) from the horizontal, then \(D_h=S\cos v\) and \(\Delta h_{IT}=S\sin v\). Confirm the instrument's angle convention before using any export or calculation.

The equations are a local surveying model. Long sights, large elevation differences, high-accuracy work or geodetic coordinate computation may require curvature, refraction, projection-scale, grid-to-ground, atmospheric and other corrections. Apply corrections once, with traceable settings; avoid double-correcting distances already reduced by the instrument or processing software.

### 3.1 EDM and atmospheric effects

EDM distance depends on the propagation of electromagnetic radiation through the atmosphere. Temperature, pressure and humidity affect refractive index and therefore measured distance. Record the atmospheric inputs and ppm correction model used, along with prism constant, reflector type, instrument mode and any applied scale or additive constants.

Prism and reflectorless observations have different measurement geometries and error behaviour. Reflectorless range may be affected by target material, incidence angle, surface condition, beam footprint and mixed returns at edges. Do not assume that reflectorless and prism measurements to a nominally identical feature are equivalent.

### 3.2 Orientation and backsight

A total station requires a defined orientation to convert observed directions into grid bearings or coordinates. Common approaches include backsight to a known control point; orientation from multiple control points; resection from observations to known control points; or local assumed coordinates for a bounded relative survey, with the local datum explicitly stated.

A backsight check tests whether the occupied point, orientation point, target identity, centring and coordinate/reference information are consistent. Record the check observations and compare them with predeclared tolerances.

## 4. Total-station field procedure

### 4.1 Preparation

1. Confirm project scope, permissions, safety constraints and required deliverable.
2. Verify control coordinates, descriptions, stability, datum, epoch and uncertainty.
3. Check instrument, tribrach, tripod, prism, poles, batteries, data collector, firmware and calibration/verification status.
4. Confirm prism constant, target type, atmospheric settings, units, angle convention, coordinate order and job configuration.
5. Inspect the survey area for intervisibility, obstructions, traffic, heat shimmer, reflective surfaces and unsafe setup locations.
6. Design stations, traverse links, check shots, redundant observations and independent checks before collection.

### 4.2 Occupy and orient

1. Identify the station mark and inspect it for disturbance.
2. Set up the tripod, centre and level the instrument, and verify centring after levelling.
3. Measure and record instrument height using the specified method and reference point.
4. Enter or independently verify station coordinates and station identifier.
5. Set the backsight target over the correct mark; measure and record target height.
6. Observe the backsight using the planned face and repetition procedure.
7. Check orientation by observing a second known point or by an independent check shot where the design permits.
8. Record setup time, operator, instrument ID, setup conditions, backsight ID, prism ID and all heights.

### 4.3 Detail and traverse observations

1. Confirm each target point's physical identity and feature definition.
2. Centre the prism or pole over the intended point and record target height at the time of observation.
3. Observe horizontal and vertical directions and slope distance using the planned face/repetition strategy.
4. Record target type, prism constant, reflectorless mode if used, atmospheric inputs, observation time and relevant environmental conditions.
5. Reobserve critical points and use independent check shots to detect setup, target-height, orientation and point-identification errors.
6. For traverses, observe required angles and distances, including redundant ties and closing observations.
7. At each setup change, repeat setup and orientation checks. Never carry a backsight orientation forward without verifying the new setup.
8. Review the field file before leaving: station names, point codes, heights, units, target modes and check observations must be complete.

### 4.4 Traverse design and adjustment

A traverse links stations through measured directions/angles and distances. It should be designed with sufficient geometric strength, redundancy and ties to reliable control. A traverse that merely returns to its starting point can still contain weak geometry or compensating errors.

For a closed traverse, inspect angular misclosure, coordinate misclosure, relative linear closure, individual residuals and the influence of control uncertainty. A common coordinate misclosure is:

\[
f_E=\sum_i \Delta E_i,\qquad
f_N=\sum_i \Delta N_i
\]

\[
f_p=\sqrt{f_E^2+f_N^2}
\]

The ratio of total traverse length to positional misclosure is sometimes reported as a relative closure statistic. It is not a complete accuracy statement and must be interpreted against the applicable project specification, geometry, observation weights and control quality.

Bowditch (compass) adjustment distributes coordinate misclosure in proportion to line lengths. It is an approximate rule for particular assumptions, not a universal replacement for a weighted least-squares network adjustment. Use a stochastic model that reflects angular and distance observation quality, correlations, instrument setup and control uncertainty when the project requires rigorous adjustment.

## 5. Differential-levelling observation model

Differential levelling transfers height differences using a level instrument that establishes a horizontal line of sight and a graduated staff held vertically at points.

For one setup:

\[
HI = RL_A + BS
\]

\[
RL_B = HI - FS
\]

where \(RL_A\) is the known reduced level of the backsight point, \(BS\) is the backsight staff reading, \(HI\) is height of instrument (line of sight), \(FS\) is the foresight staff reading, and \(RL_B\) is the derived reduced level of the foresight point.

Across a complete route:

\[
\Delta H = \sum BS-\sum FS
\]

For a closed loop returning to the starting benchmark, the computed net height change should be zero within the applicable closure tolerance. For a line between two known benchmarks, compare the computed height difference with the independently known difference.

The arithmetic is simple; the quality depends on staff verticality, stable turning points, collimation, balanced sight lengths, refraction, settlement, reading technique, benchmark stability and network design.

## 6. Differential-levelling field procedure

### 6.1 Before levelling

1. Confirm benchmark identities, descriptions, stability, datum and published heights.
2. Select required levelling class/order and closure criterion from the project specification.
3. Verify level and staff condition, staff graduation, foot plate, bubble, tripod and any digital staff/instrument pairing.
4. Perform and document the appropriate field check, such as a two-peg test, according to the instrument and governing procedure.
5. Plan the route, turning points, observation sequence, sight-length balance and independent closure.
6. Protect benchmarks and turning points from disturbance and settlement.

### 6.2 At each setup

1. Set the instrument on stable ground and allow it to settle as required.
2. Establish a stable, clearly identified turning point.
3. Take a backsight to the known or previous turning point.
4. Take a foresight to the next turning point before moving the instrument.
5. Keep backsight and foresight distances balanced where practicable, reducing systematic effects from collimation and curvature/refraction differences.
6. Keep staff vertical using the staff bubble or a controlled rocking procedure appropriate to the method.
7. Record readings, station IDs, sight distances, setup identifiers, time and unusual conditions immediately.
8. Repeat or check observations where required by the project design; do not reconstruct missing readings from memory.

For digital levels, retain native observation files and instrument reports as well as the exported height table. For optical levels, retain the original field book and calculation trail.

### 6.3 Closure and route checks

Use a route that starts and ends on known control, or closes through an independently observed benchmark. A closure check detects inconsistency but does not by itself identify the cause or prove the absence of compensating errors.

A common field-book arithmetic check is:

\[
\sum BS-\sum FS = RL_{\text{end,computed}}-RL_{\text{start}}
\]

The closure error against a known terminal benchmark is:

\[
e_c = RL_{\text{end,computed}}-RL_{\text{end,known}}
\]

Do not apply a universal numeric closure tolerance. The permitted value depends on levelling class/order, route length, observation procedure, instrument/staff system and governing specification. If a route fails, investigate and repeat the affected observations; do not simply distribute a large closure error and label the result acceptable.

When a correction is justified, document the rule and its assumptions. Equal-per-setup or distance-weighted distribution may be appropriate in defined cases, but a weighted network adjustment is preferable when route geometry, observation precision and correlations differ materially.

## 7. Quality assurance and failure modes

| Source or failure mode | Total station evidence/check | Differential levelling evidence/check |
|---|---|---|
| Instrument setup | Centring, levelling, instrument height, station identity | Tripod stability, compensator/bubble check, setup record |
| Orientation/control | Backsight check, resection residuals, independent control tie | Benchmark identity and independent closure |
| Target/staff setup | Prism constant, target height, pole verticality, target ID | Staff verticality, foot placement, staff calibration/condition |
| Instrument geometry | Face-left/face-right observations, collimation/axis checks | Two-peg test or applicable level test |
| Distance/reading effects | Atmospheric correction, prism/reflectorless mode, EDM checks | Balanced sight lengths, staff reading checks |
| Environmental effects | Heat shimmer, wind, visibility, refraction, unstable targets | Refraction, temperature gradients, wind, turning-point settlement |
| Human/data handling | Point codes, heights, units, target identification and raw files | Original readings, arithmetic checks, station sequence and transcription |
| Network strength | Traverse geometry, redundancy, closure, residuals, control uncertainty | Loop/line closure, route redundancy, benchmark stability |
| Independent verification | Check shots, repeat setups, known-point tests | Independent loop or repeat run, separate benchmark tie |

A check should be selected to expose a plausible failure mode. Repeating an observation under the same setup may not expose a common setup or reference bias.

Do not confuse instrument repeatability with end-to-end survey accuracy; traverse closure with proof of correctness; a small levelling closure with proof that all benchmarks are stable; a field verification with a full calibration; or a software adjustment with evidence that the input observations are valid.

## 8. Processing, adjustment and reporting

Preserve raw observations and field notes. The processing record should identify project, instrument, prism/staff, serial numbers and firmware; station and target identifiers and physical descriptions; instrument and target heights with raw measurement method; angle/distance observations, face, repetitions and observation times; prism constants, atmospheric inputs and correction settings; control coordinates, datum, epoch, vertical reference and uncertainty; traverse/levelling geometry and observation weighting; adjustment method, constraints, stochastic assumptions and software version; residuals, closures, rejected observations and reasons; adjusted coordinates/heights and uncertainty or quality class; independent check results and acceptance decision.

For a rigorous network, formulate observation equations and adjust with weighted least squares or generalized least squares as appropriate. Retain covariance information and distinguish fixed control constraints from uncertain control observations. Do not force control coordinates to be exact if their uncertainty is material.

For height networks, the basic observation is a height difference between points. For a network of observations \(l\), unknown heights \(x\), design matrix \(A\) and covariance \(C_l\), a linear model can be written:

\[
l + v = Ax
\]

with weighted least-squares estimate:

\[
\hat{x}=(A^T P A)^{-1}A^T P l,\qquad P=C_l^{-1}
\]

This expression assumes the normal matrix is invertible under the chosen datum constraints. A free or minimally constrained network has a datum defect and requires an explicit datum strategy; do not hide it with arbitrary fixed coordinates.

## 9. Data and provenance model

For every occupation/setup, retain project, setup, station, target and observation identifiers; feature/monument definition and field description; timestamps, operator and environmental notes; instrument, prism/staff and accessory IDs; raw instrument and field-book file paths plus checksums; instrument height, target height, staff readings and measurement method; angle convention, distance mode, prism constant and atmospheric corrections; control IDs, coordinate values, datum, epoch, vertical datum and source uncertainty; observation repetitions, face, sight lengths and setup geometry; processing software/version, adjustment method and configuration; residuals, closure, uncertainty, independent checks and acceptance status.

Preserve raw observations separately from corrected observations, adjusted coordinates and interpreted feature records. A new adjustment should create a new derived version, not overwrite the original measurement record.

## 10. Physical-world applications

Total stations and differential levelling support engineering control, topographic surveys, construction monitoring, road and rail surveys, utility and asset mapping, building and infrastructure measurement, deformation monitoring, earthworks, drainage design and vertical control.

The task determines the method. A constrained site with obstructed satellite visibility may favour a total-station traverse. A long route requiring dependable vertical control may favour differential levelling. A dense 3D scene may be better captured with terrestrial laser scanning, while a large open area may justify GNSS or aerial methods. A combined workflow is often more defensible than forcing one instrument to do everything.

## 11. Connections to Spatial Methods

- [Measurement science and survey-network adjustment](../learning-paths/measurement-science-and-survey-adjustment.md) — measurement models, covariance, least squares, datum constraints, reliability and synthetic network experiments.
- [Measurement principles and field verification](../foundations/measurement-science/measurement-principles-and-field-verification.md) — measurands, traceability, uncertainty and field checks.
- [Measurement models and measurand definition](../foundations/measurement-science/measurement-models-and-measurand-definition.md) — operational definition and propagation of uncertainty.
- [Survey-to-spatial-dataset workflow](../recipes/survey-to-spatial-dataset/README.md) — end-to-end acquisition, processing, independent checks and delivery.
- [GNSS positioning and navigation observation](gnss-positioning-and-navigation-observation.md) — complementary satellite-based positioning and reference-frame handling.

## 12. References and standards routes

- [ISO 17123-5:2018 — Field procedures for testing geodetic and surveying instruments: Total stations](https://www.iso.org/standard/71689.html). The standard specifies field procedures for evaluating coordinate-measurement repeatability and suitability for an immediate task. It is not a complete end-to-end accuracy certification.
- [ISO 17123-4:2012 — Field procedures for testing geodetic and surveying instruments: Reflector EDM](https://www.iso.org/standard/54624.html). Its stated scope is reflector-type EDM measurements; it should not be assumed to validate reflectorless mode.
- [ISO 17123-2 — Field procedures for testing levels](https://www.iso.org/obp/ui?_escaped_fragment_=iso%3Astd%3Aiso%3A17123%3A-2%3Aed-1%3Av1%3Aen). Consult the current national adoption and applicable project requirements.
- [USGS: Basic procedures of levelling](https://pubs.usgs.gov/unnumbered/70045432/report.pdf). Explains backsight/foresight transfer, height of instrument and closure checks.
- [U.S. Army Corps of Engineers: Survey Guidelines](https://www.mvn.usace.army.mil/Portals/56/docs/engineering/SurveySection/Survey_Guidelines_Rev4%201.pdf). A project-agency example of field-book requirements, setup check shots and differential-levelling verification. Its numeric tolerances are not universal and should not be transplanted to other jurisdictions.

These sources provide technical routes and examples, not a universal specification. Before real work, identify the current governing national, professional, contractual and safety requirements. For Kenyan work, verify the applicable Survey Act, Survey Regulations, professional requirements, control information and any project-specific specification before approving a field procedure.
