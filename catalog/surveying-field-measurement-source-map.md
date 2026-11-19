# Surveying and field measurement — authoritative source map

**Version:** 0.1  
**Status:** Initial source map; sources identified, individual technical claims and jurisdictional applicability not yet reviewed  
**Collection:** Spatial Data Collection, connected to Theoretical Foundations, Spatial Algorithms and Spatial Recipes  
**Related cluster:** [Reference, positioning and measurement](first-curation-cluster-reference-positioning-measurement.md)  
**Subject index:** [Geoinformatics master subject index](master-subject-index.md)

## 1. Purpose

This document establishes a traceable source base for curating surveying and field measurement. It is a source map, not a tutorial, compliance checklist, or claim that the repository already covers the subjects below.

The collection should explain how real-world quantities become defensible spatial data: how a task is specified, a reference framework selected, observations planned and acquired, instruments checked, observations reduced and adjusted, uncertainty assessed, and final data documented and delivered.

The scope is deliberately wider than conventional land surveying. It includes geodetic and engineering surveying, positioning, levelling, control networks, measurement science, field sampling, instrument verification, data capture, and field-to-office integration. Specialist acquisition technologies (for example laser scanning, photogrammetry, hydrographic systems and environmental sensors) remain connected subjects rather than being collapsed into one generic surveying workflow.

## 2. Source-selection and authority model

Sources are classified by what they are authoritative for. No source type is universally authoritative for every question.

| Source class | Primary role | How Spatial Methods should use it | Main caution |
|---|---|---|---|
| Laws, regulations and national specifications | Jurisdiction-specific legal and technical requirements | Establish what is mandatory for a defined place, project and professional activity | Never transfer another country's rules as local law |
| International and national standards | Agreed terminology, procedures, test methods and requirements | Identify normative procedures, scope, edition and status | Abstracts do not replace the full standard; standards may be paywalled |
| National geodetic agencies | Official reference frames, control, datums, geoid models and national procedures | Establish authoritative reference-system and control information for that jurisdiction | Check realisation, epoch, area of validity and current agency notices |
| Professional institutions and technical societies | Professional practice, specifications, guidance and competency context | Translate standards and theory into professional workflows | Guidance is not automatically law or a contractual specification |
| Government engineering manuals | Detailed project methods, field procedures, deliverables and QA | Use as applied technical references and workflow exemplars | Scope and date may be agency-specific; check supersession |
| Textbooks and university texts | Theory, derivations, worked examples and conceptual foundations | Build understanding and compare methods | Edition, assumptions and worked-example conventions matter |
| Manufacturer manuals and calibration documents | Instrument-specific operation, configuration, correction models and maintenance | Document exact equipment workflows and operating limitations | Vendor claims are not independent validation; model and firmware matter |
| Peer-reviewed research and technical reports | New methods, performance evidence, uncertainty models and specialist applications | Investigate contested or emerging techniques | Assess study design, reproducibility, data and external validity |

### Evidence rules

1. Record the issuing body, exact title, identifier, edition/date, stable URL, access date and jurisdiction where relevant.
2. Distinguish a standard's current status from the date of the web page that describes it.
3. Record whether the full document is openly accessible, paywalled, or represented only by an abstract/catalogue page.
4. Do not cite a source for a claim outside its stated scope.
5. Separate instrument precision, measurement repeatability, internal precision estimates, external accuracy, uncertainty and fitness for purpose.
6. Preserve historical editions when needed to explain legacy datasets or workflows, but label them as historical.
7. A source being authoritative does not mean it is the only valid method. Record alternatives and their assumptions.
8. Jurisdiction-specific requirements must be checked before a workflow is presented as suitable for legal cadastral, engineering or construction work.

## 3. Core source register

### A. Measurement science and field verification

