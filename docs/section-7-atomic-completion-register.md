# Section 7 atomic completion register

**Source:** *Spatial Analysis Algorithms: Complete Compendium*, Section 7, pages 12–14.  
**Intake:** [preserved pages 11–15 transcription](../source-inventory/pages-11-15.md).  
**Section index:** [Section 7 catalogue record](../catalog/sections/07-domain-modeling.md).

The source groups many specialist methods and named software systems. This register splits those into auditable child records and keeps frameworks, models, indices, software and workflows distinct. Follow the [verification protocol](../catalog/verification-protocol.md) and [completion standard](compendium-completion-standard.md).

| Status | Meaning |
|---|---|
| Open | No item-specific independent evidence recorded. |
| Partial | A bounded related implementation exists; variants or validation remain open. |
| Verify | Exact method, model, acronym or product version must be resolved. |
| Not applicable | A framework, platform or applied workflow is not one standalone algorithm. |

## Atomic source register

### Land change and simulation — page 12

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S07-LC-01 | Cellular automata (CA) | Spatial simulation framework | Partial | Define neighbourhood, transition rule and synchronous/asynchronous update. |
| S07-LC-02 | SLEUTH | Urban growth CA model | Verify | Pin version and calibration procedure; document slope/exclusion/urban inputs. |
| S07-LC-03 | ANN-CA | Neural cellular automata model | Verify | Resolve exact formulation; document training, neighbourhood and transition probabilities. |
| S07-LC-04 | Logistic-CA | Statistical CA model | Verify | Define logistic transition model and sampling; test calibration and spatial dependence. |
| S07-LC-05 | Markov-CA | Hybrid land-change model | Verify | Define transition matrix, CA allocation and temporal stationarity. |
| S07-LC-06 | CLUE-S | Land-use change model | Verify | Identify version and allocation constraints; document demand/competition calibration. |
| S07-LC-07 | FLUS | Future Land Use Simulation | Verify | Verify adaptive inertia competition mechanism and version; test scenario reproducibility. |
| S07-LC-08 | PLUS | Patch-generating land-use simulation | Verify | Verify LEAS/CARS components and version; test patch-level allocation. |
| S07-LC-09 | Dinamica EGO | Land-change modelling platform | Verify | Pin version and transition functions; document licence and workflow. |
| S07-LC-10 | Land Change Modeler | Land-change modelling software | Verify | Identify vendor/version and transition modelling; document reproducibility/licence. |
| S07-LC-11 | Agent-based models | Simulation family | Open | Define agents, state, behaviour and interaction; test calibration and emergent behaviour. |
| S07-LC-12 | Markov-chain land-use change | Stochastic transition model | Partial | Define states, transition interval and stationarity; test matrix powers and uncertainty. |
| S07-LC-13 | Monte Carlo spatial simulation | Stochastic simulation family | Partial | Specify stochastic process, spatial dependence and seed; test distributional recovery. |
| S07-LC-14 | Schelling segregation model | Agent-based model | Verify | Verify neighbourhood preference and update rules; reproduce phase transitions. |
| S07-LC-15 | Sugarscape | Agent-based artificial society model | Verify | Identify canonical ruleset/variant; document resource, movement and reproduction assumptions. |
| S07-LC-16 | Percolation models | Spatial stochastic process | Partial | Define site/bond and lattice; test critical behaviour and finite-size effects. |
| S07-LC-17 | Diffusion-limited aggregation | Stochastic growth model | Verify | Verify random walk/attachment rules; test fractal scaling. |
| S07-LC-18 | Sandpile models | Self-organised criticality model | Verify | Specify deterministic/stochastic toppling and boundary; test avalanche distributions. |
| S07-LC-19 | Forest-fire models | Cellular stochastic model | Verify | Define ignition, growth and suppression rules; test scaling and boundary conditions. |
| S07-LC-20 | Spatial game theory | Model family | Open | Define strategy, payoff, neighbourhood and update rule; separate replicator/agent models. |
| S07-LC-21 | Spatial random graphs | Graph model family | Open | Define vertex process, spatial connection kernel and degree distribution. |
| S07-LC-22 | Distance-decay preferential attachment | Spatial network growth | Verify | Define attachment kernel and spatial constraints; test degree/length distributions. |
| S07-LC-23 | Small-world networks | Graph model family | Verify | Identify lattice rewiring variant; test clustering/path length. |
| S07-LC-24 | Scale-free networks | Graph model family | Verify | Define generative process and power-law evidence; avoid visual/finite-sample overclaim. |

