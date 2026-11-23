# Section 19 atomic completion register

**Source:** *Spatial Analysis Algorithms: Complete Compendium*, Section 19, pages 39–41.  
**Intake:** [pages 36–40](../source-inventory/pages-36-40.md) and [pages 41–47](../source-inventory/pages-41-47.md).  
**Section index:** [Section 19 catalogue record](../catalog/sections/19-african-applications-addressing-finance.md).

> The source warns that names and tools are from memory. Regional examples are research prompts, not verified descriptions of current systems or representative accounts of Africa. This register decomposes the source groupings; it does not authenticate their availability, validity or local applicability.

## Status policy

Use [the source-entry verification protocol](../catalog/verification-protocol.md). Preserve country/region, data date, coverage, licensing and provenance. A model or workflow must not be labelled an algorithm unless its method is defined. Keep identity, bibliography, technical claims, implementation and rights separate.

| Status | Meaning |
|---|---|
| Open | No item-specific independent verification or implementation is recorded here. |
| Partial | A related implementation exists but covers only a bounded part of the grouped entry. |
| Verify | Exact named product, software, model or protocol must be identified first. |
| Not applicable | An application or workflow is not a standalone algorithm; document it as a use case/workflow. |

## Atomic source register

### Applications common in East and Sub-Saharan Africa — pages 39–40

| ID | Atomic item | Kind | Evidence/status | Required completion work |
|---|---|---|---|---|
| S19-AF-01 | Desert-locust habitat suitability from soil moisture | Ecological suitability model | Open | Define target species/life stage, soil-moisture source, season and spatial scale; validate against independent observations. |
| S19-AF-02 | Desert-locust habitat suitability from vegetation | Ecological suitability model | Open | Define vegetation variables and phenology; assess sensor/season effects and spatial transfer. |
| S19-AF-03 | Locust swarm movement forecasting | Movement forecasting | Open | Identify movement model and forcing data; test forecast horizons, uncertainty and hindcast skill. |
| S19-AF-04 | eLocust-style field data fusion | Field-data workflow | Verify | Identify exact platform/version and data schema; assess coverage, offline collection, provenance and licence. |
| S19-AF-05 | NDVI index design for livestock/crop insurance | Parametric insurance index design | Open | Define insured peril, aggregation, trigger and calibration; quantify basis risk and distributional effects. |
| S19-AF-06 | Rainfall index design for insurance | Parametric insurance index design | Open | Define station/grid data, accumulation window and trigger; test spatial representativeness and basis risk. |
| S19-AF-07 | Insurance basis-risk analysis | Risk evaluation | Open | Define payout/impact variables, spatial/temporal matching and metrics; test false-negative and false-positive loss. |
| S19-AF-08 | Pasture-condition mapping | Environmental monitoring | Open | Define pasture condition indicators and field protocol; validate seasonal and ecological transfer. |
| S19-AF-09 | Herd movement-track analysis | Movement analysis | Open | Define animal/sample unit, tracking interval and missingness; protect sensitive mobility data. |
| S19-AF-10 | Seasonal pastoral corridor detection | Corridor analysis | Open | Define seasonal movement evidence and corridor criteria; validate against community/field knowledge. |
| S19-AF-11 | Water-point access modelling | Accessibility analysis | Open | Define operational water points, seasonal availability, travel impedance and access rights. |
| S19-AF-12 | Grazing-access modelling | Accessibility / resource allocation | Open | Define tenure, seasonal restrictions and resource pressure; avoid equating geometric proximity with access. |
| S19-AF-13 | Malaria prevalence geostatistics (MAP-style) | Disease mapping | Verify | Identify MAP method/product and version; document survey likelihood, covariates, uncertainty and spatial validation. |
| S19-AF-14 | Cholera risk mapping | Disease risk modelling | Open | Define case/event data, water/sanitation covariates and temporal lag; assess reporting bias and privacy. |
| S19-AF-15 | Rift Valley fever risk modelling | Zoonotic disease modelling | Open | Define host/vector/environmental processes and outbreak labels; validate across ecological zones. |
| S19-AF-16 | Health-facility accessibility (AccessMod-style) | Cost-distance accessibility workflow | Verify | Identify AccessMod version and travel-surface assumptions; distinguish model outputs from actual service availability. |
| S19-AF-17 | Paratransit route reconstruction from GPS | Transit network inference | Open | Define vehicle/route observations, stop inference and route aggregation; validate with field-mapped services. |
| S19-AF-18 | Digital-matatu-style GTFS production | Transit data workflow | Verify | Identify data specification and project; document route/stop/trip completeness and service variability. |
| S19-AF-19 | Mobile-money data for mobility proxies | Privacy-sensitive spatial analytics | Open | Define aggregation and inference target; establish legal basis, privacy protection and bias audit before analysis. |
| S19-AF-20 | Mobile-network data for mobility proxies | Privacy-sensitive mobility analytics | Open | Define operator data, spatial/temporal aggregation and population expansion; privacy and representativeness review. |
| S19-AF-21 | Mobile-network data for poverty proxies | Socioeconomic proxy modelling | Open | Define target labels, confounders and geographic validation; test bias and avoid individual-level inference. |
| S19-AF-22 | Water-point functionality prediction (WPDx-style) | Infrastructure condition prediction | Verify | Identify dataset/project version and label definition; test temporal leakage, class imbalance and local transfer. |
| S19-AF-23 | Borehole siting from geophysics | Hydrogeological siting | Open | Define geophysical survey method and hydrogeological validation; document expert review and uncertainty. |
| S19-AF-24 | Borehole siting from remote sensing | Hydrogeological suitability | Open | Define proxy variables and regional geology; validate with borehole outcomes and field surveys. |
| S19-AF-25 | Drought early warning from VCI | Drought indicator | Partial | Verify vegetation condition index baseline and compositing; regional calibration and impact link remain open. |
| S19-AF-26 | Drought early warning from SPI | Drought indicator | Partial | Define accumulation period, distribution and zero-rainfall treatment; seasonal/regional calibration. |
| S19-AF-27 | Drought early warning from soil-moisture anomalies | Drought indicator | Open | Define reference climatology, sensor fusion and depth; test product bias and temporal stability. |
| S19-AF-28 | Food-security outlook integration | Decision-support workflow | Open | Define indicators, temporal alignment and decision thresholds; preserve source provenance and uncertainty. |

