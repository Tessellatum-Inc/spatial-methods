# Geoinformatics master subject index

**Version:** 0.1  
**Status:** Initial taxonomy; subject coverage not yet assessed  
**Role:** Canonical navigation index for the wider Geoinformatics knowledge universe  
**Related architecture:** [Four-pillar architecture](../docs/knowledge-tools-real-world-architecture.md), [subject-to-repository alignment register](subject-alignment-register.md), [record types](record-types.md), [coverage matrix](coverage-matrix.md), [editorial and resource curation standard](../docs/editorial-resource-architecture.md)

The first connected application of this taxonomy is the [reference, positioning and measurement curation cluster](first-curation-cluster-reference-positioning-measurement.md), which links existing repository assets to the relevant subject IDs and records preliminary gaps. The first technical foundation is [Measurement principles and field verification](../foundations/measurement-science/measurement-principles-and-field-verification.md), linked primarily to SM-FND-011 and its surveying/quality-control relationships. The first worked experiment is [Exercise A: repeated distance and horizontal-angle observations](../experiments/measurement/exercise-a-repeated-distance-and-angle.md), with a synthetic dataset and reproducible analysis. The second is [Exercise B: differential levelling and loop adjustment](../experiments/measurement/exercise-b-differential-levelling-loop.md), which demonstrates constrained weighted adjustment and covariance propagation. The third is [Exercise C: weighted least-squares adjustment of a vertical control network](../experiments/measurement/exercise-c-weighted-control-network.md), extending the loop exercise to a redundant multi-route network. The fourth is [Exercise D: stochastic control and correlated observations](../experiments/measurement/exercise-d-stochastic-control-and-correlation.md), comparing exact and uncertain datum control and generalized least squares with correlated observations. The fifth is [Exercise E: minimally constrained vertical networks](../experiments/measurement/exercise-e-minimally-constrained-vertical-network.md), which demonstrates the vertical datum defect, inner constraints, free-network covariance and transfer onto external control.

The sixth worked experiment is [Exercise F: network quality, statistical testing and blunder detection](../experiments/measurement/exercise-f-network-quality-and-blunder-detection.md), extending the synthetic vertical network into global and local statistical testing, gross-error propagation, multiple-testing caution and independent checking.

The seventh worked experiment is [Exercise G: reliability, detectability and network design](../experiments/measurement/exercise-g-reliability-and-network-design.md), moving from post-adjustment diagnostics to pre-survey design using redundancy numbers, minimal detectable bias and external reliability.

## 1. Purpose and boundaries

This index maps the subjects that Spatial Methods may investigate, curate, teach, implement or connect to real-world applications.

It is a **subject taxonomy**, not a list of completed resources. A subject appearing here does not mean it has been researched, verified, implemented or validated.

The four permanent pillars remain:

1. Spatial Algorithms
2. Spatial Recipes
3. Spatial Data Collection
4. Theoretical Foundations

Applications are cross-cutting contexts, not a fifth pillar. Programming, software, data engineering, standards and infrastructure are enabling domains that connect the pillars; they do not replace them.

The index is intentionally broader than the original source compendium. The [coverage matrix](coverage-matrix.md) continues to track the state of that particular source intake and its resulting canonical records.

## 2. Stable subject identifiers

Each subject receives a stable identifier. Identifiers are independent of page paths and display names.

| Prefix | Meaning |
|---|---|
| `FND` | Theoretical Foundations |
| `ALG` | Spatial Algorithms |
| `COL` | Spatial Data Collection |
| `REC` | Spatial Recipes |
| `INF` | Cross-cutting technical infrastructure |
| `APP` | Application context |

Identifier format: `SM-[PREFIX]-[NUMBER]`, for example `SM-FND-001`.

Rules:

- Never reuse an identifier for a different subject.
- Renaming a subject does not change its identifier.
- Splitting a subject creates new identifiers; retain the former identifier as a deprecated record with links to successors.
- Merging subjects requires an explicit decision and redirects or aliases from retired identifiers.
- A subject may have one primary home and multiple cross-pillar, infrastructure and application relationships.
- IDs identify subjects, not individual articles, algorithms, datasets, software packages or implementations. Those receive their own canonical record IDs under the repository's record conventions.

## 3. Curation states

Use these states consistently:

| State | Meaning |
|---|---|
| Not mapped | Scope and boundaries have not yet been investigated |
| Mapped | Scope, branches and important distinctions have been outlined |
| Sources identified | Relevant authoritative and primary sources have been identified |
| Curated | A useful, evaluated collection or synthesis exists |
| Technically investigated | Important theory, methods, assumptions and alternatives have been examined |
| Implemented | At least one reproducible implementation or practical procedure exists |
| Validated | The stated validation requirements have been met and evidence is recorded |
| Needs review | A material change, new evidence or identified weakness requires reassessment |
| Archived | No longer actively maintained; historical record retained |

A subject can have different maturity across subtopics. Do not promote an entire subject to a higher state because one small example exists.

## 4. Priority bands

Priority is a planning aid, not a measure of intellectual importance.

- **A — Core competence:** foundational capabilities with broad reuse across geospatial work.
- **B — Applied specialisation:** important domains and methods that enable deeper professional and technical work.
- **C — Expansion/frontier:** emerging, highly specialised or strategically optional areas.

Priorities may change as projects, evidence, field opportunities and user needs change.

---

## 5. Theoretical Foundations (`FND`)

| ID | Subject | Initial priority | Connected subjects |
|---|---|---:|---|
| SM-FND-001 | Mathematics for spatial science | A | SM-FND-002, SM-FND-003, SM-ALG-001 |
| SM-FND-002 | Linear algebra and matrix methods | A | SM-FND-001, SM-ALG-011, SM-INF-001 |
| SM-FND-003 | Calculus and differential methods | A | SM-FND-001, SM-FND-009, SM-ALG-012 |
| SM-FND-004 | Probability and statistical inference | A | SM-FND-005, SM-ALG-008, SM-ALG-009 |
| SM-FND-005 | Spatial statistics and stochastic processes | A | SM-FND-004, SM-ALG-008, SM-ALG-009 |
| SM-FND-006 | Geometry and computational geometry theory | A | SM-FND-001, SM-ALG-001, SM-ALG-002 |
| SM-FND-007 | Topology and spatial relations | A | SM-FND-006, SM-ALG-003 |
| SM-FND-008 | Geodesy and reference systems | A | SM-FND-009, SM-COL-001, SM-ALG-004 |
| SM-FND-009 | Earth science, physical geography and geomorphology | A | SM-FND-003, SM-FND-008, SM-ALG-012 |
| SM-FND-010 | Cartographic theory and visual perception | A | SM-FND-006, SM-REC-010 |
| SM-FND-011 | Measurement science, accuracy and uncertainty | A | SM-COL-001, SM-COL-002, SM-COL-003 |
| SM-FND-012 | Remote sensing physics and radiometry | A | SM-COL-004, SM-COL-005, SM-ALG-013 |
| SM-FND-013 | Optics, electromagnetism and wave physics | B | SM-FND-012, SM-COL-004, SM-COL-006 |
| SM-FND-014 | Signal processing and information theory | B | SM-FND-013, SM-COL-006, SM-ALG-013 |
| SM-FND-015 | Computer science, algorithms and complexity | A | SM-ALG-001, SM-INF-001, SM-INF-002 |
| SM-FND-016 | Numerical analysis and scientific computing | A | SM-FND-001, SM-FND-004, SM-ALG-011 |
| SM-FND-017 | Optimisation and operations research | A | SM-FND-002, SM-ALG-011, SM-ALG-012 |
| SM-FND-018 | Geographic information science and spatial thinking | A | All four pillars |
| SM-FND-019 | Systems theory, complexity and emergence | B | SM-ALG-012, SM-ALG-014, SM-APP-014 |
| SM-FND-020 | Physical, environmental and life-science foundations | B | SM-COL-007, SM-COL-008, SM-APP-003 |

## 6. Spatial Algorithms (`ALG`)

