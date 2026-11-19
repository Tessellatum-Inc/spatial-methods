# Subject-to-repository alignment register

**Version:** 0.1  
**Status:** Structural alignment baseline; individual-record reconciliation remains in progress  
**Related index:** [Geoinformatics master subject index](master-subject-index.md)  
**Repository:** Spatial Methods

## 1. Purpose

This register connects the master subject taxonomy to the repository's existing content locations. It is an orientation and work-planning document, not a certification of technical completeness.

The current repository contains several content systems built at different stages:

- subject-oriented algorithm directories;
- a broad methods catalogue;
- canonical verification records;
- implementation packages;
- notebooks and labs;
- learning paths;
- research notes;
- the original source inventory and its section indexes.

These are useful assets. The alignment exercise connects them without deleting or flattening their existing organisation.

## 2. Evidence and confidence rules

This initial pass is based on repository paths, directory names and the existing README/catalogue navigation. It is a **structural mapping**, not a file-by-file technical review.

Use these labels:

- **Directory-level mapping:** the directory's apparent scope aligns with a subject family.
- **Named-record mapping:** an individual record has been inspected and linked to a subject ID.
- **Confirmed crosswalk:** an existing crosswalk has inspected the relevant record/package documentation and explicitly records the relationship.
- **Unresolved:** the relationship needs inspection; do not infer equivalence from similar names.

No subject maturity state is advanced by this register. No verification, implementation or validation status is changed.

## 3. Existing repository assets and their role

| Existing location | Role in the knowledge system | Alignment treatment |
|---|---|---|
| `algorithms/` | Subject-oriented algorithm explanations | Map subdirectories and individual pages to one or more `ALG` subjects |
| `methods/` | Cross-domain analytical methods, models and techniques | Classify by record type and map to primary subject plus related subjects |
| `catalog/verification/` | Technical identity and verification records | Preserve verification workflow; add subject IDs as cross-references where reviewed |
| `implementations/python/` | Reproducible code packages | Link packages to the method/operation/algorithm they implement; preserve package-specific scope |
| `implementations/clipper2-csharp/` | Non-Python implementation examples | Link by implemented operation and technology |
| `notebooks/` | Interactive experiments, demonstrations and labs | Link to the relevant subject and implementation; a notebook alone is not validation |
| `learning-paths/` | Guided routes through connected knowledge | Link paths to their primary and supporting subjects |
| `research/` | Investigations, identity audits and technical research | Link to the subjects investigated; retain research status and evidence |
| `source-inventory/` | Preserved original source intake | Preserve source wording and provenance; never rewrite to match the taxonomy |
| `catalog/sections/` | Item-level indexes retaining the source's 22 section groupings | Use as source-entry provenance and discovery routes |
| `catalog/coverage-matrix.md` | Source-to-repository coverage tracking | Keep as the source-compendium progress view, not a substitute for the master subject map |
| `catalog/record-types.md` | Primary record classification | Continue to govern whether an item is an algorithm, operation, model, statistic, metric, method, workflow, system, standard, implementation, dataset or application |

## 4. Directory-level subject crosswalk

The following mappings are deliberately broad. A directory can contain multiple record types and may need to be split or cross-linked at individual-record level later.

