# Terrestrial laser scanning and point-cloud acquisition

> **Pillar:** Spatial Data Collection  
> **Subject:** SM-COL-008 — LiDAR and laser scanning  
> **Scope:** Static terrestrial laser scanning (TLS), scan planning, field acquisition, registration evidence, georeferencing and point-cloud quality  
> **Status:** Initial method synthesis; no instrument test or physical field campaign is claimed  
> **Connected subjects:** SM-COL-001 surveying; SM-COL-007 photogrammetry; SM-COL-009 UAV acquisition; SM-COL-010 mobile mapping; SM-ALG-016 point-cloud processing

## 1. What terrestrial laser scanning measures

A terrestrial laser scanner emits laser energy and records returns from surfaces within its field of view. Depending on the instrument architecture, it estimates range from pulse time-of-flight, phase shift, or another ranging principle, together with horizontal and vertical angular directions. These observations are transformed into 3D points in the scanner's local coordinate system. Some systems also record return intensity and co-registered RGB imagery.

A point cloud is a sampled measurement of visible surfaces, not a complete or neutral model of an object. It records only surfaces reached by the emitted energy and accepted by the sensor's detection and filtering chain. Occlusion, reflectance, incidence angle, range, beam divergence, atmospheric conditions, motion, scanner calibration and sampling configuration affect the result.

TLS is distinct from:
- **Mobile laser scanning (MLS):** the scanner moves through the environment and its trajectory and time synchronisation become part of the position solution.
- **Airborne laser scanning (ALS):** acquisition geometry, GNSS/INS trajectory, scan angle, footprint, pulse density and ground classification have platform-specific implications.
- **Photogrammetry:** 3D structure is inferred from image correspondences and camera geometry rather than direct laser range observations. The methods can complement one another but their observation models and failure modes differ.

This record focuses on static terrestrial systems. It does not prescribe a mobile mapping trajectory workflow or airborne LiDAR calibration and classification procedure.

## 2. Define the deliverable before choosing a scanner

Start with the intended use and the physical features that must be represented. Possible outputs include:
- a registered, georeferenced point cloud;
- building or infrastructure as-built records;
- topographic surfaces and breaklines;
- cross-sections, clearances and dimensions;
- deformation or change measurements;
- mesh, CAD or BIM geometry derived from the cloud;
- asset inventory and condition evidence;
- volume estimates and surface comparisons.

For each output, define:
- the measurand and physical feature boundary;
- the required coordinate reference system, datum, epoch and vertical reference;
- required absolute and relative positional quality;
- required completeness and minimum feature size;
- point spacing or density at the object surface, where relevant;
- allowable occlusion and shadow regions;
- intensity and colour requirements;
- temporal reference and whether moving objects must be retained or removed;
- independent validation method and acceptance criteria;
- deliverable format, coordinate units, metadata and archive requirements.

Do not treat a scanner's advertised range, single-point precision or angular resolution as a project accuracy specification. The complete workflow includes acquisition geometry, target/control survey, registration, georeferencing, filtering and validation.

## 3. Measurement geometry and sampling

A scanner measures polar or spherical observations and converts them to Cartesian coordinates. For a simplified local scanner frame with range \(r\), azimuth \(\theta\) and elevation angle \(\phi\), one convention is:

\[
x=r\cos\phi\cos\theta,\qquad
y=r\cos\phi\sin\theta,\qquad
z=r\sin\phi
\]

The exact axis and angle convention is instrument-specific. Verify the manufacturer's coordinate convention before interpreting exports or transformation matrices.

### 3.1 Angular sampling and point spacing

For small angular increments, approximate lateral point spacing on a surface perpendicular to the line of sight is:

\[
s \approx r\,\Delta\theta
\]

where \(r\) is range and \(\Delta\theta\) is the angular step in radians. This is an approximation: actual surface spacing depends on incidence angle and local surface orientation. For a plane viewed obliquely, the footprint and point spacing expand in the direction of incidence; grazing views can create large gaps and unstable returns.

