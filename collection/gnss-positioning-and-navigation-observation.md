# GNSS positioning and navigation observation

> **Pillar:** Spatial Data Collection  
> **Connections:** Geodetic foundations, adjustment and estimation algorithms, survey recipes, navigation and physical-world applications  
> **Status:** Initial method specification; local control-network requirements and field validation remain project-specific  
> **Scope:** Satellite-based positioning using one or more global navigation satellite systems (GNSS), including GPS, Galileo, GLONASS and BeiDou where supported by the receiver and processing chain.

## 1. Start with the position requirement

GNSS is not a single accuracy class or field procedure. Select the observation method from the required coordinate quality, feature geometry, time constraints, reference-frame requirements, environment and available correction infrastructure.

Before fieldwork, specify the feature or monument to be positioned; horizontal and vertical uncertainty requirements; coordinate reference frame, datum realisation, coordinate epoch and projection; whether the deliverable is a navigation position, detail point, control point, trajectory or deformation time series; required height type and vertical datum; observation mode and correction source; and independent checks and acceptance criteria.

A coordinate without a reference frame, epoch, height convention and quality statement is incomplete for precise spatial work.

## 2. What the receiver observes

A GNSS receiver tracks radio signals transmitted by satellites with known, time-varying orbits and clocks. It records observables such as code pseudorange, carrier phase and signal strength. A position is estimated from these observations; it is not simply read directly from a satellite.

A simplified code pseudorange observation for receiver \(r\), satellite \(s\), and frequency \(f\) is:

\[
P_{r,f}^{s}
= \rho_r^s
+ c(\delta t_r-\delta t^s)
+ I_{r,f}^{s}
+ T_r^s
+ b_{r,f}^{s}
+ \epsilon_{P}
\]

where \(\rho\) is geometric range between satellite and receiver antenna phase centres; \(c\) is the speed of light; \(\delta t_r\) and \(\delta t^s\) are receiver and satellite clock offsets; \(I\) and \(T\) represent ionospheric and tropospheric propagation delays; \(b\) groups hardware and signal biases; and \(\epsilon_P\) includes measurement noise and unmodelled effects.

A simplified carrier-phase observation, expressed in metres, is:

\[
\Phi_{r,f}^{s}
= \rho_r^s
+ c(\delta t_r-\delta t^s)
- I_{r,f}^{s}
+ T_r^s
+ \lambda_f N_{r,f}^{s}
+ B_{r,f}^{s}
+ \epsilon_{\Phi}
\]

where \(\lambda_f\) is carrier wavelength, \(N\) is the integer ambiguity while continuous phase lock is maintained, and \(B\) represents phase hardware biases. Sign and detailed bias conventions depend on the observation model.

Carrier phase is much more precise than code ranging but contains an initially unknown integer ambiguity. Cycle slips, signal obstruction, receiver resets and poor tracking can interrupt phase continuity. Precise carrier-phase positioning therefore depends on ambiguity resolution, quality control and a defensible stochastic and functional model.

These are simplified observation models, not a complete multi-frequency, multi-constellation estimator. Real processing must account for signal-specific biases, antenna phase-centre offsets and variations, orbit and clock products, Earth rotation, relativistic effects, loading and other corrections appropriate to the accuracy target.

## 3. Choose the observation method

| Method | Observation arrangement | Appropriate use | Main limitations |
|---|---|---|---|
| Standalone code positioning | One receiver, code observations, broadcast navigation data | General navigation and reconnaissance | Usually unsuitable for survey control; affected by geometry, atmosphere and multipath |
| Differential code positioning | Rover corrected using a reference receiver or service | Improved code-based positioning | Depends on reference data, baseline, corrections and common error cancellation |
| Static relative GNSS | Two or more stationary receivers observe simultaneously | Control networks and high-accuracy relative positioning | Requires session planning, stable setups, processing and redundancy |
| Rapid static | Stationary occupations with carrier-phase equipment | Efficient local control where validated | Short sessions can weaken ambiguity resolution |
| RTK | Moving rover receives real-time carrier-phase corrections from a base or network | Real-time engineering and detail survey | Requires correction communications, fixed-solution monitoring and independent checks |
| Network RTK | Rover receives corrections derived from continuously operating reference stations | Real-time positioning over a service area | Depends on network geometry, service model, datum realisation and communications |
| PPK | Base and rover raw observations processed after collection | Kinematic mapping where real-time links are unreliable or unnecessary | Depends on suitable base data, time overlap and processing quality |
| PPP | Receiver uses precise orbit/clock products and suitable observation models | Wide-area positioning without a nearby project base | Convergence, product latency, atmosphere and service characteristics matter |

