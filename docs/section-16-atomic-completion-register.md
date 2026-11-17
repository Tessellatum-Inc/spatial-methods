# Section 16 atomic completion register

**Source:** *Spatial Analysis Algorithms: Complete Compendium*, Section 16, pages 33–34.  
**Intake:** [preserved pages 31–35 transcription](../source-inventory/pages-31-35.md).  
**Section index:** [Section 16 catalogue record](../catalog/sections/16-flows-regions-deformation-marine.md).

> The source describes applied methods across several specialist fields. This register separates the named methods and products from broad research/application families. It does not establish that the source's shorthand names identify a single canonical method.

## Status policy

Apply the [source-entry verification protocol](../catalog/verification-protocol.md) and [completion standard](compendium-completion-standard.md). Distinguish mathematical methods, software/products, indicators, workflows and application domains. Existing code covers only the variants stated.

| Status | Meaning |
|---|---|
| Open | No item-specific independent verification/implementation evidence recorded. |
| Partial | A bounded related implementation exists; named variants or validation remain open. |
| Verify | Exact method, acronym, product or version must be resolved. |
| Not applicable | A field, product workflow or broad application is not a single algorithm. |

## Atomic source register

### Advanced spatial interaction — page 33

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S16-SI-01 | Wilson entropy-maximising interaction model | Spatial interaction model | Partial | Existing exponential-cost IPF baseline is bounded; verify entropy derivation, constraints and parameter interpretation. |
| S16-SI-02 | Production-constrained gravity model | Interaction model | Partial | Existing production-constrained form is implemented; verify origin constraints and balancing. |
| S16-SI-03 | Attraction-constrained gravity model | Interaction model | Partial | Existing attraction-constrained form is implemented; verify destination constraints. |
| S16-SI-04 | Doubly constrained gravity model | Interaction model | Partial | Existing IPF implementation is bounded; test convergence, structural zeros and infeasible margins. |
| S16-SI-05 | Poisson gravity regression | Count regression model | Partial | Existing PPML is a separate baseline; document link, fixed effects, exposure and robust inference. |
| S16-SI-06 | Negative-binomial gravity regression | Count regression model | Open | Specify dispersion parameterisation and estimation; test overdispersion and nested Poisson limit. |
| S16-SI-07 | Competing-destinations model | Spatial interaction model | Open | Identify exact destination competition formulation; test sensitivity to intervening opportunities and scale. |
| S16-SI-08 | Intervening-opportunities model | Spatial interaction model | Partial | Existing cumulative exponential Stouffer-style allocation is bounded; verify canonical variants and assumptions. |
| S16-SI-09 | Griffith eigenvector filtering for flows | Spatial dependence method | Verify | Identify exact flow-specific specification and eigenvector construction; test residual dependence. |
| S16-SI-10 | LeSage–Pace origin-destination models | Spatial econometric model family | Verify | Identify exact OD spatial interaction specification; document origin/destination dependence and inference. |
| S16-SI-11 | Flow-based community detection | Network clustering | Open | Define directed/weighted graph construction and resolution; compare Louvain/Leiden variants. |
| S16-SI-12 | Flow kernel density estimation | Flow density method | Open | Define kernel over origin-destination vectors/paths and bandwidth; test edge and directional effects. |
| S16-SI-13 | OD flow hotspot detection | Hotspot analysis | Open | Define local statistic, null and multiple testing; test synthetic clusters and exposure. |