Point density therefore depends on range, angular sampling, scan pattern, incidence angle, surface geometry, and the number and placement of scan stations. A nominal angular resolution does not imply uniform point spacing across a scene.

### 3.2 Beam footprint and mixed surfaces

The emitted beam has a finite divergence and illuminates a footprint that generally grows with range. If the footprint straddles an edge, a narrow object, vegetation or two surfaces at different depths, the returned range may be mixed, broadened or rejected. Small objects can be missed even when the nominal point spacing appears adequate.

A point cloud's apparent density should not be confused with the effective ability to resolve a feature. Plan station locations and scan settings around the smallest feature and surface detail that the deliverable must support.

### 3.3 Incidence, reflectance and range

Return quality varies with material, wavelength, surface roughness, moisture, colour, reflectance, incidence angle and range. Dark, wet, transparent, specular or highly oblique surfaces can yield weak, noisy, missing or misleading returns. Highly reflective surfaces can also create anomalous returns. Record relevant surface and environmental limitations rather than silently interpolating missing geometry.

## 4. Scan planning: coverage, registrability and validation

Plan the scan network before entering the field. Three quality dimensions should be considered together:

1. **Completeness:** Can the required surfaces and features be observed without unacceptable occlusion?
2. **Accuracy:** Can the required relative and absolute coordinate quality be achieved at the intended range and geometry?
3. **Registrability:** Will scans share enough stable, well-distributed overlap or targets to determine reliable transformations?

A station plan that maximises point count can still be poor if scans have weak overlap, targets are clustered, or key surfaces are observed at grazing incidence.

### 4.1 Station placement

1. Map the area, access restrictions, hazards, likely occluders and required deliverable features.
2. Select candidate scanner positions that provide complementary views of critical surfaces.
3. Avoid relying on one scan for hidden faces, corners, undersides or narrow spaces.
4. Use overlap that includes distinctive, stable 3D geometry; avoid overlap consisting only of a large featureless plane or repetitive structure.
5. Place scan stations so that control and tie targets are visible from multiple stations with useful spatial distribution.
6. Keep stations within the scanner's useful range for the required task, not merely its maximum advertised range.
7. Include independent check-point visibility and enough geometry to inspect local as well as global fit.
8. Plan repeat scans or alternative views for critical or difficult surfaces.

### 4.2 Target and control design

Targets can support scan-to-scan registration, georeferencing or independent validation, but these are different roles.

- **Registration targets/tie features** constrain transformations between scans.
- **Control points** connect the registered cloud to the project coordinate reference.
- **Independent check points** assess the final result and must not be used to determine the transformation being evaluated.

Distribute targets in 3D and across the scene. Avoid a nearly collinear or tightly clustered arrangement. A single plane or a set of targets with poor geometric distribution can leave some transformation components weakly determined. Include vertical diversity and spatial extent appropriate to the site.

Survey target centres or check features with a method whose uncertainty is suitable for the point-cloud requirement. Record target identity, physical description, centre definition, survey method, coordinates, covariance/quality, instrument and reference frame. Reserve a separate check set before registration; do not promote control residuals into independent accuracy evidence.

## 5. Field acquisition procedure

### 5.1 Pre-field checks

1. Confirm the project brief, required quality, scan plan, access and safety controls.
2. Check scanner make/model, serial number, firmware, battery, tripod/tribrach, levelling system and ancillary imaging.
3. Review calibration/verification records and perform task-appropriate field checks.
4. Confirm angular resolution, scan pattern, range mode, quality filters, intensity and RGB settings, coordinate convention, units and file format.
5. Verify storage capacity, clock synchronisation, project naming, station identifiers and data backup procedure.
6. Inspect target equipment and ensure targets are stable, correctly identified and observable from planned stations.
7. Record environmental conditions and surfaces likely to affect ranging.

### 5.2 At each scan station