Do not describe RTK, PPK, static GNSS and PPP as interchangeable. They have different observation arrangements, error cancellation, processing dependencies and failure modes.

## 4. Plan geometry and site conditions

Dilution of precision (DOP) describes the amplification of range-measurement uncertainty by satellite-receiver geometry under a specified model. A low DOP is favourable geometry, not proof of an accurate coordinate: biased observations, multipath, bad antenna heights or incorrect reference data can still produce a poor solution.

Plan satellite visibility and geometry; constellation and signal availability; elevation mask and excluded signals; obstructions, reflective surfaces and nearby transmitters; atmospheric conditions; baseline lengths and reference-station distribution; common observation windows; occupation duration and redundancy.

Avoid placing antennas close to walls, metal roofs, vehicles, fences, water surfaces or tree canopy where practicable. If an obstruction cannot be avoided, document it and assess whether the point remains suitable.

## 5. Field occupation procedure

### Before fieldwork

1. Confirm the coordinate reference frame, datum realisation, epoch, projection and vertical reference.
2. Verify reference-station coordinates, quality and suitability.
3. Select the observation method and session plan from the required uncertainty, baseline and field conditions.
4. Check receiver/antenna compatibility, supported signals, firmware, batteries, storage, cables, tribrachs, poles and measuring equipment.
5. Verify that processing has suitable antenna calibration models, orbit/clock products and geoid model where applicable.
6. Prepare station identifiers, occupation logs, file naming rules and independent check points.

### At each occupation

1. Confirm the physical monument or feature identity before setup.
2. Centre and level the antenna over the defined point; check pole or tripod stability.
3. Record receiver and antenna make, model and serial number, firmware where relevant, orientation if required, and setup configuration.
4. Measure antenna height using the specified method. Record the raw measurement, method, units, reference point and conversion to the antenna reference point (ARP). Do not record only a derived vertical height if the raw slant measurement is needed to reproduce it.
5. Record start and end times with explicit UTC offset, logging interval, elevation mask, constellation/signal selection and correction source.
6. Monitor tracking, correction age, ambiguity status, estimated uncertainty, residuals, cycle slips, communication interruptions and receiver warnings as relevant.
7. Repeat the occupation or observe an independent check point according to the project design. For high-confidence control, independent sessions should change satellite geometry and, where practicable, observer, equipment or time.
8. Before leaving, verify files were written, identifiers match the field log and antenna-height measurements are complete.

A receiver reporting a fixed RTK solution is not, by itself, an independent accuracy test. Re-observation, known-point checks and redundant network geometry are essential safeguards.

## 6. Processing and reference-frame handling

Preserve raw observations and the original field log. Where applicable, retain RINEX observation and navigation files, base-station data, correction-stream metadata, precise orbit and clock products, antenna calibration files, processing software/version, configuration and complete reports.

The processing record should state observation files and time spans; constellations, frequencies and signals included or rejected; reference-station coordinates, frame and epoch; orbit and clock products; antenna models, ARP heights and phase-centre corrections; atmospheric modelling; ambiguity-resolution strategy and fixed/float status; rejected observations, cycle slips and residual tests; estimated coordinates and covariance/uncertainty; transformations, coordinate epochs and geoid model/version.

Do not silently combine coordinates from different reference frames or epochs. A projected CRS is not a substitute for documenting the underlying geodetic reference frame. If a transformation is applied, preserve its operation, parameters, grid files and software provenance.

GNSS positioning estimates position relative to a terrestrial reference frame and produces ellipsoidal height in the corresponding ellipsoid. Orthometric height is derived using a geoid or quasigeoid model and compatible vertical datum. In a common geoid-height convention:

\[
H = h - N_g
\]

where \(H\) is orthometric height, \(h\) is ellipsoidal height and \(N_g\) is geoid undulation. Verify the model and sign convention for the selected vertical reference system; the equation does not make ellipsoidal and orthometric heights interchangeable.

## 7. Quality assurance and acceptance

Define acceptance criteria before collection. Review:

| Quality dimension | Evidence to inspect | Typical failure or warning |
|---|---|---|
| Identity | Monument ID, field description, file/station name | Wrong point or mismatched file |
| Setup | Centring, levelling, pole/tripod check, antenna model | Setup eccentricity or wrong antenna calibration |
| Antenna height | Raw measurements, method, units, ARP conversion | Incorrect height or conversion |
| Observation continuity | Tracking, cycle slips, data gaps, epoch coverage | Loss of lock or incomplete session |
| Geometry | Satellite distribution and DOP over time | Poor or changing geometry |
| Environment | Site sketch, obstructions, reflective surfaces | Multipath or signal blockage |
| Correction/reference | Base coordinates, correction age, frame and epoch | Incompatible or stale correction data |
| Estimation | Residuals, ambiguity status, covariance, baseline/network diagnostics | Weak or inconsistent solution |
| Repeatability | Independent occupation or known-point check | Disagreement beyond project tolerance |
| Vertical reference | Geoid model, vertical datum and transformation | Height type or datum mismatch |

