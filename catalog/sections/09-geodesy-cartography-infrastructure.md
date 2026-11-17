# Section 9 — Geodesy, cartography, data infrastructure, privacy, text and semantics

- **Original source section:** 9
- **Source pages:** 18–20
- **Source transcription:** [pages 16–20](../../source-inventory/pages-16-20.md)
- **Review state:** source entries extracted into this index; not every entry independently verified
- **Current canonical records:** [Coordinate transformation and CRS axis order](../../algorithms/geodesy/crs-transformation.md), [Geodetic, ECEF and local ENU coordinates](../../algorithms/geodesy/ecef-enu.md), [Helmert seven-parameter transformation](../../methods/helmert-7-parameter.md), [String similarity and probabilistic record linkage](../../algorithms/statistics/string-linkage.md), [Numeric map classification](../../algorithms/statistics/map-classification.md), and [Broad-phase collision detection](../../algorithms/statistics/collision-broadphase.md)

This section contains the supporting systems and concepts that make spatial work possible: coordinate reference systems, georeferencing, geocoding, map design, data infrastructure, quality assurance, privacy and geographic language. It also includes graph, topology and causal-analysis methods. These should become connected topic families rather than one oversized “GIS tools” lesson.

## First implemented learning record\n\nThe [Geodesy foundations learning path](../../learning-paths/geodesy-foundations.md) begins with point-coordinate transformation and explicit axis order. It does not claim to cover advanced datum, vertical or dynamic reference-frame transformations.\n\n## Geodesy and coordinate systems

The geodetic/ECEF/ENU lesson now covers ellipsoidal geodetic-to-ECEF conversion, the ECEF-to-local tangent-frame rotation and its inverse, with an EPSG:9836 reference test, intern walkthrough and visual lab. It does not perform vertical datum or geoid conversion. The first additional geocentric datum-operation lesson covers the seven-parameter Helmert Position Vector convention, parameter units, the rotation-sign trap and its relationship to a complete geographic/geocentric/geographic CRS operation. See the [method lesson](../../methods/helmert-7-parameter.md) and [tested implementation](../../implementations/python/helmert-7-parameter/README.md).

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Projections: Transverse Mercator (Gauss-Krüger), UTM, Lambert conformal, Web Mercator, Tobler hyperelliptical, adaptive composite projections | Map projections / projection families | 18 | Not checked — intake only |
| Datum transformations: [CRS transformations](../../algorithms/geodesy/crs-transformation.md), [Helmert](../../methods/helmert-7-parameter.md), Molodensky, Bursa-Wolf 7-parameter, NTv2 grids; [ECEF, ENU and geodetic conversions](../../algorithms/geodesy/ecef-enu.md); antimeridian and pole handling | Coordinate transformations / reference-frame conversions / edge-case handling | 18 | Partial — related record exists; source-entry review pending |
| Geoid and gravity: EGM2008 evaluation, Stokes integral, spherical harmonic analysis, gravity anomaly and terrain correction, IGRF and WMM magnetic models | Geoid and gravity models / geophysical calculations | 18 | Not checked — intake only |
| Spherical geometry: [spherical polygon area](../../algorithms/geodesy/spherical-polygon-area.md), spherical Voronoi and Delaunay, spherical wavelets, icosahedral and cubed-sphere grids | Spherical geometry / spatial structures / grid systems | 18 | [Spherical polygon area](../../implementations/python/spherical-polygon-area/README.md) has a tested unit-vector spherical-excess implementation with optional holes | Partial — spherical polygon area is implemented for unambiguous smaller-than-hemisphere rings; spherical Voronoi/Delaunay, wavelets and icosahedral/cubed-sphere grids remain open |
| Space geodesy: SLR, DORIS, VLBI, GNSS time series, velocity fields, strain rate, TEC maps, tropospheric delay (Saastamoinen, VMF), precise orbit determination, GRACE gravity recovery, altimetry crossover adjustment | Space-geodetic techniques / estimation and correction methods | 18 | Not checked — intake only |
| Satellite orbits: SGP4/SDP4, TLE processing, ground tracks and swaths, revisit analysis, sun-synchronous design, Walker constellations, conjunction analysis | Orbit propagation / mission and constellation analysis | 18 | Not checked — intake only |
| Astronomical: solar position, sunrise and sunset, tidal prediction, least-squares network adjustment | Astronomical calculations / prediction / adjustment | 18 | Not checked — intake only |

## Georeferencing and transformation

A first affine control-point lesson and tested least-squares implementation are available. It covers the six-parameter 2D model, rank deficiency, residual vectors and pixel-corner/centre conventions; polynomial and thin-plate-spline transformations remain open.

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Affine, polynomial and rubber-sheeting transforms; thin plate spline rectification; co-registration | Geometric transformations / image registration | 19 | [Affine georeferencing](../../implementations/python/affine-georeferencing/README.md) and [thin-plate smoothing splines](../../implementations/python/spatial-smoothing/README.md) have tested reference implementations | Partial — affine least-squares fitting and thin-plate spline smoothing are implemented; polynomial/rubber-sheeting transforms, image co-registration and robust control-point matching remain open |
| Historical map digitization: control point selection, line-following vectorization, map text spotting, symbol segmentation, legend parsing, color quantization | Digitisation and document/image-processing workflows | 19 | Not checked — intake only |
| Conflation: road and building matching, shape-based matching (turning function, Fourier descriptors, Procrustes, shape context), OSM quality and vandalism detection, completeness estimation | Feature matching / conflation / data quality assessment | 19 | Not checked — intake only |

