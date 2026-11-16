# Section 4 — Raster, terrain, hydrology, geomorphology

- **Original source section:** 4
- **Source pages:** 6–7
- **Source transcription:** [pages 6–10](../../source-inventory/pages-06-10.md)
- **Review state:** source entries extracted into this index; not every entry independently verified
- **Current canonical records:** [Focal raster statistics](../../algorithms/raster/focal-statistics.md); [Priority-Flood depression filling](../../algorithms/raster/priority-flood.md); [Euclidean distance transform](../../algorithms/raster/euclidean-distance-transform.md); [D8 flow direction](../../algorithms/raster/d8-flow-direction.md); [D8 flow accumulation](../../algorithms/raster/d8-flow-accumulation.md); [power-law MFD routing](../../algorithms/raster/mfd-flow-routing.md); [single-outlet watershed delineation](../../algorithms/raster/watershed-delineation.md); [Strahler and Shreve stream ordering](../../algorithms/raster/stream-order.md); [Horn slope and aspect](../../algorithms/raster/slope-aspect.md); [local hillshade](../../algorithms/raster/hillshade.md); [topographic wetness index](../../algorithms/raster/topographic-wetness-index.md); [topographic position index](../../algorithms/raster/topographic-position-index.md); [Riley terrain ruggedness index](../../algorithms/raster/terrain-ruggedness-index.md); [radial sky-view factor](../../algorithms/raster/sky-view-factor.md); [nearest/bilinear raster resampling](../../algorithms/raster/resampling.md); [zonal statistics](../../algorithms/raster/zonal-statistics.md); [connected-component labeling](../../algorithms/raster/connected-components.md); [raster least-cost distance](../../algorithms/raster/cost-distance.md) (first scoped and tested raster distance, flow-direction, accumulation, contributing-area and stream-network measures; remaining entries are still unverified)

The source groups raster operations, terrain analysis, hydrological modelling, geomorphology and coastal methods. The terrain package now also includes tested raster cut-and-fill depth and volume calculations for aligned existing/design surfaces, with rectangular cell areas and explicit NoData masking. A tested hypsometric curve and integral now add a normalized basin-elevation distribution summary with explicit valid-cell masking and a flat-relief rejection policy. The list includes algorithms, physical models, metrics, software packages, data formats and applied workflows. Preserve those differences during research.

## Raster operations

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Map algebra: local, focal, zonal and global operations; reclassification; resampling (nearest, bilinear, cubic, Lanczos) | Raster operations / resampling methods | 6 | Partially implemented: focal and zonal statistics, nearest/bilinear/cubic/Lanczos same-extent resampling plus a separately documented exact-overlap area-aggregation extension and explicit half-open range reclassification have tested baselines; global/neighbourhood map algebra and CRS-aware warping remain open; local arithmetic/reducers and categorical lookup now have tested reference implementations |
| Connected component labeling, flood fill, run-length encoding, image pyramids | Image and raster algorithms / data structures | 6 | Partially implemented: tested deterministic 4/8-connected 2D and 6/18/26-connected 3D component labeling with NoData/invalid-voxel barriers is available; run-length encoding and image-pyramid construction remain open |
| Distance: Euclidean distance transform (Felzenszwalb), chamfer, cost-distance, least-cost path, fast marching and Eikonal solvers, heat method | Distance transforms / path methods / numerical solvers | 6 | Partially implemented: exact regular-grid Euclidean distance transform, tested eight-neighbour chamfer graph distance and weighted-raster Dijkstra cost distance have tested baselines; continuous fast marching/Eikonal solvers and heat-method distance remain open |
| Efficient statistics: integral images for focal statistics, zonal histograms | Data structures / statistical summaries | 6 | Partially implemented: summed-area integral images support NoData-aware square-window focal means, and grouped zonal summaries are tested; zonal histograms and generalized integral-image statistics remain open |
| Vectorization and contouring: raster-to-vector, [marching squares](../../algorithms/raster/marching-squares.md), marching cubes | Conversion / contouring / surface extraction algorithms | 6 | Partial — a tested rectilinear-grid marching-squares segment extractor now covers isolines; segment stitching, filled polygonisation, marching cubes and general raster-to-vector conversion remain open |
| Compression: quadtree, JPEG2000, LERC, wavelet; formats such as COG, Zarr, GeoParquet | Compression methods / data formats / storage layouts | 6 | Not checked — intake only |