1. Set up on a stable support and level/centre the instrument as required by its design.
2. Record station ID, instrument ID, setup location, height/reference information if relevant, time, operator and environmental conditions.
3. Capture the planned scan resolution and field of view; do not reduce settings without recording the change and its impact.
4. Capture sufficient overlap with neighbouring scans and observe planned registration targets or stable tie features.
5. Inspect the scan in the field for occlusions, missing surfaces, range noise, moving objects, weak returns and target visibility.
6. Add supplementary stations where required; do not assume registration software can reconstruct surfaces never observed.
7. Capture RGB imagery only when lighting, exposure and camera-to-scanner calibration support the intended colour use.
8. Preserve native scanner files and associated images, project files, logs and configuration exports.

### 5.3 Field completeness check

Before leaving the site, compare observed coverage against the feature list and scan plan. Identify unobserved surfaces and inaccessible regions. Record whether each omission is acceptable, requires another station, or must be explicitly excluded from the deliverable.

Do not fill substantial occlusions with smooth interpolation and then present the result as measured geometry. Any reconstructed or modelled surfaces must be separately labelled and traceable to their derivation.

## 6. Registration and georeferencing

Registration aligns individual scans into a common coordinate system. It is a computational estimation step that contributes additional uncertainty; it is not a trivial file-merging operation.

### 6.1 Registration approaches

Common strategies include:
- target-based registration using surveyed or scanner-observed targets;
- cloud-to-cloud registration using corresponding surface geometry;
- feature-based coarse alignment followed by local refinement;
- hybrid registration combining control targets and cloud geometry;
- network adjustment across multiple scans rather than independent pairwise alignment alone.

The appropriate method depends on scene geometry, overlap, target availability, initial alignment, symmetry, movement and required quality.

### 6.2 Rigid transformation model

For a point \(\mathbf{x}_i\) in a scanner-local frame, a rigid transformation into a project frame is:

\[
\mathbf{X}_i=\mathbf{R}\mathbf{x}_i+\mathbf{t}
\]

where \(\mathbf{R}\) is a proper rotation matrix and \(\mathbf{t}\) is a translation vector. A rigid transform preserves lengths and angles. A similarity transform additionally includes a scale parameter, but scale should not be introduced merely to reduce residuals when the instrument's scale is physically defined and the project expects metric coordinates.

For row-vector implementations, the equivalent expression may be \(\mathbf{X}=\mathbf{x}\mathbf{R}+\mathbf{t}\). Confirm the convention and multiplication order when transferring transforms between software packages.

### 6.3 ICP and local refinement

Iterative closest point (ICP) alternates between correspondence assignment and transform estimation. It is a local optimisation method: a plausible initial alignment, adequate overlap and sufficiently distinctive geometry are required. Symmetry, repetitive structures, moving objects, poor normals, planar geometry and outliers can produce a low-residual but incorrect local solution.

The repository's [point-cloud registration algorithm](../algorithms/geometry/point-cloud-registration.md) and [Python implementation](../implementations/python/point-cloud-registration/README.md) include point-to-point, point-to-plane, generalized ICP and a bounded normal-distributions-transform baseline. These are computational methods, not automatic guarantees of correct field registration.

Do not use the same cloud-to-cloud residual both to optimise a registration and as the sole independent validation of that registration.

### 6.4 Registration network design and diagnostics

Prefer a connected scan network with loops and redundant links over a long chain of pairwise registrations. A loop provides a way to inspect accumulated inconsistency, although loop closure does not alone prove absolute correctness.

Retain:
- scan-to-scan transformations and their conventions;
- target identities and target residuals;
- overlap regions and correspondence rules;
- registration sequence, software/version and parameters;
- per-pair and global residual summaries;
- rejected targets/correspondences and reasons;
- loop-closure or network consistency diagnostics;
- control constraints and independent check results.

Inspect residuals spatially. A single global RMSE can conceal local deformation, systematic drift, poor geometry or a cluster of bad correspondences.

## 7. Quality assessment and acceptance

Quality is multidimensional. Define thresholds before acquisition and interpret each statistic according to what it measures.