### Addressing and location encoding — page 40

| ID | Atomic item | Kind | Evidence/status | Required completion work |
|---|---|---|---|---|
| S19-AD-01 | Open Location Code / Plus Codes | Location encoding system | Partial | Existing full-code encode/decode and cell bounds are tested; add short-code recovery, validation and authoritative conformance fixtures. |
| S19-AD-02 | Geohash | Location encoding system | Partial | Existing encode/decode is tested; verify boundary conventions, precision semantics and interoperability fixtures. |
| S19-AD-03 | what3words-style grids | Proprietary location encoding | Verify | Identify provider and licence; document API dependence and avoid reproducing proprietary word lists. |
| S19-AD-04 | S2 cell addresses | Spherical hierarchical spatial index | Open | Identify S2 library/version; implement cell IDs, hierarchy and geometry semantics only against official specifications. |
| S19-AD-05 | H3 cell addresses | Hexagonal hierarchical spatial index | Open | Identify H3 version and aperture/resolution semantics; verify pentagon and boundary behaviour. |
| S19-AD-06 | Descriptive geocoding | Geocoding approach | Open | Define address/place vocabulary, candidate ranking and confidence; validate against local reference data. |
| S19-AD-07 | Landmark-based geocoding | Geocoding workflow | Open | Define landmark gazetteer, relation language and ambiguity resolution; evaluate with local users. |
| S19-AD-08 | Building-based addressing | Address assignment workflow | Open | Define building entrance/unit and address authority; validate positional and administrative correctness. |
| S19-AD-09 | Address-free geocoding for informal settlements | Geocoding approach | Open | Define privacy, community consent and location granularity; avoid exposing sensitive household locations. |
| S19-AD-10 | Address generation from street segments | Address interpolation | Partial | Existing cumulative-distance interpolation is a geometric baseline; local numbering, parity, block rules and authority validation remain open. |
| S19-AD-11 | Address generation from building footprints | Address assignment | Open | Define entrance association and numbering authority; validate against field-assigned addresses. |
| S19-AD-12 | Address quality scoring | Data quality method | Open | Define completeness, positional, logical and temporal dimensions; calibrate against adjudicated records. |