| ID | Subject | Initial priority | Connected subjects |
|---|---|---:|---|
| SM-ALG-001 | Computational geometry | A | SM-FND-006, SM-FND-007 |
| SM-ALG-002 | Geometric predicates, constructions and overlay | A | SM-ALG-001, SM-ALG-003 |
| SM-ALG-003 | Spatial topology and topological operations | A | SM-FND-007, SM-ALG-002 |
| SM-ALG-004 | Coordinate transformations and geodetic computation | A | SM-FND-008, SM-COL-001 |
| SM-ALG-005 | Spatial indexing and search structures | A | SM-FND-015, SM-INF-003 |
| SM-ALG-006 | Proximity, neighbourhood and spatial joins | A | SM-ALG-005, SM-ALG-007 |
| SM-ALG-007 | Spatial networks, graph algorithms and routing | A | SM-FND-017, SM-APP-001 |
| SM-ALG-008 | Spatial statistics and point-pattern analysis | A | SM-FND-004, SM-FND-005 |
| SM-ALG-009 | Geostatistics and spatial interpolation | A | SM-FND-004, SM-FND-005 |
| SM-ALG-010 | Raster analysis and map algebra | A | SM-ALG-012, SM-REC-004 |
| SM-ALG-011 | Spatial optimisation and location science | A | SM-FND-002, SM-FND-017 |
| SM-ALG-012 | Terrain analysis and hydrological algorithms | A | SM-FND-003, SM-FND-009 |
| SM-ALG-013 | Image processing, classification and change detection | A | SM-FND-012, SM-FND-014 |
| SM-ALG-014 | Spatial simulation and agent-based modelling | B | SM-FND-019, SM-APP-014 |
| SM-ALG-015 | Spatiotemporal analysis and trajectory computation | B | SM-ALG-007, SM-INF-004 |
| SM-ALG-016 | Point-cloud processing and 3D spatial algorithms | B | SM-COL-006, SM-FND-006 |
| SM-ALG-017 | GeoAI and spatial machine learning | B | SM-FND-004, SM-FND-015, SM-ALG-013 |
| SM-ALG-018 | Spatial uncertainty, error propagation and sensitivity | A | SM-FND-011, SM-FND-016 |
| SM-ALG-019 | Spatial data generalisation and simplification | B | SM-ALG-001, SM-FND-010 |
| SM-ALG-020 | Distributed and large-scale spatial computation | B | SM-INF-001, SM-INF-002, SM-INF-003 |

## 7. Spatial Data Collection (`COL`)

| ID | Subject | Initial priority | Connected subjects |
|---|---|---:|---|
| SM-COL-001 | Geodetic and engineering surveying | A | SM-FND-008, SM-FND-011 |
| SM-COL-002 | GNSS, positioning and navigation systems | A | SM-COL-001, SM-FND-008 |
| SM-COL-003 | Ground control, reference networks and field measurement | A | SM-COL-001, SM-FND-011 |
| SM-COL-004 | Satellite and airborne optical remote sensing | A | SM-FND-012, SM-ALG-013 |
| SM-COL-005 | Hyperspectral and thermal sensing | B | SM-COL-004, SM-FND-012 |
| SM-COL-006 | Radar, SAR and interferometric sensing | B | SM-FND-013, SM-FND-014 |
| SM-COL-007 | Photogrammetry and structure from motion | A | SM-COL-004, SM-ALG-016 |
| SM-COL-008 | LiDAR and laser scanning | A | SM-COL-001, SM-ALG-016 |
| SM-COL-009 | UAV platforms, robotics and autonomous acquisition | B | SM-COL-004, SM-COL-007, SM-COL-008 |
| SM-COL-010 | Mobile mapping and indoor positioning | B | SM-COL-002, SM-COL-008 |
| SM-COL-011 | Field surveys, sampling and ground truth | A | SM-FND-004, SM-FND-011 |
| SM-COL-012 | Environmental, weather and ecological sensor networks | B | SM-FND-020, SM-INF-004 |
| SM-COL-013 | Hydrographic, marine and bathymetric surveying | B | SM-COL-001, SM-FND-013 |
| SM-COL-014 | Geophysical and subsurface measurement | B | SM-FND-020, SM-APP-009 |
| SM-COL-015 | Administrative, census and operational data acquisition | A | SM-REC-001, SM-INF-005 |
| SM-COL-016 | Volunteered geographic information and citizen science | B | SM-COL-011, SM-INF-005 |
| SM-COL-017 | Industrial sensing, telemetry and machine vision | B | SM-FND-013, SM-FND-014 |
| SM-COL-018 | Data fusion, calibration and sensor integration | B | SM-FND-011, SM-FND-014 |
| SM-COL-019 | Experimental, simulated and synthetic spatial data generation | C | SM-ALG-014, SM-FND-019 |
| SM-COL-020 | Emerging collection platforms and measurement technologies | C | Cross-pillar; classify by actual measurement principle |

