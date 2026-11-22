# Mobile laser scanning and kinematic point-cloud acquisition

> **Pillar:** Spatial Data Collection  
> **Subject:** SM-COL-010 — Mobile mapping and indoor positioning; connected to SM-COL-008 LiDAR and laser scanning  
> **Scope:** Kinematic laser scanning from moving ground platforms, including vehicle-based and pedestrian/backpack systems where a time-resolved navigation solution is available  
> **Status:** Initial method synthesis; no platform calibration, trajectory test or physical field campaign is claimed  
> **Related methods:** [Static terrestrial laser scanning](terrestrial-laser-scanning-and-point-cloud-acquisition.md); [GNSS positioning and navigation observation](gnss-positioning-and-navigation-observation.md); [terrestrial surveying](terrestrial-surveying-total-station-and-levelling.md)

## 1. What changes when the scanner moves?

Mobile laser scanning (MLS) records range and scan direction while the scanner platform moves. Unlike static terrestrial laser scanning, every laser observation must be related to the position and orientation of the platform at the observation epoch. A georeferenced point therefore depends on a synchronised chain of sensor measurements and coordinate transformations.

A typical survey-grade system combines:
- one or more LiDAR scanners;
- a GNSS receiver and antenna, often with access to one or more reference stations or correction services;
- an inertial measurement unit (IMU);
- a navigation/trajectory estimator that fuses GNSS and inertial observations;
- a common time base and event/measurement synchronisation;
- calibrated lever arms and boresight rotations between sensor frames;
- sometimes wheel odometry, cameras, radar, SLAM sensors or additional aiding.

Not every mobile mapping system uses the same architecture. Some systems are designed for outdoor GNSS-aided corridors; others target indoor or GNSS-denied environments and rely on SLAM, wheel odometry, visual-inertial navigation or control constraints. The system architecture must be known before its point cloud can be interpreted.

This method is about the kinematic acquisition and georeferencing chain. It does not replace static TLS, a GNSS field procedure, an IMU calibration specification or a mobile mapping platform's safety and operational manual.

## 2. Define the corridor or environment deliverable

Specify the intended use before choosing a platform or route:
- road and rail asset inventory, clearance and condition assessment;
- streetscape, kerb, pavement and roadside feature mapping;
- utility corridor and infrastructure documentation;
- indoor facilities, tunnels, stations and industrial spaces;
- urban digital twins and 3D base mapping;
- repeat surveys and change/deformation assessment.

Define the deliverable's coordinate reference system, datum realisation, epoch, vertical datum, units, required absolute and relative accuracy, point density, feature completeness, classification scheme, intensity/colour requirements, occlusion tolerance, temporal coverage and independent validation design.

Specify the corridor width and height envelope, access restrictions, traffic management, speed limits, platform path, GNSS visibility, likely multipath and outage zones, safe stopping locations, required passes and cross-check geometry. A single drive-through may not see façades, road edges, overhead assets or surfaces hidden by parked vehicles and vegetation.

## 3. Kinematic observation and georeferencing model

Let:
- \(t\) be the laser observation epoch in the project time scale;
- \(\mathbf{x}^{s}\) be a measured point in the scanner frame, derived from range and scan angles;
- \(R_s^b\) be the calibrated rotation from scanner frame \(s\) to platform/body frame \(b\);
- \(\mathbf{l}_{I\rightarrow S}^{b}\) be the calibrated lever-arm vector from the navigation IMU origin \(I\) to the scanner origin \(S\), expressed in body frame \(b\);
- \(R_b^E(t)\) be the platform/body-to-earth-fixed rotation at epoch \(t\);
- \(\mathbf{r}_I^E(t)\) be the earth-fixed position of the IMU origin at epoch \(t\).

A simplified georeferencing equation is:

\[
\mathbf{X}^{E}(t)=\mathbf{r}_{I}^{E}(t)+
R_b^E(t)\left[
\mathbf{l}_{I\rightarrow S}^{b}+R_s^b\mathbf{x}^{s}
\right]
\]