### Insurance, finance and risk transfer — page 40

| ID | Atomic item | Kind | Evidence/status | Required completion work |
|---|---|---|---|---|
| S19-FI-01 | Parametric insurance trigger selection | Insurance design | Open | Define peril, index distribution and payout function; evaluate trigger robustness and basis risk. |
| S19-FI-02 | Parametric index construction | Insurance design | Open | Specify input data, spatial aggregation and temporal window; validate against insured loss. |
| S19-FI-03 | Basis-risk quantification | Insurance risk metric | Open | Define loss/payout pairing, portfolio and subgroup metrics; assess tail risk and coverage gaps. |
| S19-FI-04 | Catastrophe-bond trigger design | Risk transfer design | Open | Identify trigger type and event definition; document model risk, data source and legal/financial review. |
| S19-FI-05 | Geospatial credit-risk features | Predictive modelling | Open | Define permissible features and unit of analysis; test spatial leakage, fairness and privacy. |
| S19-FI-06 | Geospatial risk models | Risk modelling | Open | Define hazard/exposure/vulnerability dimensions and target; validate out of region/time. |
| S19-FI-07 | Automated property valuation (AVM) | Valuation model | Open | Define target value/date, property attributes and market sample; validate calibration and spatial transfer. |
| S19-FI-08 | Comparable-property selection with kNN | Similarity search | Open | Define feature scaling, geographic constraints and temporal comparability; test ranking against expert adjudication. |
| S19-FI-09 | Geographically weighted regression for valuation | Local regression model | Open | Define kernel/bandwidth and spatial diagnostics; test instability and out-of-sample prediction. |
| S19-FI-10 | Flood-zone exposure assignment | Exposure analysis | Open | Define hazard map vintage, asset location uncertainty and depth/return period; document overlay assumptions. |
| S19-FI-11 | Wind exposure aggregation | Portfolio exposure analysis | Open | Define hazard intensity, vulnerability and geocoding uncertainty; avoid implying loss without vulnerability model. |
| S19-FI-12 | Earthquake exposure aggregation | Portfolio exposure analysis | Open | Define ground-motion measure, site effects and asset inventory; validate exposure aggregation. |
| S19-FI-13 | Portfolio accumulation analysis | Risk aggregation | Open | Define accumulation zones, correlated peril and policy limits; test concentration and exceedance summaries. |

### Telecom and network planning — page 40

| ID | Atomic item | Kind | Evidence/status | Required completion work |
|---|---|---|---|---|
| S19-TC-01 | RF coverage prediction | Radio propagation modelling | Open | Identify propagation model and frequency; validate against drive-test measurements. |
| S19-TC-02 | Propagation-model calibration | Parameter estimation | Open | Define measurement protocol, loss function and spatial holdout; report uncertainty. |
| S19-TC-03 | Cellular site planning | Network optimisation | Open | Define demand, capacity, interference and candidate sites; document engineering constraints. |
| S19-TC-04 | Handover analysis | Network performance analysis | Open | Define signal thresholds, mobility and handover events; validate with network traces. |
| S19-TC-05 | Interference mapping | Radio network analysis | Open | Define interference metric and frequency reuse; validate with measured spectrum/network data. |
| S19-TC-06 | Backhaul routing | Network design | Open | Define capacity, reliability, terrain/cost and existing infrastructure constraints. |
| S19-TC-07 | Fibre least-cost corridors | Least-cost path optimisation | Open | Define cost surface, wayleave and environmental constraints; compare with surveyed routes. |
| S19-TC-08 | Fibre ring design | Network topology optimisation | Open | Define redundancy, capacity and failure criteria; test resilience under link/node loss. |
| S19-TC-09 | Last-mile network design | Network design optimisation | Open | Define service targets, terrain and affordability constraints; document technology assumptions. |
| S19-TC-10 | Satellite constellation coverage | Satellite coverage analysis | Open | Define constellation ephemerides, elevation masks and time window; validate against orbital truth. |
| S19-TC-11 | Satellite beam planning | Communications optimisation | Open | Define antenna/beam model, demand and interference; distinguish planning from operational control. |
| S19-TC-12 | Satellite link-budget analysis | RF engineering calculation | Open | Define frequency, losses, antenna gains, atmospheric conditions and units; test link-budget closure. |