| Source | Authority and scope | Main use | Subject links | Access/status notes |
|---|---|---|---|---|
| [ISO 17123-1:2014 — Field procedures for testing geodetic and surveying instruments, Part 1: Theory](https://www.iso.org/standard/64156.html) | ISO standard; general rules for evaluating and expressing measurement uncertainty in field test procedures | Establish the measurement-theory foundation for instrument field tests and the interpretation of repeatability/uncertainty | SM-FND-011, SM-COL-001, SM-COL-002, SM-REC-017 | ISO reports this edition was reviewed and confirmed in 2024; full standard is paid |
| [ISO 17123-5:2018 — Part 5: Total stations](https://www.iso.org/standard/71689.html) | ISO standard; field procedures for evaluating coordinate-measurement precision of total stations and ancillary equipment | Instrument-and-procedure field verification; understand what the test does and does not establish | SM-COL-001, SM-COL-003, SM-REC-008, SM-REC-017 | ISO page says confirmed in 2023; full standard is paid |
| [ISO 17123-8:2015 — Part 8: GNSS field measurement systems in RTK](https://www.iso.org/standard/62961.html) | ISO standard; field procedures for evaluating repeatability of RTK GNSS systems | RTK field verification and quality-control design | SM-COL-002, SM-COL-003, SM-REC-008, SM-REC-017 | ISO page says reviewed and confirmed in 2025; full standard is paid |
| [ISO 17123-11:2025 — Part 11: GNSS instruments](https://www.iso.org/standard/85271.html) | ISO standard; field verification that a GNSS-based system and measurement procedure meets required uncertainty by comparing 3D coordinates with reference coordinates | Newer, technology-independent GNSS field verification source; compare scope with Part 8 rather than treating them as interchangeable | SM-FND-011, SM-COL-002, SM-REC-008, SM-REC-017 | Published July 2025; full standard is paid |

**Curation note:** ISO 17123 parts are not a substitute for a full survey specification, network design, datum realisation or independent project validation. Their stated test scopes must be retained when describing what a field check demonstrates.

### B. Professional GNSS surveying practice

| Source | Authority and scope | Main use | Subject links | Access/status notes |
|---|---|---|---|---|
| [RICS — Use of GNSS in Land Surveying and Mapping, 3rd edition (2023)](https://www.rics.org/profession-standards/rics-standards-and-guidance/sector-standards/land-standards/guidelines-for-the-use-of-gnss-in-land-surveying-and-mapping) | Professional institution guidance; GNSS survey methods, control, errors, coordinate systems, QC and office processing | Strong professional-practice spine for GNSS planning, field procedures, client specifications and processing | SM-COL-002, SM-COL-003, SM-REC-008, SM-REC-017, SM-REC-020 | Published 16 May 2023; check the current RICS page for revisions and terms |
| [RICS GNSS guidelines — 2nd edition PDF](https://www.rics.org/content/dam/ricsglobal/documents/standards/guidelines_for_the_use_of_gnss_in_surveying_and_mapping_2nd_edition_rics.pdf) | Earlier professional guidance | Useful historical comparison for how operational recommendations and QC expectations evolved | SM-COL-002, SM-REC-008 | Superseded by 3rd edition; do not present as current primary guidance |

### C. Control and topographic surveying

| Source | Authority and scope | Main use | Subject links | Access/status notes |
|---|---|---|---|---|
| [USACE EM 1110-1-1005 — Control and Topographic Surveying](https://www.publications.usace.army.mil/portals/76/publications/engineermanuals/em_1110-1-1005.pdf) | US Army Corps of Engineers engineering manual; control/topographic survey planning, reference systems, data collection, processing, deliverables and project examples | Broad applied reference for connecting survey design, field capture, processing and spatial deliverables | SM-COL-001, SM-COL-003, SM-REC-008, SM-REC-017, SM-REC-020 | Dated 1 January 2007; verify current applicability and any superseding guidance before operational use |
| [USACE official Engineer Manuals catalogue](https://www.publications.usace.army.mil/USACE-Publications/Engineer-Manuals/) | Official catalogue of USACE manuals | Verify document identity, publication metadata and related manuals | SM-COL-001, SM-COL-003, SM-COL-008, SM-COL-013 | Catalogue currently lists relevant manuals including control/topographic surveying, monumentation, GNSS, photogrammetric/LiDAR and hydrographic surveying |
| [USACE EM 1110-1-1002 — Survey Markers and Monumentation](https://www.publications.usace.army.mil/USACE-Publications/Engineer-Manuals/) | USACE engineering manual; criteria and guidance for installing and documenting survey monuments | Control point design, monumentation, recovery and metadata | SM-COL-001, SM-COL-003, SM-REC-008, SM-REC-020 | Catalogue lists publication date 1 March 2012; retrieve and inspect the exact manual before detailed use |
| [USACE EM 1110-1-1003 — NAVSTAR GPS Surveying](https://www.publications.usace.army.mil/USACE-Publications/Engineer-Manuals/) | USACE engineering manual; technical specifications and procedural guidance for GPS/GNSS surveying and mapping | GNSS control and project workflow reference; historical agency practice | SM-COL-002, SM-COL-003, SM-REC-008 | Catalogue lists 28 February 2011; check for newer agency guidance and current GNSS constellation coverage |

### D. Levelling and vertical control

| Source | Authority and scope | Main use | Subject links | Access/status notes |
|---|---|---|---|---|
| [NOAA Manual NOS NGS 3 — Geodetic Leveling](https://geodesy.noaa.gov/library/pdfs/NOAA_Manual_NOS_NGS_0003.pdf) | US National Geodetic Survey manual; vertical control, reconnaissance, benchmark setting, geodetic levelling, crossings and field data processing | Detailed primary technical reference for precise levelling and vertical-control field procedures | SM-FND-008, SM-FND-011, SM-COL-001, SM-COL-003, SM-REC-008 | NOAA repository describes an October 2020 revision; US vertical-network context, not a universal specification |
| [NOAA NGS — Geodetic Leveling](https://www.ngs.noaa.gov/leveling/index.shtml) | National Geodetic Survey operational guidance and project submission information | Digital-level specifications, benchmark ties, calibration, misclosure and adjustment workflow | SM-COL-001, SM-COL-003, SM-ALG-018, SM-REC-008, SM-REC-017 | US national programme requirements; use as a technical example, not local legal authority |
| [NOAA repository record — Geodetic Leveling](https://repository.library.noaa.gov/view/noaa/52332) | Official repository metadata for NOS NGS 3 | Verify edition history, authorship, revision information and reuse status | SM-FND-008, SM-COL-001, SM-COL-003 | Repository describes October 2020 revision and CC0 public-domain rights for this record |

### E. Reference frames, datums and geodetic control

The sources above are useful technical starting points, but a complete reference-system collection requires a separate authoritative source stream for:
- International Terrestrial Reference System (ITRS) and realisations (ITRF);
- coordinate epochs, plate motion and time-dependent coordinates;
- national geodetic reference frames and control networks;
- horizontal and vertical datums, height systems and geoid models;
- transformation parameters, grids and area-of-use constraints;
- monument descriptions, station metadata, stability and discontinuities.

Primary source targets for the next source-discovery pass:
- International Association of Geodesy (IAG) and International Earth Rotation and Reference Systems Service (IERS) for geodetic conventions and reference-system definitions.
- International GNSS Service (IGS) for precise products, reference-frame contributions, station information and GNSS conventions.
- National mapping/geodetic agencies for official national frames, control stations, transformation tools and vertical datums.
- ISO 19111 for referencing by coordinates and ISO 19127 for geodetic register concepts, with current editions/status checked directly through ISO.

Do not publish transformation advice from a generic GIS tutorial where an official national transformation or grid is required.

### F. Textbooks and deeper theory — candidates for evaluation

These are candidates for a curated bibliography, not yet individually edition-verified in this register:
- E. M. Mikhail and G. Gracie, *Analysis and Adjustment of Survey Measurements* — observation models, weights, least-squares adjustment and network analysis.
- Standard surveying texts covering elementary measurements, traversing, levelling, total stations, setting out and field practice. Select editions only after bibliographic and content review.
- Geodetic texts covering reference systems, ellipsoids, datums, coordinate transformations and height systems.
- Measurement-science references based on the International Vocabulary of Metrology (VIM) and Guide to the Expression of Uncertainty in Measurement (GUM).

Textbooks should support conceptual learning and worked examples; they should not replace current jurisdictional specifications or standards.

### G. Instrument manuals and manufacturer documentation

A later instrument-specific register should capture manuals and technical documents from the actual equipment families being studied or used, for example:
- total stations and robotic total stations;
- digital, automatic and precise levels;
- GNSS receivers, antennas and controllers;
- laser scanners and mobile mapping systems;
- field data collectors and survey-processing software.

For every instrument record: manufacturer, model, hardware revision, firmware/software version, manual revision, supported measurement modes, calibration/adjustment procedures, environmental limits, correction settings, export formats and known limitations.

Manufacturer documents explain how a particular system is operated. They do not independently establish that a project achieved its required accuracy.

## 4. Source-to-subject map

The initial subject mapping is:

| Subject ID | Subject | Source families to prioritise |
|---|---|---|
| SM-FND-008 | Geodesy and reference systems | IAG, IERS, IGS, national geodetic agencies, ISO 19111, NOAA NGS |
| SM-FND-011 | Measurement science, accuracy and uncertainty | ISO 17123-1, VIM, GUM, peer-reviewed metrology and surveying literature |
| SM-FND-016 | Numerical analysis and scientific computing | Least-squares texts, numerical methods references, adjustment literature |
| SM-ALG-004 | Coordinate transformations and geodetic computation | ISO 19111, national transformation documentation, IERS/IAG conventions |
| SM-ALG-018 | Spatial uncertainty, error propagation and sensitivity | ISO 17123, GUM, adjustment texts, NGS levelling documentation |
| SM-COL-001 | Geodetic and engineering surveying | USACE control/topographic manual, textbooks, national surveying specifications |
| SM-COL-002 | GNSS, positioning and navigation systems | RICS GNSS guidance, ISO 17123-8/-11, IGS, national geodetic agencies |
| SM-COL-003 | Ground control, reference networks and field measurement | USACE control and monumentation manuals, NGS, national control authorities |
| SM-COL-011 | Field surveys, sampling and ground truth | Project-specific professional guidance, statistical sampling references and domain standards |
| SM-REC-008 | Survey planning, field capture and quality control | RICS, USACE, ISO 17123, national specifications and instrument manuals |
| SM-REC-017 | Spatial quality assurance and accuracy assessment | ISO 17123, GUM, NGS, professional specifications and independent check procedures |
| SM-REC-020 | Field-to-office data lifecycle and delivery | USACE project workflows, RICS processing guidance, national deliverable specifications |
| SM-INF-005 | Data engineering, ETL, metadata and provenance | Survey data formats, national station metadata, instrument export specifications and geospatial metadata standards |
| SM-INF-009 | Open geospatial standards, formats and service specifications | ISO/OGC specifications and authoritative format documentation |

This mapping is an initial classification. It does not imply that each source covers every listed subject or that the subjects are fully curated.

## 5. Collection structure to build from this source map

The source map should lead to a connected set of subject collections, not one enormous surveying chapter:

1. **Measurement principles:** measurands, observation models, units, systematic and random effects, precision, accuracy, uncertainty, traceability and fitness for purpose.
2. **Reference and control:** reference frames, datums, epochs, control design, monumentation, reconnaissance, network geometry and station metadata.
3. **Conventional field measurement:** distances, angles, bearings, traversing, total stations, levelling, profiles, setting out and field booking.
4. **GNSS field surveying:** static, rapid static, differential, RTK, network RTK and PPP; observation planning, antenna models, multipath, atmospheric effects, ambiguity status and independent checks.
5. **Adjustment and analysis:** reductions, corrections, weights, least squares, network adjustment, residual analysis, outlier investigation, covariance and uncertainty propagation.
6. **Instrument verification and calibration:** field tests, calibration records, environmental effects, instrument/target setup and instrument-specific limitations.
7. **Field data management:** coding, metadata, naming, observations, raw-data preservation, coordinate transformations, QA flags, provenance and export.
8. **Integrated delivery:** survey control and topographic capture into GIS, CAD, engineering models, spatial databases and documented client deliverables.

Specialist branches—hydrographic surveying, deformation monitoring, cadastral surveying, construction setting-out, mobile mapping, laser scanning and subsurface measurement—should be connected where their measurement principles and workflows warrant it.

## 6. Important boundaries and quality distinctions

- **Precision is not accuracy.** Repeatability under a test does not by itself establish closeness to the true or accepted reference value.
- **A coordinate is incomplete without its reference context.** CRS, datum, epoch, height type, units, axis order and transformation history may be essential.
- **A control point is not merely a coordinate pair.** Its monument, description, reference framework, observation history, uncertainty and stability matter.
- **GNSS solution status is not a complete quality statement.** Fixed ambiguities or a small receiver-reported precision estimate do not replace independent checks and project-level uncertainty assessment.
- **Network adjustment is not a cosmetic post-processing step.** It depends on a defensible observation model, stochastic model, constraints, weights and diagnostic review.
- **Instrument checks are scoped tests.** State what was tested, under what conditions, against which reference, and which performance properties were not assessed.
- **A field-to-office workflow must preserve raw observations and provenance.** Do not overwrite raw observations with corrected or transformed outputs.
- **Legal cadastral and engineering work requires jurisdiction-specific requirements and qualified professional oversight.** Educational examples must not be represented as authority to certify regulated surveys.

## 7. Geographic and jurisdictional strategy

The source map currently includes international standards and selected US/UK professional and government sources because they expose useful technical procedures. They are not a substitute for Kenyan authority.

Before publishing Kenya-specific operational guidance, establish a dedicated local source register covering:
- Survey of Kenya and the responsible national mapping/geodetic authorities;
- applicable survey, land registration and professional practice legislation and regulations;
- official national coordinate reference systems, control networks, benchmarks, vertical datum and transformation guidance;
- professional requirements and applicable engineering/client specifications;
- data licensing, access conditions and restrictions on cadastral or control information.

The applicable current Kenyan documents have not yet been confirmed in this source map. Do not infer local compliance from the foreign manuals listed above.

## 8. Curation workflow and acceptance criteria

For each source:
1. Verify title, issuer, edition, publication/revision date and current status.
2. Read the scope and exclusions, not just the title or search snippet.
3. Extract the concepts, procedures, assumptions, equations, quality criteria and deliverables relevant to the subject.
4. Compare with at least one independent authoritative source where the claim is consequential.
5. Record jurisdiction and equipment/software dependencies.
6. Identify what the source does not establish.
7. Link the source to stable subject IDs and to the specific canonical records it supports.
8. Record rights and permitted reuse before reproducing figures, tables or substantial text.

A subject should not be marked **Curated** until its scope, major branches, source hierarchy, important distinctions and unresolved questions are documented. A workflow should not be marked **Implemented** or **Validated** without reproducible field or simulated evidence appropriate to its claims.

## 9. Immediate next work

The next pass should deepen the source map in this order:

1. Identify the authoritative IAG/IERS/IGS references for reference frames, coordinate epochs and geodetic conventions.
2. Establish the current Kenyan legal and national geodetic source set, distinguishing verified local requirements from international technical references.
3. Retrieve and inspect the full USACE control, monumentation and GNSS manuals and the NOAA levelling manual.
4. Build the surveying textbook bibliography with edition-level verification.
5. Create an instrument-document register only when actual equipment families are selected.
6. Then begin the first technical synthesis: measurement principles and field verification, before producing instrument-specific tutorials.

**Current state:** sources identified for initial measurement science, total-station and GNSS field verification, professional GNSS practice, control/topographic surveying and precise levelling. Reference-frame, Kenyan jurisdictional, textbook and instrument-specific source streams remain open.