## Terrain analysis

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Slope, aspect, curvature (multiscale), hillshade, multi-directional shading, openness, sky-view factor, local relief models, red relief image maps | Terrain derivatives / visualisation methods / metrics | 6 | Partially implemented: Horn and Zevenbergen–Thorne slope/aspect, local profile/plan curvature, tested Gaussian multiscale curvature, analytical hillshade, four-azimuth multidirectional hillshade and radial-sampling sky-view factor have tested baselines; openness, local-relief and red-relief products remain open |
| Position and form: [topographic position index](../../algorithms/raster/topographic-position-index.md), [Riley terrain ruggedness index](../../algorithms/raster/terrain-ruggedness-index.md), geomorphons, landform classification, ridge and valley extraction, pit and peak detection | Terrain metrics / classification and feature extraction | 6 | Partially implemented: tested focal TPI with integral-image means and Riley eight-neighbour TRI with strict NoData handling are available in the terrain-indices package; geomorphons, landform classification, ridge/valley extraction and pit/peak detection remain open |
| Visibility: viewshed (R3, R2, XDraw), cumulative viewshed, isovist, intervisibility, radar coverage and shadow, Fresnel clearance | Visibility algorithms / propagation and clearance methods | 6 | Not checked — intake only |
| Solar and microclimate: solar radiation modeling, wind exposure, cold-air drainage, insolation indices | Environmental models / derived indices | 6 | Not checked — intake only |
| Volumes: [cut-and-fill](../../algorithms/raster/cut-fill-volume.md), reservoir volume from DEM, [hypsometric curves](../../algorithms/raster/hypsometric-curve.md) | Volume calculations / terrain summaries | 6 | Partially implemented: aligned-surface cut-and-fill volume and an empirical hypsometric curve/integral have tested baselines; reservoir-stage curves and uncertainty propagation remain open |
| DEM quality: void filling, error modeling, DEM fusion (SRTM, ASTER, TanDEM-X), bare-earth extraction, hydro-conditioning, stream burning | Data correction / fusion / terrain-processing workflows | 6 | Not checked — intake only |
| Terrain simplification and rendering: Lindstrom-Pascucci, quadric error metrics, ROAM, geometry clipmaps, CDLOD, TIN generalization | Simplification algorithms / rendering methods / metrics | 6 | Not checked — intake only |

## Hydrology

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Flow routing: [D8](../../algorithms/raster/d8-flow-direction.md), D-infinity, [power-law MFD](../../algorithms/raster/mfd-flow-routing.md), [priority-flood depression filling](../../algorithms/raster/priority-flood.md), sink breaching | Flow-direction algorithms / terrain conditioning | 6–7 | Partial — tested D8, D-infinity facet routing and power-law MFD baselines exist; sink breaching and source-entry review remain open |
| [Flow accumulation](../../algorithms/raster/d8-flow-accumulation.md), [watershed and basin delineation](../../algorithms/raster/watershed-delineation.md), [stream ordering](../../algorithms/raster/stream-order.md) (Strahler, Shreve), HAND, topographic wetness index | Hydrological operations / network metrics / terrain indices | 7 | Partially implemented: D8 accumulation, single-outlet watershed delineation, Strahler/Shreve ordering and HAND/TWI baselines are tested; multi-outlet basin hierarchies and additional hydrological indices remain open |
| Rainfall-runoff: SCS curve number, unit hydrograph, Green-Ampt, TOPMODEL, SWAT, HEC-HMS, LISFLOOD, VIC | Hydrological models / software systems | 7 | Not checked — intake only |
| Routing and hydrodynamics: Muskingum, Manning, Saint-Venant, kinematic wave, 2D shallow water equations, SPH | Flow-routing methods / physical equations / numerical methods | 7 | Not checked — intake only |
| Flood: frequency analysis (GEV, Gumbel, return periods), bathtub versus hydrodynamic inundation, SAR flood mapping | Statistical methods / inundation models / remote-sensing workflow | 7 | Not checked — intake only |
| Groundwater: MODFLOW, MODPATH, MT3D, DRASTIC, recharge estimation (water table fluctuation, chloride mass balance) | Groundwater models / assessment index / estimation methods | 7 | Not checked — intake only |
| Land surface models: Noah-MP, CLM, JULES; GRACE downscaling; snow and soil moisture assimilation | Land-surface models / downscaling / data assimilation | 7 | Not checked — intake only |

## Geomorphology and slope processes

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Chi analysis, slope-area analysis, knickpoint detection, drainage basin morphometry | Geomorphic analysis methods / morphometric measures | 7 | Not checked — intake only |
| Landslide susceptibility (frequency ratio, logistic regression), SHALSTAB, weights of evidence | Susceptibility models / statistical methods | 7 | Not checked — intake only |
| Glacier mass balance, snow models, avalanche runout | Cryosphere models / hazard modelling | 7 | Not checked — intake only |
| Erosion: USLE, RUSLE, hydraulic and thermal erosion simulation | Empirical models / physical simulation | 7 | Not checked — intake only |

## Coastal

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| DSAS (end-point rate, linear and weighted regression), waterline extraction, tide-coordinated shorelines | Shoreline change analysis / extraction workflows | 7 | Partial — EPR, OLS and inverse-variance WLR rate estimators implemented; shoreline extraction, transect generation and tide coordination remain unimplemented |
| Wave runup (Stockdon), longshore transport (CERC, Kamphuis), Bruun rule, Dean profile, coastal vulnerability index | Coastal process models / empirical rules / vulnerability index | 7 | Partial — Stockdon R2 and scoped CERC energy-flux estimate implemented; Kamphuis, Bruun, Dean profile and CVI remain unimplemented |
| Bathymetry: satellite-derived (ratio, physics-based, ICESat-2 calibrated), multibeam gridding, topo-bathymetric lidar refraction correction | Bathymetric retrieval / gridding / sensor correction | 7 | Not checked — intake only |