| Repository path | Primary subject mapping | Notes |
|---|---|---|
| `algorithms/geometry/` | SM-ALG-001, SM-ALG-002, SM-ALG-003 | Geometry, overlay, predicates, topology and mesh structures |
| `algorithms/indexing/` | SM-ALG-005 | Spatial indexes and search structures |
| `algorithms/network/` and `algorithms/networks/` | SM-ALG-007, SM-ALG-015 | Routing, graph methods, mobility and temporal networks; directory naming duplication needs later review |
| `algorithms/optimization/` | SM-ALG-011 | Location, coverage, allocation and optimisation |
| `algorithms/statistics/` | SM-ALG-008, SM-ALG-009, SM-ALG-018 | Statistical methods, point patterns, geostatistics and uncertainty; classify individual records more precisely |
| `algorithms/interpolation/` | SM-ALG-009 | Interpolation and prediction methods |
| `algorithms/geostatistics/` | SM-ALG-009 | Geostatistical methods and models |
| `algorithms/raster/` | SM-ALG-010, SM-ALG-012 | Raster operations, terrain and hydrology |
| `algorithms/hydrology/` | SM-ALG-012 | Hydrological and terrain-related computation |
| `algorithms/remote-sensing/` | SM-ALG-013 | Image processing, spectral methods and Earth observation |
| `algorithms/segmentation/` | SM-ALG-013, SM-ALG-017 | Image and object segmentation; inspect individual method scope |
| `algorithms/geoai/` | SM-ALG-017 | Spatial machine learning and GeoAI |
| `algorithms/geodesy/` | SM-ALG-004 | Geodetic computation and coordinate operations |
| `algorithms/photogrammetry/` | SM-COL-007, SM-REC-007 | Photogrammetric measurement and processing workflows |
| `algorithms/cartography/` | SM-FND-010, SM-REC-010 | Cartographic theory and production methods |
| `algorithms/query-processing/` | SM-ALG-005, SM-ALG-006, SM-ALG-020 | Query execution, spatial joins and scalable processing |
| `algorithms/streaming/` | SM-ALG-015, SM-INF-004 | Streaming and dynamic spatial data |
| `algorithms/spatial-interaction/` | SM-ALG-007, SM-ALG-011 | Interaction, accessibility and spatial allocation models |
| `algorithms/mobility/` | SM-ALG-007, SM-ALG-015 | Movement, mobility and trajectory analysis |
| `algorithms/domain-modeling/` | SM-ALG-014, relevant APP records | Domain-specific models; classify each record by application |
| `algorithms/biodiversity/` | SM-APP-003 | Biodiversity and ecological applications |
| `algorithms/coastal/` | SM-APP-009, SM-APP-017 | Coastal and marine applications; collection methods cross-link to COL |
| `methods/` | Multiple ALG, FND, COL and APP subjects | Broad catch-all catalogue; do not assign the entire directory to one pillar |
| `implementations/python/` | Related algorithm, method and recipe subjects | Package names and scopes require explicit crosswalks; package existence does not prove validation |
| `notebooks/` | Related subject IDs | Lab-specific mapping; notebooks are evidence of an experiment or demonstration, not automatically a validated result |
| `learning-paths/` | Related FND, ALG and REC subjects | Learning paths connect subjects and should not become subject owners |
| `research/` | Related subject IDs | Research notes should cite the exact subjects, sources and claims they investigate |

### Important structural observations

1. Both `algorithms/network/` and `algorithms/networks/` exist. The former currently appears very small, while the latter contains a broader network collection. Do not merge or move them without inspecting links and history.
2. Several algorithm directories mix concepts, operations, data structures and application-specific methods. The record-type taxonomy remains authoritative for classifying individual pages.
3. `methods/` is a broad catalogue. It should not be treated as a fifth pillar or as a synonym for Spatial Recipes.
4. Collection technologies and field procedures are less visibly represented as a coherent dedicated collection than algorithms and analytical methods. This is a likely expansion gap, but must be confirmed through file-level inventory before creating new content.
5. The existing repository has strong computational and analytical content. The new index makes theoretical foundations, field acquisition, instruments, physical measurement and real-world application relationships more visible.

## 5. Existing source-section crosswalk

The 22 source sections are historical intake groupings. They remain intact and may contribute to several subjects.

