# First curation cluster — reference, positioning and measurement

**Version:** 0.1  
**Status:** Existing-asset crosswalk; gap analysis is preliminary  
**Cluster:** Geodetic reference, positioning, field measurement, uncertainty and spatial data quality  
**Primary index:** [Geoinformatics master subject index](master-subject-index.md)  
**Alignment method:** Direct inspection of selected learning-path, lesson, method and package README files, plus repository path inventory.

## 1. Why this cluster comes first

This cluster connects mathematical foundations to real-world measurement and dependable spatial data. It is useful across surveying, engineering, mapping, transport, infrastructure, environmental monitoring, remote sensing and field research.

It is also a practical test of the four-pillar architecture: theory, algorithms, data acquisition and repeatable procedures must connect without being collapsed into one category.

## 2. Subject coverage and existing assets

The statuses below describe the **repository evidence inspected for this cluster**, not the user's personal mastery or the entire state of the discipline.

| Subject ID | Subject | Existing repository assets | Preliminary assessment |
|---|---|---|---|
| SM-FND-008 | Geodesy and reference systems | [Geodesy foundations path](../learning-paths/geodesy-foundations.md); [CRS transformation](../algorithms/geodesy/crs-transformation.md); [ECEF and ENU](../algorithms/geodesy/ecef-enu.md); [Helmert seven-parameter method](../methods/helmert-7-parameter.md) | Partial foundation exists; reference-frame realisations, coordinate epochs, vertical datums, geoid models and operation selection need deeper coverage |
| SM-FND-011 | Measurement science, accuracy and uncertainty | [Accuracy assessment package](../implementations/python/accuracy-assessment/README.md); [uncertainty propagation package](../implementations/python/uncertainty-propagation/README.md); [uncertainty propagation verification record](verification/uncertainty-propagation.md) | Useful applied assets exist; broader metrology, traceability, calibration, error budgets and uncertainty theory need a dedicated foundation |
| SM-FND-015 | Computer science, algorithms and complexity | Existing tested code packages, tests and repository CI | Enabling infrastructure exists; a coherent subject-level foundation and spatial-computation performance guide are not established by this audit |
| SM-ALG-004 | Coordinate transformations and geodetic computation | [CRS transformation](../algorithms/geodesy/crs-transformation.md); [ECEF–ENU](../algorithms/geodesy/ecef-enu.md); [geodesy foundations path](../learning-paths/geodesy-foundations.md); [CRS transform package](../implementations/python/crs-transform/README.md) | Several concrete lessons and implementations exist; coverage remains scoped, not comprehensive |
| SM-ALG-018 | Spatial uncertainty, error propagation and sensitivity | [Uncertainty propagation package](../implementations/python/uncertainty-propagation/README.md); [accuracy assessment package](../implementations/python/accuracy-assessment/README.md) | Applied baseline exists; spatially correlated errors, covariance propagation, stochastic adjustment and sensitivity analysis need a broader map |
| SM-COL-001 | Geodetic and engineering surveying | Existing adjacent geodesy, GNSS, affine georeferencing and field-sampling material | **Major gap:** no coherent survey-methods collection was confirmed in the inspected paths; total stations, levelling, traversing, control networks, field procedures and adjustment need investigation |
| SM-COL-002 | GNSS, positioning and navigation systems | [GNSS dual-frequency combinations](../methods/gnss-dual-frequency-combinations.md); [integer ambiguity resolution](../methods/gnss-integer-ambiguity-resolution.md); [GNSS RAIM/FDE baseline](../methods/gnss-residual-raim-fde.md); [GNSS ambiguity package](../implementations/python/gnss-ambiguity/README.md); [GNSS RAIM package](../implementations/python/gnss-raim/README.md); associated GNSS notebooks and verification records | Substantial bounded educational coverage exists; not a raw-observation PPP/RTK processor or production integrity system |
| SM-COL-003 | Ground control, reference networks and field measurement | [Affine georeferencing](../methods/affine-georeferencing.md); [Helmert transformation](../methods/helmert-7-parameter.md); [ECEF–ENU](../algorithms/geodesy/ecef-enu.md) | Partial adjacent coverage; field control design, monumentation, network adjustment and field measurement procedures need investigation |
| SM-REC-003 | CRS selection, transformation and coordinate QA | [Geodesy foundations path](../learning-paths/geodesy-foundations.md); [CRS lesson](../algorithms/geodesy/crs-transformation.md); [CRS transform package](../implementations/python/crs-transform/README.md); [CRS notebook](../notebooks/crs-transformation-lab.ipynb) | A useful reproducible workflow exists; production operation selection and complete dataset/raster transformation workflows need expansion |
| SM-REC-008 | Survey planning, field capture and quality control | [Adaptive sampling methods](../methods/adaptive-spatial-sampling.md); [adaptive and Bayesian sampling](../methods/adaptive-and-bayesian-spatial-sampling.md); sampling notebooks | Adjacent sampling methods exist; they do not substitute for a complete field-survey planning and capture recipe |
| SM-REC-017 | Spatial quality assurance and accuracy assessment | [Accuracy assessment package](../implementations/python/accuracy-assessment/README.md); [uncertainty propagation package](../implementations/python/uncertainty-propagation/README.md) | Partial applied coverage; domain-specific acceptance criteria, positional QA, independent checkpoints and reporting need deeper treatment |
| SM-INF-005 | Data engineering, ETL, metadata and provenance | Repository source inventory, coverage matrix, source verification protocol and package-level reproducibility conventions | Governance/provenance infrastructure exists; a reusable spatial ETL and metadata engineering knowledge collection needs mapping |
| SM-INF-009 | Open geospatial standards, formats and service specifications | CRS/PROJ and coordinate-operation references appear in existing lessons | **Major gap:** standards, data-format interoperability and OGC service/API coverage were not established as a coherent collection in this pass |
| SM-INF-011 | Software testing, reproducibility, CI and version control | Package tests, notebooks and repository CI; package READMEs document test commands and bounded contracts | Implementation infrastructure exists; create a concise public guide connecting reproducible geospatial research, environments, test data and CI |