### Seismology and earthquake early warning — page 40

| ID | Atomic item | Kind | Evidence/status | Required completion work |
|---|---|---|---|---|
| S19-SE-01 | Geiger earthquake-location method | Hypocentre estimation | Verify | Verify exact linearisation/iteration convention; test synthetic travel-time recovery and local minima. |
| S19-SE-02 | HypoDD double-difference relocation | Relative earthquake relocation | Verify | Verify paper/software version and differential-time assumptions; reproduce benchmark cluster. |
| S19-SE-03 | Magnitude estimation | Seismic estimation | Open | Identify magnitude scale and regional calibration; avoid mixing ML, Mw and other scales. |
| S19-SE-04 | Focal-mechanism inversion | Source mechanism estimation | Open | Define waveform/first-motion data and velocity model; report non-uniqueness. |
| S19-SE-05 | STA/LTA event detection | Signal detection | Verify | Define short/long windows and threshold logic; test noise and event onset scenarios. |
| S19-SE-06 | Template matching | Signal detection | Open | Define template, similarity metric and network coherence; evaluate false detections. |
| S19-SE-07 | PhaseNet phase picking | ML phase picker | Verify | Verify model/repository version, sample rate and label schema; benchmark against manual picks. |
| S19-SE-08 | EQTransformer-style phase picking | ML phase picker | Verify | Verify exact model version and event association; evaluate calibration and domain shift. |
| S19-SE-09 | Ambient-noise tomography | Seismic imaging | Open | Define correlation/dispersion workflow and station geometry; validate synthetic velocity models. |
| S19-SE-10 | Receiver-function analysis | Seismic imaging | Open | Define deconvolution and phase interpretation; test synthetic layered Earth models. |
| S19-SE-11 | ElarmS early warning | Early-warning system | Verify | Identify version and operational context; document latency, magnitude and location uncertainty. |
| S19-SE-12 | PLUM-style early warning | Early-warning algorithm family | Verify | Verify exact PLUM method and thresholds; evaluate regional network-density assumptions. |
| S19-SE-13 | GNSS rapid magnitude estimation | Geodetic earthquake estimation | Open | Define displacement products and magnitude relation; test finite-fault and saturation cases. |
| S19-SE-14 | Tsunami-warning inversion | Inverse modelling / early warning | Open | Define observations, source parameterisation and latency; validate synthetic tsunami scenarios. |
| S19-SE-15 | Volcanic deformation monitoring | Multi-sensor monitoring | Open | Define GNSS/InSAR/tilt observations, reference frame and uncertainty; document alert context. |
| S19-SE-16 | Volcanic SO2 monitoring | Atmospheric remote sensing | Open | Define sensor/product and retrieval; assess plume height, cloud and wind effects. |
| S19-SE-17 | Volcanic thermal monitoring | Thermal remote sensing | Open | Define thermal anomaly metric and sensor; validate detection and false-alarm behaviour. |
| S19-SE-18 | Failure Forecast Method for eruption forecasting | Time-to-failure model | Verify | Verify original formulation and assumptions; test retrospective data and false-alarm rates. |

### Atmospheric transport, receptor models and space weather — page 41