| Source section | Broad subject alignment |
|---|---|
| 01 — Core GIS | SM-FND-018; SM-ALG-001 to SM-ALG-006; SM-REC-003 to SM-REC-005 |
| 02 — Spatial statistics | SM-FND-004, SM-FND-005; SM-ALG-008, SM-ALG-018 |
| 03 — Geostatistics | SM-ALG-009; SM-FND-004, SM-FND-005, SM-FND-016 |
| 04 — Raster, terrain and hydrology | SM-ALG-010, SM-ALG-012; SM-APP-005, SM-APP-009 |
| 05 — Remote sensing | SM-FND-012 to SM-FND-014; SM-COL-004 to SM-COL-006; SM-ALG-013 |
| 06 — Optimization, mobility and transport | SM-FND-017; SM-ALG-007, SM-ALG-011; SM-APP-001 |
| 07 — Domain modelling | SM-ALG-014; relevant application contexts |
| 08 — GeoAI | SM-ALG-017; SM-INF-010 |
| 09 — Geodesy, cartography and infrastructure | SM-FND-008, SM-FND-010; SM-ALG-004; SM-INF-003, SM-INF-006, SM-INF-009 |
| 10 — Classical statistical and computational additions | SM-FND-004 to SM-FND-007; SM-ALG-001, SM-ALG-008, SM-ALG-009 |
| 11 — GeoAI and computer vision additions | SM-ALG-013, SM-ALG-017; SM-FND-012, SM-FND-014 |
| 12 — Signal, GNSS and regional science | SM-FND-008, SM-FND-013, SM-FND-014; SM-COL-002; SM-ALG-004 |
| 13 — GeoFM workflows, urban mobility and LLMs | SM-ALG-007, SM-ALG-015, SM-ALG-017; SM-INF-010; SM-APP-001 |
| 14 — Databases, graphics, morphology and hazards | SM-ALG-001, SM-ALG-005, SM-ALG-010, SM-ALG-012; SM-INF-003 |
| 15 — Vision, registration and vector extraction | SM-COL-007, SM-COL-008; SM-ALG-013, SM-ALG-016 |
| 16 — Flows, regions, deformation and marine | SM-ALG-007, SM-ALG-012, SM-ALG-014; SM-APP-009 |
| 17 — Geometry, scalability, design and siting | SM-ALG-001, SM-ALG-005, SM-ALG-011, SM-ALG-020 |
| 18 — Moving objects, routing, transit and water | SM-ALG-007, SM-ALG-015; SM-APP-001, SM-APP-009 |
| 19 — African applications, addressing and finance | SM-ALG-004, SM-ALG-011; SM-APP-004, SM-APP-012 |
| 20 — Indices, microwave, events and information | SM-FND-012 to SM-FND-014; SM-COL-006; SM-ALG-013, SM-ALG-015 |
| 21 — Neural fields, climate, accounting and robust geometry | SM-FND-006, SM-FND-019; SM-ALG-001, SM-ALG-017; SM-APP-017 |
| 22 — Inference, covariance, spherical and asset monitoring | SM-FND-004, SM-FND-005, SM-FND-008, SM-FND-011; SM-ALG-008, SM-ALG-009, SM-APP-006 |

This table is a discovery crosswalk based on section titles and known catalogue scope. It is not a claim that every item in a section has been individually classified.

## 6. Existing reconciliation work to preserve

The repository already contains a structural catalogue audit and four crosswalk batches:

- [Catalogue alignment audit](../docs/catalogue-alignment-audit.md)
- [Crosswalk batch 1 — confirmed aliases](catalogue-crosswalk-batch-1.md)
- [Crosswalk batch 2 — inspected direct matches](catalogue-crosswalk-batch-2.md)
- [Crosswalk batch 3 — package-name questions](catalogue-crosswalk-batch-3.md)
- [Crosswalk batch 4 — bundled methods and resolved mappings](catalogue-crosswalk-batch-4.md)

The dated audit reports a tree snapshot with 218 canonical verification records, 321 Python implementation package READMEs and 180 notebook files. It explicitly warns that filename mismatches are not confirmed orphans. These counts belong to that audit snapshot and must not be represented as a fresh count of the current default branch.