## Geocoding and record linkage

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Geocoding, reverse geocoding, rooftop and parcel geocoding, address interpolation, address parsing (libpostal-style CRFs, transformers) | Geocoding operations / address-parsing models | 19 | [Street address interpolation](../../implementations/python/street-address-interpolation/README.md) provides a tested cumulative-distance interpolation baseline along projected street polylines | Partial — rooftop/parcel matching, reverse geocoding, authoritative address validation and CRF/transformer parsing remain open |
| String similarity: Levenshtein, Jaro-Winkler, n-gram, Soundex, Metaphone; Fellegi-Sunter, blocking, canopy clustering | String similarity / record-linkage algorithms | 19 | Partial — tested Levenshtein, Jaro-Winkler, character n-gram cosine, Soundex, exact-prefix blocking, a small-data canopy candidate generator and supplied-parameter Fellegi-Sunter scoring; Metaphone, m/u estimation, scalable blocking and source-entry bibliography/identity review remain open |
| POI deduplication, gazetteer fusion, entity resolution at scale, embedding-based place matching | Entity resolution / gazetteer and place-matching workflows | 19 | Not checked — intake only |

## First record-linkage implementation

The [string similarity and record-linkage lesson](../../algorithms/statistics/string-linkage.md) and [tested Python package](../../implementations/python/string-linkage/README.md) provide field-level similarity, phonetic coding, candidate generation and Fellegi-Sunter scoring baselines. They are not a production POI matching pipeline.

## First numeric map-classification implementation

The [numeric map-classification lesson](../../algorithms/statistics/map-classification.md) and [tested Python package](../../implementations/python/map-classification/README.md) cover equal interval, quantile and Fisher-Jenks natural breaks. Bivariate classification and perceptual color design remain open.

## First broad-phase collision implementation

The [AABB broad-phase lesson](../../algorithms/statistics/collision-broadphase.md) and [tested Python package](../../implementations/python/collision-broadphase/README.md) implement sweep-and-prune, spatial hashing and a static BVH. They do not implement dynamic or continuous collision detection.

## Cartography and geovisualization

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Classification: Jenks natural breaks, quantiles, equal interval, bivariate choropleth, perceptual color scales | Map classification methods / visual encoding | 19 | Partial — tested exact Fisher-Jenks one-dimensional dynamic programming, empirical quantile and equal-interval breaks with explicit class-boundary assignment; bivariate choropleths, perceptual color scales, optimal class-count selection and source-entry review remain open |
| Generalization: smoothing (Bezier, Gaussian, PAEK), aggregation, displacement, exaggeration, building generalization | Cartographic generalisation methods | 19 | Not checked — intake only |
| Labeling: label placement optimization, collision-free layouts, glyph placement | Label placement and layout optimisation | 19 | Not checked — intake only |
| Special maps: dot density, cartograms (Dorling, Gastner-Newman), flow maps with edge bundling (FDEB), hexbin maps, schematic and metro layout | Thematic map forms / cartogram and flow-map algorithms | 19 | Not checked — intake only |
| Rendering: isosurfaces, streamlines and LIC, ray marching, hillshade variants, vector tile styling, tile pyramids, level-of-detail, WebGL and WebGPU pipelines | Rendering algorithms / tile and graphics pipelines | 19 | Not checked — intake only |

## Data infrastructure and computing

A first format-selection guide now separates authoritative storage, analytical layout, discovery metadata and delivery products. It compares COG, Zarr, GeoParquet, FlatGeobuf, STAC, vector tiles and spatial databases by access pattern. It is a decision guide, not a claim that all listed formats are equally mature or interchangeable.

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Formats and catalogs: COG, Zarr, GeoParquet, FlatGeobuf, STAC, Mapbox Vector Tile, TopoJSON, WKB and WKT, Google polyline, Draco, spatial deduplication | Data formats / catalogue standards / encoding and deduplication methods | 19 | Not checked — intake only |
| Distributed and GPU computing: Sedona, GeoMesa, Dask, Spark, cuSpatial, GPU raster algebra, parallel viewshed and flow accumulation, out-of-core and streaming raster algorithms | Distributed systems / GPU libraries / scalable algorithms | 19 | Not checked — intake only |
| Pipelines: openEO, xarray, Rasterio, Snakemake, Airflow; process graphs, lineage tracking, data versioning | Software tools / workflow orchestration / provenance systems | 19 | Not checked — intake only |
| Numerical methods: finite difference, finite volume, finite element, spectral, semi-Lagrangian, multigrid, conjugate gradient, FFT solvers, lattice Boltzmann, level set | Numerical discretisation and solver methods | 19 | Not checked — intake only |
| Collision detection: sweep and prune, BVH, spatial hash grids | Collision detection algorithms / spatial data structures | 19 | Partial — tested 2-D AABB sweep-and-prune, uniform spatial hashing and median-split static BVH with brute-force pair oracle; dynamic updates, 3-D, continuous collision and polygon/mesh narrow phase remain open |
| Procedural terrain: Perlin and simplex noise, fractional Brownian motion, diamond-square, Poisson disk sampling, wave function collapse, L-systems, synthetic city generation | Procedural generation / stochastic sampling / synthetic data workflows | 20 | Not checked — intake only |