### Functional regions and urban boundaries — page 33

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S16-FR-01 | Intramax regionalisation | Functional regionalisation | Verify | Verify algorithm/version, objective and stopping; compare against published examples. |
| S16-FR-02 | CURDS regionalisation | Functional regionalisation | Verify | Identify exact method and implementation; document flow thresholds and hierarchy. |
| S16-FR-03 | Louvain clustering on flow networks | Network community detection | Open | Define directed/weighted modularity and resolution; assess instability. |
| S16-FR-04 | Leiden clustering on flow networks | Network community detection | Open | Define objective and guarantees for directed/weighted graphs; compare with Louvain. |
| S16-FR-05 | Commuting-zone definition | Functional geography workflow | Open | Define commuting flows, thresholds, contiguity and minimum size; document jurisdiction-specific conventions. |
| S16-FR-06 | City clustering algorithm (CCA) | Urban boundary method | Verify | Resolve exact CCA source and parameters; distinguish competing algorithms with same acronym. |
| S16-FR-07 | DBSCAN on building density | Urban boundary clustering | Open | Define density representation, metric and eps/min-samples; test scale and building-data bias. |
| S16-FR-08 | Percolation-based urban clustering | Urban boundary method | Open | Define occupancy, adjacency and critical threshold; test sensitivity and finite-size effects. |
| S16-FR-09 | Natural cities via head/tail breaks | Urban delineation method | Verify | Verify exact natural-cities method and head/tail recursion; test distributional assumptions. |
| S16-FR-10 | Home-location inference from traces | Mobility inference | Open | Define dwell/stop clustering and temporal window; evaluate uncertainty, bias and privacy. |
| S16-FR-11 | Work-location inference from traces | Mobility inference | Open | Define weekday/time rules and competing locations; test against consented reference labels. |
| S16-FR-12 | Activity-space delineation | Mobility metric | Open | Define standard deviational ellipse/convex hull/network methods separately; document temporal support. |
| S16-FR-13 | Co-location pattern extraction | Spatial-temporal pattern mining | Open | Define co-presence and spatial/temporal thresholds; protect sensitive group inference. |
| S16-FR-14 | Contact pattern extraction | Contact-network inference | Open | Define contact evidence, duration and uncertainty; require privacy and epidemiological review. |

### Classification and aggregation — page 33

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S16-CL-01 | Head/tail breaks | Classification method | Partial | Existing implementation is tested; verify recursion and heavy-tail suitability. |
| S16-CL-02 | Maximum breaks | Classification method | Verify | Resolve exact meaning; do not assume it means Jenks/natural breaks. |
| S16-CL-03 | Geometric interval | Classification method | Partial | Existing implementation is tested; define positive-domain and ratio conventions. |
| S16-CL-04 | Standard-deviation classification | Classification method | Partial | Existing implementation is tested; document reference mean/std and outlier behaviour. |
| S16-CL-05 | Box-plot classification | Classification method | Partial | Existing implementation is tested; define quartile convention and fence handling. |
| S16-CL-06 | Pretty breaks | Classification method | Verify | Identify exact algorithm/library convention and version; do not substitute a generic rounded sequence. |
| S16-CL-07 | Dalenius–Hodges stratification | Sampling/classification method | Partial | Existing implementation is tested; verify cumulative square-root frequency boundaries and ties. |
| S16-CL-08 | Optimal one-dimensional k-means (ckmeans) | Exact classification optimisation | Partial | Existing dynamic program is tested against exhaustive partitions; document objective and tie-breaking. |
| S16-CL-09 | AMOEBA regionalisation | Spatial regionalisation | Verify | Identify exact AMOEBA method and objective; test spatial contiguity and scale. |
| S16-CL-10 | Automated zoning procedures | Zoning optimisation family | Open | Split methods by objective/constraints; define contiguity and aggregation criteria. |
| S16-CL-11 | Scale-effect analysis | MAUP/scale diagnostic | Open | Define scale perturbations and comparison statistics; avoid claiming a single correction. |
| S16-CL-12 | Variance by aggregation level | Spatial aggregation diagnostic | Open | Define target variable and zoning hierarchy; quantify within/between-zone variance. |