| Quality dimension | Evidence | What it does not establish alone |
|---|---|---|
| Scanner repeatability | Task-specific field verification and repeated observations | End-to-end project accuracy |
| Range/angle behaviour | Instrument tests and reference artefacts/known geometry | Correct scan registration or georeferencing |
| Registration fit | Target residuals, overlap residuals, network consistency | Absolute coordinate accuracy |
| Absolute accuracy | Independent surveyed check points not used in adjustment | Completeness or correct semantic interpretation |
| Relative accuracy | Independent distances, planes, sections or local geometry checks | Correct external datum |
| Completeness | Feature-by-feature coverage review, occlusion maps and scan plan comparison | Positional accuracy |
| Point spacing/density | Surface-specific spacing and density summaries | Ability to resolve every feature or meet accuracy |
| Surface quality | Noise, outlier, incidence and reflectance diagnostics | Truth of derived CAD/BIM geometry |
| Temporal stability | Repeat observations and stable reference control | Sensor calibration unless separately tested |

For independent checkpoints with reference coordinates \(\mathbf{X}_i\) and cloud-derived coordinates \(\hat{\mathbf{X}}_i\), coordinate residuals are:

\[
\mathbf{e}_i=\hat{\mathbf{X}}_i-\mathbf{X}_i
\]

Component biases and RMSE values can be summarised, for example:

\[
RMSE_X=\sqrt{\frac{1}{n}\sum_{i=1}^{n} e_{X,i}^{2}}
\]

\[
RMSE_{3D}=\sqrt{\frac{1}{n}\sum_{i=1}^{n}
\left(e_{X,i}^{2}+e_{Y,i}^{2}+e_{Z,i}^{2}\right)}
\]

Report sample size, checkpoint distribution, reference uncertainty, coordinate system, axis-specific bias, outliers and the method used to obtain cloud coordinates at check locations. The reference check uncertainty must be small enough for the intended assessment. Do not subtract reference uncertainty mechanically unless the uncertainty model and independence assumptions justify it.

A cloud-to-cloud distance statistic is not equivalent to checkpoint accuracy. Nearest-neighbour distances are sensitive to density, surface orientation, roughness and correspondence choice. For deformation/change analysis, establish stable reference control, comparable acquisition geometry, registration strategy and a change-detection uncertainty model.

## 8. Processing and point-cloud preparation

Keep raw scanner data immutable. Derived processing should be versioned and reproducible.

A defensible sequence may include:
1. ingest native scans and validate file integrity;
2. retain station metadata, scanner configuration and raw observations;
3. identify and register targets or establish coarse scan alignment;
4. solve scan-network registration and inspect residuals;
5. georeference to project control using the stated reference frame;
6. evaluate independent check points;
7. classify or remove noise and moving objects with explicit rules;
8. generate derived products such as subsets, sections, meshes, surfaces or BIM geometry;
9. inspect each product against the source cloud and independent evidence;
10. package deliverables, metadata, transformations, QA reports and archive copies.

Filtering is an interpretation step. Keep an unfiltered or minimally processed source cloud and document the effect of each filter. Do not remove points solely because they disagree with a design model if the purpose is to detect construction deviations.

The [point-cloud voxelization implementation](../implementations/python/point-cloud-voxelization/README.md) provides grid indexing and aggregation, not a substitute for raw-data archiving or a sensor-specific noise model. The [RANSAC plane-fitting implementation](../implementations/python/ransac-plane-fitting/README.md) and [progressive morphological filter](../implementations/python/progressive-morphological-filter/README.md) are bounded examples for specific geometric fitting and ground-filtering tasks; neither is a universal semantic classifier.

## 9. Data and provenance model

At project level, preserve:
- project ID, study boundary, intended use and acceptance plan;
- coordinate reference system, datum realisation, epoch, vertical datum and units;
- instrument make/model, serial, firmware, verification and calibration evidence;
- scanner configuration, angular sampling, range mode, filters and colour settings;
- operator, station IDs, timestamps, setup information and environmental notes;
- native scan files, images, logs, checksums and storage locations;
- target/control/check-point identities, coordinates, uncertainties and roles;
- registration graph, transformations, parameter sets, residuals and rejected observations;
- georeferencing constraints and coordinate operations;
- filtering, classification, decimation, voxelization and derived-product history;
- independent validation results, completeness report and acceptance decision;
- software versions, export settings, file formats and archive checksums.