| ID | Atomic item | Kind | Evidence/status | Required completion work |
|---|---|---|---|---|
| S19-AT-01 | HYSPLIT back trajectories | Atmospheric transport model | Verify | Verify NOAA version and meteorological inputs; document trajectory uncertainty and vertical motion. |
| S19-AT-02 | STILT footprint modelling | Atmospheric footprint model | Verify | Verify model version and adjoint/particle formulation; define receptor sensitivity units. |
| S19-AT-03 | FLEXPART footprint modelling | Lagrangian transport model | Verify | Verify version and release; document turbulence, emissions and footprint interpretation. |
| S19-AT-04 | Potential Source Contribution Function (PSCF) | Receptor/source attribution statistic | Open | Define trajectory endpoints, concentration threshold and cell weighting; test sensitivity and uncertainty. |
| S19-AT-05 | Concentration-Weighted Trajectory (CWT) | Receptor/source attribution statistic | Open | Define concentration weighting, trajectory filtering and grid support; compare with PSCF. |
| S19-AT-06 | Positive Matrix Factorization (PMF) | Receptor model | Verify | Verify EPA/US-EPA formulation and version; document uncertainty, constraints and factor ambiguity. |
| S19-AT-07 | Chemical Mass Balance (CMB) | Receptor model | Verify | Verify source-profile assumptions and software; test synthetic mixtures and collinearity. |
| S19-AT-08 | Source apportionment with spatial covariates | Statistical source attribution | Open | Define source profiles and spatial effects; validate against known source contributions. |
| S19-AT-09 | Total Electron Content (TEC) mapping | Ionospheric mapping | Open | Define GNSS geometry, mapping function and reference; test with known synthetic ionosphere. |
| S19-AT-10 | Scintillation indices | Space-weather metrics | Open | Identify index definitions and sampling rates; document receiver and geomagnetic limitations. |
| S19-AT-11 | Ionospheric correction models | GNSS correction model | Open | Identify model family (broadcast/regional/precise) and version; test residual positioning error. |

### Acoustic and marine sensor analysis — page 41

| ID | Atomic item | Kind | Evidence/status | Required completion work |
|---|---|---|---|---|
| S19-AC-01 | Time-difference-of-arrival (TDOA) localisation | Acoustic localisation | Open | Define synchronisation, propagation speed and geometry; test analytic source recovery with noise. |
| S19-AC-02 | Acoustic beamforming | Array signal processing | Open | Define array geometry, steering and frequency domain; test known source directions and sidelobes. |
| S19-AC-03 | Acoustic multilateration | Source localisation | Open | Define sensor layout and range/time observations; test degenerate geometries and uncertainty. |
| S19-AC-04 | Soundscape acoustic indices | Ecological signal metric | Open | Identify exact indices and sampling conventions; validate against annotated soundscapes. |
| S19-AC-05 | Bird-call detection from acoustic arrays | Bioacoustic detection | Open | Define species labels, array localisation and temporal aggregation; evaluate spatial/seasonal transfer. |
| S19-AC-06 | Wildlife detection from passive acoustic networks | Bioacoustic monitoring workflow | Open | Define detection/occupancy distinction, effort and false positives; protect sensitive species locations. |
| S19-AC-07 | Side-scan sonar processing | Sonar image processing | Open | Define sensor geometry, slant-range correction and mosaicking; test calibration targets. |
| S19-AC-08 | Sub-bottom sonar processing | Subsurface acoustic imaging | Open | Define chirp/pulse processing, sound velocity and stratigraphic interpretation; test reference profiles. |
| S19-AC-09 | Seabed classification | Marine classification | Open | Define classes, sonar features and ground truth; spatially independent validation. |

### Cross-cutting diagnostics and reporting — page 41

