# Section 4 atomic completion register

**Source:** *Spatial Analysis Algorithms: Complete Compendium*, Section 4, pages 6–7.  
**Intake:** [preserved pages 6–10 transcription](../source-inventory/pages-06-10.md).  
**Section index:** [Section 4 catalogue record](../catalog/sections/04-raster-terrain-hydrology.md).

This register atomises the source groupings. Use the [verification protocol](../catalog/verification-protocol.md) and [completion standard](compendium-completion-standard.md). A model or software product is not automatically an algorithm; a bounded implementation is not evidence for every variant.

| Status | Meaning |
|---|---|
| Open | No item-specific independent evidence recorded. |
| Partial | A bounded related implementation exists; variants or validation remain open. |
| Verify | Exact algorithm, model or product must be resolved. |
| Not applicable | A data format, model suite or workflow needs a different record type. |

## Atomic source register

### Raster operations — page 6

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S04-RA-01 | Local map algebra | Raster operation | Partial | Define cell alignment, NoData and units; test arithmetic and masks. |
| S04-RA-02 | Focal map algebra | Raster operation | Partial | Define kernel, boundary and NoData policy; test focal statistics. |
| S04-RA-03 | Zonal map algebra | Raster operation | Partial | Define zone raster/vector semantics and overlap; test partial cells. |
| S04-RA-04 | Global map algebra | Raster operation | Partial | Define global reduction and masks; test chunked equivalence. |
| S04-RA-05 | Raster reclassification | Raster operation | Partial | Define interval inclusivity, nodata and type conversion; test boundary values. |
| S04-RA-06 | Nearest-neighbour resampling | Resampling algorithm | Partial | Define grid transform and tie convention; test categorical preservation. |
| S04-RA-07 | Bilinear resampling | Resampling algorithm | Partial | Define pixel-centre convention and nodata weighting; test affine surfaces. |
| S04-RA-08 | Cubic resampling | Resampling algorithm | Verify | Identify cubic convolution kernel/version and overshoot behaviour. |
| S04-RA-09 | Lanczos resampling | Resampling algorithm | Verify | Define windowed-sinc kernel and support; test ringing and nodata edges. |
| S04-RA-10 | Connected-component labelling | Raster topology algorithm | Partial | Define 4/8 connectivity and label equivalence; test tiled boundary reconciliation. |
| S04-RA-11 | Flood fill | Raster traversal algorithm | Partial | Define connectivity and predicate; test diagonal connectivity and boundaries. |
| S04-RA-12 | Run-length encoding | Compression/data structure | Partial | Define scan order and row boundaries; test lossless round-trip. |
| S04-RA-13 | Image pyramids | Multiresolution data structure | Partial | Define reduction/resampling and tile overlap; test scale consistency. |
| S04-RA-14 | Felzenszwalb Euclidean distance transform | Distance transform algorithm | Verify | Verify exact algorithm/variant and feature transform; compare with brute-force distance. |
| S04-RA-15 | Chamfer distance transform | Approximate distance transform | Partial | Define mask weights and approximation error; test directional bias. |
| S04-RA-16 | Cost-distance | Raster accumulation algorithm | Partial | Define edge connectivity and directional cost; compare with graph shortest path. |
| S04-RA-17 | Least-cost path | Raster path optimisation | Partial | Define predecessor/tie rules and path geometry; compare with graph oracle. |
| S04-RA-18 | Fast marching method | Eikonal solver | Verify | Verify upwind discretisation and causality; test analytic travel-time fields. |
| S04-RA-19 | Eikonal solvers | PDE solver family | Open | Split fast marching, fast sweeping and ordered-upwind methods; define anisotropy. |
| S04-RA-20 | Integral images | Summed-area data structure | Partial | Verify inclusive/exclusive indexing and numeric overflow; test arbitrary window sums. |
| S04-RA-21 | Focal statistics via integral images | Raster optimisation | Partial | Test sum/count/mean and variance with NoData and edge policies. |
| S04-RA-22 | Zonal histograms | Raster summary method | Partial | Define bins, exactness and zone overlap; test tiled aggregation. |
| S04-RA-23 | Raster-to-vector conversion | Vectorisation workflow | Partial | Define connectivity, polygonisation and NoData; test topology and raster round-trip. |
| S04-RA-24 | Marching squares | Contour extraction algorithm | Partial | Define saddle disambiguation and interpolation; test ambiguous cells. |
| S04-RA-25 | Marching cubes | Isosurface extraction algorithm | Partial | Verify case table and ambiguity resolution; test manifoldness. |
| S04-RA-26 | Quadtree compression | Hierarchical compression | Partial | Define split/termination and error tolerance; test reconstruction. |
| S04-RA-27 | JPEG2000 | Image compression standard | Verify | Pin standard/profile and codec version; test lossless/lossy and geospatial metadata. |
| S04-RA-28 | LERC | Raster compression codec | Verify | Verify codec version and error bound semantics; test nodata and multiband. |
| S04-RA-29 | Wavelet compression | Compression method family | Open | Specify wavelet, quantisation and lossless/lossy mode; test distortion. |
| S04-RA-30 | Cloud Optimized GeoTIFF (COG) | Raster file layout/standard | Verify | Verify OGC/GeoTIFF specification and overview/layout requirements; test range access. |
| S04-RA-31 | Zarr | Chunked array format | Verify | Pin format version and codecs; test metadata/coordinate interoperability. |
| S04-RA-32 | GeoParquet | Geospatial columnar format | Verify | Verify current specification and geometry encoding; test CRS and bbox metadata. |