Maintain clear distinctions between raw scans, registered scans, georeferenced point clouds, cleaned/classified clouds and derived surfaces/models. Each derived product should retain lineage to its source scans and processing configuration.

## 10. Physical-world applications

Static TLS is useful for building and infrastructure documentation, heritage recording, industrial plant measurement, tunnels and underground spaces, construction progress/as-built checks, deformation monitoring, quarry faces, stockpiles, road corridors from static setups, and complex terrain or structures where line-of-sight scanning is practical.

Method choice remains task-dependent. GNSS and total-station control may establish the reference network; TLS supplies dense visible-surface geometry; photogrammetry may add texture and complementary coverage; mobile mapping may be more efficient for long corridors; airborne LiDAR may cover broad terrain. Combining sensors is valuable only when coordinate frames, timing, control, uncertainty and validation are managed coherently.

## 11. Connections within Spatial Methods

- [Terrestrial surveying: total station and differential levelling](terrestrial-surveying-total-station-and-levelling.md) — control, reference, field checks and independent survey observations.
- [GNSS positioning and navigation observation](gnss-positioning-and-navigation-observation.md) — geodetic control and reference-frame context.
- [Photogrammetric image acquisition](photogrammetry/image-acquisition.md) — complementary image-based 3D observation with a different measurement model.
- [Point-cloud registration and geometric comparison](../algorithms/geometry/point-cloud-registration.md) — ICP, GICP, NDT and geometric comparison methods.
- [Point-cloud registration implementation](../implementations/python/point-cloud-registration/README.md) — bounded registration baselines.
- [Point-cloud voxelization](../implementations/python/point-cloud-voxelization/README.md) — point aggregation and spatial reduction.
- [Survey-to-spatial-dataset workflow](../recipes/survey-to-spatial-dataset/README.md) — field-to-office provenance, independent checks and delivery.

## 12. Standards and further reading

- [ISO 17123-9:2018 — Field procedures for testing terrestrial laser scanners](https://www.iso.org/standard/68382.html). It specifies field procedures for evaluating scanner precision/repeatability and suitability for an immediate task. It is not a complete project acceptance or end-to-end accuracy assessment.
- [ISO/CD 17123-9 (2026) — revision under development](https://www.iso.org/standard/91344.html). The committee draft is under development and is not a published replacement standard; consult the published edition and applicable national adoption until the status changes.
- [DVW Guideline 18-2022 — TLS point-cloud registration](https://dvw.de/api/assets/downloads/ev/publikationen/merkblatter/18_23_dvwguideline18tlspointcloudregistration20230424.pdf). Discusses scan acquisition, registration methods, uncertainty contributions and quality evaluation.
- [Hong Kong Lands Department, Engineering Survey Practice Guides (2025), Chapter 15: Laser Scanning Survey](https://www.landsd.gov.hk/doc/en/survey-mapping/Survey-related-guides-specifications/ESPG_2025_Edition.pdf). A detailed agency guide covering TLS concepts, control, tie points, check points, acquisition and deliverables; its jurisdiction-specific requirements should not be transplanted uncritically.
- [Archaeology Data Service: Scan data acquisition and processing](https://archaeologydataservice.ac.uk/help-guidance/guides-to-good-practice_old/data-collection-and-fieldwork/laser-scanning-for-archaeology/acquiring-and-processing-laser-scan-data/scan-data-lifecycle/). Guidance on acquisition metadata, registration, transformations and derived products.
- [Aryan, Bosché and Tang (2021), Planning for terrestrial laser scanning in construction](https://doi.org/10.1016/j.autcon.2021.103551). Reviews scan planning around completeness, accuracy/spatial resolution and registrability.

For actual work, identify the current national and project specifications, instrument manuals, professional requirements and safety controls. In Kenya, verify applicable surveying, access, occupational-safety and project requirements before approving field procedures.