### Multi-criteria and decision support — page 12

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S07-MC-01 | Weighted overlay | Multi-criteria decision method | Partial | Define scaling, weights and compensation; test sensitivity. |
| S07-MC-02 | Boolean overlay | Decision rule | Partial | Define threshold logic and missing data; test constraint combinations. |
| S07-MC-03 | Analytic Hierarchy Process (AHP) | Multi-criteria method | Partial | Existing `ahp-weights` package derives a normalised principal-eigenvector priority vector from a positive reciprocal pairwise matrix and reports lambda-max, CI and conventional CR (RI table orders 1–10; CR undefined for n≤2). Tests recover analytic ratio weights, check consistency and reject invalid matrices/names. Stakeholder elicitation, hierarchy construction, aggregation, rank-reversal analysis and exact source-variant verification remain open. |
| S07-MC-04 | Fuzzy overlay | Fuzzy decision method | Partial | Existing `fuzzy-overlay` package supplies Boolean AND/OR masks and fuzzy min, max, product, probabilistic-sum and gamma operators with strict common-footprint NoData propagation. Tests cover analytic values, gamma endpoints, zero memberships, shape/dtype/range validation. Membership-curve design, geospatial alignment/CRS handling, decision semantics and source-specific operator variants remain open. |
| S07-MC-05 | TOPSIS | Multi-criteria ranking | Verify | Verify normalisation, ideal/anti-ideal and distance; test criterion direction. |
| S07-MC-06 | ELECTRE | Outranking method family | Partial | Existing `electre-i` package implements a bounded ELECTRE I-style weighted concordance and range-normalised discordance relation, plus exhaustive internal/external-stability kernel enumeration for small choice sets (default cap 20). Tests cover benefit/cost directions, ties, incompleteness, thresholds and relation properties. This is not ELECTRE III/TRI, does not elicit weights or thresholds, and is not a complete ranking; exact source variant and decision-threshold justification remain open. |
| S07-MC-07 | Ordered Weighted Averaging (OWA) | Aggregation operator | Partial | Existing `owa` package implements standard OWA and GIS weighted OWA: values are sorted per cell, order weights attach to rank positions, and criterion importance weights are reordered with the values. It includes orness, strict common-footprint NoData and tests for max/min/mean endpoints and weighted examples. It does not derive weights, align georeferenced rasters or validate the decision model; source-specific variants remain open. |
| S07-MC-08 | Weights of evidence | Bayesian evidence method | Verify | Define conditional independence and contrast; test evidence correlation. |
| S07-MC-09 | Spatial decision support | Decision workflow | Not applicable | Document alternatives, constraints, stakeholder process and provenance. |
| S07-MC-10 | Participatory GIS | Participatory method | Not applicable | Document participation, representation, consent and uncertainty. |
| S07-MC-11 | Scenario analysis | Decision workflow | Not applicable | Define scenarios, assumptions and sensitivity; do not present scenarios as forecasts. |
| S07-MC-12 | InVEST | Ecosystem service modelling suite | Verify | Pin version/model module and data requirements; document assumptions and licence. |
| S07-MC-13 | Social Vulnerability Index (SoVI) | Composite index | Verify | Identify exact edition, variables and PCA/weighting; test sensitivity and ecological fallacy. |
| S07-MC-14 | Multi-hazard risk index | Composite risk metric | Open | Define hazard, exposure, vulnerability and aggregation; preserve non-compensability. |
| S07-MC-15 | Compound-risk index | Composite risk metric | Open | Define dependence and joint exceedance; test correlation and tail risk. |
| S07-MC-16 | Environmental justice index | Equity metric family | Open | Identify jurisdiction-specific index; define exposure, sensitivity and demographics. |
| S07-MC-17 | Integral Index of Connectivity (IIC) | Landscape connectivity metric | Verify | Verify graph patch definition and probability of connectivity; test small landscapes. |
| S07-MC-18 | Probability of Connectivity (PC) | Landscape connectivity metric | Verify | Verify dispersal probability and component decomposition; test distance-decay assumptions. |

### Ecology and conservation — pages 12–13

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S07-EC-01 | MaxEnt | Species distribution model | Verify | Pin version and feature classes/regularisation; document sampling bias and background. |
| S07-EC-02 | BIOCLIM | Climate-envelope model | Verify | Verify percentile envelope and implementation; assess extrapolation. |
| S07-EC-03 | Habitat suitability modelling | Model family | Open | Split expert, statistical and ML models; define validation and thresholds. |
| S07-EC-04 | Joint species distribution models (JSDM) | Multispecies model family | Open | Define residual association and environmental response; assess identifiability. |
| S07-EC-05 | Occupancy models | Detection-corrected ecological model | Partial | Define detection/occupancy hierarchy and repeat surveys; test identifiability. |
| S07-EC-06 | N-mixture models | Abundance estimation model | Verify | Verify closure/detection assumptions; assess identifiability and overdispersion. |
| S07-EC-07 | Spatial capture–recapture | Population estimation model | Verify | Define detector geometry, movement and encounter process; test simulated populations. |
| S07-EC-08 | Distance sampling | Abundance estimation method | Verify | Verify detection function and truncation; test effective strip width. |
| S07-EC-09 | Circuitscape | Connectivity modelling software | Verify | Pin version and circuit formulation; document resistance, boundary and licence. |
| S07-EC-10 | Omniscape | Moving-window connectivity software | Verify | Pin version and focal/current density semantics; document scale sensitivity. |
| S07-EC-11 | Conefor | Connectivity analysis software | Verify | Pin version and PC/IIC metrics; document dispersal thresholds. |
| S07-EC-12 | Least-cost corridors | Connectivity workflow | Partial | Define resistance surface and corridor method; compare with circuit-theory alternatives. |
| S07-EC-13 | Dispersal kernels | Ecological movement model | Open | Define kernel family, tail and scale; fit to telemetry/mark-recapture. |
| S07-EC-14 | Metapopulation models | Ecological dynamics family | Open | Define patch occupancy, colonisation/extinction and connectivity. |
| S07-EC-15 | FRAGSTATS | Landscape metrics software | Verify | Pin version and metric definitions; document raster/patch adjacency and licence. |
| S07-EC-16 | Patch density | Landscape metric | Partial | Define patch count/area denominator and class/landscape level. |
| S07-EC-17 | Edge density | Landscape metric | Partial | Define edge types, units and boundary treatment. |
| S07-EC-18 | Contagion | Landscape configuration metric | Verify | Verify adjacency matrix and normalisation; test raster resolution. |
| S07-EC-19 | Alpha diversity | Biodiversity metric | Partial | Define richness/evenness metric and sampling effort. |
| S07-EC-20 | Beta diversity | Biodiversity metric family | Open | Split turnover/nestedness and dissimilarity measures; define abundance/presence. |
| S07-EC-21 | Species–area relationships | Ecological scaling model | Verify | Define functional form and sampling design; test scale and extrapolation. |
| S07-EC-22 | Isolation by distance | Population genetics statistic/model | Verify | Verify genetic distance and geographic distance regression; account for spatial autocorrelation. |
| S07-EC-23 | Isolation by resistance | Landscape genetics method | Verify | Define resistance optimisation and circuit/least-cost distance; avoid circular inference. |
| S07-EC-24 | Spatial PCA | Spatial genetics method | Verify | Identify exact spatial PCA formulation and weights; test structure recovery. |
| S07-EC-25 | Geneland | Landscape genetics software/model | Verify | Pin version and spatial prior; document MCMC and priors. |
| S07-EC-26 | TESS | Spatial genetic clustering software | Verify | Identify exact TESS version and admixture model; document inference. |
| S07-EC-27 | Wombling | Boundary analysis method | Verify | Verify gradient/boundary formulation; test known discontinuities. |
| S07-EC-28 | Allele-frequency autocorrelation | Spatial genetics statistic | Open | Define distance classes and estimator; test sampling/kinship effects. |

