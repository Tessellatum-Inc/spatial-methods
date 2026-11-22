# Cross-pillar pathways

**Status:** Initial curated pathway index  
**Purpose:** Help readers move between the four permanent pillars through real questions and workflows, without turning the pillars into a compulsory sequence or duplicating canonical content.

The four pillars are distinct homes for knowledge. A pathway is a navigational route across them. It should make the relationship visible, explain why each resource belongs, and state what the route currently demonstrates—and what it does not.

## How to use this index

Choose the entry point that matches your question. You may begin with a theory, an algorithm, a collection technology or a practical task. Follow only the links relevant to your goal.

A pathway is not complete merely because it links to one resource in each pillar. Its quality depends on whether the connections are technically meaningful, whether the hand-offs are understandable, and whether the practical evidence supports the claims made.

## Pathway 1 — From images to a defensible photogrammetric deliverable

**Application context:** Produce a spatially referenced image-derived product for a defined mapping purpose.

**Best entry point:** [Photogrammetric mapping recipe](../recipes/photogrammetric-mapping/README.md).

| Pillar | Canonical route | Why it belongs |
|---|---|---|
| Theoretical Foundations | [Measurement principles and field verification](../foundations/measurement-science/measurement-principles-and-field-verification.md); [linear algebra and matrix methods](../foundations/linear-algebra/README.md) | Measurement quality, uncertainty, estimation and matrix structure underpin control, adjustment and validation. |
| Spatial Data Collection | [Photogrammetric image acquisition](../collection/photogrammetry/image-acquisition.md) | Explains image formation context, acquisition geometry, camera behaviour, control and check-point design. |
| Spatial Algorithms | [Photogrammetric flight-design calculations](../implementations/python/photogrammetric-flight-design/README.md); [photogrammetric methods and algorithms](../algorithms/README.md) | Connects planning calculations and computational procedures to the acquired imagery. Select the specific algorithm records required by the project rather than treating the entire index as one workflow. |
| Spatial Recipes | [Photogrammetric mapping: project-to-validated-deliverable](../recipes/photogrammetric-mapping/README.md) | Combines requirements, reconnaissance, acquisition, processing, independent checks and delivery into a gated project workflow. |

**Practical evidence and current boundary**

The public HEIG-VD dataset has an executed EXIF-only OpenDroneMap baseline and structural output inspection. That establishes that a bounded processing chain ran and that its outputs were readable; it does not establish controlled-GCP performance, independent checkpoint accuracy or field validation. The separate role-blind review and independent checkpoint gates remain open. See the recipe and its [review status](../implementations/python/photogrammetry-odm/REVIEW-STATUS.md) before interpreting the rehearsal.

**Useful outcome:** Understand how acquisition design, measurement assumptions, image processing and independent validation combine—and why a visually convincing orthomosaic is not by itself an accuracy claim.

## Pathway 2 — From field observations to a quality-assessed spatial dataset

**Application context:** Design a bounded survey or asset-mapping workflow and deliver a dataset with traceable observations, reference information and quality evidence.

**Best entry point:** [Survey-to-spatial-dataset recipe](../recipes/survey-to-spatial-dataset/README.md).

| Pillar | Canonical route | Why it belongs |
|---|---|---|
| Theoretical Foundations | [Measurement science and survey adjustment](measurement-science-and-survey-adjustment.md); [measurement-science foundations](../foundations/README.md) | Defines measurands, observation models, uncertainty, covariance, datum and estimation. |
| Spatial Data Collection | [Spatial observation and sampling design](../collection/spatial-observation-and-sampling-design.md); [sampling-design exercise](../collection/spatial-observation-sampling-exercise.md); [surveying and field measurement source map](../catalog/surveying-field-measurement-source-map.md) | Defines the frame, measurand, spatial support, selection design, technology choice and field evidence before acquisition. |
| Spatial Algorithms | [Neyman allocation and stratified estimation](../algorithms/statistics/neyman-allocation-stratified-estimator.md); [Horvitz–Thompson estimator](../algorithms/statistics/horvitz-thompson.md); [Covariance and GLS implementation](../implementations/python/covariance-gls/README.md); [coordinate transformation](../algorithms/geodesy/crs-transformation.md) | Connects probability-based sample allocation and population estimation to adjustment and reference handling. The estimator must match the actual selection design. |
| Spatial Recipes | [Survey-to-spatial-dataset workflow](../recipes/survey-to-spatial-dataset/README.md) | Connects requirements, reference, acquisition, adjustment, independent checks, dataset construction and delivery. |

