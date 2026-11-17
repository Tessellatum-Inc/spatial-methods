# Section 21 atomic completion register

**Source:** *Spatial Analysis Algorithms: Complete Compendium*, Section 21, pages 43–45.  
**Intake:** [preserved page transcription](../source-inventory/pages-41-47.md).  
**Section index:** [Section 21 catalogue record](../catalog/sections/21-neural-fields-climate-accounting-robust-geometry.md).

> The source explicitly says the names are from memory and should be verified before citation. This register decomposes the intake wording; it does not authenticate every named model, establish that every item is a standalone algorithm, or claim completion.

## Status and acceptance policy

Use the source-entry verification protocol in `catalog/verification-protocol.md`. A related package is only partial evidence for the specific functionality it implements. Keep identity, bibliography, technical claims, implementation/reproduction and rights separate. Do not mark a row complete until the evidence and teaching gates are satisfied.

| Status | Meaning |
|---|---|
| Open | No item-specific independent verification or implementation is recorded here. |
| Partial | A related implementation or record exists, but it covers only part of the item or its grouped variants. |
| Verify | The source label is ambiguous, version-sensitive or a named project/model must be resolved before implementation. |
| Not applicable | The item is a framework, workflow or application rather than a standalone algorithm; document it accurately instead. |

## Atomic source register

### Neural fields and implicit representations — page 43

| ID | Atomic item | Kind | Evidence/status | Required completion work |
|---|---|---|---|---|
| S21-NF-01 | SIREN coordinate networks | Neural implicit representation | Verify | Resolve exact paper/version; document periodic activation, initialization and derivative behaviour; reproduce a small coordinate-field task. |
| S21-NF-02 | Fourier-feature coordinate networks | Neural representation / encoding | Verify | Distinguish random Fourier features from positional encodings; verify bandwidth and spectral-bias claims; test coordinate regression. |
| S21-NF-03 | Multiresolution hash-grid encoding (Instant-NGP family) | Spatial encoding / acceleration structure | Verify | Verify paper and implementation details; document level resolution, interpolation, hash collisions and parameter scaling; benchmark a bounded reproduction. |
| S21-NF-04 | Location-conditioned implicit neural representations | Neural field model | Open | Define conditioning variables and target field; distinguish coordinate input from location metadata; test interpolation and extrapolation. |
| S21-NF-05 | Satellite NeRF (S-NeRF) | Remote-sensing neural rendering | Verify | Resolve exact title/authors and sensor geometry; record radiometric, atmospheric and acquisition assumptions; reproduce only with licensed data. |
| S21-NF-06 | Earth-observation NeRF (EO-NeRF) | Remote-sensing neural rendering | Verify | Identify exact paper/model rather than treating acronym as unique; document multi-view and temporal assumptions. |
| S21-NF-07 | SatNeRF | Satellite neural rendering | Verify | Confirm canonical paper/repository and variant; test view synthesis and geometry claims independently. |
| S21-NF-08 | Gaussian splatting for satellite imagery | 3D scene representation | Open | Separate 3D Gaussian Splatting core from satellite-specific adaptations; define camera model, georeferencing and evaluation. |
| S21-NF-09 | Shadow-aware radiance fields | Neural rendering / illumination modelling | Open | Identify the intended method family; define shadow/illumination decomposition and test ambiguity under limited views. |
| S21-NF-10 | Implicit digital elevation models | Continuous terrain representation | Open | Define field parameterisation, vertical datum, interpolation and uncertainty; compare against held-out elevation samples. |
| S21-NF-11 | Neural compression of reanalysis and model output | Learned scientific-data compression | Open | Specify tensor/grid/time layout, lossy metric and conservation constraints; report rate-distortion and downstream forecast impacts. |
| S21-NF-12 | Continuous-resolution surface models | Continuous spatial field | Open | Resolve whether this means neural implicit surfaces or another representation; define scale consistency and validation. |

### Climate and Earth-system machine learning — page 43