### Agriculture and forestry — page 13

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S07-AG-01 | DSSAT | Crop simulation software | Verify | Pin version/crop modules and input requirements; document calibration. |
| S07-AG-02 | APSIM | Farming systems simulator | Verify | Pin version and modules; document soil/weather/management inputs. |
| S07-AG-03 | WOFOST | Crop growth model | Verify | Identify version and crop parameters; validate phenology/yield. |
| S07-AG-04 | AquaCrop | Crop water productivity model | Verify | Pin version and water balance; document calibration and applicability. |
| S07-AG-05 | SCYM | Satellite-based crop yield model | Verify | Resolve exact model/paper and input data; validate crop/region transfer. |
| S07-AG-06 | Regression crop-yield estimation | Statistical prediction family | Open | Define predictors, spatial/temporal splits and yield reference. |
| S07-AG-07 | Deep-learning crop-yield estimation | ML prediction family | Open | Identify architecture and labels; test transfer and uncertainty. |
| S07-AG-08 | Crop calendar estimation | Phenology workflow | Open | Define crop stages and temporal observations; validate against field calendars. |
| S07-AG-09 | TIMESAT | Phenology software | Verify | Pin version and fitting method; document season extraction. |
| S07-AG-10 | Savitzky–Golay smoothing | Signal smoothing | Partial | Define window/order and edge handling; test peak preservation. |
| S07-AG-11 | Field boundary delineation | EO vector extraction | Partial | Split segmentation and temporal methods; validate geometry/topology. |
| S07-AG-12 | Irrigation detection | EO classification workflow | Open | Define crop/water signatures and temporal evidence; validate field observations. |
| S07-AG-13 | Crop rotation mapping | Time-series classification | Open | Define crop sequence labels and temporal coverage; test missing seasons. |
| S07-AG-14 | Forest disturbance mapping | Change detection workflow | Partial | Split optical/radar and alert methods; quantify detection delay/false alarms. |
| S07-AG-15 | Biomass estimation | Biophysical model family | Open | Define allometry/remote-sensing model and support; validate field plots. |
| S07-AG-16 | Allometric equations | Biomass estimation model | Verify | Identify species/region/equation and units; quantify extrapolation. |
| S07-AG-17 | Species classification from hyperspectral/LiDAR | Classification workflow | Open | Define species taxonomy and sensor features; spatially independent validation. |
| S07-AG-18 | Growing degree days (GDD) | Agroclimate metric | Partial | Define base/upper temperatures and accumulation; test missing temperature. |
| S07-AG-19 | SPI | Drought index | Partial | Define accumulation scale and distribution fit; test zero precipitation. |
| S07-AG-20 | SPEI | Drought index | Verify | Verify PET method and log-logistic fitting; document time scale. |
| S07-AG-21 | VCI | Vegetation condition index | Partial | Define NDVI climatology period and scaling; test sensor consistency. |
| S07-AG-22 | PDSI | Drought index/model | Verify | Verify Palmer water balance and calibration; document regional limitations. |
| S07-AG-23 | Crop stress detection | Monitoring workflow | Open | Define stress label and sensor/biophysical mechanism; validate independent observations. |

