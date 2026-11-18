# Section 20 atomic completion register

**Source:** *Spatial Analysis Algorithms: Complete Compendium*, Section 20, pages 41–43.  
**Intake:** [preserved page transcription](../source-inventory/pages-41-47.md).  
**Section index:** [Section 20 catalogue record](../catalog/sections/20-indices-microwave-events-information.md).

> The source explicitly warns that names are from memory and should be verified before citation. This register decomposes source groupings into auditable children. It does not establish that every item is a unique algorithm or that related implementations close the full grouped entry.

## Status policy

Use the independent dimensions in [the source-entry verification protocol](../catalog/verification-protocol.md). A tested formula or related package is evidence only for its stated scope. Keep identity, bibliography, technical claims, implementation, rights and canonicalisation distinct.

| Status | Meaning |
|---|---|
| Open | No item-specific independent verification or implementation is recorded here. |
| Partial | A related implementation exists but does not cover all variants or requirements. |
| Verify | Exact named method, model, acronym or software version must be resolved first. |
| Not applicable | A workflow/framework is not a standalone algorithm; document it as such. |

## Atomic source register

### Spectral indices — page 41

| ID | Atomic item | Kind | Evidence/status | Required completion work |
|---|---|---|---|---|
| S20-SI-01 | GNDVI | Spectral index | Partial | Verify canonical formula and band convention; sensor-specific band mapping and reference-scene tests. |
| S20-SI-02 | ARVI | Spectral index | Partial | Verify atmospheric-resistance formulation and coefficients; test reflectance domain and sensor variants. |
| S20-SI-03 | GCI | Spectral index | Partial | Verify green chlorophyll index definition and band units; compare independent formula fixtures. |
| S20-SI-04 | MSAVI | Spectral index | Partial | Distinguish MSAVI and MSAVI2; test soil-background and reflectance assumptions. |
| S20-SI-05 | OSAVI | Spectral index | Partial | Verify soil-adjustment constant and sensor/band convention. |
| S20-SI-06 | WDRVI | Spectral index | Partial | Record alpha parameter and sensitivity; test known limiting behaviour. |
| S20-SI-07 | NIRv | Spectral index | Partial | Verify NIR reflectance and NDVI product definition; document reflectance scaling. |
| S20-SI-08 | kNDVI | Spectral index | Partial | Verify kernel parameterisation and exact formulation; test numerical range and scaling. |
| S20-SI-09 | MTCI | Red-edge index | Partial | Verify red-edge band placement and sensor compatibility; test narrow-band requirements. |
| S20-SI-10 | REIP | Red-edge position metric | Partial | Distinguish linear interpolation variants; test spectral sampling and wavelength units. |
| S20-SI-11 | TCARI | Pigment index | Partial | Verify exact reflectance formula and band requirements; compare published examples. |
| S20-SI-12 | CIgreen | Chlorophyll index | Partial | Resolve equivalence/aliasing with GCI; preserve source label and canonical relationship. |
| S20-SI-13 | CIrededge | Chlorophyll index | Partial | Verify red-edge wavelength convention and sensor mapping. |
| S20-SI-14 | PSRI | Pigment/stress index | Partial | Verify formula and intended stress interpretation; avoid overclaiming physiological specificity. |
| S20-SI-15 | ARI | Anthocyanin reflectance index | Partial | Separate ARI variants; verify wavelength and reflectance conventions. |
| S20-SI-16 | CRI | Carotenoid reflectance index | Partial | Resolve CRI1/CRI2 variants and wavelength requirements. |
| S20-SI-17 | SIPI | Pigment index | Partial | Verify formula and sensitivity to canopy/background conditions. |
| S20-SI-18 | PRI | Photochemical reflectance index | Partial | Verify band pair and illumination/geometry sensitivity. |
| S20-SI-19 | NDII | Moisture index | Partial | Resolve NDII naming collision with other indices; verify NIR/SWIR bands. |
| S20-SI-20 | NMDI | Moisture index | Partial | Verify SWIR band definitions and intended drought/moisture context. |
| S20-SI-21 | BSI | Soil index | Partial | Verify formula variant and band order; test reflectance scaling. |
| S20-SI-22 | NDTI | Tillage/residue index | Partial | Verify sensor band convention and intended tillage interpretation. |
| S20-SI-23 | STI | Soil/tillage index | Partial | Resolve formula ambiguity and naming collision; identify source and wavelength pair. |
| S20-SI-24 | CAI crop-residue index | Hyperspectral index | Partial | Verify narrow-band wavelengths and calibration; do not imply broadband sensor support. |
| S20-SI-25 | Clay mineral ratio | Mineral ratio | Open | Identify exact ratio, wavelengths and sensor; validate against mineral reference spectra. |
| S20-SI-26 | Iron-oxide ratio | Mineral ratio | Open | Identify ratio variant and atmospheric/illumination corrections; validate on reference spectra. |
| S20-SI-27 | Ferrous-iron index | Mineral index | Open | Verify exact band/formula and sensor; distinguish ferrous from ferric response. |
| S20-SI-28 | ASTER mineral indices | Sensor-specific index family | Verify | Resolve official ASTER band-ratio definitions and product documentation; version and resampling caveats. |