| ID | Atomic item | Kind | Evidence/status | Required completion work |
|---|---|---|---|---|
| S21-CL-01 | Spherical Fourier Neural Operator (SFNO) | Spherical neural operator | Verify | Verify primary publication and exact architecture; document spherical transform, truncation and grid conventions; compare on a reproducible benchmark. |
| S21-CL-02 | ACE-style atmosphere emulators | Earth-system emulator | Verify | Resolve exact model/version and acronym; record training data, forcing, rollout horizon and conservation diagnostics. |
| S21-CL-03 | Ocean emulators | Earth-system emulator | Open | Do not treat as one method; identify model family, state variables, boundary/forcing conditions and benchmark. |
| S21-CL-04 | Subseasonal ML forecasting | Forecasting task / model family | Open | Define lead-time range, target, baselines, hindcast protocol and probabilistic skill metrics. |
| S21-CL-05 | Seasonal ML forecasting | Forecasting task / model family | Open | Distinguish seasonal initialisation, hindcast calibration and verification; report skill by lead and region. |
| S21-CL-06 | Diffusion-based data assimilation | Generative data assimilation | Open | Identify specific formulation; define prior, observation operator, likelihood and posterior sampling; test on a known linear-Gaussian case. |
| S21-CL-07 | Ensemble-free assimilation with generative priors | Data assimilation framework | Verify | Resolve whether this is a distinct method or umbrella description; define uncertainty representation and calibration tests. |
| S21-CL-08 | Learned subgrid parameterisations | ML physical parameterisation | Open | Define resolved/unresolved variables and coupling interval; test stability, conservation and out-of-distribution forcing. |
| S21-CL-09 | Learned convection schemes | ML parameterisation | Open | Identify target physical scheme and model resolution; assess conservation, extremes and coupled-model stability. |
| S21-CL-10 | Stochastic parameterisations | Stochastic modelling | Open | Separate classical stochastic schemes from learned variants; define conditional distribution and calibration. |
| S21-CL-11 | Hybrid ML–physics coupling stability checks | Model validation / stability diagnostics | Open | Define stability criteria, integration scheme and failure modes; test long rollouts and conservation under perturbation. |

### Land-change accounting — page 44

| ID | Atomic item | Kind | Evidence/status | Required completion work |
|---|---|---|---|---|
| S21-LC-01 | Intensity analysis (Aldwaik–Pontius) | Land-change accounting method | Partial | Verify original method and equations; test interval-level category and transition intensities against published examples. |
| S21-LC-02 | Net versus swap change decomposition | Change accounting | Partial | Verify definitions and units; add independent fixtures with balanced gains/losses and zero-net swap. |
| S21-LC-03 | Gain–loss decomposition | Change accounting | Partial | Verify class/transition accounting and consistency identities; test persistence and cross-class flows. |
| S21-LC-04 | Land-cover transition matrices | Categorical change summary | Partial | Document class ordering, NoData and area weighting; test conservation and unequal cell-area handling. |
| S21-LC-05 | Land-change trajectory analysis | Multi-date categorical analysis | Open | Define trajectory encoding, temporal gaps and class harmonisation; test known multi-epoch sequences. |
| S21-LC-06 | Legend harmonisation / LCCS-style crosswalks | Classification ontology / crosswalk | Open | Verify framework and version; represent one-to-many mappings and uncertainty without silently collapsing classes. |
| S21-LC-07 | Class-hierarchy mapping | Semantic classification mapping | Open | Define hierarchy and aggregation rules; test non-bijective mappings and conservation of mapped area. |
| S21-LC-08 | Semantic harmonisation across land-cover products | Data harmonisation workflow | Open | Document source legends, temporal/sensor differences and provenance; provide an auditable crosswalk workflow. |
| S21-LC-09 | Cramér's V for map association | Association statistic | Partial | Added uncorrected Cramér's V for rectangular non-negative integer contingency tables, zero-margin handling, independence/perfect-association fixtures and explicit effect-size caveat; inferential uncertainty remains outside this function. |
| S21-LC-10 | Mean absolute error of class areas | Area comparison metric | Partial | Added class-area MAE with explicit class ordering/units and optional non-negative class weights; tests cover analytic, zero and invalid cases. Sampling-design uncertainty and area-adjusted estimators remain open. |
| S21-LC-11 | Pontius quantity disagreement | Map comparison metric | Partial | Added a named public function and independent analytic fixtures; defined against reference-row/prediction-column confusion counts. Primary-source and sampling-design interpretation review remain open. |
| S21-LC-12 | Pontius allocation disagreement | Map comparison metric | Partial | Added a named public function and identity tests showing quantity plus allocation disagreement equals 1 minus overall accuracy for the stated count convention; primary-source review remains open. |