### Terrain analysis — pages 6–7

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S04-TE-01 | Slope | Terrain derivative | Partial | Define gradient operator, units and CRS; test planes and grid anisotropy. |
| S04-TE-02 | Aspect | Terrain derivative | Partial | Define azimuth convention and flat-cell handling; test known planar slopes. |
| S04-TE-03 | Multiscale curvature | Terrain derivative family | Partial | Implements Gaussian scale-space profile and plan curvature: separable Gaussian smoothing at requested map-unit scales, reflective padding, rectangular cell spacing, explicit finite-DEM contract and the existing 3×3 curvature operator. Tests cover planar invariance across scales, suppression of short-wavelength noise, spacing/border behaviour and invalid scales/inputs. Tangential/mean/Gaussian curvature variants, geographic-grid correction, alternative boundary conditions and exact source-variant verification remain open: [implementation](../implementations/python/terrain-derivatives/README.md). |
| S04-TE-04 | Hillshade | Terrain visualisation | Partial | Define illumination azimuth/altitude and z-factor; test analytical plane. |
| S04-TE-05 | Multidirectional hillshade | Terrain visualisation | Verify | Verify light directions and combination rule; distinguish visual enhancement from physical illumination. |
| S04-TE-06 | Openness | Terrain metric | Verify | Verify positive/negative openness and search radius; test synthetic landforms. |
| S04-TE-07 | Sky-view factor | Terrain/radiation metric | Partial | Define angular integration and horizon sampling; test flat and canyon surfaces. |
| S04-TE-08 | Local relief model | Terrain filter/metric | Verify | Verify detrending kernel and scale; test broad/narrow landforms. |
| S04-TE-09 | Red relief image map | Terrain visualisation | Verify | Verify exact formulation and parameterisation; document interpretive limits. |
| S04-TE-10 | Topographic Position Index (TPI) | Terrain classification metric | Partial | Define neighbourhood/scale and standardisation; test ridges/valleys/flat terrain. |
| S04-TE-11 | Terrain ruggedness index | Terrain metric | Partial | Verify Riley and alternative formulations; test grid resolution dependence. |
| S04-TE-12 | Geomorphons | Landform classification | Verify | Verify ternary pattern and lookup table; test scale and flatness threshold. |
| S04-TE-13 | Landform classification | Classification workflow | Open | Define class scheme and thresholds; separate TPI, geomorphons and other methods. |
| S04-TE-14 | Ridge extraction | Terrain feature extraction | Open | Define ridge criteria and scale; test noisy surfaces and branching. |
| S04-TE-15 | Valley extraction | Terrain feature extraction | Open | Define valley network and scale; test flat/closed depressions. |
| S04-TE-16 | Pit detection | Terrain feature extraction | Partial | Define local minima and hydrological versus geomorphic pits; test plateaus. |
| S04-TE-17 | Peak detection | Terrain feature extraction | Partial | Define prominence and neighbourhood; test nested peaks and noise. |
| S04-TE-18 | R3 viewshed | Viewshed algorithm | Verify | Identify exact R3 method/version and curvature/refraction treatment; test reference surfaces. |
| S04-TE-19 | R2 viewshed | Viewshed algorithm | Verify | Identify exact R2 method/version; compare with brute ray tracing. |
| S04-TE-20 | XDraw viewshed | Viewshed algorithm | Verify | Resolve exact algorithm name and source; document acceleration/approximation. |
| S04-TE-21 | Cumulative viewshed | Visibility aggregation | Partial | Define observer weighting and count/probability; test tiled aggregation. |
| S04-TE-22 | Isovist | Visibility geometry | Partial | Define viewpoint and polygon construction; test occlusion and boundary cases. |
| S04-TE-23 | Intervisibility | Line-of-sight query | Partial | Define endpoints, curvature/refraction and obstruction; test exact ray profiles. |
| S04-TE-24 | Radar coverage and shadow | Visibility/radar modelling | Open | Define antenna pattern, terrain and propagation assumptions; distinguish geometric shadow from RF coverage. |
| S04-TE-25 | Fresnel clearance | Radio link geometry | Partial | Define frequency, path profile and clearance fraction; test units and ellipsoid assumptions. |
| S04-TE-26 | Solar radiation modelling | Terrain radiation workflow | Partial | Define direct/diffuse components, atmosphere and time integration; validate against pyranometers. |
| S04-TE-27 | Wind exposure | Terrain climatology metric | Open | Identify exact exposure metric and wind direction; validate with observations/CFD. |
| S04-TE-28 | Cold-air drainage | Microclimate model family | Open | Define terrain flow, stability and meteorology; validate under inversion conditions. |
| S04-TE-29 | Insolation indices | Terrain solar metric family | Open | Split potential/actual insolation and topographic indices; document atmospheric assumptions. |
| S04-TE-30 | Cut-and-fill volume | Terrain volume calculation | Partial | Define reference surface, cell area and sign; test analytic solids and nodata. |
| S04-TE-31 | Reservoir volume from DEM | Hypsometric storage estimation | Partial | Define water level, basin boundary and vertical datum; validate with bathymetry. |
| S04-TE-32 | Hypsometric curves | Terrain summary metric | Partial | Define area-elevation normalisation and bins; test known surfaces. |
| S04-TE-33 | DEM void filling | Elevation repair workflow | Partial | Split interpolation/patch and hydrological methods; preserve provenance and uncertainty. |
| S04-TE-34 | DEM error modelling | Uncertainty model | Open | Define sensor/terrain error and spatial covariance; test against control points. |
| S04-TE-35 | DEM fusion (SRTM, ASTER, TanDEM-X) | Multi-source fusion workflow | Verify | Identify product versions/licences and fusion method; validate vertical bias and resolution. |
| S04-TE-36 | Bare-earth extraction | Terrain filtering workflow | Partial | Split point-cloud filtering methods and ground class; test vegetation/building edges. |
| S04-TE-37 | Hydro-conditioning | DEM preprocessing workflow | Partial | Split fill/breach/carve and stream enforcement; quantify terrain alteration. |
| S04-TE-38 | Stream burning | Hydro-conditioning operation | Partial | Define burn depth and network source; test drainage consistency and artefacts. |
| S04-TE-39 | Lindstrom–Pascucci terrain simplification | Terrain LOD algorithm | Verify | Verify exact method and error metric; test topology and silhouette. |
| S04-TE-40 | Quadric error metrics | Mesh simplification algorithm | Verify | Verify quadric accumulation and boundary constraints; test geometric error. |
| S04-TE-41 | ROAM | Terrain LOD algorithm | Verify | Verify diamond-tree refinement/coarsening and screen-space criteria. |
| S04-TE-42 | Geometry clipmaps | Terrain rendering architecture | Verify | Verify nested regular-grid representation and update; document GPU constraints. |
| S04-TE-43 | CDLOD | Continuous distance-dependent LOD | Verify | Verify quadtree selection and morphing; test popping and geometric error. |
| S04-TE-44 | TIN generalisation | Terrain simplification | Open | Define vertex/edge removal and breakline preservation; test elevation error. |