### Thermal and land-surface temperature — page 42

| ID | Atomic item | Kind | Evidence/status | Required completion work |
|---|---|---|---|---|
| S20-TH-01 | Temperature–emissivity separation (TES) | Thermal retrieval algorithm | Open | Verify canonical TES formulation and sensor assumptions; test emissivity/temperature recovery on synthetic spectra. |
| S20-TH-02 | NDVI-threshold emissivity | Emissivity estimation | Open | Define vegetation fraction thresholds and emissivity constants; document land-cover limitations. |
| S20-TH-03 | Mono-window LST algorithm | Thermal retrieval | Open | Identify exact formulation and atmospheric inputs; compare with independent reference fixtures. |
| S20-TH-04 | Single-channel LST algorithm | Thermal retrieval | Partial | Existing radiative-transfer inversion is a bounded baseline; verify method variant and atmospheric parameter contract. |
| S20-TH-05 | Split-window LST algorithm | Thermal retrieval | Partial | Existing caller-calibrated generalized kernel is not a universal sensor algorithm; verify coefficients and emissivity assumptions. |
| S20-TH-06 | Surface urban heat-island intensity metrics | Urban climate metric | Open | Define urban/rural reference, spatial support and temporal aggregation; test sensitivity to reference selection. |
| S20-TH-07 | DisTrad thermal sharpening | Thermal downscaling | Verify | Verify original method and regression assumptions; reproduce on synthetic coarse/fine scenes. |
| S20-TH-08 | TsHARP thermal sharpening | Thermal downscaling | Verify | Verify exact formulation, vegetation-index relation and limits; compare independent implementation. |
| S20-TH-09 | Regression-based LST downscaling | Statistical downscaling | Open | Define predictors, scale consistency and spatial validation; quantify aggregation error. |
| S20-TH-10 | Deep-learning LST downscaling | ML downscaling | Open | Identify architecture/data protocol; prevent spatial/temporal leakage and evaluate conservation across scales. |

### Microwave and radar retrieval — page 42