### Ecosystem accounting — page 44

| ID | Atomic item | Kind | Evidence/status | Required completion work |
|---|---|---|---|---|
| S21-EA-01 | SEEA Ecosystem Accounting extent accounts | Statistical accounting framework | Verify | Use official UN framework/version; define ecosystem types, spatial units and account tables. |
| S21-EA-02 | Ecosystem condition accounts | Statistical accounting framework | Verify | Define condition variables, reference conditions, indicators and aggregation limitations. |
| S21-EA-03 | Ecosystem-service supply–use tables | Accounting framework / tabulation | Open | Define service classifications, provider/user dimensions and spatial flow conventions. |
| S21-EA-04 | Natural-capital valuation | Valuation framework | Open | Separate monetary/non-monetary valuation approaches; document exchange values, welfare values and assumptions. |
| S21-EA-05 | Spatial ecosystem-service flow models | Spatial flow model | Open | Define source, sink, beneficiary and flow impedance; validate against independent service-flow evidence. |

### Urban design analytics — page 44

| ID | Atomic item | Kind | Evidence/status | Required completion work |
|---|---|---|---|---|
| S21-UR-01 | Floor-space index (FSI) | Urban density metric | Open | Define numerator/denominator, gross/net parcel area and floor inclusion rules; test boundary cases. |
| S21-UR-02 | Ground-space index (GSI) | Urban coverage metric | Open | Define building footprint and site-area conventions; test overlapping footprints and parcel edges. |
| S21-UR-03 | Spacematrix | Urban form classification framework | Verify | Verify canonical framework and metric definitions; document typology thresholds and context dependence. |
| S21-UR-04 | View-corridor analysis | Visibility / urban design analysis | Open | Define observer, target, corridor geometry and occlusion model; validate against synthetic buildings. |
| S21-UR-05 | Viewshed analysis for urban design | Visibility analysis | Partial | Distinguish raster viewshed from 3D building-aware analysis; document observer/target heights and resolution. |
| S21-UR-06 | Daylight computation | Building environmental simulation | Open | Identify daylight metric and simulation standard; define sky model, material assumptions and geometry requirements. |
| S21-UR-07 | Sunlight-hour computation | Solar exposure analysis | Open | Define time period, location, obstruction geometry and sun-position algorithm; compare against analytic cases. |
| S21-UR-08 | Transit-oriented development indices | Urban accessibility / policy metric | Open | Identify exact index variants; define transit service, walking catchment and density/diversity measures. |
| S21-UR-09 | Street-connectivity metrics | Network morphology metric | Open | Separate intersection density, link-node ratio, circuity and centrality; define graph cleaning rules. |
| S21-UR-10 | Block-morphology metrics | Urban morphology analysis | Open | Define block boundaries and compactness/shape metrics; test topology and scale sensitivity. |
| S21-UR-11 | Morphological tessellation | Urban morphology / spatial partition | Verify | Resolve method and implementation identity; define seed features, partition geometry and edge treatment. |

### Robust geometric computation — page 44

| ID | Atomic item | Kind | Evidence/status | Required completion work |
|---|---|---|---|---|
| S21-RG-01 | Exact orientation predicate | Geometric predicate | Partial | Existing rational reference is not Shewchuk's adaptive expansion algorithm; document exact scope and independent degeneracy fixtures. |
| S21-RG-02 | Adaptive exact predicates (Shewchuk) | Robust geometric predicate | Verify | Verify paper and public-domain implementation; implement or explicitly wrap a versioned reference with adversarial near-degenerate tests. |
| S21-RG-03 | Exact arithmetic for geometric computation | Arithmetic strategy | Partial | Distinguish rational, integer and expansion arithmetic; document growth/performance and supported constructions. |
| S21-RG-04 | Interval arithmetic for geometry | Certified numerical method | Open | Define outward rounding and interval semantics; test containment of exact rational results. |
| S21-RG-05 | Floating-point robustness in overlay | Computational geometry robustness | Partial | Separate predicate robustness from construction robustness; differential tests on nearly coincident/overlapping polygons. |
| S21-RG-06 | Floating-point robustness in triangulation | Computational geometry robustness | Partial | Test orientation/incircle degeneracies, cocircularity and reproducibility; identify exact/adaptive kernel boundaries. |
| S21-RG-07 | Snapping strategies | Precision / topology operation | Partial | Define snap tolerance and reference grid; test topology changes and displacement bounds. |
| S21-RG-08 | Tolerance handling | Numerical policy | Partial | State units, scale dependence and propagation; reject implicit coordinate-unit assumptions. |
| S21-RG-09 | Topological robustness | Computational geometry property | Partial | Define validity invariants and failure taxonomy; test overlays, ring closure and self-intersection cases. |
| S21-RG-10 | Simulation of simplicity | Degeneracy resolution technique | Verify | Verify formal perturbation scheme and ordering; test degeneracies without changing non-degenerate outcomes. |
| S21-RG-11 | JTS precision models | Library precision model | Verify | Pin JTS version and semantics; distinguish floating, floating-single and fixed precision behaviour. |
| S21-RG-12 | GEOS precision models | Library precision model | Verify | Pin GEOS version/API and compare precision reduction, snapping and overlay semantics. |