The four batches contain confirmed mappings and unresolved questions. Preserve their scope notes. In particular, do not conflate related but distinct methods, implementations or estimator variants merely because they share a topic.

## 7. File-level reconciliation workflow

The next reconciliation pass should create one row per meaningful canonical record or source-entry relationship. Recommended fields:

| Field | Meaning |
|---|---|
| `subject_id` | Primary stable ID from the master subject index |
| `related_subject_ids` | Additional meaningful cross-pillar/application links |
| `record_path` | Canonical repository record |
| `record_kind` | Primary kind from record-types.md |
| `source_entry` | Original source section/entry, if applicable |
| `implementation_paths` | One or more related implementation packages |
| `notebook_paths` | Relevant labs and notebooks |
| `learning_path` | Relevant guided path |
| `mapping_status` | Proposed, inspected, confirmed, unresolved, or not applicable |
| `evidence_note` | Why the relationship is justified |
| `reviewed_at` | Date of actual inspection |

Rules:

1. Inspect the canonical record and implementation README before confirming a relationship.
2. Inspect code and tests before claiming implementation behaviour or validation.
3. Inspect notebooks before claiming they demonstrate the same scope as a canonical record.
4. Keep variants separate where assumptions, estimands, input contracts or guarantees differ.
5. Use aliases for naming differences only when scope is genuinely equivalent.
6. Mark unresolved mappings explicitly.
7. Never upgrade bibliography, technical-claim or rights status through a structural mapping.
8. Keep the original source label and source page even after assigning a canonical subject.

## 8. Recommended first connected curation cluster

Start with a connected cluster that has strong existing repository assets and broad professional reuse:

**Spatial reference, measurement, data quality and reproducible spatial data workflows.**

Initial subject IDs:

- SM-FND-008 — Geodesy and reference systems
- SM-FND-011 — Measurement science, accuracy and uncertainty
- SM-FND-015 — Computer science, algorithms and complexity
- SM-ALG-004 — Coordinate transformations and geodetic computation
- SM-ALG-018 — Spatial uncertainty, error propagation and sensitivity
- SM-COL-001 — Geodetic and engineering surveying
- SM-COL-002 — GNSS, positioning and navigation systems
- SM-COL-003 — Ground control, reference networks and field measurement
- SM-REC-003 — CRS selection, transformation and coordinate QA
- SM-REC-008 — Survey planning, field capture and quality control
- SM-REC-017 — Spatial quality assurance and accuracy assessment
- SM-INF-005 — Data engineering, ETL, metadata and provenance
- SM-INF-009 — Open geospatial standards, formats and service specifications
- SM-INF-011 — Software testing, reproducibility, CI and version control

Why this cluster: it connects theoretical foundations, field measurement, GNSS, coordinate operations, data quality and practical delivery. It supports work in surveying, infrastructure, mapping, environmental monitoring, transport and many other domains.

The cluster is a recommendation for the next curation sprint, not a claim that its contents are already complete.

The first cluster has its own inspected asset crosswalk and preliminary gap analysis: [Reference, positioning and measurement](first-curation-cluster-reference-positioning-measurement.md). It distinguishes existing GNSS/geodesy assets from the field-survey and standards work that remains.

## 9. Immediate next actions

1. Create a file-level inventory of the existing canonical records, verification records, packages, notebooks and learning paths.
2. Assign primary subject IDs to existing records where the scope is clear.
3. Record secondary subject links where they add real navigational value.
4. Reconcile the existing crosswalk batches with the subject IDs without rewriting their historical findings.
5. Identify genuine gaps in field acquisition, theoretical foundations and applied workflows only after the inventory is complete.
6. Build the first connected curation cluster from inspected existing material before creating duplicate pages.

**Current conclusion:** the repository has a substantial existing computational and analytical collection. This alignment register makes its relationship to the wider subject universe explicit at directory and source-section level. Individual-record mapping, technical completeness and the state of field-collection coverage remain open work.