### Weather, climate and air quality — page 13

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S07-WC-01 | Weather radar clutter filtering | Radar processing family | Open | Split statistical/texture/polarimetric filters; test precipitation preservation. |
| S07-WC-02 | Radar attenuation correction | Radar correction | Verify | Verify path-integrated attenuation methods; test heavy precipitation. |
| S07-WC-03 | Z–R relationship | Radar rainfall estimation | Verify | Define coefficients and drop-size regime; calibrate regionally. |
| S07-WC-04 | Hydrometeor classification | Radar classification | Open | Define polarimetric features and class priors; validate with gauges/radar. |
| S07-WC-05 | TITAN storm tracking | Weather radar tracking software | Verify | Pin version and tracking parameters; test split/merge events. |
| S07-WC-06 | SCIT storm identification/tracking | Weather radar algorithm | Verify | Verify exact method and version; compare with TITAN. |
| S07-WC-07 | TREC motion estimation | Radar echo tracking | Verify | Verify cross-correlation motion estimation and quality control. |
| S07-WC-08 | pySTEPS | Precipitation nowcasting software | Verify | Pin version and ensemble nowcasting modules; document motion/extrapolation assumptions. |
| S07-WC-09 | Optical-flow nowcasting | Short-term precipitation forecast | Partial | Split optical flow algorithms; test advection and growth/decay. |
| S07-WC-10 | IMERG | Satellite precipitation product | Verify | Pin version and algorithm; document gauge adjustment and latency. |
| S07-WC-11 | PERSIANN | Satellite precipitation retrieval | Verify | Pin model/product version; document input sensors and calibration. |
| S07-WC-12 | CMORPH | Satellite precipitation product | Verify | Verify morphing algorithm and product version; document bias correction. |
| S07-WC-13 | Radar–gauge merging | Data fusion workflow | Open | Define bias correction/kriging and gauge representativeness; test extremes. |
| S07-WC-14 | Köppen climate classification | Climate classification | Verify | Define period and climate normals; test class boundary sensitivity. |
| S07-WC-15 | ETCCDI climate indices | Climate extremes indices | Verify | Pin definitions and software; document baseline and missing data. |
| S07-WC-16 | ERA5 processing | Reanalysis workflow | Verify | Pin dataset release and variables; document grid/time semantics and licence. |
| S07-WC-17 | Climate bias correction | Statistical correction family | Open | Split univariate/multivariate and trend-preserving methods; test tails/spatial coherence. |
| S07-WC-18 | Local Climate Zones (LCZ) | Urban climate classification | Verify | Verify WUDAPT classification and classes; document training/validation. |
| S07-WC-19 | Urban heat island analysis | Urban climate workflow | Open | Define canopy/surface UHI and temporal baseline; validate with stations. |
| S07-WC-20 | Land-use regression (LUR) | Exposure prediction model | Partial | Define monitoring design and covariates; spatial CV and external validation. |
| S07-WC-21 | AERMOD | Atmospheric dispersion model | Verify | Pin version and regulatory options; document meteorology/terrain. |
| S07-WC-22 | CALPUFF | Atmospheric dispersion model | Verify | Pin version and chemistry/meteorology options; document applicability. |
| S07-WC-23 | CMAQ | Chemical transport model | Verify | Pin version and configuration; document emissions and boundary conditions. |
| S07-WC-24 | WRF-Chem | Coupled weather-chemistry model | Verify | Pin version/chemistry options; document emissions and evaluation. |
| S07-WC-25 | GEOS-Chem | Chemical transport model | Verify | Pin version and grid/nesting; document emissions and licence. |
| S07-WC-26 | AOD-based PM2.5 estimation | Exposure estimation workflow | Partial | Define AOD retrieval, vertical profile and monitor calibration; assess missingness. |
| S07-WC-27 | Low-cost sensor fusion | Environmental sensor workflow | Open | Define calibration, drift and spatial interpolation; validate against reference stations. |
| S07-WC-28 | ISO 9613 noise propagation | Environmental acoustics standard/model | Verify | Identify part/version and terrain/building assumptions; test sound levels. |
| S07-WC-29 | CNOSSOS-EU | Environmental noise model | Verify | Pin directive/technical method version; document traffic/rail/industry inputs. |
| S07-WC-30 | Gaussian plume dispersion | Atmospheric dispersion model | Partial | Define stability, wind and source assumptions; test mass conservation. |
| S07-WC-31 | HYSPLIT | Lagrangian dispersion software | Verify | Pin version and meteorology; document trajectory/concentration settings. |
| S07-WC-32 | Volcanic ash dispersion | Hazard modelling workflow | Open | Define source term, particle settling and meteorology; validate against observations. |