### Hydrology — page 6–7

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S04-HY-01 | D8 flow routing | Flow direction algorithm | Partial | Define tie-breaking and flats; test convergent/divergent synthetic terrain. |
| S04-HY-02 | D-infinity flow routing | Flow direction algorithm | Partial | Verify facet partition and proportional flow; test planar surfaces. |
| S04-HY-03 | Multiple Flow Direction (MFD) | Flow direction algorithm | Partial | Define exponent/partition and flats; test mass conservation. |
| S04-HY-04 | Priority-Flood depression filling | Depression treatment algorithm | Partial | Verify priority queue and epsilon variants; test nested depressions and flats. |
| S04-HY-05 | Sink breaching | Depression treatment algorithm | Partial | Define breach path/cost and constraints; test terrain alteration and drainage. |
| S04-HY-06 | Flow accumulation | Hydrological accumulation algorithm | Partial | Define weighted/unweighted and routing graph; test mass conservation. |
| S04-HY-07 | Watershed delineation | Basin algorithm | Partial | Define pour point snapping and flow direction; test nested basins. |
| S04-HY-08 | Basin delineation | Hydrological partition workflow | Partial | Define outlet hierarchy and connectivity; compare with graph reachability. |
| S04-HY-09 | Strahler stream order | Network metric | Partial | Verify order rules and headwater handling; test branching trees. |
| S04-HY-10 | Shreve stream magnitude | Network metric | Partial | Verify additive magnitude and network direction; test branching trees. |
| S04-HY-11 | Height Above Nearest Drainage (HAND) | Terrain hydrology metric | Verify | Verify drainage association and vertical datum; test disconnected/flat terrain. |
| S04-HY-12 | Topographic Wetness Index (TWI) | Terrain hydrology metric | Partial | Define contributing area and slope floor; test grid resolution and units. |
| S04-HY-13 | SCS Curve Number method | Rainfall-runoff model | Verify | Verify CN tables, antecedent moisture and initial abstraction; test runoff examples. |
| S04-HY-14 | Unit hydrograph | Rainfall-runoff model | Partial | Define effective rainfall and convolution; test volume conservation. |
| S04-HY-15 | Green–Ampt infiltration | Infiltration model | Verify | Verify wetting-front equation and parameter units; test ponding time. |
| S04-HY-16 | TOPMODEL | Distributed/conceptual hydrology model | Verify | Verify topographic index and saturation deficit; test mass balance. |
| S04-HY-17 | SWAT | Hydrological model software | Verify | Pin SWAT version and modules; document inputs, calibration and licence. |
| S04-HY-18 | HEC-HMS | Hydrological modelling software | Verify | Pin release and component methods; document reproducibility and licensing. |
| S04-HY-19 | LISFLOOD | Hydrological model software | Verify | Identify model version and configuration; document data and process modules. |
| S04-HY-20 | VIC | Variable Infiltration Capacity model | Verify | Identify VIC version and routing/cold-land modules; document parameterisation. |
| S04-HY-21 | Muskingum routing | Channel routing method | Partial | Define K/X and time step stability; test hydrograph translation/storage. |
| S04-HY-22 | Manning equation | Open-channel flow relation | Partial | Define hydraulic radius, slope and roughness; check units and regime assumptions. |
| S04-HY-23 | Saint-Venant equations | Shallow-water governing equations | Not applicable | Define 1D equations and closure; link numerical solvers separately. |
| S04-HY-24 | Kinematic wave model | Hydrodynamic approximation | Verify | Verify assumptions and numerical scheme; compare with full shallow-water solution. |
| S04-HY-25 | 2D shallow-water equations | Hydrodynamic governing equations | Not applicable | Define conservation form and closures; document numerical solver and boundary conditions. |
| S04-HY-26 | Smoothed Particle Hydrodynamics (SPH) | Mesh-free numerical method | Verify | Verify kernel, boundary and stability; test conservation and convergence. |
| S04-HY-27 | GEV flood-frequency analysis | Extreme-value model | Partial | Define block maxima, covariates and return period; test uncertainty/extrapolation. |
| S04-HY-28 | Gumbel flood-frequency analysis | Extreme-value model | Partial | Define parameterisation and fit; compare with GEV. |
| S04-HY-29 | Return-period estimation | Risk metric | Partial | Define exceedance probability, stationarity and exposure period; clarify non-periodic meaning. |
| S04-HY-30 | Bathtub inundation mapping | Static flood screening | Partial | Define water level and connectivity; state lack of hydrodynamics. |
| S04-HY-31 | Hydrodynamic inundation modelling | Flood simulation workflow | Open | Define terrain, roughness, boundary conditions and solver; validate hydrographs/extents. |
| S04-HY-32 | SAR flood mapping | EO classification workflow | Partial | Define sensor, threshold/classifier and permanent water masking; validate independent events. |
| S04-HY-33 | MODFLOW | Groundwater flow model software | Verify | Pin MODFLOW family/version and packages; document discretisation and calibration. |
| S04-HY-34 | MODPATH | Groundwater particle tracking software | Verify | Identify MODPATH version and MODFLOW compatibility; test path/time semantics. |
| S04-HY-35 | MT3D | Groundwater transport model software | Verify | Identify MT3D/MT3D-USGS version and reaction modules; document coupling. |
| S04-HY-36 | DRASTIC | Groundwater vulnerability index | Verify | Verify parameter ratings/weights and calibration; document non-probabilistic interpretation. |
| S04-HY-37 | Water-table fluctuation recharge estimation | Recharge estimation method | Verify | Verify assumptions, specific yield and temporal scale; test uncertainty. |
| S04-HY-38 | Chloride mass-balance recharge estimation | Recharge estimation method | Verify | Verify chloride sources/steady-state assumptions; test sensitivity. |
| S04-HY-39 | Noah-MP | Land surface model | Verify | Pin model version/options; document energy/water balance and forcing. |
| S04-HY-40 | CLM | Community Land Model | Verify | Identify CLM version and configuration; document parameterisation and licence. |
| S04-HY-41 | JULES | Land surface model | Verify | Identify version and process options; document forcing and evaluation. |
| S04-HY-42 | GRACE downscaling | Satellite gravimetry workflow | Open | Define target variable, ancillary predictors and conservation; validate at independent scale. |
| S04-HY-43 | Snow assimilation | Data assimilation workflow | Open | Define observation operator and snow state; test mass/energy consistency. |
| S04-HY-44 | Soil moisture assimilation | Data assimilation workflow | Open | Define sensor/product, observation operator and bias correction; test uncertainty. |