| ID | Atomic item | Kind | Evidence/status | Required completion work |
|---|---|---|---|---|
| S19-QA-01 | Spatial-autocorrelation leakage in validation splits | Validation diagnostic | Partial | Existing spatial folds address some leakage; test residual dependence across train/test boundaries. |
| S19-QA-02 | Tile-overlap leakage | Image validation diagnostic | Open | Define tile overlap and source-scene grouping; implement explicit overlap audit. |
| S19-QA-03 | Neighbouring-patch leakage under random splits | Image validation diagnostic | Open | Define patch adjacency and buffer; compare random and spatially separated validation. |
| S19-QA-04 | MAUP diagnostics | Spatial inference diagnostic | Open | Define zoning/scale perturbation experiment; report sensitivity, not a universal correction. |
| S19-QA-05 | Ecological-fallacy checks | Inference limitation diagnostic | Open | Define aggregation levels and individual-level inference risks; document interpretation boundaries. |
| S19-QA-06 | Edge and boundary effects | Spatial analysis diagnostic | Open | Identify affected estimators and boundary correction; test synthetic edge cases. |
| S19-QA-07 | Tile-boundary artifacts in segmentation | Image QA diagnostic | Open | Define overlap/blending and seam metrics; test objects crossing tile edges. |
| S19-QA-08 | Extrapolation outside covariate space | Applicability diagnostic | Partial | Existing applicability envelopes cover selected feature-space distances; define thresholds and multivariate support. |
| S19-QA-09 | Label shift between regions | Distribution-shift diagnostic | Open | Define class-prior shift and estimation assumptions; test with synthetic prior changes. |
| S19-QA-10 | Temporal drift | Monitoring diagnostic | Open | Define drift statistic, window and alert policy; test known shifts and seasonality. |
| S19-QA-11 | Sensor changes | Domain-shift diagnostic | Open | Define sensor/processing metadata and harmonisation; test cross-sensor holdouts. |
| S19-QA-12 | Spatial confounding diagnostics | Statistical model diagnostic | Partial | Existing residual Moran/LM diagnostics do not identify all confounding; document model-specific limits. |
| S19-QA-13 | Residual spatial autocorrelation checks | Model diagnostic | Partial | Specify weights, null and multiple testing; compare residual diagnostics across scales. |
| S19-QA-14 | Calibration across regions | Model evaluation | Open | Define regional reliability metrics and sample size; evaluate transfer and recalibration. |
| S19-QA-15 | Spatial cross-validation reporting | Reporting standard | Partial | Report fold construction, buffers, grouping and temporal separation explicitly. |
| S19-QA-16 | Area-of-applicability reporting | Reporting standard | Partial | Report covariate support, threshold, maps and uncertainty; distinguish distance from calibrated applicability. |
| S19-QA-17 | Uncertainty-map reporting | Reporting standard | Open | Define uncertainty type, units, calibration and masking; avoid displaying uncalibrated scores as probabilities. |
| S19-QA-18 | Per-region metrics | Reporting standard | Open | Define region strata and minimum support; report confidence intervals and sample counts. |
| S19-QA-19 | Class-wise area estimates | Area estimation | Partial | Separate raw mapped area from design-adjusted area estimates; document sampling design and confidence intervals. |

## Completion gates

1. Verify named tools, projects, products and methods against official documentation or primary publications; record version/date and geographic coverage.
2. For African applications, specify country/region, local context, data provenance, observation date, licence and representativeness.
3. Define mathematical/statistical contracts, spatial units, uncertainty, data quality and known failure modes.
4. For privacy-sensitive health, telecom, mobile-money, pastoral and location data, perform a documented privacy/legal review before implementation or examples.
5. Test algorithms independently with analytical fixtures, synthetic truth, field data or authoritative reference outputs.
6. Document workflows as workflows; do not invent generic algorithms for a named product or service.
7. Reconcile section indexes, implementation indexes, coverage matrix and review dashboard after evidence changes.
8. Review rights for datasets, software, imagery, model weights and copied material.

## Execution priorities

1. Establish the cross-cutting validation and reporting methods as reusable quality gates across the repository.
2. Verify location encodings and address workflows, preserving privacy and local addressing conventions.
3. Prioritise locally grounded, reproducible applications (transit, water, drought, health access) only where suitable public/licensed data and field validation exist.
4. Treat insurance, finance, telecom, seismic early warning and GNSS integrity as high-stakes domains requiring authoritative validation.
5. Complete source identity and rights review before claiming any regional product or system is available or operational.

**Current conclusion:** Section 19 is decomposed into atomic review items. It remains open; this register is not a verification, operational endorsement or completion claim.