## 3. GNSS scope boundaries to preserve

The GNSS material has several distinct components. Do not merge them into a generic “GNSS algorithm” page.

- Dual-frequency combinations form observables with different noise, ionosphere and bias behaviour.
- Geometry-free and Melbourne–Wübbena cycle-slip screens are complementary detection baselines, not interchangeable detectors and not integer slip repair.
- Integer least-squares search consumes a supplied float ambiguity vector and covariance. It does not estimate those quantities from raw observations.
- LAMBDA decorrelation and conditional search are distinct from the basic Cholesky sphere-enumeration baseline.
- The residual RAIM/FDE package is a bounded snapshot linear-model exercise, not certified aviation RAIM/ARAIM and not a complete navigation processor.

These limits are documented in the relevant method and package READMEs and must travel with any future learning path or public summary.

## 4. Confirmed and provisional links

The following are direct file relationships inspected in this pass:

| Canonical subject/lesson | Supporting asset | Relationship |
|---|---|---|
| CRS transformation | `implementations/python/crs-transform/` | Lesson links to package; package README links back to lesson |
| CRS transformation | `notebooks/crs-transformation-lab.ipynb` | Learning path links to the notebook |
| Geodesy foundations | `methods/helmert-7-parameter.md` | Learning path explicitly connects Helmert method |
| Helmert method | `implementations/python/helmert-7-parameter/` | Learning path links to tested Position Vector implementation |
| Affine georeferencing | `implementations/python/affine-georeferencing/` | Learning path links to least-squares example |
| GNSS dual-frequency and ambiguity methods | `implementations/python/gnss-ambiguity/` | Method and package README describe the shared bounded components |
| GNSS residual RAIM/FDE | `implementations/python/gnss-raim/` | Method and package README describe the same bounded snapshot baseline |
| Uncertainty propagation | `implementations/python/uncertainty-propagation/` | Package provides a reproducible applied baseline |

These are inspected documentation relationships. They do not, by themselves, certify source completeness, scientific validity or production suitability.

## 5. Gaps to investigate before creating new material

The initial audit suggests these priorities:

1. **Surveying foundations and field practice:** measurement principles, control establishment, total stations, traversing, levelling, GNSS field workflows, network adjustment and field QA.
2. **Reference frames and vertical positioning:** reference-frame realisations, epochs, tectonic motion, vertical datums, geoid/quasigeoid models and height systems.
3. **Metrology and uncertainty:** traceability, calibration, systematic/random errors, covariance, adjustment, uncertainty budgets and acceptance testing.
4. **GNSS systems engineering:** observation models, receiver/satellite errors, positioning modes, RTK/Network RTK, PPP, integrity and field operating constraints.
5. **Geospatial data quality engineering:** positional/thematic/completeness/temporal consistency, independent validation, lineage and fitness for purpose.
6. **Standards and interoperability:** OGC/ISO standards, CRS encodings, GeoPackage, GeoParquet, Cloud Optimized GeoTIFF, STAC and relevant service/API specifications.
7. **Field-to-office recipes:** planning, acquisition, metadata, transfer, validation, processing, delivery and archiving.

These are candidate gaps based on the files inspected, not claims that no related material exists anywhere in the repository. A wider file-level search should precede new pages.

## 6. Recommended first curation sprint

Do not begin by writing seven new tutorials. First build an evidence-backed map of the cluster:

1. Inspect the existing geodesy and GNSS records, source citations, tests and notebooks.
2. Map each record to its primary and secondary subject IDs.
3. Identify the missing theoretical foundations and field procedures.
4. Select authoritative standards, textbooks, professional guidance and primary literature.
5. Produce one integrated field-to-office reference workflow.
6. Test at least one complete path using real or responsibly sourced sample data, documenting accuracy, uncertainty and limitations.

The first applied capstone should be a **survey-to-spatial-dataset workflow**: plan a small field capture, establish reference/control requirements, collect observations, process and transform coordinates, validate against independent checks, attach metadata and deliver a reusable spatial dataset.

This capstone should be designed only after its measurement method, equipment assumptions, data availability and validation plan are specified. It is not yet a claim that a field campaign has been conducted.

## 7. Completion criteria for this cluster

The cluster is ready for a meaningful first release when:

- Each included subject has a scope statement and authoritative source trail.
- Existing lessons, packages and notebooks have explicit subject mappings.
- Surveying and field measurement coverage has been researched rather than inferred from adjacent GNSS material.
- At least one end-to-end workflow is reproducible.
- Accuracy and uncertainty are reported with suitable independent checks.
- Operational limitations, equipment assumptions, safety considerations and data rights are explicit.
- Public explanations distinguish educational baselines from professional or safety-critical systems.

**Current status:** the cluster has usable geodesy, coordinate-transformation, GNSS and uncertainty assets. Surveying/field practice, reference-frame depth, geospatial standards and end-to-end field workflows remain the highest-value gaps to investigate.
