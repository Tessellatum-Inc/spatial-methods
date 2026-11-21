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
| Spatial Data Collection | [Spatial Data Collection subject map](../collection/README.md); [surveying and field measurement source map](../catalog/surveying-field-measurement-source-map.md) | Helps select observation methods and identify instrument, control, sampling, field verification and provenance requirements. |
| Spatial Algorithms | [Covariance and GLS implementation](../implementations/python/covariance-gls/README.md); [coordinate transformation](../algorithms/geodesy/crs-transformation.md) | Provides reproducible computational components for adjustment and reference handling. Other algorithms should be selected from the actual feature and delivery requirements. |
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