This equation assumes the stated frame directions, a rigid platform and a consistent rotation convention. Production implementations must explicitly document axis order, handedness, rotation order, units, coordinate frame realisation and whether matrices act on column or row vectors. Some systems use navigation frames such as NED or ENU internally and require a further transformation to the project frame.

The scanner point \(\mathbf{x}^{s}\) is itself obtained from range and scanner angles. For example, with one spherical convention:

\[
\mathbf{x}^{s}=
\begin{bmatrix}
r\cos\phi\cos\theta\\
r\cos\phi\sin\theta\\
r\sin\phi
\end{bmatrix}
\]

The scanner's actual angle convention and scan mechanism must be read from its specification. The point must be transformed using the platform pose at the laser measurement epoch, not the nearest GNSS fix or a generic timestamp rounded to a whole second.

### 3.1 Timing is a geometric parameter

A timing offset between the scanner and navigation solution causes a position and orientation mismatch. For a moving platform, even a small offset can displace points along the direction of travel; angular motion can create larger errors at distant surfaces.

Record:
- sensor clock sources and time scales;
- synchronisation mechanism (for example hardware pulse, PTP or another documented protocol);
- timestamp semantics (pulse emission, return, scan line, packet or frame time);
- latency and any measured or estimated time offsets;
- interpolation method for position and attitude;
- dropped, duplicated, reordered or delayed packets;
- time conversion, leap-second and GNSS week handling where applicable.

Estimate or verify time offsets using suitable calibration manoeuvres and overlapping observations. Do not treat software receipt time as measurement time unless the system explicitly defines and validates that relationship.

### 3.2 Lever arms and boresight

A lever arm is a physical translation between reference points, such as the IMU origin, GNSS antenna phase centre and scanner origin. Boresight is the angular misalignment between sensor coordinate frames. Both affect every transformed point.

Maintain a frame diagram and calibration record showing:
- reference origin and axes for every sensor;
- measured or estimated lever arms and their uncertainty;
- rotation direction and parameterisation for every boresight;
- antenna phase-centre conventions and antenna reference point;
- calibration date, method, equipment configuration and validity conditions;
- whether mounts, brackets, scanners, antennas or IMUs were moved or reinstalled.

A calibration belongs to a particular physical system configuration. Disassembly, impact, mount changes, sensor replacement or unexplained strip misalignment should trigger review and potentially a new calibration.

## 4. Trajectory estimation

The trajectory is the time series of platform position and attitude used to georeference each laser observation. A common architecture fuses GNSS position/velocity information with IMU angular-rate and specific-force observations using a Kalman filter or related estimator. GNSS constrains long-term position and drift; inertial measurements provide high-rate motion information between GNSS updates. Wheel odometry, visual or LiDAR SLAM, barometric height and control observations may provide additional constraints.

Trajectory quality depends on satellite geometry, multipath, obstruction, correction data, reference-station geometry, IMU grade and calibration, platform dynamics, initialisation, outages, aiding sensors and estimator design. GNSS-denied segments can exhibit growing position and attitude error; the size and rate of degradation are system- and environment-dependent.

### 4.1 Mission planning and reference support

For outdoor corridors:
1. Review GNSS visibility, nearby buildings, bridges, tree canopy, tunnels and likely multipath.
2. Select suitable base/reference stations or correction services and document their coordinates, datum, epoch and observation quality.
3. Plan initialisation and any static alignment periods required by the platform.
4. Define route direction, speed, lane/path, overlap, return passes and safe locations for interruptions.
5. Identify areas where GNSS will degrade and plan alternative aiding or independent control.
6. Ensure the route is long enough and geometrically diverse enough for the intended trajectory and calibration checks.
7. Include repeated or cross-direction passes where they provide meaningful independent geometry.