**Practical evidence and current boundary**

The recipe is at design stage with a limited synthetic software rehearsal. No field campaign has been conducted. Its examples do not establish instrument performance, field accuracy, legal compliance or professional acceptance.

**Useful outcome:** Learn to preserve the chain from a real-world quantity and observation method to a documented spatial dataset, rather than treating a GIS export as the whole deliverable.

## Pathway 3 — From a measurement question to a network adjustment

**Application context:** Understand how repeated or correlated observations support an adjusted estimate and how its quality should be assessed.

**Best entry point:** [Measurement science and survey adjustment learning path](measurement-science-and-survey-adjustment.md).

| Pillar | Canonical route | Why it belongs |
|---|---|---|
| Theoretical Foundations | [Measurement models](../foundations/measurement-science/measurement-models-and-measurand-definition.md); [uncertainty evaluation](../foundations/measurement-science/standard-uncertainty-type-a-type-b.md); [covariance and GLS](../foundations/measurement-science/covariance-correlated-observations-and-gls.md); [linear algebra](../foundations/linear-algebra/README.md) | Establishes the quantities, stochastic model and matrix operations used by adjustment. |
| Spatial Data Collection | [Measurement principles and field verification](../foundations/measurement-science/measurement-principles-and-field-verification.md) and the [surveying source map](../catalog/surveying-field-measurement-source-map.md) | Connects error and covariance assumptions to actual observation procedures and instrument behaviour. |
| Spatial Algorithms | [Covariance and GLS implementation](../implementations/python/covariance-gls/README.md) | Demonstrates covariance validation, Cholesky-based GLS and constrained adjustment on synthetic cases. |
| Spatial Recipes | [Measurement science and survey adjustment path](measurement-science-and-survey-adjustment.md) | Provides a sequenced route through foundations, synthetic experiments, implementation and interpretation. |

**Practical evidence and current boundary**

Exercises A–O use synthetic data or simulated scenarios. They support reproducible learning and software checks, not claims about a real instrument, field campaign or survey network.

**Useful outcome:** Be able to formulate an observation model, explain the stochastic assumptions, reproduce an adjustment and distinguish internal diagnostics from independent external validation.

## Pathway 4 — From sensor measurements to remote-sensing evidence

**Application context:** Understand how optical multispectral and radar observations become interpretable spatial evidence, while keeping their sensor physics and processing chains distinct.

**Best entry point:** [Remote sensing cross-pillar pathway](remote-sensing-cross-pillar-pathway.md).

This is a partial pathway and gap map, not a claim that remote sensing is now a complete four-pillar route. It links the existing [remote-sensing indices path](remote-sensing-indices.md), [Radar exploration](../explorations/radar/README.md), the [Fiji multispectral pilot](../implementations/python/area-adjusted-accuracy/fiji-multispectral-pilot-spec.md), and the [Nairobi Sentinel-1 scene specification](../explorations/radar/nairobi-sentinel-1-scene-record.md).

The optical branch has a broad algorithm catalogue, an initial electromagnetic/radiometric foundation module, an initial optical satellite acquisition method and a bounded live-data retrieval pilot; detailed optical physics, technical review and application validation remain incomplete. The SAR branch now has an [initial SAR acquisition and observation design method](../collection/sar-acquisition-and-observation-design.md), a guided backscatter investigation and scoped algorithms, but the Nairobi scene has not yet been selected or processed. Neither branch has a mature, independently validated end-to-end recipe. The pathway records these gaps rather than filling them with superficial links.

## Pathway 6 — From terrestrial observations to an adjusted spatial dataset