| ID | Atomic item | Kind | Evidence/status | Required completion work |
|---|---|---|---|---|
| S20-MW-01 | Water Cloud Model | Radar backscatter model | Verify | Verify canonical equations, vegetation parameters and calibration domain; test limiting cases. |
| S20-MW-02 | Oh backscatter model | Radar scattering model | Verify | Identify exact model variant and roughness assumptions; compare against published curves. |
| S20-MW-03 | Dubois backscatter model | Radar scattering model | Verify | Verify incidence-angle, frequency and roughness validity range; add parameter-domain checks. |
| S20-MW-04 | Integral Equation Model (IEM) | Electromagnetic scattering model | Verify | Identify IEM formulation/version and surface assumptions; validate against reference calculations. |
| S20-MW-05 | Advanced IEM (AIEM) | Electromagnetic scattering model | Verify | Verify exact AIEM variant and implementation; do not conflate with original IEM. |
| S20-MW-06 | TU Wien-style soil-moisture change detection | Soil-moisture retrieval workflow | Verify | Identify algorithm/product and version; define baseline, vegetation and temporal normalisation assumptions. |
| S20-MW-07 | Vegetation optical depth (VOD) | Microwave retrieval quantity | Open | Define retrieval sensor/frequency and radiative-transfer model; validate against independent vegetation data. |
| S20-MW-08 | Random-volume-over-ground (RVoG) model | PolInSAR model | Verify | Verify equations, polarimetric assumptions and parameter identifiability; synthetic inversion tests. |
| S20-MW-09 | PolInSAR forest-height retrieval | Forest structure retrieval | Open | Define coherence model, baseline and ground phase; validate height bias/uncertainty. |
| S20-MW-10 | P-band biomass retrieval | Radar biomass estimation | Open | Define frequency, saturation and calibration domain; independent plot validation and uncertainty. |
| S20-MW-11 | Tau–omega radiative-transfer model | Passive microwave model | Verify | Verify equation convention and parameter definitions; test emissivity/brightness-temperature behaviour. |
| S20-MW-12 | SMAP soil-moisture retrieval context | Satellite product/system | Verify | Identify product/version and algorithm level; distinguish model from mission/product workflow. |
| S20-MW-13 | SMOS soil-moisture retrieval context | Satellite product/system | Verify | Identify product/version and algorithm; distinguish L-band radiometry from a single retrieval equation. |
| S20-MW-14 | AMSR2 snow-water-equivalent retrieval | Passive microwave retrieval | Verify | Identify exact algorithm/product version and snow conditions; assess forest/deep-snow limitations. |
| S20-MW-15 | GPROF-style precipitation retrieval | Passive microwave retrieval system | Verify | Verify GPROF version and Bayesian database; document sensor-specific training and uncertainty. |
| S20-MW-16 | CMOD5-type ocean-wind retrieval | SAR geophysical model function | Verify | Verify CMOD5/CMOD5.N variant and wind-direction inputs; compare with buoy/reference winds. |
| S20-MW-17 | SAR wave spectra | Ocean remote-sensing retrieval | Open | Define spectral inversion and imaging modulation; validate against buoy/wave-model data. |
| S20-MW-18 | Delay-Doppler altimetry | Radar altimetry processing | Verify | Identify mission/product processing chain and retracker; document waveform and geophysical corrections. |

### Product validation and merging without ground truth — page 42

| ID | Atomic item | Kind | Evidence/status | Required completion work |
|---|---|---|---|---|
| S20-PV-01 | Classical triple collocation | Error-variance estimator | Partial | Verify assumptions (mutually uncorrelated errors, linear scaling, common truth); independent analytic fixtures. |
| S20-PV-02 | Extended triple collocation | Error covariance / validation method | Open | Verify exact formulation and assumptions; test correlated-error synthetic data. |
| S20-PV-03 | Error covariance estimation across products | Statistical estimation | Open | Define latent truth and covariance identifiability; test known covariance matrices. |
| S20-PV-04 | Signal-to-noise ratio of products | Product quality metric | Open | Define signal/error variance convention and scaling invariance; verify estimator assumptions. |
| S20-PV-05 | Gauge–satellite kriging blending | Precipitation data fusion | Open | Define residual variogram, gauge support and satellite bias; spatially blocked validation. |
| S20-PV-06 | CHIRPS-style precipitation merging | Product/workflow family | Verify | Identify exact product algorithm/version; distinguish data product from generic merging method. |
| S20-PV-07 | MSWEP-style precipitation merging | Product/workflow family | Verify | Identify exact product/version and component datasets; document gauge/satellite reanalysis blending. |
| S20-PV-08 | Conditional merging | Geostatistical data fusion | Open | Verify formulation and covariance requirements; compare with kriging and independent synthetic fields. |
| S20-PV-09 | Optimal interpolation | Data assimilation / interpolation | Open | Define background-error and observation-error covariance; test linear-Gaussian reference cases. |