For indoor or GNSS-denied operation, explicitly describe the navigation solution: LiDAR SLAM, visual-inertial odometry, wheel encoders, surveyed control, loop closures or hybrid constraints. A SLAM map may be locally consistent without being tied to an external datum. Absolute georeferencing requires external control or another defensible reference.

### 4.2 Forward, reverse and smoothed solutions

Where supported, process raw GNSS and IMU data with a documented forward and backward or smoothed trajectory solution. Compare trajectory quality indicators and inspect outage recovery, attitude behaviour, velocity, residuals and covariance. A smoothed solution can improve estimates using observations from both temporal directions, but it does not repair unmodelled sensor offsets, poor calibration or incorrect time alignment.

Preserve raw GNSS, IMU, wheel/odometry and auxiliary sensor observations as well as the processed trajectory. A final point cloud without its trajectory and calibration provenance is difficult to audit or reprocess.

## 5. Acquisition procedure

### 5.1 Before mobilisation

1. Confirm deliverables, coordinate reference, accuracy, completeness and independent validation requirements.
2. Confirm platform configuration, scanner count and mounting geometry, IMU, GNSS antenna, odometry and auxiliary sensors.
3. Review calibration certificates and verify lever arms, boresight and time synchronisation for the installed configuration.
4. Check navigation firmware/software, GNSS correction source, base/reference station plan, data rates and storage.
5. Verify scanner settings: field of view, scan rate, angular sampling, range mode, return selection, intensity and colour capture.
6. Review route access, traffic/pedestrian management, weather, lighting and operational safety.
7. Define naming, timestamps, route IDs, pass IDs, raw-data backup and processing logs.

### 5.2 Field run

1. Install and secure the complete sensor package; record any configuration change.
2. Complete required static initialisation and calibration manoeuvres.
3. Confirm common time synchronisation and inspect live sensor health.
4. Run the planned route at the specified speed and path while recording raw scanner and navigation observations.
5. Monitor GNSS quality, IMU status, trajectory warnings, packet loss, scanner returns, temperature and storage.
6. Record stops, sharp turns, reversing, speed changes, GNSS outages, occlusions and unusual platform motion.
7. Acquire planned return/cross passes and independent control/check observations.
8. Repeat calibration or verification observations after a configuration disturbance or where the system specification requires them.
9. Back up raw observations and verify checksums before leaving the site.

### 5.3 Corridor completeness

Review coverage by feature and by route segment. Record blind zones behind vehicles, vegetation, street furniture, bridge decks, building recesses and overhead structures. Plan multiple scanner orientations or passes where needed. A moving platform may produce dense roadside coverage but still miss surfaces hidden from its path.

## 6. Calibration and geometric quality control

A robust calibration/verification programme addresses at least:
- GNSS antenna to IMU lever arm;
- IMU to scanner lever arm;
- scanner-to-body boresight;
- sensor clock offset and latency;
- scanner range and angular behaviour;
- GNSS antenna reference/phase-centre conventions;
- odometry scale and alignment if used;
- camera-to-navigation calibration if imagery is co-registered.

Use a suitable calibration site or route with stable surfaces and features observed from different directions and orientations. Parallel, opposing and cross-direction passes can expose angular and timing misalignment. A calibration should be estimated using appropriate observations and then evaluated using independent geometry or checkpoints.

Inspect:
- double surfaces and edge ghosting;
- vertical and horizontal strip offsets;
- discrepancies between forward/reverse or cross-direction passes;
- systematic residual patterns with scan angle, range, time or vehicle attitude;
- trajectory jumps, drift and outage recovery;
- changes in residuals before and after calibration.

Do not hide a trajectory or calibration problem by independently warping each strip to fit the nearest surface. Where control observations are used, incorporate them through a documented estimation model or rigorously constrained adjustment, and preserve the original trajectory and correction parameters.

## 7. Strip alignment, control and independent checks