### Cost surfaces and movement through terrain — page 33

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S16-CS-01 | Tobler hiking function | Terrain travel-time model | Partial | Existing directional raster baseline is tested; verify original speed function, slope sign and units. |
| S16-CS-02 | Naismith rule | Terrain travel-time model | Partial | Existing baseline is tested; define ascent/descent and time convention variants. |
| S16-CS-03 | Langmuir rule | Terrain travel-time model | Partial | Existing per-edge model is bounded; verify exact piecewise ascent/descent rule and units. |
| S16-CS-04 | Anisotropic cost surface | Raster movement model | Partial | Existing directional edge-cost baseline is bounded; verify orientation and neighbourhood dependence. |
| S16-CS-05 | Vertical-factor path distance | Terrain path-distance model | Open | Define vertical factor and cumulative path semantics; test uphill/downhill asymmetry. |
| S16-CS-06 | Backlink rasters | Least-cost path output | Open | Define predecessor encoding, tie handling and path reconstruction; test no-path and multi-source cases. |
| S16-CS-07 | Least-cost corridors | Corridor analysis | Partial | Existing additive-tolerance raster corridor is bounded; distinguish from probabilistic corridors and uncertainty surfaces. |
| S16-CS-08 | Cost-weighted distance with turning penalties | Movement optimisation | Open | Define heading state and turn cost; test against expanded-state graph oracle. |
| S16-CS-09 | Walking energy expenditure | Biophysical movement model | Open | Identify model family and physiological inputs; validate across grade, speed and body mass. |
| S16-CS-10 | Loaded-travel energy expenditure | Biophysical movement model | Open | Define load, terrain and metabolic cost; validate independently from unloaded walking models. |

### SAR geometry, InSAR time series and crustal deformation — page 34

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S16-INS-01 | Radiometric terrain correction (RTC) | SAR preprocessing | Open | Identify calibration/DEM conventions and software; test radiometric terrain effects. |
| S16-INS-02 | SAR geocoding | SAR geometry processing | Open | Define orbit, DEM and range-Doppler geometry; validate against control points. |
| S16-INS-03 | SAR multilooking | SAR processing | Open | Define looks, resolution and speckle trade-off; test radiometric statistics. |
| S16-INS-04 | SAR radiometric calibration | SAR calibration | Open | Identify sigma0/beta0/gamma0 conventions and sensor metadata; compare reference targets. |
| S16-INS-05 | Enhanced spectral diversity (ESD) coregistration | Interferometric processing | Verify | Verify algorithm and burst-overlap phase assumptions; test residual azimuth misregistration. |
| S16-INS-06 | Atmospheric phase-screen estimation | InSAR correction | Open | Define atmospheric/turbulent model and temporal filtering; separate atmosphere from deformation. |
| S16-INS-07 | GACOS tropospheric correction | External correction product/workflow | Verify | Identify GACOS version, inputs and licence; document interpolation and correction conventions. |
| S16-INS-08 | ERA5-based tropospheric correction | Atmospheric correction workflow | Verify | Define ERA5 variables, vertical interpolation and delay model; validate against GNSS/independent products. |
| S16-INS-09 | Orbital ramp removal | InSAR phase correction | Open | Define ramp order and reference region; avoid removing long-wavelength deformation. |
| S16-INS-10 | DEM-error correction | InSAR phase correction | Open | Define perpendicular baseline and elevation-error relation; test synthetic phase contributions. |
| S16-INS-11 | SBAS time-series InSAR | Time-series inversion | Verify | Identify exact SBAS variant and network inversion; test synthetic deformation and temporal gaps. |
| S16-INS-12 | NSBAS | Time-series InSAR method | Verify | Verify acronym/formulation and regularisation; distinguish from generic SBAS. |
| S16-INS-13 | MintPy pipeline | InSAR software workflow | Verify | Identify version, supported products and processing assumptions; treat as software integration. |
| S16-INS-14 | LiCSBAS pipeline | InSAR software workflow | Verify | Identify version and input-product conventions; document corrections and quality controls. |
| S16-INS-15 | GNSS–InSAR 3D velocity decomposition | Geodetic fusion method | Open | Define look vectors, reference frame and regularisation; test synthetic 3D displacement recovery. |
| S16-INS-16 | Okada dislocation model | Elastic deformation model | Open | Verify source geometry, coordinate convention and half-space assumptions; test published reference cases. |
| S16-INS-17 | Mogi point-source model | Elastic deformation model | Partial | Existing analytical point-source baseline is tested; document source-depth and half-space limits. |
| S16-INS-18 | Finite-fault slip inversion | Geophysical inverse problem | Open | Define Green functions, regularisation and data covariance; test synthetic slip recovery. |
| S16-INS-19 | Elastic deformation models | Geophysical model family | Open | Split source geometries/material assumptions and define governing equations. |
| S16-INS-20 | Viscoelastic deformation models | Geophysical model family | Open | Define rheology, time dependence and boundary conditions; compare with analytical limits. |