### Nighttime lights processing — page 42

| ID | Atomic item | Kind | Evidence/status | Required completion work |
|---|---|---|---|---|
| S20-NT-01 | Saturation correction | Radiometric correction | Open | Identify sensor/product and correction model; quantify radiance bias and clipping recovery. |
| S20-NT-02 | Blooming correction | Image artifact correction | Open | Define point-spread/crosstalk model and sensor version; test spatial spillover on synthetic sources. |
| S20-NT-03 | DMSP–VIIRS harmonisation | Cross-sensor harmonisation | Open | Verify intercalibration method and temporal overlap; test stable-site and saturation behaviour. |
| S20-NT-04 | Background and noise removal | Image processing | Open | Define noise/background model and masking; test low-light preservation and false removal. |
| S20-NT-05 | Lights-per-capita normalisation | Derived indicator | Open | Define population denominator, temporal alignment and zero-population handling; document ecological interpretation. |

### Climate and ocean event detection and tracking — page 42

| ID | Atomic item | Kind | Evidence/status | Required completion work |
|---|---|---|---|---|
| S20-EV-01 | Hobday marine heatwave definition | Event definition | Partial | Verify original threshold definition, baseline period, seasonal percentile and gap bridging; spatial tracking remains separate. |
| S20-EV-02 | Heatwave definitions | Event definition | Open | Identify domain-specific thresholds and duration rules; do not conflate air, land and marine definitions. |
| S20-EV-03 | Cold-spell definitions | Event definition | Open | Define variable, percentile baseline, duration and gap policy; compare official climate indices. |
| S20-EV-04 | Run-theory drought events | Threshold-run event extraction | Partial | Existing extractor is a generic run baseline; verify drought-specific threshold, accumulation and event-merging conventions. |
| S20-EV-05 | Percentile-threshold event detection | Threshold method | Partial | Define climatology window, quantile estimator and calendar-day smoothing; test missing data and nonstationarity. |
| S20-EV-06 | 3-D connected-component labeling | Raster/voxel algorithm | Partial | Existing 6/18/26-neighbour voxel labeling is scoped; test periodicity, time gaps and component identity separately. |
| S20-EV-07 | Storm and cyclone tracking (TempestExtremes-style) | Feature tracking framework | Verify | Verify exact package/version and feature definitions; distinguish detection, stitching and track filtering. |
| S20-EV-08 | Atmospheric-river detection (IVT-based / ARTMIP) | Climate feature detection | Verify | Identify ARTMIP algorithm family; define IVT threshold, geometry, duration and regional sensitivity. |
| S20-EV-09 | Blocking detection | Atmospheric feature detection | Open | Identify blocking index/algorithm; define latitude, persistence and reversal criteria. |
| S20-EV-10 | Jet-stream detection | Atmospheric feature detection | Open | Define wind component/pressure level and jet object criteria; validate seasonal/hemispheric behaviour. |
| S20-EV-11 | Monsoon onset indices | Climate index family | Open | Identify regional onset definitions and rainfall/wind criteria; avoid a universal monsoon index claim. |
| S20-EV-12 | Mesoscale eddy tracking | Ocean feature tracking | Open | Define SLA/SSH contour or Okubo–Weiss detection, temporal association and split/merge handling. |
| S20-EV-13 | Upwelling indices | Oceanographic indicator | Open | Identify wind-stress or SST index variant; define coastline orientation and units. |
| S20-EV-14 | Lagrangian coherent structures / FTLE | Dynamical systems diagnostic | Open | Define velocity field, integration interval and interpolation; test analytic flows. |
| S20-EV-15 | Geostrophic currents from sea-surface height | Ocean dynamics calculation | Open | Define geoid/SSH reference, Coriolis parameter and derivative scheme; handle equatorial singularity. |
| S20-EV-16 | Ekman drift | Ocean transport model | Open | Define wind stress, Coriolis and mixed-layer assumptions; test hemisphere sign and units. |
| S20-EV-17 | Stokes drift | Wave-induced transport model | Open | Define wave spectrum/depth and vertical profile; test deep/shallow-water limits. |