### Hazards and risk — page 13

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S07-HA-01 | Probabilistic seismic hazard analysis (PSHA) | Hazard assessment framework | Verify | Define source recurrence, ground-motion models and logic tree; document epistemic uncertainty. |
| S07-HA-02 | Ground-motion prediction equations | Ground-motion model family | Open | Identify model versions and applicability; validate residuals and site terms. |
| S07-HA-03 | ETAS earthquake model | Seismic point process | Verify | Cross-link exact ETAS model; verify productivity/triggering and magnitude scaling. |
| S07-HA-04 | Coulomb stress transfer | Geophysical stress model | Verify | Define fault geometry, friction and stress convention; test sign/unit consistency. |
| S07-HA-05 | PAGER loss estimation | Earthquake impact system | Verify | Identify current methodology/version; distinguish official product from general exposure modelling. |
| S07-HA-06 | Tsunami propagation | Hydrodynamic hazard modelling | Open | Define source, bathymetry and solver; validate travel time/runup. |
| S07-HA-07 | Rothermel fire spread | Wildfire spread model | Verify | Verify fuel/heat/moisture equations and assumptions; test benchmark cases. |
| S07-HA-08 | FARSITE | Wildfire simulation software | Verify | Pin version and fire behaviour modules; document fuels/weather/topography. |
| S07-HA-09 | Elliptical fire spread | Fire geometry model | Verify | Define ellipse parameters and wind/slope; validate against observed perimeters. |
| S07-HA-10 | Fire risk indices | Risk index family | Open | Split indices and calibration; distinguish hazard, exposure and vulnerability. |
| S07-HA-11 | xBD-style building damage classification | Remote-sensing workflow | Verify | Identify dataset/model version; document classes, pre/post registration and licence. |
| S07-HA-12 | Catastrophe loss models | Risk model family | Open | Define hazard, vulnerability, exposure and financial modules; document uncertainty. |
| S07-HA-13 | Exposure aggregation | Risk calculation workflow | Partial | Define spatial overlay and portfolio aggregation; test double counting. |
| S07-HA-14 | Contraflow evacuation | Traffic operations workflow | Open | Define reversible capacity, access control and demand; simulate network stability. |
| S07-HA-15 | Capacity-constrained evacuation routing | Routing optimisation | Partial | Define departure time, shelter capacity and congestion; test assignment feasibility. |
| S07-HA-16 | Crowd simulation | Agent/flow model family | Open | Split social-force/cellular/continuum models; validate density and evacuation times. |
| S07-HA-17 | Shelter location | Facility location optimisation | Partial | Define capacity, hazard exposure and equity; compare robust scenarios. |
| S07-HA-18 | Near-repeat analysis | Crime/event statistic | Verify | Verify temporal/spatial kernel and risk window; test baseline and false positives. |
| S07-HA-19 | Risk Terrain Modeling (RTM) | Spatial risk modelling workflow | Verify | Identify RTM formulation/software and validation; document factor selection. |
| S07-HA-20 | STAC crime analysis | Crime analysis framework | Verify | Resolve acronym and exact methodology; avoid conflating with Spatio-Temporal Analysis of Crime or data catalogue STAC. |

### Health and epidemiology — page 13

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S07-HE-01 | BYM disease mapping | Bayesian spatial model | Partial | Cross-link BYM/BYM2; document priors, scaling and confounding. |
| S07-HE-02 | Standardised morbidity/mortality ratios | Epidemiological metric | Partial | Define standard population and expected counts; document instability for small areas. |
| S07-HE-03 | Empirical Bayes disease smoothing | Rate estimation | Partial | Define prior and area population; compare with direct rates. |
| S07-HE-04 | SIR on networks | Epidemic network model | Open | Define transmission/recovery and network; test stochastic simulation. |
| S07-HE-05 | Reaction–diffusion epidemic model | PDE model | Open | Define diffusion, reaction and boundary conditions; test mass/positivity. |
| S07-HE-06 | Metapopulation epidemic model | Compartmental network model | Open | Define patches, mobility and transmission; validate mobility coupling. |
| S07-HE-07 | Gravity-based importation | Spatial interaction epidemiology | Partial | Define origin prevalence, travel impedance and importation; test conservation. |
| S07-HE-08 | Mobility-driven forecasting | Forecast workflow | Open | Define mobility data, privacy and causal assumptions; validate temporal/geographic holdout. |
| S07-HE-09 | MaxEnt vector-borne risk | Species/environment model | Verify | Identify exact vector species and MaxEnt formulation; assess sampling bias. |
| S07-HE-10 | Mechanistic temperature models | Vector suitability model family | Open | Define vector life-cycle/temperature response and validation. |
| S07-HE-11 | Contact-tracing graphs | Contact network workflow | Open | Define exposure edge/time and uncertainty; protect identities and sensitive data. |
| S07-HE-12 | Spatial survival analysis | Survival model family | Open | Define spatial frailty and censoring; test proportional hazards. |
| S07-HE-13 | Personal exposure from trajectories | Exposure assessment workflow | Open | Define time-activity and concentration field; quantify missingness and privacy. |
| S07-HE-14 | Environmental justice analysis | Equity assessment | Open | Define exposure, population and distributional metric; document causal limitations. |