### Time-dependent datums and vertical reference — page 44

| ID | Atomic item | Kind | Evidence/status | Required completion work |
|---|---|---|---|---|
| S21-GD-01 | Dynamic geodetic datums | Reference-frame concept | Verify | Use authoritative geodetic definitions; distinguish datum, frame, realisation and epoch. |
| S21-GD-02 | Plate-motion models | Geodetic velocity model | Open | Identify model and validity region/epoch; test coordinate propagation and uncertainty. |
| S21-GD-03 | ITRF realisations and coordinate epochs | Terrestrial reference frame | Verify | Identify realisation and official transformation parameters; document epoch propagation. |
| S21-GD-04 | NAD83 coordinate epoch handling | Datum/frame operation | Verify | Identify NAD83 realisation and epoch; avoid generic NAD83 labels where precision matters. |
| S21-GD-05 | HTDP transformations | Geodetic transformation software | Verify | Verify NOAA release, supported frames and deformation models; reproduce official control examples. |
| S21-GD-06 | NADCON transformations | Datum transformation software/model | Verify | Identify NADCON version/grid family and region; test official control points and grid availability. |
| S21-GD-07 | Geoid-based orthometric heights (GEOID18 family) | Vertical datum/geoid model | Verify | Verify model version, units and area; distinguish geoid undulation from vertical datum realisation. |
| S21-GD-08 | VERTCON transformations | Vertical datum transformation | Verify | Verify version and coverage; test official benchmark transformations. |
| S21-GD-09 | Tidal vertical datums | Vertical reference system | Verify | Identify datum and tidal epoch/constituents; document local/regional coverage and conversion limitations. |
| S21-GD-10 | Ellipsoidal-to-orthometric height conversion | Height transformation | Open | Define (H=h-N), geoid model, sign and units; test known control values. |
| S21-GD-11 | Velocity-field interpolation for coordinate updates | Geodetic interpolation | Open | Define vector components, reference epoch, interpolation domain and uncertainty; test synthetic known fields. |

### Semantic maps and spatial AI for robotics and AR — page 44