**Application context:** Capture relative positions and height differences with total stations and levels, evaluate the observation network, and deliver a traceable spatial dataset.

**Best entry point:** [Terrestrial surveying: total station and differential levelling](../collection/terrestrial-surveying-total-station-and-levelling.md).

| Pillar | Canonical route | Why it belongs |
|---|---|---|
| Theoretical Foundations | [Measurement models and measurand definition](../foundations/measurement-science/measurement-models-and-measurand-definition.md); [measurement principles and field verification](../foundations/measurement-science/measurement-principles-and-field-verification.md); [covariance and GLS](../foundations/measurement-science/covariance-correlated-observations-and-gls.md) | Defines the observed quantity, instrument/setup effects, uncertainty and correlated control information. |
| Spatial Data Collection | [Terrestrial surveying: total station and differential levelling](../collection/terrestrial-surveying-total-station-and-levelling.md) | Describes physical observations, station orientation, EDM and staff readings, field verification, closure and metadata. |
| Spatial Algorithms | [Covariance and GLS implementation](../implementations/python/covariance-gls/README.md); [measurement exercises F–O](../learning-paths/measurement-science-and-survey-adjustment.md) | Provides adjustment, datum, reliability, robust estimation and covariance-model experiments. The exercises are synthetic. |
| Spatial Recipes | [Survey-to-spatial-dataset workflow](../recipes/survey-to-spatial-dataset/README.md); [measurement science and survey adjustment path](measurement-science-and-survey-adjustment.md) | Connects acquisition, independent checks, adjustment, dataset construction and delivery. |

**Practical evidence and current boundary**

The adjustment exercises use synthetic observations. The terrestrial collection method is an initial technical synthesis; no field campaign, instrument test, local control validation or project acceptance is claimed. Apply the governing specification and professional requirements for the actual jurisdiction and task.

**Useful outcome:** Understand how instrument observations become coordinates and heights, why closures and residuals are diagnostics rather than guarantees, and how to preserve enough evidence for another competent person to assess the dataset.

## Pathway 5 — From GNSS observations to an accepted position

**Application context:** Acquire satellite-based position observations and determine whether the resulting coordinates are suitable for a survey, asset record, control network or navigation task.

**Best entry point:** [GNSS positioning and navigation observation](../collection/gnss-positioning-and-navigation-observation.md).

| Pillar | Canonical route | Why it belongs |
|---|---|---|
| Theoretical Foundations | [Measurement models and measurand definition](../foundations/measurement-science/measurement-models-and-measurand-definition.md); [measurement principles and field verification](../foundations/measurement-science/measurement-principles-and-field-verification.md); [covariance and GLS](../foundations/measurement-science/covariance-correlated-observations-and-gls.md) | Defines the observation model, reference, uncertainty and evidence needed to interpret an estimated coordinate. |
| Spatial Data Collection | [GNSS positioning and navigation observation](../collection/gnss-positioning-and-navigation-observation.md) | Connects physical signal observables, field occupation, reference frames, correction modes, antenna heights and independent checks. |
| Spatial Algorithms | [GNSS carrier-phase integer ambiguity resolution](../algorithms/geodesy/gnss-carrier-phase-ambiguity-resolution.md); [GNSS ambiguity implementation](../implementations/python/gnss-ambiguity/README.md); [GNSS residual-based RAIM implementation](../implementations/python/gnss-raim/README.md) | Connects integer ambiguity estimation and residual screening to the observations while preserving their bounded implementation scopes. |
| Spatial Recipes | [Survey-to-spatial-dataset workflow](../recipes/survey-to-spatial-dataset/README.md); [measurement science and survey adjustment path](measurement-science-and-survey-adjustment.md) | Provides the broader acquisition-to-delivery and estimation context. Neither resource is a GNSS-specific field procedure; project-specific control specifications still govern execution. |

**Practical evidence and current boundary**

The GNSS ambiguity and RAIM packages are computational teaching components with explicit input and integrity boundaries. They do not process raw receiver observations into a certified position solution. No GNSS field campaign or local control-network validation is claimed by this pathway.