## 8. Spatial Recipes (`REC`)

Recipes are task-oriented and may combine any of the other pillars. The following are initial workflow families, not a closed list of procedures.

| ID | Workflow family | Initial priority | Connected subjects |
|---|---|---:|---|
| SM-REC-001 | Spatial data discovery, acquisition and ingestion | A | SM-COL-015, SM-INF-005 |
| SM-REC-002 | Data cleaning, schema harmonisation and validation | A | SM-INF-005, SM-ALG-018 |
| SM-REC-003 | CRS selection, transformation and coordinate QA | A | SM-FND-008, SM-ALG-004 |
| SM-REC-004 | Vector and raster preprocessing | A | SM-ALG-002, SM-ALG-010 |
| SM-REC-005 | Spatial database design, loading and querying | A | SM-INF-003, SM-ALG-005 |
| SM-REC-006 | Remote sensing image preparation and analysis | A | SM-COL-004, SM-ALG-013 |
| SM-REC-007 | Photogrammetry and 3D reconstruction workflows | B | SM-COL-007, SM-COL-009 |
| SM-REC-008 | Survey planning, field capture and quality control | A | SM-COL-001, SM-COL-011 |
| SM-REC-009 | Terrain, watershed and flood analysis | A | SM-ALG-012, SM-APP-005 |
| SM-REC-010 | Cartographic design and map production | A | SM-FND-010, SM-INF-006 |
| SM-REC-011 | Network construction, routing and accessibility analysis | A | SM-ALG-007, SM-APP-001 |
| SM-REC-012 | Spatial statistical analysis and geostatistical modelling | B | SM-ALG-008, SM-ALG-009 |
| SM-REC-013 | Site selection and multi-criteria decision analysis | A | SM-ALG-011, SM-APP-004 |
| SM-REC-014 | Spatial machine-learning model development and evaluation | B | SM-ALG-017, SM-FND-004 |
| SM-REC-015 | Spatial ETL, automation and reproducible pipelines | A | SM-INF-001, SM-INF-005 |
| SM-REC-016 | Web GIS, spatial APIs and map application delivery | B | SM-INF-006, SM-INF-007 |
| SM-REC-017 | Spatial quality assurance and accuracy assessment | A | SM-FND-011, SM-ALG-018 |
| SM-REC-018 | Monitoring, change detection and operational reporting | B | SM-ALG-013, SM-APP-003 |
| SM-REC-019 | Spatial simulation and scenario workflow | B | SM-ALG-014, SM-APP-014 |
| SM-REC-020 | Field-to-office data lifecycle and delivery | A | SM-COL-001, SM-COL-011, SM-INF-005 |

## 9. Cross-cutting technical infrastructure (`INF`)

| ID | Subject | Initial priority | Connected subjects |
|---|---|---:|---|
| SM-INF-001 | Programming languages and scientific software engineering | A | SM-FND-015, all pillars |
| SM-INF-002 | Algorithms, data structures and performance engineering | A | SM-FND-015, SM-ALG-005 |
| SM-INF-003 | Spatial databases, storage and indexing infrastructure | A | SM-ALG-005, SM-REC-005 |
| SM-INF-004 | Streaming, event systems and real-time spatial data | B | SM-COL-012, SM-ALG-015 |
| SM-INF-005 | Data engineering, ETL, metadata and provenance | A | SM-REC-001, SM-REC-002 |
| SM-INF-006 | GIS platforms, desktop tools and cartographic software | A | SM-REC-010, SM-REC-016 |
| SM-INF-007 | Web mapping, APIs and geospatial interoperability standards | B | SM-REC-016, SM-INF-005 |
| SM-INF-008 | Cloud, distributed and high-performance geospatial computing | B | SM-ALG-020, SM-INF-003 |
| SM-INF-009 | Open geospatial standards, formats and service specifications | A | All pillars |
| SM-INF-010 | AI, machine-learning frameworks and agent-assisted workflows | B | SM-ALG-017, SM-REC-014 |
| SM-INF-011 | Software testing, reproducibility, CI and version control | A | SM-REC-015, all technical records |
| SM-INF-012 | Data governance, licensing, privacy and security | A | SM-COL-015, SM-INF-005 |