## First audited lesson

The [focal raster statistics lesson](../../algorithms/raster/focal-statistics.md) uses value and count integral images for a NoData-aware square-window mean, with truncated edge windows and an explicit minimum valid count. The [Euclidean distance transform lesson](../../algorithms/raster/euclidean-distance-transform.md) defines centre-to-centre distance on a regular grid, including non-square cell spacing; its package now implements the Felzenszwalb–Huttenlocher lower-envelope transform directly in O(HW), with brute-force reference tests. The [Priority-Flood lesson](../../algorithms/raster/priority-flood.md) fills depressions to their lowest spill elevation and returns a fill-depth surface, with explicit NoData-boundary assumptions. It does not breach depressions or resolve flats. The [D8 flow-direction lesson](../../algorithms/raster/d8-flow-direction.md) adds strict steepest-descent assignment with explicit direction codes, cell spacing and NoData rules. The fourteen pre-existing raster and terrain lessons have tested implementations and interactive notebooks; the additional power-law MFD lesson has its own tested implementation, tests and interactive notebook. Connected-component labeling uses a deterministic row-major breadth-first traversal and makes 4/8-connectivity and invalid-cell barriers explicit. Zonal statistics groups already-aligned raster cells by integer zone labels and distinguishes empty zones from absent zones. The resampling baseline compares nearest-neighbour and bilinear interpolation on same-extent grids, with strict and renormalized NoData policies; it is not a CRS-aware warp. TWI is calculated from supplied specific catchment area and slope; it is not treated as a direct soil-moisture measurement. The terrain package derives local analytical hillshade from slope/aspect and a declared sun position, and now includes a four-azimuth multidirectional composite to reduce single-light directional bias; neither method models cast shadows. The least-cost baseline uses multi-source Dijkstra on an explicit weighted raster graph; it is not a continuous fast-marching solver. Horn's 3×3 terrain-derivative lesson makes the horizontal spacing, vertical-unit conversion, downslope aspect convention and strict NoData policy explicit. The [power-law MFD routing lesson](../../algorithms/raster/mfd-flow-routing.md) now has tested flow-fraction and accumulation routines. It supports rectangular cells, masks and NoData, validates strictly downhill edges, and uses a topological traversal to conserve contributions at sinks. It is a bounded Freeman/Holmgren-family power-law baseline, not D-infinity or a full depression/flat-resolution workflow. The D8 accumulation routine processes an existing acyclic direction graph in topological order; the watershed routine traverses reverse flow links from a selected outlet. The accumulation, watershed and stream-order packages reject cycles. These are scoped baselines: Euclidean distance is not cost-distance, D8 does not fill depressions or resolve flats, and accumulation does not delineate watersheds.

## Decisions for the next pass

1. Separate raster algebra and data structures from terrain-specific algorithms.
2. Document grid resolution, cell alignment, NoData handling and resampling choices in raster examples.
3. State the assumptions behind flow direction, depression treatment, accumulation, watershed delineation and terrain derivatives.
4. Distinguish empirical indices from physical models and numerical solvers.
5. Use a small, known DEM or synthetic surface for teaching, then compare with a documented real dataset where licensing permits.
6. Keep Euclidean distance, raster cost distance and continuous Eikonal solvers conceptually distinct.

## Bibliographic checks on selected hydrology foundations

- O'Callaghan and Mark (1984), “The extraction of drainage networks from digital elevation data,” *Computer Vision, Graphics, and Image Processing*, 28(3), 323–344, [10.1016/S0734-189X(84)80011-0](https://doi.org/10.1016/S0734-189X(84)80011-0).
- Jenson and Domingue (1988), “Extracting topographic structure from digital elevation data for geographic information system analysis,” *Photogrammetric Engineering & Remote Sensing*, 54(11), 1593–1600, [USGS publication record](https://pubs.usgs.gov/publication/70142175).
- Strahler (1957), “Quantitative analysis of watershed geomorphology,” *Eos, Transactions American Geophysical Union*, 38(6), 913–920, [10.1029/TR038i006p00913](https://doi.org/10.1029/TR038i006p00913).
- Shreve (1966), “Statistical law of stream numbers,” *The Journal of Geology*, 74(1), 17–37, [10.1086/627137](https://doi.org/10.1086/627137).

These are selected bibliographic checks for the D8, watershed and stream-order lessons, not a complete audit of all raster/hydrology entries or all DEM-conditioning assumptions.


The terrain-index package now also includes a tested Gaussian local-relief model (DEM minus smoothed background, with normalized finite-cell convolution) and a multi-window TPI helper. These provide scale-explicit local terrain residuals and TPI rasters; geomorphons, openness, red-relief mapping and a landform classifier remain open.