### Urban and socioeconomic — pages 13–14

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S07-UR-01 | VIIRS nighttime lights harmonisation | EO harmonisation workflow | Verify | Pin product/version and intersensor calibration; test saturation/background. |
| S07-UR-02 | Poverty mapping | Socioeconomic estimation | Open | Define target, labels and spatial support; evaluate uncertainty and transfer. |
| S07-UR-03 | Wealth mapping | Socioeconomic estimation | Open | Define wealth measure and training data; assess ecological inference and privacy. |
| S07-UR-04 | GHSL urban extent | Urban settlement product | Verify | Pin GHSL release and built-up/urban definitions; document licence. |
| S07-UR-05 | WSF urban extent | Urban settlement product | Verify | Pin World Settlement Footprint release and class semantics. |
| S07-UR-06 | Impervious surface mapping | EO classification workflow | Partial | Define impervious fraction and validation; test seasonal/sensor transfer. |
| S07-UR-07 | Informal settlement detection | EO classification workflow | Open | Define evidence and local context; address harms, uncertainty and sensitive publication. |
| S07-UR-08 | Building height estimation | 3D attribute inference | Partial | Split stereo/shadow/LiDAR/ML methods; validate independent heights. |
| S07-UR-09 | Building footprint estimation | Vector extraction | Partial | Split segmentation/polygon methods; evaluate geometry and topology. |
| S07-UR-10 | Footprint regularisation | Geometry postprocessing | Partial | Define orthogonality/parallelism priors; preserve true irregular geometry. |
| S07-UR-11 | Footprint orthogonalisation | Geometry postprocessing | Partial | Define angle/edge constraints and tolerance; test rotated/irregular buildings. |
| S07-UR-12 | Urban morphometrics | Metric family | Open | Split building/block/street measures; define scale and units. |
| S07-UR-13 | Walkability | Accessibility metric family | Open | Define network, destinations, slope, safety and weighting; test equity. |
| S07-UR-14 | POI topic-model land-use inference | Text/spatial classification | Open | Define POI taxonomy, topic model and spatial unit; validate against surveys. |
| S07-UR-15 | Place2Vec | POI/place embedding model | Verify | Verify exact model and training corpus; document spatial context/window. |
| S07-UR-16 | Functional zone discovery | Urban classification workflow | Open | Split clustering/flow-based methods; validate temporal stability. |
| S07-UR-17 | Alonso–Muth–Mills model | Urban economics theory/model | Verify | State assumptions, equilibrium and comparative statics; distinguish theory from estimator. |
| S07-UR-18 | von Thünen model | Land-use location theory | Verify | Define transport/land rent assumptions; identify extensions. |
| S07-UR-19 | Hotelling model | Spatial competition theory | Verify | Define location/price competition and equilibrium assumptions. |
| S07-UR-20 | Central place theory | Spatial economic theory | Verify | Define hierarchy/market assumptions; distinguish theoretical geometry from empirical model. |
| S07-UR-21 | Rank-size rule | Urban system statistic | Partial | Define rank/size sample and Zipf exponent; test uncertainty and city definition. |
| S07-UR-22 | Location quotient | Regional specialisation metric | Partial | Define employment/output base and reference region; test zero denominators. |
| S07-UR-23 | Shift-share analysis | Regional decomposition | Partial | Define national/industry/competitive components; document reference period. |
| S07-UR-24 | Agglomeration analysis | Urban economics family | Open | Split localisation/urbanisation and identification; avoid causal overclaim. |
| S07-UR-25 | Land value capitalisation | Hedonic/urban economic model | Open | Define price/rent outcome, spatial effects and causal assumptions. |
| S07-UR-26 | Urban scaling laws | Scaling relationship | Verify | Verify allometric regression and city boundary sensitivity; test confidence intervals. |
| S07-UR-27 | Urban digital twins | Platform/workflow | Not applicable | Define model/data synchronization, provenance and uncertainty; not one algorithm. |
| S07-UR-28 | CityGML processing | 3D city data standard/workflow | Verify | Pin CityGML version and schema; test semantic/geometric conformance. |
| S07-UR-29 | CityJSON processing | 3D city data format/workflow | Verify | Pin CityJSON version and extensions; test round-trip/conformance. |
| S07-UR-30 | Rooftop solar potential | Energy suitability workflow | Open | Define roof segmentation, shading, irradiance and panel assumptions; validate. |
| S07-UR-31 | Parcel subdivision | Cadastre geometry workflow | Open | Define legal rules, topology and area constraints; require cadastral review. |
| S07-UR-32 | COGO | Survey computation workflow | Verify | Define coordinate/angle/distance conventions and traverse closure. |
| S07-UR-33 | Traverse computation | Survey adjustment method | Partial | Define open/closed traverse and error distribution; test closure. |
| S07-UR-34 | Survey network adjustment | Geodetic estimation | Partial | Define observations, datum constraints and covariance; test residuals. |
| S07-UR-35 | Cadastral topological validation | QA workflow | Partial | Define parcel adjacency/overlap/gap rules and legal exception handling. |

### Energy and infrastructure — page 14

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S07-EN-01 | WAsP | Wind resource modelling software | Verify | Pin version and terrain/roughness model; document licence and validation. |
| S07-EN-02 | Jensen wake model | Wind turbine wake model | Verify | Verify top-hat wake assumptions and expansion coefficient; test power deficit. |
| S07-EN-03 | Park wake model | Wind farm wake model | Verify | Identify exact Park/Jensen implementation and superposition; document calibration. |
| S07-EN-04 | NREL Solar Position Algorithm (SPA) | Solar geometry algorithm | Verify | Pin algorithm version and time/coordinate conventions; test reference ephemerides. |
| S07-EN-05 | Ineichen clear-sky model | Solar irradiance model | Verify | Verify Linke turbidity and altitude assumptions; test clear-sky irradiance. |
| S07-EN-06 | Perez transposition model | Solar irradiance transposition | Verify | Verify diffuse sky model coefficients and input irradiance; test orientation. |
| S07-EN-07 | REST2 | Clear-sky irradiance model | Verify | Verify atmospheric input requirements and spectral bands; compare reference. |
| S07-EN-08 | PV yield estimation | Energy production workflow | Open | Define module/inverter, temperature and shading; validate measured output. |
| S07-EN-09 | Hydropower potential | Energy resource assessment | Open | Define head, flow duration and environmental constraints; quantify uncertainty. |
| S07-EN-10 | Least-cost transmission corridors | Infrastructure routing optimisation | Partial | Define terrain, land rights and engineering costs; compare network alternatives. |
| S07-EN-11 | Pipeline routing | Infrastructure routing optimisation | Open | Define terrain, hazard, environmental and construction constraints; test feasibility. |
| S07-EN-12 | Electrification planning | Energy access optimisation | Open | Define demand, grid extension, mini-grid and affordability; scenario-test. |
| S07-EN-13 | Mini-grid sizing | Energy system optimisation | Open | Define load, generation, storage and reliability; test hourly simulation. |
| S07-EN-14 | Capacity expansion | Energy planning optimisation | Open | Define investment horizon, dispatch and uncertainty; validate scenarios. |
| S07-EN-15 | Okumura–Hata propagation | RF propagation model | Verify | Verify frequency/distance/antenna domains and urban/suburban variants. |
| S07-EN-16 | COST-231 Hata | RF propagation model | Verify | Verify frequency/height limits and environment corrections. |
| S07-EN-17 | ITM / Longley–Rice | Terrain-aware propagation model | Verify | Pin version and variability mode; test terrain profiles. |
| S07-EN-18 | Ray-tracing radio propagation | RF simulation method | Open | Define reflections/diffraction/materials and geometry; validate against measurements. |