### Information theory, nonlinear dynamics and causality — page 42

| ID | Atomic item | Kind | Evidence/status | Required completion work |
|---|---|---|---|---|
| S20-IT-01 | Shannon entropy | Information measure | Partial | Verify log base, normalisation and zero-probability handling; independent categorical fixtures. |
| S20-IT-02 | Rényi entropy | Information measure | Partial | Verify order parameter, alpha=1 limit and support handling. |
| S20-IT-03 | Tsallis entropy | Information measure | Partial | Verify q parameter and Shannon limit; test numerical stability. |
| S20-IT-04 | Sample entropy | Time-series complexity measure | Partial | Verify embedding/tolerance conventions and short-series behaviour; benchmark known sequences. |
| S20-IT-05 | Permutation entropy | Ordinal-pattern measure | Partial | Verify embedding dimension, delay and tie handling; test known periodic/random sequences. |
| S20-IT-06 | Spatial entropy variants | Spatial information measure | Partial | Identify neighbourhood/partition definition and spatial support; separate from ordinary categorical entropy. |
| S20-IT-07 | Recurrence plots | Nonlinear time-series representation | Partial | Verify distance/threshold and embedding; test deterministic trajectories and scaling. |
| S20-IT-08 | Recurrence quantification analysis | Nonlinear time-series statistics | Partial | Verify RR, DET, line-length and entropy definitions; state threshold dependence. |
| S20-IT-09 | Lyapunov exponents | Dynamical systems statistic | Partial | Distinguish largest-exponent estimators and embedding assumptions; compare with analytic systems. |
| S20-IT-10 | Granger causality | Predictive temporal dependence test | Open | Define lag/order, stationarity and confounders; distinguish prediction from causal identification. |
| S20-IT-11 | Transfer entropy | Information-flow statistic | Open | Define estimator, conditioning and bias correction; test known directed synthetic processes. |
| S20-IT-12 | Convergent cross mapping | Nonlinear causality method | Open | Verify original formulation; test convergence and common-driver failure cases. |
| S20-IT-13 | PCMCI-style causal networks for gridded fields | Causal discovery workflow | Verify | Verify exact PCMCI variant and assumptions; define lagged graph, autocorrelation and spatial confounding. |
| S20-IT-14 | Teleconnection graphs | Climate network representation | Open | Define nodes, edge statistic, significance and multiple testing; test surrogate nulls. |

### Phylogeography, epidemiology and survey sampling — page 43

| ID | Atomic item | Kind | Evidence/status | Required completion work |
|---|---|---|---|---|
| S20-PH-01 | SAX symbolic aggregate approximation | Time-series representation | Open | Verify breakpoints and word encoding; test reconstruction and distance lower-bound properties. |
| S20-PH-02 | Shapelets | Time-series classification feature | Open | Define discovery/selection method and distance; test leakage-safe classification. |
| S20-PH-03 | Matrix profile | Time-series motif/discord discovery | Open | Verify distance profile definition and exclusion zone; compare with brute-force oracle. |
| S20-PH-04 | Spatial time-series motif discovery | Pattern discovery | Open | Define spatial alignment, temporal window and distance; test synthetic repeated motifs. |
| S20-PH-05 | Continuous phylogeographic diffusion (BEAST-style) | Bayesian phylogeographic model | Verify | Identify BEAST module/model and version; document tree prior, diffusion process and coordinate projection. |
| S20-PH-06 | BSSVS for spread-route inference | Bayesian variable selection | Verify | Verify exact model and prior; document inclusion indicators and posterior interpretation. |
| S20-PH-07 | Genomic epidemiology with spatial covariates | Integrated modelling workflow | Open | Define sequence/phylogeny and spatial covariates; protect privacy and assess sampling bias. |
| S20-PH-08 | Bayesian reproduction-number maps | Epidemiological spatial model | Open | Define Rt estimand, generation interval and spatial dependence; test posterior calibration. |
| S20-PH-09 | Spatial Rt estimation | Epidemiological estimation | Open | Distinguish local Rt estimators and transmission kernels; validate against synthetic epidemics. |
| S20-PH-10 | Nowcasting with reporting delays | Bayesian/statistical nowcasting | Open | Define delay distribution, right truncation and revision process; backtest by issue date. |
| S20-PH-11 | Wastewater surveillance spatial models | Environmental epidemiology | Open | Define catchment, flow/population normalisation and sampling; document uncertainty and privacy. |
| S20-PH-12 | EPI cluster sampling | Survey design | Verify | Identify EPI protocol/version and design assumptions; test selection probabilities and design effects. |
| S20-PH-13 | Lot Quality Assurance Sampling (LQAS) | Survey design / decision rule | Verify | Verify classification thresholds and sampling design; test operating characteristics. |
| S20-PH-14 | Sampling frames from building footprints and imagery | Spatial sampling-frame construction | Open | Define frame completeness, inclusion probabilities and settlement coverage; field-audit omissions. |
| S20-PH-15 | DHS cluster GPS displacement and correction | Survey geospatial disclosure workflow | Verify | Verify DHS policy/version and displacement distributions; preserve confidentiality and avoid reverse-identification. |