### Marine and fisheries spatial analysis — page 34

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S16-MA-01 | CPUE standardisation with GAM | Fisheries statistical model | Open | Define catch/effort, covariates and estimand; assess zero inflation and sampling design. |
| S16-MA-02 | VAST-style spatiotemporal model | Fisheries statistical model/software | Verify | Identify exact VAST formulation/version; document latent spatial and temporal structure. |
| S16-MA-03 | Spatial stock assessment | Fisheries assessment family | Open | Define population dynamics, observation and movement models; require fisheries domain validation. |
| S16-MA-04 | Fishing-effort allocation | Spatial allocation model | Open | Define fleet, constraints and behavioural assumptions; protect confidential vessel data. |
| S16-MA-05 | Larval dispersal | Lagrangian transport model | Open | Define hydrodynamic forcing, larval behaviour and mortality; test mass conservation. |
| S16-MA-06 | Parcels particle tracking | Software framework | Verify | Identify version and particle kernels; document advection/interpolation and licence. |
| S16-MA-07 | OpenDrift particle tracking | Software framework | Verify | Identify version and process modules; document forcing and reproducibility. |
| S16-MA-08 | Ocean connectivity matrices | Connectivity metric | Open | Define source/sink, time horizon and normalisation; test particle conservation and uncertainty. |
| S16-MA-09 | Marine protected area network design | Conservation planning | Open | Define biodiversity/connectivity targets and costs; compare exact/heuristic plans. |
| S16-MA-10 | Marxan spatial planning | Planning software | Verify | Identify version, objective and licence; document input feature/cost conventions. |
| S16-MA-11 | Zonation prioritisation | Conservation software | Verify | Identify version and ranking method; document feature representation and uncertainty. |
| S16-MA-12 | Multibeam benthic habitat mapping | Marine classification workflow | Open | Define backscatter/bathymetry features and ground truth; spatially independent validation. |

### Biodiversity and conservation — page 34

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S16-BI-01 | Extent of occurrence (convex hull) | Range metric | Partial | Existing planar convex hull baseline is tested; document projection and outlier sensitivity. |
| S16-BI-02 | Extent of occurrence (alpha hull) | Range metric | Open | Define alpha-shape parameter and disconnected components; compare with convex hull. |
| S16-BI-03 | Area of occupancy | Range metric | Partial | Existing aligned-grid AOO baseline is tested; verify grid origin/resolution and occupancy criteria. |
| S16-BI-04 | Range fragmentation indices | Range metric | Open | Identify exact indices and ecological interpretation; test patch/edge sensitivity. |
| S16-BI-05 | Essential biodiversity variables | Indicator framework | Not applicable | Identify EBV class/standard and data requirements; do not represent framework as one algorithm. |
| S16-BI-06 | Protected-area gap analysis | Conservation assessment | Open | Define biodiversity features, protected-area coverage and representation targets. |
| S16-BI-07 | Key Biodiversity Area delineation | Conservation standard/workflow | Verify | Identify current KBA standard and thresholds; preserve expert review and evidence requirements. |
| S16-BI-08 | Species richness | Biodiversity metric | Partial | Existing cellwise richness from binary presence matrix is tested; document sampling/effort bias. |
| S16-BI-09 | Weighted endemism | Biodiversity metric | Partial | Existing inverse-range-size weighted endemism is tested; verify range denominator and grid support. |
| S16-BI-10 | Phylogenetic diversity | Biodiversity metric | Open | Define phylogeny, branch lengths and taxon sampling; test known tree examples. |
| S16-BI-11 | Green security games | Security/game-theoretic model | Open | Define attacker/defender strategies and uncertainty; test equilibrium and policy assumptions. |
| S16-BI-12 | Learned patrol planning | Patrol optimisation | Open | Define observation bias, effort and reward; evaluate on held-out patrol areas and seasons. |
| S16-BI-13 | Patrol-data risk maps | Risk mapping workflow | Open | Correct effort/detection bias; protect sensitive species and ranger locations. |