## Quality assurance and validation

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Topology checks, DE-9IM validation rules, temporal consistency checks, automated QA/QC, outlier rules | Data validation rules / quality assurance workflows | 20 | [DE-9IM and RCC-8 relations](../../implementations/python/spatial-topological-relations/README.md) have tested GEOS-backed predicates | Partial — DE-9IM and RCC-8 wrappers are implemented; temporal consistency, automated QA/QC workflows and general outlier rules remain open |
| Benchmark design and geographic bias audits for GeoAI | Evaluation design / geographic representativeness audits | 20 | Not checked — intake only |

## Location privacy

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Geomasking (random perturbation, donut masking), spatial k-anonymity and cloaking, geo-indistinguishability, differential privacy for location data | Privacy protection methods / formal privacy models | 20 | [Spatial k-anonymity and differential privacy](../../implementations/python/spatial-privacy/README.md) have tested reference components | Partial — hierarchical quadtree k-anonymity and a bounded-contribution Laplace mechanism are implemented; random/donut geomasking, geo-indistinguishability and trace-level protection remain open |
| Synthetic population and trajectory generation, federated learning on spatial data | Synthetic data generation / privacy-preserving distributed learning | 20 | Not checked — intake only |

## Text, social and semantic geography

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Geoparsing, place NER, toponym resolution, spatial relation extraction, qualitative spatial reasoning (RCC-8, Allen intervals, cone-based directions), natural-language route instructions | Geographic language processing / spatial reasoning methods | 20 | Not checked — intake only |
| Geographic information retrieval: spatial keyword search, query understanding, map search ranking, geographic topic models | Information retrieval / geographic search methods | 20 | Not checked — intake only |
| Social sensing: tweet and post geolocation, burst and event detection, VGI validation, tourist trajectory mining from photo sharing sites | Social-media analysis / event detection / volunteered geographic information validation | 20 | Not checked — intake only |
| Knowledge graphs: GeoSPARQL, spatial RDF, ontology alignment, entity linking, GeoQA, ontology-driven reasoning (SWRL) | Standards / knowledge representation / semantic reasoning systems | 20 | Not checked — intake only |

## Indoor, sports and retail analytics

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Indoor: IndoorGML, indoor routing, floor plan reconstruction, indoor SLAM | Standards / routing and reconstruction workflows | 20 | Not checked — intake only |
| Sports: Voronoi pitch control, expected threat, passing networks, player tracking | Spatial analytics metrics / network analysis / tracking methods | 20 | Not checked — intake only |
| Retail: customer flow, indoor heatmaps, dwell-time analysis | Movement and behavioural analytics workflows | 20 | Not checked — intake only |

## Topological, graph and geometric data analysis

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Persistent homology, Mapper, Reeb graphs, Morse-Smale complexes | Topological data analysis methods / data structures | 20 | Not checked — intake only |
| Optimal transport (Wasserstein, Sinkhorn, Gromov-Wasserstein), manifold learning (t-SNE, UMAP, Isomap) | Optimisation and transport methods / dimensionality reduction | 20 | Not checked — intake only |
| Graph signal processing, spectral clustering, graph kernels, random walk with restart, HITS, heat kernel diffusion, graph Laplacian smoothing, motif mining | Graph analysis / signal processing / ranking and diffusion methods | 20 | Not checked — intake only |

## Spatial causal inference

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Spatial difference-in-differences, synthetic control, geographic regression discontinuity, spatial instrumental variables | Causal inference designs / econometric methods | 20 | Not checked — intake only |

## Decisions for the next pass

1. Keep coordinate reference systems, transformations and geodesic calculations distinct.
2. Treat data formats and standards as infrastructure records, not algorithms.
3. Explain map design as a decision about communication, not only a rendering technique.
4. Treat location privacy as a first-class requirement; do not publish identifiable trajectories or sensitive location data as teaching examples.
5. Verify standard names and software support against current specifications and maintained documentation.
6. Separate causal identification assumptions from the mechanics of fitting a spatial model.


## Atomic completion tracking

The grouped source entries above have been decomposed into individually auditable child IDs in the [Section 9 atomic completion register](../../docs/section-9-atomic-completion-register.md). The register distinguishes geodetic operations, reference models, standards, formats, software, workflows, privacy methods and causal designs. It is a traceability backlog, not a completion claim.