### Urban 3D and growth — page 43

| ID | Atomic item | Kind | Evidence/status | Required completion work |
|---|---|---|---|---|
| S20-U3-01 | Building height from radar | 3D remote-sensing estimation | Open | Identify sensor/method and layover/shadow limits; validate against surveyed heights. |
| S20-U3-02 | Building height from stereo imagery | Photogrammetric estimation | Open | Define stereo geometry, matching and datum; compare with lidar/control data. |
| S20-U3-03 | Floor-count inference | Building attribute estimation | Open | Define evidence (height, imagery, footprints), regional priors and uncertainty; validate field labels. |
| S20-U3-04 | Urban volume estimation | 3D urban metric | Open | Define building geometry and volume convention; test synthetic solids and incomplete footprints. |
| S20-U3-05 | 3D city-model generation from oblique imagery | 3D reconstruction workflow | Open | Define camera calibration, multi-view reconstruction and semantic attributes; document accuracy/LOD. |
| S20-U3-06 | Urban growth boundary delineation | Spatial delineation method | Open | Define built-up mask, contiguity and planning criteria; compare alternative boundary rules. |
| S20-U3-07 | Spatially constrained urban expansion modelling | Urban simulation | Open | Define transition potential, neighbourhood constraints and calibration; validate hindcast and uncertainty. |

## Completion gates

1. Resolve exact identity, variant, acronym and version against primary literature, official standards or maintained project documentation.
2. Record formula/equations, units, coordinate/sensor conventions, input requirements, calibration domain and failure modes.
3. Distinguish index calculation from sensor calibration, retrieval, validation and downstream interpretation.
4. Implement only a clearly specified method; document wrappers and external dependencies accurately.
5. Test with analytical fixtures, synthetic truth, published benchmarks or independent implementations; include edge cases and uncertainty.
6. Provide a canonical lesson, implementation walkthrough and runnable example/notebook where educationally useful.
7. Reconcile source indexes, implementation indexes, coverage matrix and dashboard after evidence changes.
8. Review rights and provenance for source text, data, imagery, software and model weights.

## Execution priorities

1. Resolve high-impact sensor/model identities first: ASTER indices, TES, microwave scattering models, RVoG, tau–omega, GPROF, CMOD5, TempestExtremes and ARTMIP.
2. Expand the existing spectral-index, thermal-retrieval, triple-collocation, event and information-theory implementations only against verified variants.
3. Treat satellite products, mission workflows and named software systems as versioned systems rather than standalone algorithms.
4. Implement mathematically self-contained methods with independent tests before attempting large coupled climate, ocean or epidemiological models.
5. Reconcile all 22 sections and run full CI, notebook and release checks before declaring completion.

**Current conclusion:** Section 20 is decomposed into atomic review items. It remains open; this register is a traceability backlog, not a verification or completion claim.