### Geomorphology and slope processes — page 7

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S04-GM-01 | Chi analysis | River profile analysis | Verify | Verify χ transform, reference concavity and drainage area; test knickpoint sensitivity. |
| S04-GM-02 | Slope-area analysis | Geomorphic relationship | Partial | Define channel extraction and regression domain; test concavity and thresholds. |
| S04-GM-03 | Knickpoint detection | Geomorphic feature detection | Open | Split slope-break/statistical methods; test DEM noise and channel smoothing. |
| S04-GM-04 | Drainage basin morphometry | Morphometric metric family | Open | Split area, shape, relief and network metrics; define units and scale. |
| S04-GM-05 | Frequency-ratio landslide susceptibility | Susceptibility model | Partial | Define class bins and inventory sampling; spatially independent validation. |
| S04-GM-06 | Logistic-regression landslide susceptibility | Statistical susceptibility model | Partial | Define predictors, class imbalance and spatial CV; calibrate probabilities. |
| S04-GM-07 | SHALSTAB | Physically based slope stability model | Verify | Verify infinite-slope and hydrological assumptions; test parameter sensitivity. |
| S04-GM-08 | Weights-of-evidence landslide model | Bayesian evidence model | Verify | Verify conditional independence assumptions and contrast; test spatial transfer. |
| S04-GM-09 | Glacier mass balance | Cryosphere metric/workflow | Open | Define geodetic/glaciological methods and temporal support; quantify uncertainty. |
| S04-GM-10 | Snow models | Cryosphere model family | Open | Split energy-balance, degree-day and snowpack models; define forcing and validation. |
| S04-GM-11 | Avalanche runout | Hazard modelling family | Open | Split empirical/continuum models; define release volume, friction and terrain. |
| S04-GM-12 | USLE | Soil erosion model | Verify | Verify factor definitions and intended annual sheet/rill erosion scope. |
| S04-GM-13 | RUSLE | Revised soil erosion model | Verify | Verify RUSLE version and factor updates; distinguish from USLE. |
| S04-GM-14 | Hydraulic erosion simulation | Process model family | Open | Define flow shear, sediment transport and detachment/deposition; test mass balance. |
| S04-GM-15 | Thermal erosion simulation | Permafrost/coastal process model | Open | Define thermal forcing, ground ice and geometry; validate retreat rates. |