| ID | Atomic item | Kind | Evidence/status | Required completion work |
|---|---|---|---|---|
| S21-SM-01 | Hydra-style 3D scene graphs | Scene graph / software framework | Verify | Identify intended Hydra project/version; document graph schema and spatial semantics. |
| S21-SM-02 | Topological maps | Spatial representation | Open | Define nodes/edges, adjacency and metric attributes; test connectivity preservation. |
| S21-SM-03 | Hierarchical maps | Spatial representation | Open | Define levels, aggregation and cross-level links; test consistency under updates. |
| S21-SM-04 | Semantic SLAM | Robotics mapping framework | Open | Separate SLAM backend from semantic perception; define data association and map update evaluation. |
| S21-SM-05 | ConceptFusion | Open-vocabulary 3D mapping | Verify | Verify primary paper/repository; document feature fusion and language-query evaluation. |
| S21-SM-06 | CLIP-Fields | Language-aligned neural field | Verify | Verify exact method and version; define field representation, training observations and retrieval tests. |
| S21-SM-07 | VLMaps | Vision-language mapping | Verify | Verify primary source and code; document map construction, grounding and navigation evaluation. |
| S21-SM-08 | Visual positioning systems | Visual localisation system | Open | Distinguish image retrieval, feature matching and learned localisation; report spatial/temporal accuracy. |
| S21-SM-09 | Geo-anchors | AR spatial anchoring | Verify | Identify platform/specification and coordinate frame; document persistence, accuracy and drift. |
| S21-SM-10 | Street-level localisation for AR | Localisation workflow | Open | Define camera/sensor inputs, urban canyon failure modes and geodetic output accuracy. |
| S21-SM-11 | Digital-twin synchronisation | Distributed systems workflow | Open | Define identity, event ordering, temporal consistency and conflict resolution; do not present as one algorithm. |
| S21-SM-12 | Lane-level HD maps | Mapping data model / workflow | Open | Define lane topology, attributes, localisation frame and update provenance. |
| S21-SM-13 | HD-map change detection | Map maintenance method | Open | Define change classes, temporal alignment and confidence; evaluate false changes. |
| S21-SM-14 | Crowdsourced map maintenance | Data integration workflow | Open | Define contributor trust, conflation, conflict resolution and audit trail. |
| S21-SM-15 | Normal Distributions Transform (NDT) lidar map matching | Point-cloud registration | Partial | Existing local single-resolution NDT baseline is scoped; verify covariance likelihood and add independent registration benchmarks. |
| S21-SM-16 | Road-marking extraction | Feature extraction | Open | Define marking classes, sensor geometry and georeferencing; spatially independent validation. |

### GNSS integrity and location verification — page 45

| ID | Atomic item | Kind | Evidence/status | Required completion work |
|---|---|---|---|---|
| S21-GN-01 | GNSS spoofing detection | Signal integrity / anomaly detection | Open | Define attack model, observables and detection latency; evaluate false alarms and missed detections. |
| S21-GN-02 | GNSS jamming detection | Signal integrity / interference detection | Open | Define interference classes and receiver observables; test detection under varying C/N0 and geometry. |
| S21-GN-03 | GNSS signal authentication | Security protocol / signal feature | Verify | Identify specific authentication standard/service; document cryptographic and receiver assumptions. |
| S21-GN-04 | Pseudorange anomaly detection | Measurement integrity monitoring | Partial | Existing RAIM/FDE is only supplied-model residual screening; add fault hypotheses, protection levels and independent fixtures. |
| S21-GN-05 | Doppler anomaly detection | Measurement integrity monitoring | Open | Define Doppler residual model, clock/velocity terms and fault hypotheses; test injected faults. |
| S21-GN-06 | GNSS integrity monitoring | Safety/integrity framework | Partial | Separate RAIM/FDE from full integrity risk/protection-level requirements; verify standards and scope. |
| S21-GN-07 | Crowdsourced location verification | Location trust workflow | Open | Define adversary model, corroboration and privacy constraints; avoid claiming cryptographic proof from plausibility checks. |
| S21-GN-08 | Proof-of-location verification | Security protocol / attestation | Verify | Identify protocol and threat model; distinguish trusted hardware, cryptographic attestation and probabilistic evidence. |
| S21-GN-09 | Mock-location detection | Device/location fraud detection | Open | Define platform signals and attacker capabilities; test evasion and false-positive behaviour. |
| S21-GN-10 | Cross-sensor consistency checks | Sensor fusion / integrity check | Open | Define sensors, time alignment and uncertainty; test inconsistent and correlated failure cases. |

### Geology and geoscience machine learning — page 45

| ID | Atomic item | Kind | Evidence/status | Required completion work |
|---|---|---|---|---|
| S21-GM-01 | Lithology classification from remote sensing | Geological classification | Open | Define lithology taxonomy, sensor preprocessing and spatial validation; quantify class imbalance. |
| S21-GM-02 | Lithology classification from geophysics | Geophysical classification | Open | Specify modalities, inversion products and labels; use spatially blocked validation. |
| S21-GM-03 | Geological map generation | Mapping workflow / ML application | Open | Define target legend, scale, evidence layers and human review; preserve uncertainty/provenance. |
| S21-GM-04 | Stratigraphic modelling | Geological modelling | Open | Define surfaces, ordering constraints and uncertainty; validate against boreholes/sections. |
| S21-GM-05 | Basin modelling | Geoscience simulation | Open | Identify process model and assumptions; distinguish thermal, burial and fluid-flow components. |
| S21-GM-06 | Thermochronology spatial analysis | Geochronological inference | Open | Define thermochronometer, thermal history model and spatial sampling; cite authoritative methods. |
| S21-GM-07 | Geochronology spatial analysis | Geochronological analysis | Open | Define dating system, uncertainty propagation and spatial interpolation assumptions. |
| S21-GM-08 | Weights-of-evidence mineral prospectivity | Spatial evidence integration | Open | Define conditional-independence assumptions, training deposits and spatial validation. |
| S21-GM-09 | Neural-network mineral prospectivity modelling | Predictive mapping | Open | Define features, labels, spatial CV and calibration; test leakage and extrapolation. |