**Useful outcome:** Understand why a GNSS coordinate depends on the signal model, reference frame, processing choices and field evidence—and how to avoid treating a receiver status indicator as a complete accuracy assessment.

## Pathway 7 — From terrestrial laser scans to a validated 3D point cloud

**Application context:** Capture visible 3D surfaces from static terrestrial scan stations, align the scans, georeference the result and assess whether the cloud is complete and accurate enough for its intended use.

**Best entry point:** [Terrestrial laser scanning and point-cloud acquisition](../collection/terrestrial-laser-scanning-and-point-cloud-acquisition.md).

| Pillar | Canonical route | Why it belongs |
|---|---|---|
| Theoretical Foundations | [Measurement models and measurand definition](../foundations/measurement-science/measurement-models-and-measurand-definition.md); [measurement principles and field verification](../foundations/measurement-science/measurement-principles-and-field-verification.md); [covariance and GLS](../foundations/measurement-science/covariance-correlated-observations-and-gls.md) | Frames range/angle observations, reference control, uncertainty and the distinction between repeatability and end-to-end quality. |
| Spatial Data Collection | [Terrestrial laser scanning and point-cloud acquisition](../collection/terrestrial-laser-scanning-and-point-cloud-acquisition.md); [terrestrial surveying](../collection/terrestrial-surveying-total-station-and-levelling.md) | Connects scanner setup, coverage, overlap, targets, georeferencing and independent survey control. |
| Spatial Algorithms | [Point-cloud registration and geometric comparison](../algorithms/geometry/point-cloud-registration.md); [point-cloud registration implementation](../implementations/python/point-cloud-registration/README.md); [voxelization](../implementations/python/point-cloud-voxelization/README.md); [RANSAC plane fitting](../implementations/python/ransac-plane-fitting/README.md) | Provides local rigid registration, geometric comparison and bounded point-cloud processing components. |
| Spatial Recipes | [Survey-to-spatial-dataset workflow](../recipes/survey-to-spatial-dataset/README.md) | Supplies the project gates for requirements, reference, acquisition, independent checks, provenance and delivery. |

**Practical evidence and current boundary**

The registration and point-cloud packages are computational baselines, not a field-validated TLS processing chain. The collection method is an initial synthesis. No scanner field verification, site scan, georeferencing campaign or independent checkpoint assessment is claimed. Mobile and airborne LiDAR require separate acquisition and trajectory procedures.

**Useful outcome:** Understand why a dense point cloud can still be incomplete or misregistered, why registration residuals are not independent accuracy evidence, and how control and check points support a defensible 3D deliverable.

## Pathway 8 — From mobile laser observations to a trajectory-referenced corridor cloud

**Application context:** Capture 3D corridor or indoor geometry from a moving platform, estimate the platform trajectory, transform time-tagged laser observations into a project frame and assess strip consistency and independent accuracy.

**Best entry point:** [Mobile laser scanning and kinematic point-cloud acquisition](../collection/mobile-laser-scanning-and-kinematic-point-cloud-acquisition.md).

| Pillar | Canonical route | Why it belongs |
|---|---|---|
| Theoretical Foundations | [Measurement models and measurand definition](../foundations/measurement-science/measurement-models-and-measurand-definition.md); [measurement principles and field verification](../foundations/measurement-science/measurement-principles-and-field-verification.md); [covariance and GLS](../foundations/measurement-science/covariance-correlated-observations-and-gls.md); [geodesy and reference systems](../learning-paths/geodesy-foundations.md) | Defines sensor observations, time-dependent coordinate transformations, reference frames and uncertainty. |
| Spatial Data Collection | [Mobile laser scanning and kinematic point-cloud acquisition](../collection/mobile-laser-scanning-and-kinematic-point-cloud-acquisition.md); [GNSS positioning and navigation observation](../collection/gnss-positioning-and-navigation-observation.md); [terrestrial surveying](../collection/terrestrial-surveying-total-station-and-levelling.md) | Connects scanner observations to platform trajectory, calibration, reference support and independent survey control. |
| Spatial Algorithms | [Point-cloud registration and geometric comparison](../algorithms/geometry/point-cloud-registration.md); [point-cloud registration implementation](../implementations/python/point-cloud-registration/README.md) | Provides bounded local strip/point-cloud comparison methods. It does not implement a complete GNSS/INS navigation filter or production MLS georeferencing chain. |
| Spatial Recipes | [Survey-to-spatial-dataset workflow](../recipes/survey-to-spatial-dataset/README.md) | Connects requirements, field records, reference control, independent checks, provenance and delivery. |