### Coastal — page 7

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S04-CO-01 | DSAS end-point rate | Shoreline change metric | Verify | Pin DSAS version and endpoint conventions; test transect generation and uncertainty. |
| S04-CO-02 | DSAS linear regression rate | Shoreline change metric | Verify | Verify regression method and minimum observations; test temporal sampling. |
| S04-CO-03 | DSAS weighted linear regression | Shoreline change metric | Verify | Verify weighting and uncertainty; compare with unweighted regression. |
| S04-CO-04 | Waterline extraction | EO shoreline workflow | Open | Define sensor/tide correction and classification; validate against reference shorelines. |
| S04-CO-05 | Tide-coordinated shorelines | Shoreline normalisation workflow | Open | Define tidal datum and runup correction; quantify vertical/horizontal uncertainty. |
| S04-CO-06 | Stockdon wave runup model | Coastal process model | Verify | Verify empirical equation and beach/swell assumptions; test units and domain. |
| S04-CO-07 | CERC longshore transport | Sediment transport model | Verify | Verify CERC coefficient and wave inputs; document calibration and limitations. |
| S04-CO-08 | Kamphuis longshore transport | Sediment transport model | Verify | Verify formulation and beach parameters; compare with CERC. |
| S04-CO-09 | Bruun rule | Shoreline response model | Verify | Verify assumptions and applicability debate; avoid unqualified sea-level prediction. |
| S04-CO-10 | Dean equilibrium beach profile | Coastal profile model | Verify | Verify profile exponent and sediment assumptions; test observed profiles. |
| S04-CO-11 | Coastal Vulnerability Index (CVI) | Composite index | Verify | Identify CVI formulation and weights; report ordinal limitations and sensitivity. |
| S04-CO-12 | Ratio-based satellite bathymetry | Bathymetric retrieval | Partial | Define bands, log ratio and calibration; validate by depth and water clarity. |
| S04-CO-13 | Physics-based satellite bathymetry | Bathymetric retrieval | Open | Define radiative transfer model and inversion; test bottom type/turbidity. |
| S04-CO-14 | ICESat-2-calibrated bathymetry | Bathymetric retrieval workflow | Verify | Verify photon classification and calibration; document coverage/uncertainty. |
| S04-CO-15 | Multibeam bathymetry gridding | Survey processing workflow | Partial | Define sound-speed/tide corrections and gridding; test uncertainty and resolution. |
| S04-CO-16 | Topo-bathymetric LiDAR refraction correction | Sensor correction method | Verify | Verify refraction geometry and water surface assumptions; test depth-dependent bias. |

## Completion gates

1. State grid geometry, CRS, units, cell registration, NoData and resampling semantics for every raster method.
2. Compare raster algorithms against exact graph/analytic oracles where possible; test tiling seams, nodata, flats and edge conditions.
3. For terrain metrics, report scale, neighbourhood, derivative operator and resolution sensitivity.
4. For hydrology, test flow conservation, routing direction, mass balance, boundary conditions and calibration; distinguish screening indices from process models.
5. For coastal and cryosphere methods, record sensor/product versions, physical assumptions, vertical datums and independent validation.
6. Review licences and provenance for model software, DEMs, EO products and derived datasets.
7. Reconcile canonical lessons, implementation contracts, independent tests, notebooks and coverage records after evidence is recorded.

**Current conclusion:** Section 4 is atomised into auditable child records. It remains open; this register is not proof of independent verification or operational hydrological/coastal validation.


## Implementation reconciliation — multiscale terrain curvature

The Partial status for S04-TE-03 is supported by a tested Gaussian scale-space implementation of profile and plan curvature. The implementation does not claim the broader set of curvature invariants or landform-classification methods sometimes grouped under multiscale terrain analysis.