### Ocean, cryosphere and marine — page 14

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S07-OC-01 | WAVEWATCH III | Wave model software | Verify | Pin version and source terms; document grids/forcing and validation. |
| S07-OC-02 | SWAN | Nearshore wave model | Verify | Pin version and physics options; document bathymetry/boundary. |
| S07-OC-03 | ADCIRC | Hydrodynamic circulation model | Verify | Pin version and mesh/forcing; document wetting/drying and validation. |
| S07-OC-04 | T_TIDE | Tidal harmonic analysis software | Verify | Pin version and constituent selection; test nodal corrections. |
| S07-OC-05 | UTide | Tidal harmonic analysis software | Verify | Pin version and inference options; compare with T_TIDE. |
| S07-OC-06 | Ocean drift / Lagrangian particle tracking | Ocean transport workflow | Open | Define currents, diffusion, windage and beaching; test mass conservation. |
| S07-OC-07 | Oil spill SAR detection | EO detection workflow | Open | Define slick classes and lookalikes; validate with confirmed incidents. |
| S07-OC-08 | Ship detection | Maritime EO detection | Partial | Split SAR/optical methods and detector; assess false positives. |
| S07-OC-09 | AIS anomaly analysis | Trajectory anomaly workflow | Partial | Define vessel behaviour baseline and missing AIS; protect sensitive data. |
| S07-OC-10 | Mangrove mapping | EO classification workflow | Partial | Define species/ecozone and tide/sensor; validate field plots. |
| S07-OC-11 | Coral mapping | Marine habitat classification | Open | Define benthic classes, depth/clarity and ground truth; spatially independent validation. |
| S07-OC-12 | Glacier analysis | Cryosphere workflow | Open | Split mass balance, velocity, outline and thickness; state sensor/time support. |
| S07-OC-13 | Sea-ice analysis | Cryosphere workflow | Open | Split concentration, motion, thickness and classification; validate with reference data. |