A strip is a point-cloud segment acquired during a pass or trajectory interval. Compare overlapping strips on stable surfaces and features. Strip adjustment can help estimate systematic discrepancies, but it must not obscure the distinction between:
- sensor calibration parameters;
- trajectory errors;
- control-network errors;
- local surface change or moving objects;
- point correspondence and surface-modelling errors.

Use surveyed control and independent check points with different roles. Control can constrain the trajectory or adjustment. Check points must remain excluded from those constraints if they are to provide independent validation. Distribute checks along the route and across the corridor, including locations with different GNSS conditions and viewing geometry.

A low strip-to-strip residual is not proof of absolute positional accuracy: strips can agree with each other and still be displaced together. Conversely, a large residual can arise from moving objects, vegetation, incidence-angle effects or genuine surface change rather than only navigation error.

Report coordinate biases and RMSE by axis, 3D residuals, sample size, checkpoint distribution, reference uncertainty and the applicable acceptance criteria. Also report completeness, density, strip consistency and trajectory quality. Do not collapse these into a single accuracy number.

## 8. Processing workflow

1. Ingest and checksum raw scanner, GNSS, IMU, odometry and auxiliary sensor files.
2. Validate timestamps, time systems, sensor packet continuity and configuration metadata.
3. Process the navigation solution with documented reference data and estimator settings.
4. Apply the calibrated lever arms, boresight and time alignment.
5. Transform each laser observation using the interpolated trajectory at its acquisition epoch.
6. Inspect trajectory and point-cloud strip consistency before any geometric correction.
7. If justified, perform a documented trajectory/strip adjustment with explicit constraints and uncertainty assumptions.
8. Evaluate independent checkpoints and surface-specific quality.
9. Classify, filter and derive products while preserving raw and intermediate point clouds.
10. Package point clouds, trajectory, calibration, processing reports, validation, metadata and provenance.

Do not treat SLAM loop closure or strip adjustment as independent external accuracy validation. Keep raw sensor observations and the unadjusted trajectory to allow reprocessing.

## 9. Failure modes and diagnostic signatures

| Failure mode | Possible manifestation | Required response |
|---|---|---|
| GNSS multipath/outage | Drift, jumps, poor absolute position, local strip displacement | Inspect trajectory and GNSS quality; use appropriate aiding/control or reacquire |
| IMU drift or poor initialisation | Growing attitude/position error, especially through outages | Review sensor grade, alignment, outage duration and estimator |
| Lever-arm error | Position-dependent systematic offsets as platform attitude changes | Verify physical offsets and reference origins |
| Boresight error | Strip divergence varying with scan direction/angle; doubled edges | Recalibrate and verify independent geometry |
| Time offset/latency | Along-track displacement and motion-dependent distortion | Verify timestamp semantics, clock synchronisation and latency |
| Wheel odometry scale error | Distance-dependent along-track drift | Calibrate wheel scale and check slip/turning effects |
| Weak strip geometry | Unstable adjustment, unobservable parameters | Add cross passes, control and diverse stable surfaces |
| Moving objects | Ghosts, duplicated vehicles/pedestrians, false change | Classify dynamic objects and define temporal filtering |
| GNSS-denied indoor SLAM drift | Locally coherent map with global deformation or arbitrary datum | Add control/loop constraints; assess global consistency independently |
| Poor point correspondence | False strip alignment or local surface deformation | Restrict to stable surfaces and inspect residuals spatially |

## 10. Data and provenance requirements

Retain:
- project, route, corridor and pass identifiers;
- platform type, make/model, configuration and mounting diagrams;
- scanner, GNSS, IMU, odometer and camera IDs and firmware;
- raw measurements and checksums;
- time base, synchronisation method, clock offsets and latency;
- calibration parameters, covariance/quality, date and verification evidence;
- GNSS reference stations, correction source, antenna details and datum;
- processed trajectory, covariance/quality indicators and processing settings;
- point-cloud generation and strip-adjustment parameters;
- control/check-point coordinates, uncertainties and roles;
- processing software, version, filters and classification history;
- strip diagnostics, completeness review and independent validation;
- export format, coordinate metadata and archive lineage.