**Practical evidence and current boundary**

The point-cloud registration package is a local computational baseline, not a mobile navigation or trajectory estimator. The collection method is an initial synthesis; no sensor calibration, trajectory solution, platform test or field campaign is claimed. Indoor SLAM and GNSS-denied mapping require separate system-specific validation and external datum control where absolute coordinates are required.

**Useful outcome:** Understand why a mobile point cloud depends on time-aligned sensor observations and a calibrated trajectory, why strip agreement is not absolute accuracy evidence, and how control and independent checks constrain the result.

## Pathway 9 — From airborne LiDAR flightlines to a validated terrain or surface product

**Application context:** Acquire broad-area 3D observations from an aircraft or UAV, georeference each laser pulse using the navigation trajectory and calibrated sensor geometry, reconcile overlapping flightlines, classify returns and validate derived products.

**Best entry point:** [Airborne LiDAR acquisition and strip adjustment](../collection/airborne-lidar-acquisition-and-strip-adjustment.md).

| Pillar | Canonical route | Why it belongs |
|---|---|---|
| Theoretical Foundations | [Measurement models and measurand definition](../foundations/measurement-science/measurement-models-and-measurand-definition.md); [measurement principles and field verification](../foundations/measurement-science/measurement-principles-and-field-verification.md); [geodesy and reference systems](../learning-paths/geodesy-foundations.md); [covariance and GLS](../foundations/measurement-science/covariance-correlated-observations-and-gls.md) | Frames pulse observations, trajectory transformations, reference systems, calibration and uncertainty. |
| Spatial Data Collection | [Airborne LiDAR acquisition and strip adjustment](../collection/airborne-lidar-acquisition-and-strip-adjustment.md); [GNSS positioning and navigation observation](../collection/gnss-positioning-and-navigation-observation.md); [mobile laser scanning](../collection/mobile-laser-scanning-and-kinematic-point-cloud-acquisition.md) | Connects flight planning, GNSS/IMU trajectory, boresight, control and strip diagnostics to the broader kinematic sensing family. |
| Spatial Algorithms | [Point-cloud registration and geometric comparison](../algorithms/geometry/point-cloud-registration.md); [point-cloud registration implementation](../implementations/python/point-cloud-registration/README.md); [voxelization](../implementations/python/point-cloud-voxelization/README.md) | Supplies bounded geometric comparison and point-cloud handling components. It does not implement a full airborne navigation solution, strip bundle adjustment or semantic classifier. |
| Spatial Recipes | [Survey-to-spatial-dataset workflow](../recipes/survey-to-spatial-dataset/README.md) | Provides the requirements, control, independent validation, provenance and delivery gates. |

**Practical evidence and current boundary**

The point-cloud packages are computational components, not a validated airborne LiDAR production chain. The acquisition method is an initial synthesis; no flight, calibration, strip adjustment, classification or checkpoint campaign is claimed. Flight operations must comply with the applicable aviation and UAS permissions, safety requirements and project specifications.

**Useful outcome:** Understand how flight geometry, trajectory, calibration, strip adjustment, classification and independent checks determine whether a point cloud or terrain model is fit for its intended use.

## Pathway 10 — From acoustic observations to a datum-referenced bathymetric surface

**Application context:** Acquire and reduce water-depth observations, account for sound-speed refraction and vessel motion, tie soundings to a defined vertical reference, and assess coverage and uncertainty before producing a bathymetric surface.

**Best entry point:** [Multibeam hydrographic surveying and bathymetric acquisition](../collection/multibeam-hydrographic-surveying-and-bathymetric-acquisition.md).