### Geoscience, mining and planetary — page 14

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S07-GS-01 | Seismic tomography | Geophysical inverse problem | Open | Define ray/wave formulation, regularisation and resolution; test synthetic recovery. |
| S07-GS-02 | Full waveform inversion | Geophysical inverse problem | Verify | Define objective, source, parameterisation and cycle skipping; document resolution. |
| S07-GS-03 | Seismic migration | Imaging algorithm family | Open | Split Kirchhoff/RTM/one-way methods; define velocity model and imaging condition. |
| S07-GS-04 | Gravity inversion | Geophysical inverse problem | Open | Define density parameterisation, kernel and regularisation; test non-uniqueness. |
| S07-GS-05 | Magnetic inversion | Geophysical inverse problem | Open | Define magnetisation and remanence; test ambiguity and regularisation. |
| S07-GS-06 | Euler deconvolution | Potential-field source estimation | Verify | Verify structural index and windowing; test synthetic sources. |
| S07-GS-07 | Reduction to the pole | Potential-field transform | Verify | Define magnetisation/field direction and low-latitude limits. |
| S07-GS-08 | Upward continuation | Potential-field transform | Partial | Verify Fourier/space-domain formulation and altitude; test harmonic fields. |
| S07-GS-09 | Downward continuation | Potential-field inverse transform | Open | Define regularisation and instability; test noise amplification. |
| S07-GS-10 | Electrical Resistivity Tomography (ERT) | Geophysical inversion | Open | Define electrode array, forward solver and regularisation; validate with synthetic models. |
| S07-GS-11 | Ground Penetrating Radar (GPR) processing | Geophysical workflow | Open | Split time-zero, dewow, gain, migration and velocity estimation; document units. |
| S07-GS-12 | Implicit geological modelling with RBF | Geological interpolation | Partial | Define contacts/orientations and geological constraints; test known synthetic structures. |
| S07-GS-13 | 3D geostatistics | Geostatistical model family | Open | Split covariance, simulation and estimation; define anisotropy/support. |
| S07-GS-14 | Stochastic reservoir modelling | Subsurface simulation | Open | Define facies/petrophysical uncertainty and conditioning; test spatial statistics. |
| S07-GS-15 | History matching | Reservoir inverse modelling | Open | Define dynamic simulator, objective and ensemble/adjoint method; test forecast uncertainty. |
| S07-GS-16 | Mining block models | Spatial data model/workflow | Not applicable | Define block support, attributes and estimation; document reporting standards. |
| S07-GS-17 | Grade-tonnage curves | Mining metric | Partial | Define cut-off, tonnage and grade; test cumulative monotonicity. |
| S07-GS-18 | Lerchs–Grossmann pit optimisation | Mine planning algorithm | Verify | Verify graph-theoretic maximum closure formulation and slope constraints. |
| S07-GS-19 | Pseudoflow pit optimisation | Mine planning algorithm | Verify | Verify maximum-flow/pseudoflow formulation and implementation; compare with LG. |
| S07-GS-20 | Mine scheduling | Operations research family | Open | Define precedence, capacity and blending; distinguish long/short-term planning. |
| S07-GS-21 | Mineral prospectivity mapping | Predictive mapping workflow | Open | Define deposits, evidence layers and spatial validation; quantify bias. |
| S07-GS-22 | U-statistic geochemical anomaly detection | Geochemical statistic | Verify | Identify exact U-statistic and reference; test background distributions. |
| S07-GS-23 | Concentration–area fractal analysis | Geochemical anomaly method | Verify | Verify log-log segmentation and threshold selection; test scale sensitivity. |
| S07-GS-24 | Crater detection and counting | Planetary mapping workflow | Open | Define crater morphology and size completeness; validate counts. |
| S07-GS-25 | Photoclinometry | Shape-from-shading method | Verify | Verify photometric assumptions and illumination; test shape recovery. |
| S07-GS-26 | Shape from shading | Computer vision method | Verify | Define reflectance/lighting assumptions and ambiguity; test synthetic surfaces. |
| S07-GS-27 | Planetary mineral mapping | Spectral classification workflow | Open | Define sensor/spectral library and mineral classes; validate ground truth/mission data. |
| S07-GS-28 | Landing-site hazard detection | Planetary terrain workflow | Open | Define slope/roughness/boulder hazards and sensor scale; document safety thresholds. |
| S07-GS-29 | Archaeological predictive modelling | Archaeological spatial model | Open | Define site evidence, survey bias and validation; avoid deterministic site claims. |
| S07-GS-30 | Site-catchment analysis | Archaeological accessibility workflow | Partial | Define cost surface, resources and travel assumptions; test sensitivity. |
| S07-GS-31 | Cumulative visibility | Visibility analysis | Partial | Cross-link viewshed; define observer/target weighting and DEM effects. |
| S07-GS-32 | Tobler hiking function | Travel-time model | Partial | Cross-link terrain movement; verify slope sign and units. |
| S07-GS-33 | Archaeological cost surfaces | Movement model | Open | Define terrain/cultural impedance and calibration; compare routes with field evidence. |

### Cross-disciplinary spatial methods — page 14

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S07-XD-01 | Spatial transcriptomics | Spatial omics workflow | Open | Define assay/platform, coordinate scale and spot/cell resolution; validate spatial effects. |
| S07-XD-02 | SpatialDE | Spatial gene-expression method/software | Verify | Verify exact model/version and null; document spatial covariance assumptions. |
| S07-XD-03 | Cell-neighbourhood analysis | Spatial omics method family | Open | Define cell segmentation, adjacency and composition; assess resolution sensitivity. |
| S07-XD-04 | Histopathology point patterns | Spatial pathology workflow | Open | Define cell types, marks and tissue window; account for segmentation error. |
| S07-XD-05 | Materials grain-boundary analysis | Materials image analysis | Open | Define grain segmentation and adjacency; validate orientation/size distributions. |
| S07-XD-06 | Astronomical two-point correlation | Spatial point statistic | Verify | Define angular/spatial estimator and random catalogue; test edge correction. |
| S07-XD-07 | Friends-of-friends clustering | Point cloud clustering | Verify | Define linking length and transitive grouping; test percolation/bridging. |
| S07-XD-08 | HEALPix cross-matching | Spherical catalogue query | Verify | Pin HEALPix order and coordinate convention; test polar/edge cases. |
| S07-XD-09 | Microscopy particle tracking | Image tracking workflow | Open | Define detection, linking and motion model; quantify identity switches. |
| S07-XD-10 | Microscopy Voronoi analysis | Spatial neighbourhood metric | Partial | Define point extraction and boundary clipping; test density and edge effects. |

## Completion gates

1. Verify all model/software names and versions; several are suites or broad families rather than single methods.
2. Preserve domain-specific units, physical assumptions, temporal support and calibration.
3. Use spatial/temporal/region-held-out validation, independent field observations and transparent baselines.
4. For ecology/health/social domains, document sampling bias, detection, privacy, consent and possible harms.
5. For hazard, mining, energy and engineering, document uncertainty and expert review; no decision-grade claim from a teaching baseline.
6. Check licences and provenance for datasets, model weights, software and third-party outputs independently.
7. Reconcile canonical lessons, implementations, tests, notebooks and catalogue after evidence changes.

**Current conclusion:** Section 7 is decomposed into auditable child records. It remains open; this register does not imply that the named specialist models, software suites or applied workflows have been independently verified.