## 10. Application contexts (`APP`)

Applications are connected contexts. Each application may draw on multiple subjects from all four pillars and the infrastructure layer. The list is expandable and does not imply equal depth or general-purpose competence.

| ID | Application context | Initial priority | Typical connections |
|---|---|---:|---|
| SM-APP-001 | Transportation, mobility and logistics | A | SM-ALG-007, SM-ALG-011, SM-REC-011 |
| SM-APP-002 | Agriculture and food systems | B | SM-COL-004, SM-ALG-013, SM-ALG-017 |
| SM-APP-003 | Environment, ecology and conservation | B | SM-COL-012, SM-ALG-009, SM-REC-018 |
| SM-APP-004 | Urban planning, land administration and property | A | SM-ALG-011, SM-REC-013, SM-COL-015 |
| SM-APP-005 | Disaster risk, hazards and emergency management | A | SM-ALG-012, SM-COL-006, SM-REC-009 |
| SM-APP-006 | Energy, utilities and infrastructure networks | B | SM-ALG-007, SM-COL-001, SM-REC-020 |
| SM-APP-007 | Public health and health geography | B | SM-ALG-008, SM-COL-015, SM-REC-012 |
| SM-APP-008 | Mining, geology and natural resources | B | SM-COL-014, SM-COL-006, SM-ALG-013 |
| SM-APP-009 | Water resources, hydrology and coastal systems | B | SM-COL-013, SM-ALG-012, SM-ALG-009 |
| SM-APP-010 | Telecommunications and network infrastructure | B | SM-ALG-007, SM-ALG-011, SM-COL-017 |
| SM-APP-011 | Humanitarian operations and development | B | SM-COL-015, SM-REC-011, SM-REC-013 |
| SM-APP-012 | Insurance, finance and geographic risk | C | SM-ALG-008, SM-ALG-017, SM-REC-018 |
| SM-APP-013 | Maritime, aviation and navigation | C | SM-COL-002, SM-COL-013, SM-ALG-015 |
| SM-APP-014 | Digital twins, simulation and complex systems | C | SM-ALG-014, SM-INF-004, SM-COL-018 |
| SM-APP-015 | Archaeology, heritage and cultural landscapes | C | SM-COL-007, SM-COL-008, SM-ALG-013 |
| SM-APP-016 | Defence, security and intelligence applications | C | SM-COL-006, SM-ALG-015, SM-INF-012 |
| SM-APP-017 | Climate science and Earth observation | B | SM-COL-004, SM-COL-006, SM-ALG-013 |
| SM-APP-018 | Retail, markets and location intelligence | B | SM-ALG-006, SM-ALG-011, SM-REC-013 |

## 11. How to use and extend the index

### Adding a subject

Before adding a new row:

1. Search for an existing subject, alias or broader parent.
2. Decide whether the proposed item is a subject, a canonical technical record, an application context, a tool or a workflow.
3. Assign one primary home.
4. Add cross-links where they explain a meaningful relationship.
5. Assign a stable ID only when the subject is sufficiently distinct.
6. Record its scope and boundaries in a dedicated page when useful.
7. Leave its curation state as **Not mapped** until the scope has actually been investigated.

### Avoiding taxonomy inflation

Do not create a new subject for every algorithm, software package, sensor model, dataset or industry use case. Those belong in the relevant canonical record catalogue and should link back to this subject index.

Create a new subject when it represents a coherent area of inquiry with meaningful boundaries, internal structure or ongoing curation needs.

### Connecting the index to repository content

- The subject index answers: **What areas do we cover, and how do they connect?**
- The coverage matrix answers: **What has been captured, researched, implemented or validated against a particular source?**
- Canonical records answer: **What do we know about this specific method, concept, tool, standard or application?**
- Learning paths and explorations answer: **How can someone navigate and use this knowledge for a particular purpose?**
- Research and implementation records answer: **What has actually been investigated, tested or built?**

These layers should reference one another rather than duplicate one another.

## 12. Initial implementation rule

The index is a map, not a completion target. Do not attempt to fill every row before publishing useful work.

Start with a small connected cluster of high-value subjects, build the source and curation trail, test the navigation, and expand according to actual use. Keep the public material accurate, attributable, appropriately licensed and clear about its validation status.