DOP, receiver-reported precision, residuals and ambiguity status are diagnostic evidence, not standalone accuracy certificates. Acceptance must consider independent checks and the full measurement chain.

For a control network, assess closure, redundancy, baseline consistency, network adjustment, reference constraints and uncertainty propagation. For RTK detail capture, check a known point before and after work, repeat critical points, and monitor correction communication and ambiguity resets. For static work, compare independent sessions and inspect baseline and network diagnostics.

Never convert a receiver's displayed precision into a claim of achieved survey accuracy without supporting evidence.

## 8. Data model and provenance

A GNSS observation record should preserve:

- project, station and occupation identifiers and feature/monument identity;
- observation start/end timestamps and UTC offset;
- raw observation file names and cryptographic checksums;
- receiver and antenna make, model, serial number and firmware;
- antenna-height raw value, units, method, reference point and ARP conversion;
- observation interval, elevation mask, constellations and signals;
- method (standalone, static, rapid static, RTK, network RTK, PPK or PPP);
- base/reference station identifiers, coordinates, frame, epoch and correction source;
- processing software/version, models, products and configuration;
- coordinate output, CRS, reference frame, epoch, height type and geoid model;
- quality indicators, independent-check results, uncertainty and acceptance status;
- operator, field notes, environmental conditions and processing provenance.

Keep raw observations, processed coordinates and interpreted feature records as separate but linked entities. Do not overwrite the raw record when a coordinate is reprocessed.

## 9. Method boundaries and common misinterpretations

- GNSS positioning is not synonymous with GPS; GPS is one constellation.
- A coordinate solution is an estimate from observations and models, not a direct measurement of true position.
- More satellites do not guarantee a better result if geometry, signal quality or multipath are poor.
- Low DOP does not establish accuracy.
- Fixed RTK ambiguity status does not replace independent checks.
- Centimetre-level horizontal performance does not imply the same vertical performance.
- Ellipsoidal height is not automatically elevation above mean sea level.
- A datum label without realisation and epoch may be insufficient for high-accuracy work.
- A coordinate exported from a GIS may have lost observation method, uncertainty and processing provenance.
- Consumer navigation tracks should not be promoted to survey control without validation against the required specification.

## 10. Physical-world applications

GNSS observations support cadastral and engineering control, construction set-out, infrastructure inventory, asset mapping, road and rail surveys, precision agriculture, mobile mapping trajectories, environmental monitoring, deformation studies, disaster response and navigation.

The appropriate method depends on the physical decision. A road-asset inventory may accept a validated metre-level position; a bridge deformation network may require stable monuments, long sessions, controlled antenna models and rigorous adjustment. The same receiver can be used in different modes, but the evidence required to accept its outputs changes with the task.

## 11. Connections to the wider Spatial Methods repository

- [Measurement science and survey adjustment](../learning-paths/measurement-science-and-survey-adjustment.md) — reference frames, observations, least-squares estimation and uncertainty.
- [Spatial observation and sampling design](spatial-observation-and-sampling-design.md) — sampling frame, support, independent checks and provenance.
- [Geoinformatics master subject index](../catalog/master-subject-index.md) — stable subject taxonomy and related positioning methods.

This method describes an observation and quality framework. It is not a substitute for national geodetic control specifications, manufacturer procedures, professional survey judgement or local field validation.

## References and further reading

- [U.S. National Geodetic Survey: OPUS and improving GNSS solutions](https://www.ngs.noaa.gov/OPUS/about.jsp) — session duration, independent observations, antenna identification and solution diagnostics.
- [U.S. Geological Survey: Global Positioning System field procedures](https://water.usgs.gov/usgs/osw/gps/index.html) — static, RTK and PPK arrangements, carrier-phase equipment and height considerations.
- [Intergovernmental Committee on Surveying and Mapping: Guideline for Control Surveys by GNSS](https://icsm.gov.au/publications/guideline-control-surveys-gnss) — control-network design, observation redundancy, antenna setup and reference-frame considerations.
- [RICS: Guidelines for the use of GNSS in surveying and mapping](https://www.rics.org/content/dam/ricsglobal/documents/standards/guidelines_for_the_use_of_gnss_in_surveying_and_mapping_2nd_edition_rics.pdf) — planning, independent sessions and field records.

These references provide technical guidance from different jurisdictions. Their numeric specifications are not universal acceptance thresholds; apply the current governing specification for the project location and purpose.