### Climate analogs, velocity, refugia and land degradation — page 34

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S16-CLM-01 | Mahalanobis climate analog distance | Climate similarity metric | Partial | Existing global-covariance analog ranking is bounded; document covariance estimation, regularisation and extrapolation. |
| S16-CLM-02 | Climate velocity | Climate change metric | Partial | Existing gradient-based vector baseline is tested; verify sign, units, anisotropy and flat-gradient handling. |
| S16-CLM-03 | Climate-change refugia | Ecological modelling workflow | Open | Define persistence/stability criteria, topography and biotic interactions; validate ecological outcomes. |
| S16-CLM-04 | Bioclimatic envelope shifts | Ecological niche modelling | Open | Define envelope method, climate scenario and transferability; assess extrapolation. |
| S16-CLM-05 | RESTREND | Land degradation method | Verify | Verify original residual-trend formulation and productivity baseline; document rainfall model. |
| S16-CLM-06 | NPP residual methods | Land degradation indicator family | Open | Define NPP baseline and climate covariates; distinguish residual trends from causal degradation. |
| S16-CLM-07 | Desertification indicators | Indicator family | Open | Split indicators by process and scale; define validation against independent evidence. |
| S16-CLM-08 | Soil salinity mapping | Remote-sensing/soil mapping workflow | Open | Define spectral/terrain/soil covariates and field samples; validate regionally. |

### Humanitarian, food security and conflict — page 34

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S16-HU-01 | Relief facility location | Facility location optimisation | Open | Define demand, service radius, capacity and equity objective; test network accessibility. |
| S16-HU-02 | Humanitarian logistics routing | Routing/operations research | Open | Define uncertain demand, disruptions, fleet and service constraints; test scenario robustness. |
| S16-HU-03 | Displacement-camp mapping | Remote-sensing workflow | Open | Define camp boundary/structure classes and dates; assess privacy and protection risks. |
| S16-HU-04 | Tent/temporary-structure counting | Object detection/estimation | Open | Define unit, resolution and counting protocol; quantify omission/commission and uncertainty. |
| S16-HU-05 | IPC-style food-security analysis | Food-security classification framework | Verify | Identify IPC version/protocol and evidence rules; distinguish framework from geospatial model. |
| S16-HU-06 | FEWS NET-style outlooks | Early-warning workflow | Verify | Identify current methodology and product version; distinguish official outlook from generic forecast. |
| S16-HU-07 | Livelihood-zone delineation | Regionalisation workflow | Open | Define livelihood indicators, expert process and boundaries; document temporal validity. |
| S16-HU-08 | Market integration | Spatial econometric analysis | Open | Define market pairs, price series and cointegration/threshold model; test structural breaks. |
| S16-HU-09 | Price transmission models | Econometric model family | Open | Specify asymmetric/linear/nonlinear transmission and spatial link; test identification. |
| S16-HU-10 | ACLED-style event analysis | Event data workflow | Verify | Identify dataset version, coding rules and licence; preserve event uncertainty and bias. |
| S16-HU-11 | Conflict diffusion models | Spatiotemporal event model | Open | Define contagion/diffusion mechanism and reporting process; validate out of sample. |
| S16-HU-12 | ViEWS-style conflict forecasting | Forecasting system | Verify | Identify exact system/version and target; distinguish platform from component models. |
| S16-HU-13 | Spatial event clustering | Event clustering | Open | Define point-process model, scale and null; test cluster stability. |
| S16-HU-14 | Conflict early-warning indicators | Indicator/forecasting family | Open | Define lead time, outcome and decision threshold; assess calibration and harms. |

## Completion gates

1. Verify every named algorithm, product, framework and standard against primary/official sources; record versions and claim-level citations.
2. Preserve CRS, temporal scale, units, observation process, sampling bias and uncertainty.
3. Separate spatial interaction, regionalisation, classification and cost-distance algorithms from their application workflows.
4. Use independent analytical/synthetic oracles and spatially/temporally blocked validation; do not use random splits where they leak dependence.
5. For deformation, fisheries, biodiversity, humanitarian and conflict data, document specialist review, privacy and potential harm.
6. Review licences and reuse rights for all datasets, software, imagery, models and derived outputs.
7. Reconcile canonical lessons, implementations, verification records, coverage matrix and dashboard after evidence changes.

**Current conclusion:** Section 16 is decomposed into atomic review items. It remains open; this register is not a claim of independent verification or full application readiness.