| Pillar | Canonical route | Why it belongs |
|---|---|---|
| Theoretical Foundations | [Measurement models and measurand definition](../foundations/measurement-science/measurement-models-and-measurand-definition.md); [measurement principles and field verification](../foundations/measurement-science/measurement-principles-and-field-verification.md); [uncertainty propagation](../algorithms/statistics/uncertainty-propagation.md); [geodesy foundations](geodesy-foundations.md) | Frames travel-time/range observations, sensor geometry, reference surfaces, correlated uncertainty and datum transformations. Dedicated water-column acoustics and tidal-datum foundations remain a gap. |
| Spatial Data Collection | [Multibeam hydrographic surveying and bathymetric acquisition](../collection/multibeam-hydrographic-surveying-and-bathymetric-acquisition.md); [GNSS positioning](../collection/gnss-positioning-and-navigation-observation.md); [terrestrial surveying](../collection/terrestrial-surveying-total-station-and-levelling.md) | Connects sonar, sound-speed profiles, vessel motion, positioning, vertical control, patch tests and independent checks. |
| Spatial Algorithms | [Layered-water-column acoustic ray tracing](../algorithms/coastal/layered-water-column-acoustic-ray-tracing.md); [uncertainty propagation](../algorithms/statistics/uncertainty-propagation.md); [CRS transformation](../algorithms/geodesy/crs-transformation.md); [Stumpf bathymetry and OC4v4](../algorithms/remote-sensing/stumpf-bathymetry-and-oc4v4.md) | Supplies uncertainty and reference-frame operations while explicitly distinguishing optical satellite-derived bathymetry from acoustic sounding. A dedicated bathymetric gridding/uncertainty implementation remains to be developed. |
| Spatial Recipes | [Multibeam bathymetry recipe](../recipes/multibeam-bathymetry/README.md); [survey-to-spatial-dataset workflow](../recipes/survey-to-spatial-dataset/README.md) | The hydrographic recipe connects sonar-specific acquisition, corrections, datum reduction, uncertainty, surface generation and validation. The generic survey workflow remains useful for transferable measurement and delivery principles. |

**Practical evidence and current boundary**

The hydrographic method and recipe are desk-designed technical syntheses. The acoustic ray-tracing implementation has synthetic unit tests; it is not a full MBES processing chain. No vessel mobilisation, sonar calibration, patch test, water-level tie, bathymetric acquisition, surface generation from real sonar data or field validation is claimed. The route must not be used as a substitute for the current IHO order, national hydrographic authority instructions or project specifications.

**Useful outcome:** Understand why bathymetry is a coupled acoustic, navigation, motion, water-level and datum problem—and why a dense sounding grid alone does not demonstrate full feature search or absolute vertical accuracy.

## What is not yet represented

This index is deliberately selective. It does not imply that every subject has a complete cross-pillar route. In particular:

- Remote sensing now has a partial cross-pillar pathway and explicit optical/SAR branches. The route still needs reviewed sensor-physics foundations, executed acquisition methods and end-to-end validated recipes.
- Spatial statistics has substantial methods and learning paths, but the data-generation and study-design choices should be made more explicit in future integrated routes.
- Transport, hydrology, environmental monitoring and other application families should receive pathways when their collection, theoretical, algorithmic and recipe records are sufficiently developed to support honest hand-offs.

Do not create artificial links just to fill all four columns. A missing or immature pillar connection is a useful development finding.

## Pathway maintenance standard

When adding or revising a pathway:

1. Name the application or question and its intended outcome.
2. State plausible entry points; do not require a fixed starting level.
3. Link to canonical records, not duplicated summaries.
4. Explain the contribution of each linked resource.
5. Identify prerequisites and decision points only where they matter.
6. State whether evidence is theoretical, synthetic, public-data, prototype, field or operational.
7. Record open gaps and validation limits.
8. Review links and status when a canonical resource changes.

A pathway is ready for broader teaching use only when its sequence has been reviewed, the hand-offs are understandable, and its practical outputs and limitations have been checked. This index is an initial navigation aid, not a certification of pathway completeness.
