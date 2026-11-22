# Spatial Data Collection

Spatial Data Collection explains how information about the world is observed, measured, sampled, sensed, recorded and acquired.

It covers more than sensors or platforms. A collection method includes the physical quantity or phenomenon being observed, the measurement process, sampling geometry, instrument and platform behaviour, calibration, field conditions, metadata, uncertainty and quality control.

## Connect collection to analysis and application

The [cross-pillar pathway index](../learning-paths/cross-pillar-pathways.md) shows how observations and measurement systems connect to their theoretical basis, computational methods and reproducible workflows.

## Subject domains

The stable subject identities are defined in the [Geoinformatics master subject index](../catalog/master-subject-index.md).

| Subject | ID | Entry point |
|---|---|---|
| Geodetic and engineering surveying | SM-COL-001 | [Terrestrial surveying: total station and differential levelling](terrestrial-surveying-total-station-and-levelling.md); [Measurement science and survey adjustment](../learning-paths/measurement-science-and-survey-adjustment.md) |
| GNSS, positioning and navigation systems | SM-COL-002 | [GNSS positioning and navigation observation](gnss-positioning-and-navigation-observation.md); [GNSS methods and implementations](../catalog/first-curation-cluster-reference-positioning-measurement.md#3-gnss-scope-boundaries-to-preserve) |
| Satellite and airborne optical remote sensing | SM-COL-004 | [Optical satellite imagery acquisition](optical-satellite-imagery-acquisition.md) |
| Radar, SAR and interferometric sensing | SM-COL-006 | [SAR acquisition and observation design](sar-acquisition-and-observation-design.md) |
| Photogrammetry and structure from motion | SM-COL-007 | [Photogrammetric image acquisition](photogrammetry/image-acquisition.md) |
| LiDAR and laser scanning | SM-COL-008 | [Terrestrial laser scanning and point-cloud acquisition](terrestrial-laser-scanning-and-point-cloud-acquisition.md); [Point-cloud registration algorithm](../algorithms/geometry/point-cloud-registration.md) |
| UAV platforms, robotics and autonomous acquisition | SM-COL-009 | [Photogrammetric image acquisition](photogrammetry/image-acquisition.md) |
| Field surveys, sampling and ground truth | SM-COL-011 | [Spatial observation and sampling design](spatial-observation-and-sampling-design.md); [practical sampling campaign exercise](spatial-observation-sampling-exercise.md) |

This is an initial navigation page, not a claim that every collection domain has been comprehensively curated. The subject index remains the complete taxonomy.

## LiDAR and laser scanning

LiDAR and laser scanning (SM-COL-008) now has an initial [terrestrial laser scanning and point-cloud acquisition method](terrestrial-laser-scanning-and-point-cloud-acquisition.md). It covers static TLS measurement geometry, scan planning, completeness and registrability, target/control/check-point roles, field acquisition, registration, georeferencing, independent quality assessment and provenance. It is explicitly separate from mobile and airborne LiDAR, which require their own platform and trajectory models.

## Terrestrial surveying

Geodetic and engineering surveying (SM-COL-001) now has an initial [total-station and differential-levelling observation method](terrestrial-surveying-total-station-and-levelling.md). It connects angular and EDM observations, station orientation, instrument/target heights, traverse design, differential height transfer, closure, field checks and provenance to the measurement-science and network-adjustment material. It is a method synthesis, not a substitute for instrument-specific procedures, current local standards or project acceptance criteria.

## GNSS positioning and navigation

GNSS positioning (SM-COL-002) now has an initial [positioning and navigation observation method](gnss-positioning-and-navigation-observation.md). It distinguishes code and carrier-phase observables, static and kinematic positioning modes, reference-frame and height handling, field occupation records, independent checks and quality acceptance. It is a technology-aware collection method, not a claim that receiver precision or a fixed RTK status proves survey accuracy. Local control specifications and field validation remain necessary.

## Remote-sensing collection route

Satellite and airborne optical remote sensing (SM-COL-004) has an initial [optical satellite imagery acquisition method](optical-satellite-imagery-acquisition.md). It establishes observation design, product selection, discovery, quality screening, asset access and provenance, using Sentinel-2 as a bounded reference. Technical review and application testing remain pending.

Earth-observation SAR (SM-COL-005) now has an initial [SAR acquisition and observation design method](sar-acquisition-and-observation-design.md). It distinguishes detected GRD, phase-preserving SLC and derived RTC products; specifies acquisition geometry and temporal compatibility; and defines discovery, metadata, quality and provenance gates. Technical review and scene execution remain pending. SAR acquisition is deliberately separate from optical acquisition.

The [remote-sensing cross-pillar pathway](../learning-paths/remote-sensing-cross-pillar-pathway.md) connects both branches while preserving their different measurement and processing requirements.

## How to investigate a collection method

A good collection account answers:

1. What real-world quantity, object or phenomenon is being observed?
2. What physical interaction produces the recorded signal?
3. What does the instrument measure directly, and what is inferred later?
4. How do platform motion, geometry, environment and sampling design affect observations?
5. What calibration, control, metadata and quality checks are required?
6. What uncertainty and blind spots remain?
7. What downstream products can reasonably be derived?

Connect collection methods to their theoretical foundations, algorithms, reproducible recipes and applications. Do not treat a data product as a transparent copy of reality: every observation is shaped by a measurement system and a collection design.

## Development status

The first focused collection unit is [photogrammetric image acquisition](photogrammetry/image-acquisition.md). It develops a measurement-centred account of image capture, acquisition geometry and quality assurance, with a worked planning implementation and learner exercise. Its examples are educational and do not constitute flight approval, survey certification or field validation.

## Cross-technology observation design

Before choosing a platform or instrument, use the [spatial observation and sampling design framework](spatial-observation-and-sampling-design.md). It connects the target phenomenon, measurand, sampling frame, spatial/temporal support, sampling design, technology choice, calibration, independent checks, uncertainty and provenance. It is intentionally technology-neutral: specialised methods should add their own physical measurement models and quality requirements rather than being forced into one sensor workflow.

This framework complements the [survey-to-spatial-dataset capstone](../recipes/survey-to-spatial-dataset/README.md), which turns a bounded collection task into a traceable spatial dataset. It is not a substitute for instrument-specific procedures, professional standards or field validation.

A [synthetic sampling-design exercise](spatial-observation-sampling-exercise.md) provides a worked stratified allocation and weighted total-estimation example, followed by design challenges involving access, cost, spatial dependence and missing observations. It is an instructional exercise, not field evidence.