### Maritime and aviation analytics — page 45

| ID | Atomic item | Kind | Evidence/status | Required completion work |
|---|---|---|---|---|
| S21-MA-01 | Ship-to-ship transfer detection | Maritime event detection | Open | Define AIS encounter, transfer evidence and temporal/spatial thresholds; validate adjudicated events. |
| S21-MA-02 | Vessel loitering detection | Trajectory/event detection | Open | Define speed, duration and spatial context; test against manoeuvring and anchorage cases. |
| S21-MA-03 | Vessel rendezvous detection | Spatiotemporal event detection | Open | Define relative motion and proximity duration; distinguish rendezvous from routine traffic. |
| S21-MA-04 | Port-call inference | Trajectory classification | Open | Define port polygons, dwell/stop criteria and uncertainty; test boundary and anchorage cases. |
| S21-MA-05 | Trade-flow estimation from AIS | Flow estimation | Open | Define vessel-to-cargo inference assumptions and coverage bias; validate against independent trade statistics. |
| S21-MA-06 | Vessel emissions inventories | Emissions estimation | Open | Define engine/load/fuel models, activity data and uncertainty; document inventory boundary. |
| S21-MA-07 | ADS-B trajectory clustering | Trajectory analysis | Open | Define trajectory normalisation, distance and clustering parameters; evaluate route/airport stratification. |
| S21-MA-08 | Aircraft holding-pattern detection | Trajectory/event detection | Open | Define geometric/temporal pattern and altitude constraints; test procedural and non-holding turns. |
| S21-MA-09 | Aircraft emissions inventories | Emissions estimation | Open | Define flight phase, engine and fuel models; document uncertainty and data coverage. |
| S21-MA-10 | Contrail detection from satellite imagery | Remote-sensing detection | Open | Define sensor/time/label source and contrail taxonomy; evaluate spatially independent scenes. |

## Cross-cutting completion gates

For every applicable row:

1. **Identity:** resolve the exact method, named model, framework, software or standard. Section 21 names are explicitly memory-based; acronym resemblance is not sufficient.
2. **Bibliography/version:** verify the primary publication, official standard or maintained project source. Pin software and model versions.
3. **Technical claims:** record equations, assumptions, coordinate frames, physical units, validity domain and known failure modes.
4. **Implementation contract:** specify inputs, shapes, missing-data behaviour, determinism, tolerances and dependencies.
5. **Independent tests:** use analytical fixtures, synthetic truth, published benchmarks or differential comparison to an independent implementation. Include adversarial and boundary cases.
6. **Teaching record:** provide a canonical method explanation, scoped implementation walkthrough, runnable example/notebook where useful, and explicit limitations.
7. **Catalogue reconciliation:** update the section index, implementation index, coverage matrix and review dashboard only after evidence changes.
8. **Rights/provenance:** review code, datasets, model weights, imagery and source text licences independently.

## Execution priorities

1. Resolve primary identities and standards first for the memory-based named models (SIREN, SFNO, named NeRF variants, ACE, ConceptFusion, CLIP-Fields, VLMaps, Hydra, HTDP, NADCON, GEOID18 and VERTCON).
2. Expand the existing land-change accounting and robust-predicate foundations with independent reference fixtures, without broadening their claims.
3. Treat climate emulators, ecosystem accounting, digital-twin synchronisation, proof-of-location and domain workflows as model/framework records rather than forcing them into algorithm packages.
4. Implement small, mathematically self-contained items only after the exact formulation and licence are established.
5. Reconcile the full 22-section source inventory and run the complete CI/notebook/release checks before declaring repository completion.

**Current conclusion:** Section 21 is now decomposed into atomic review work. It remains open; this file is a traceability backlog, not a verification or completion claim.