Distinguish raw scans, trajectory-georeferenced strips, adjusted strips, merged clouds, filtered/classified clouds and derived surfaces. Record each transformation and processing decision.

## 11. Physical-world applications and platform selection

MLS is particularly useful for road and rail corridors, urban streetscapes, roadside assets, utilities, tunnels, indoor facilities and large industrial spaces where rapid acquisition from a moving platform is advantageous.

Platform choice changes the collection design:
- **Vehicle MLS:** efficient for road corridors and roadside features, but vulnerable to GNSS blockage, traffic, mounting vibration and occlusion.
- **Backpack/pedestrian systems:** useful for indoor and pedestrian environments, often with SLAM or hybrid navigation; trajectory drift and external datum control need explicit treatment.
- **Rail-based systems:** benefit from constrained path geometry but still require trajectory, timing, calibration and independent checks.
- **Handheld systems:** flexible for confined spaces but require careful motion tracking, operator technique and coverage verification.

For broad-area terrain or vegetation mapping, airborne or UAV LiDAR may be more suitable. For detailed stationary scenes, TLS may be more suitable. These methods can complement one another if their reference frames, epochs, control and uncertainty are reconciled.

## 12. Connections within Spatial Methods

- [Static terrestrial laser scanning and point-cloud acquisition](terrestrial-laser-scanning-and-point-cloud-acquisition.md) — static scan geometry, overlap, target control and independent checks.
- [GNSS positioning and navigation observation](gnss-positioning-and-navigation-observation.md) — satellite observables, reference frames, correction and field quality.
- [Terrestrial surveying: total station and differential levelling](terrestrial-surveying-total-station-and-levelling.md) — control networks and independent survey checks.
- [Point-cloud registration and geometric comparison](../algorithms/geometry/point-cloud-registration.md) — local registration and geometric diagnostics.
- [Survey-to-spatial-dataset workflow](../recipes/survey-to-spatial-dataset/README.md) — traceable acquisition-to-delivery framework.

## 13. Standards and technical references

- [Queensland Department of Transport and Main Roads — Mobile Laser Scanning Guideline (March 2023)](https://www.tmr.qld.gov.au/~/media/busind/techstdpubs/Surveying/Surveying%20support%20documents/MLS%20Guideline/MLSGuideline.pdf). Agency guidance for mobile laser scanning, including system configuration, boresight calibration and point-cloud requirements. Its project requirements are jurisdiction-specific.
- [NCHRP 15-44 — Guidelines for the Use of Mobile LiDAR in Transportation Applications](https://onlinepubs.trb.org/onlinepubs/nchrp/docs/nchrp15-44_finalguidelines.pdf). Technical guidance on MLS calibration, lever arms, boresight, trajectory correction and transportation applications.
- [Pöppl et al. (2024), A flexible trajectory estimation methodology for kinematic laser scanning](https://doi.org/10.1016/j.isprsjprs.2024.06.014). Research on GNSS/IMU-supported trajectory estimation for moving laser scanners.
- [Rigorous Boresight Self-Calibration of Mobile and UAV LiDAR Scanning Systems by Strip Adjustment (2019)](https://www.mdpi.com/2072-4292/11/4/442). Research on joint boresight calibration and strip adjustment.
- [ISO/TS 19159-2:2016 — Lidar systems calibration and validation](https://www.iso.org/standard/629 ಮತ್ತೆ.html). Consult the official ISO catalogue for current status, amendments and applicable adoption before specifying a project requirement.

The above sources inform the method but do not establish a universal acceptance specification. Confirm current national, client and professional requirements, platform manuals, safety procedures and local reference-frame requirements before field execution. In Kenya, verify applicable surveying, road-access, traffic-management and occupational-safety requirements.

