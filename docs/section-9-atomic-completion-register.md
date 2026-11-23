# Section 9 atomic completion register

**Source:** *Spatial Analysis Algorithms: Complete Compendium*, Section 9, pages 18–20.  
**Intake:** [preserved pages 16–20 transcription](../source-inventory/pages-16-20.md).  
**Section index:** [Section 9 catalogue record](../catalog/sections/09-geodesy-cartography-infrastructure.md).

This register decomposes grouped supporting systems into atomic child records. Standards, formats, software, methods and workflows remain distinct. The source-entry verification protocol and completion standard apply; a library link or partial implementation is not evidence of full coverage.

## Status vocabulary

| Status | Meaning |
|---|---|
| Open | No item-specific independent verification or implementation evidence recorded. |
| Partial | A bounded related implementation exists; remaining variants or validation are explicit. |
| Verify | Exact standard, model, method or software version must be resolved. |
| Not applicable | A framework, format or workflow is not a standalone algorithm. |

## Atomic source register

### Projections and coordinate reference systems — page 18

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S09-PR-01 | Transverse Mercator | Map projection | Verify | Verify ellipsoidal formula and implementation; test high-latitude/zone-edge behaviour. |
| S09-PR-02 | Gauss–Krüger | Projection family/zone convention | Verify | Resolve zone/central-meridian conventions and ellipsoid; distinguish from generic TM. |
| S09-PR-03 | Universal Transverse Mercator (UTM) | Zoned projection system | Verify | Verify zone numbering, false origins and special zones; test antimeridian and Norway/Svalbard. |
| S09-PR-04 | Lambert Conformal Conic | Map projection | Verify | Define 1SP/2SP variants and ellipsoid; test conformality and standard parallels. |
| S09-PR-05 | Web Mercator | Spherical/auxiliary projection | Verify | Verify EPSG:3857 conventions, latitude clipping and scale distortion. |
| S09-PR-06 | Tobler hyperelliptical projection | Map projection | Verify | Verify exact projection parameters and formula; test world boundary behaviour. |
| S09-PR-07 | Adaptive composite projections | Projection design family | Open | Identify concrete methods and objective; document region-dependent distortion and continuity. |
| S09-PR-08 | CRS axis order | CRS interoperability convention | Partial | Existing CRS transformation guide covers axis order; add authority-specific conformance fixtures. |

### Datum transformations and geodetic coordinates — page 18

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S09-DT-01 | Coordinate reference system transformations | Geodetic operation | Partial | Existing lesson covers explicit transformation/axis-order scope; add operation-pipeline selection and grid dependencies. |
| S09-DT-02 | Seven-parameter Helmert transformation | Datum transformation | Partial | Existing Position Vector implementation tested; verify coordinate-frame convention and Bursa–Wolf distinction. |
| S09-DT-03 | Molodensky transformation | Datum transformation | Open | Verify abridged/full formulas and ellipsoid assumptions; compare with Helmert. |
| S09-DT-04 | Bursa–Wolf 7-parameter transformation | Datum transformation | Verify | Verify convention, signs and parameter units; test against authoritative CRS operation. |
| S09-DT-05 | NTv2 grid shift | Grid-based datum transformation | Verify | Verify grid format/version, interpolation and licence; test known control points. |
| S09-DT-06 | Geodetic to ECEF conversion | Coordinate conversion | Partial | Existing implementation tested; verify ellipsoid and height convention. |
| S09-DT-07 | ECEF to local ENU conversion | Local frame conversion | Partial | Existing implementation tested; verify origin and rotation convention. |
| S09-DT-08 | ECEF to geodetic conversion | Coordinate conversion | Partial | Existing inverse conversion tested; add poles/centre and convergence edge cases. |
| S09-DT-09 | Antimeridian handling | Geometric/CRS edge case | Open | Define wrap/unwrap and geometry splitting; test polygons crossing ±180°. |
| S09-DT-10 | Pole handling | Geometric/CRS edge case | Open | Define singularity and longitude conventions; test polar geometries. |

### Geoid, gravity and magnetic reference models — page 18

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S09-GG-01 | EGM2008 evaluation | Geoid/gravity model | Verify | Identify official coefficients/grid and release; document interpolation and tide system. |
| S09-GG-02 | Stokes integral | Geodetic gravity method | Open | Define kernel, integration domain and corrections; test synthetic gravity anomalies. |
| S09-GG-03 | Spherical harmonic analysis | Geophysical/geodetic method | Open | Define normalisation and coefficient conventions; test synthesis/analysis round-trip. |
| S09-GG-04 | Gravity anomaly computation | Geophysical calculation | Open | Define normal/observed/free-air/Bouguer anomalies; document reference field and units. |
| S09-GG-05 | Terrain correction | Gravity correction | Open | Define DEM resolution, density and integration geometry; validate against reference examples. |
| S09-GG-06 | International Geomagnetic Reference Field (IGRF) | Magnetic reference model | Verify | Verify current IGRF release and coefficient epoch; document secular variation. |
| S09-GG-07 | World Magnetic Model (WMM) | Magnetic reference model | Verify | Verify current WMM release, validity dates and model use restrictions. |

### Spherical geometry and global grids — page 18

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S09-SG-01 | Spherical polygon area | Spherical geometry algorithm | Partial | Existing unit-vector spherical-excess implementation bounded to smaller-than-hemisphere rings; verify holes and large-region conventions. |
| S09-SG-02 | Spherical Voronoi diagram | Spherical tessellation | Open | Define geodesic distance and cell boundaries; test antipodal/degenerate sites. |
| S09-SG-03 | Spherical Delaunay triangulation | Spherical triangulation | Open | Define convex-hull dual and degeneracy; test spherical empty-cap property. |
| S09-SG-04 | Spherical wavelets | Spherical signal-processing family | Open | Identify wavelet construction and scale; test reconstruction and localisation. |
| S09-SG-05 | Icosahedral grids | Global grid family | Verify | Identify subdivision and indexing variant; test cell areas and neighbours. |
| S09-SG-06 | Cubed-sphere grids | Global grid family | Verify | Define face projection and seam treatment; test equal-area/conformal properties as applicable. |

### Space geodesy and satellite observations — page 18

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S09-SGEO-01 | Satellite laser ranging (SLR) | Space-geodetic technique | Not applicable | Document observation model, normal points and reference-frame products. |
| S09-SGEO-02 | DORIS | Space-geodetic technique | Not applicable | Document Doppler observation model and orbit/clock products. |
| S09-SGEO-03 | Very Long Baseline Interferometry (VLBI) | Space-geodetic technique | Not applicable | Document delay observables, Earth orientation and reference frames. |
| S09-SGEO-04 | GNSS time-series analysis | Geodetic estimation workflow | Open | Define discontinuities, seasonal terms and noise models; test velocity uncertainty. |
| S09-SGEO-05 | Geodetic velocity fields | Spatial estimation | Open | Define reference frame, interpolation and covariance; quantify uncertainty. |
| S09-SGEO-06 | Strain-rate estimation | Geodetic spatial derivative | Open | Define interpolation/derivative method and coordinate frame; test synthetic displacement fields. |
| S09-SGEO-07 | Total Electron Content (TEC) maps | Ionospheric mapping | Open | Define slant-to-vertical mapping and bias estimation; validate against independent products. |
| S09-SGEO-08 | Saastamoinen tropospheric delay | GNSS atmospheric correction | Verify | Verify hydrostatic/wet delay formula and meteorological inputs; test reference cases. |
| S09-SGEO-09 | Vienna Mapping Functions (VMF) | GNSS mapping function | Verify | Identify VMF1/VMF3 and grids; document interpolation and height correction. |
| S09-SGEO-10 | Precise orbit determination | Orbit estimation workflow | Open | Define force models, observations and estimator; validate residuals and orbit overlap. |
| S09-SGEO-11 | GRACE gravity recovery | Satellite gravimetry workflow | Verify | Identify mission/product level and processing release; document leakage/scaling. |
| S09-SGEO-12 | Altimetry crossover adjustment | Geodetic adjustment method | Open | Define crossover selection, bias parameters and least-squares model; test synthetic tracks. |

### Satellite orbit and constellation analysis — page 18

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S09-OR-01 | SGP4 propagation | Orbit propagation algorithm | Verify | Verify current implementation and TLE conventions; test reference satellite states. |
| S09-OR-02 | SDP4 deep-space propagation | Orbit propagation algorithm | Verify | Verify deep-space branch and resonance handling; test reference ephemerides. |
| S09-OR-03 | Two-Line Element (TLE) processing | Data format/workflow | Verify | Verify format fields, epoch and checksum; distinguish propagation from element fitting. |
| S09-OR-04 | Satellite ground-track computation | Orbit geometry | Open | Define Earth rotation and reference ellipsoid; test longitude wrapping. |
| S09-OR-05 | Satellite swath computation | Sensor geometry workflow | Open | Define field of regard, attitude and Earth intersection; test edge-of-swath geometry. |
| S09-OR-06 | Revisit analysis | Mission analysis | Open | Define access criteria, sensor constraints and time window; test orbit sampling. |
| S09-OR-07 | Sun-synchronous orbit design | Orbit design | Open | Define nodal precession and altitude/inclination relation; verify perturbation assumptions. |
| S09-OR-08 | Walker constellation design | Constellation geometry | Verify | Verify Walker Delta/Star parameters and phasing; test coverage. |
| S09-OR-09 | Satellite conjunction analysis | Collision-risk workflow | Open | Define screening, covariance and probability of collision; distinguish screening from operational assessment. |

### Astronomical calculations and survey adjustment — page 18

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S09-AS-01 | Solar position | Astronomical calculation | Verify | Identify algorithm/version and time-scale convention; compare with authoritative ephemerides. |
| S09-AS-02 | Sunrise and sunset | Astronomical calculation | Open | Define refraction, horizon and solar-disc convention; test polar-day/night cases. |
| S09-AS-03 | Tidal prediction | Harmonic prediction method | Open | Define constituents, nodal corrections and datum; compare with observed tides. |
| S09-AS-04 | Least-squares survey network adjustment | Geodetic estimation | Partial | Existing Baarda/collocation components do not constitute a complete network adjustment; define datum constraints and covariance. |

### Georeferencing and image transformation — page 19

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S09-GR-01 | Affine georeferencing | Image transformation | Partial | Existing six-parameter least-squares implementation tested; verify pixel centre/corner and robust estimation. |
| S09-GR-02 | Polynomial georeferencing | Image transformation | Open | Split polynomial order and basis; test extrapolation and control-point distribution. |
| S09-GR-03 | Rubber-sheeting | Nonrigid transformation | Open | Define triangulation/local interpolation and topology; test foldovers. |
| S09-GR-04 | Thin-plate-spline rectification | Nonrigid transformation | Partial | Existing smoothing spline is not a complete rectification contract; define control-point interpolation/regularisation. |
| S09-GR-05 | Image co-registration | Registration workflow | Open | Define transform model, resampling and residual metrics; validate with independent tie points. |
| S09-GR-06 | Historical map control-point selection | Digitisation workflow | Open | Define landmark strategy and uncertainty; preserve provenance. |
| S09-GR-07 | Line-following vectorisation | Image-to-vector workflow | Open | Define tracing algorithm and topology repair; evaluate against manually digitised lines. |
| S09-GR-08 | Map text spotting | Document vision task | Open | Define text detector/recogniser and historical fonts; evaluate transcription/geolocation. |
| S09-GR-09 | Symbol segmentation | Document/image processing | Open | Define symbol taxonomy and connected-component/learned segmentation; test overlap. |
| S09-GR-10 | Legend parsing | Document understanding workflow | Open | Define legend swatch/text association and class mapping; validate against map semantics. |
| S09-GR-11 | Colour quantisation | Image processing algorithm | Open | Identify quantisation method and palette extraction; test colour separation under scan degradation. |

### Conflation and data quality — page 19

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S09-CO-01 | Road feature matching | Feature conflation | Open | Define geometry/topology/attributes and candidate generation; test split/merge cases. |
| S09-CO-02 | Building feature matching | Feature conflation | Open | Define shape, footprint and temporal evidence; validate across resolution. |
| S09-CO-03 | Turning-function shape matching | Shape descriptor | Verify | Verify normalisation and distance; test rotation/scale invariance. |
| S09-CO-04 | Fourier shape descriptors | Shape descriptor | Open | Define contour parameterisation and coefficient normalisation; test invariances. |
| S09-CO-05 | Procrustes shape matching | Shape analysis | Open | Define alignment, scaling and correspondence; test landmark noise. |
| S09-CO-06 | Shape context | Shape descriptor | Verify | Verify descriptor histogram and matching cost; test partial occlusion. |
| S09-CO-07 | OSM quality assessment | Data quality workflow | Open | Define completeness/positional/attribute metrics and reference data; report geographic bias. |
| S09-CO-08 | OSM vandalism detection | Change/anomaly detection | Open | Define edit history, anomaly labels and false-positive review; avoid accusing contributors without adjudication. |
| S09-CO-09 | Map completeness estimation | Data quality estimation | Open | Define reference feature universe and omission model; quantify uncertainty. |

### Geocoding and address linkage — page 19

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S09-GC-01 | Forward geocoding | Geocoding workflow | Open | Define candidate generation, ranking and confidence; test ambiguous names. |
| S09-GC-02 | Reverse geocoding | Geocoding workflow | Open | Define containment/nearest-address and interpolation; test boundaries. |
| S09-GC-03 | Rooftop geocoding | Address localisation | Open | Define rooftop evidence and positional uncertainty; validate against authoritative points. |
| S09-GC-04 | Parcel geocoding | Address localisation | Open | Define parcel centroid/entrance/official point semantics; test multi-unit parcels. |
| S09-GC-05 | Address interpolation | Geocoding method | Partial | Existing cumulative-distance interpolation is a geometric baseline; local numbering conventions and parity remain open. |
| S09-GC-06 | CRF-style address parsing (libpostal-style) | Sequence labelling | Verify | Identify exact model/version and training data; document locale coverage/licence. |
| S09-GC-07 | Transformer address parsing | NLP model | Open | Identify model and schema; test multilingual/local address formats. |
| S09-GC-08 | Levenshtein similarity | String metric | Partial | Existing implementation tested; verify Unicode/grapheme semantics and normalisation. |
| S09-GC-09 | Jaro–Winkler similarity | String metric | Partial | Existing implementation tested; verify prefix boost and short-string cases. |
| S09-GC-10 | Character n-gram similarity | String metric | Partial | Existing cosine baseline tested; define tokenisation and weighting. |
| S09-GC-11 | Soundex | Phonetic encoding | Partial | Existing implementation tested; document language limitations. |
| S09-GC-12 | Metaphone | Phonetic encoding | Open | Identify original/Double Metaphone variant and language scope. |
| S09-GC-13 | Fellegi–Sunter linkage | Probabilistic record linkage | Partial | Existing supplied-parameter score is bounded; add m/u estimation and calibration. |
| S09-GC-14 | Blocking | Record-linkage candidate reduction | Partial | Existing exact-prefix blocking is bounded; add scalable multi-pass blocking. |
| S09-GC-15 | Canopy clustering | Record-linkage candidate reduction | Partial | Existing small-data canopy baseline is bounded; verify threshold semantics and scalability. |
| S09-GC-16 | POI deduplication | Entity resolution workflow | Open | Define entity schema, temporal updates and matching evaluation. |
| S09-GC-17 | Gazetteer fusion | Entity resolution workflow | Open | Define source authority, provenance and conflict resolution. |
| S09-GC-18 | Large-scale entity resolution | Record-linkage system | Open | Define distributed blocking, scoring and human adjudication. |
| S09-GC-19 | Embedding-based place matching | Semantic retrieval | Open | Define embedding model and geographic constraints; evaluate bias and recall. |

### Cartography and geovisualisation — page 19

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S09-CM-01 | Jenks natural breaks | Map classification | Partial | Existing Fisher–Jenks dynamic program tested; verify objective and tie convention. |
| S09-CM-02 | Quantile classification | Map classification | Partial | Existing implementation tested; define duplicate boundary handling. |
| S09-CM-03 | Equal-interval classification | Map classification | Partial | Existing implementation tested; define constant/empty data handling. |
| S09-CM-04 | Bivariate choropleth | Cartographic encoding | Open | Define two-variable class breaks and legend design; test perceptual decoding. |
| S09-CM-05 | Perceptual colour scales | Cartographic design | Open | Define colour space and perceptual criteria; test colour-vision accessibility. |
| S09-CM-06 | Bezier line smoothing | Cartographic generalisation | Open | Define curve fitting and topology constraints; test displacement. |
| S09-CM-07 | Gaussian line smoothing | Cartographic generalisation | Open | Define kernel and scale; test endpoint and network continuity. |
| S09-CM-08 | PAEK smoothing | Cartographic generalisation | Verify | Verify exact ArcGIS/PAEK algorithm and parameters; distinguish from generic Gaussian smoothing. |
| S09-CM-09 | Feature aggregation | Cartographic generalisation | Open | Define scale-dependent aggregation and semantic preservation. |
| S09-CM-10 | Displacement | Cartographic generalisation | Open | Define conflict model and constraints; test topology/legibility. |
| S09-CM-11 | Exaggeration | Cartographic generalisation | Open | Define feature selection and scale; preserve positional context. |
| S09-CM-12 | Building generalisation | Cartographic generalisation | Open | Split typification, aggregation, simplification and displacement; test building pattern preservation. |
| S09-CM-13 | Label placement optimisation | Cartographic optimisation | Open | Define candidate positions, conflict graph and objective; test optimality gap. |
| S09-CM-14 | Collision-free map layout | Cartographic layout | Open | Define labels/symbols and priority; test density and readability. |
| S09-CM-15 | Glyph placement | Cartographic layout | Open | Define orientation/overlap and semantic constraints; test legibility. |
| S09-CM-16 | Dot-density mapping | Thematic mapping method | Not applicable | Define point placement, population weighting and stochastic reproducibility. |
| S09-CM-17 | Dorling cartogram | Cartogram algorithm | Verify | Verify circle-packing force model and area mapping; test overlap/convergence. |
| S09-CM-18 | Gastner–Newman diffusion cartogram | Cartogram algorithm | Verify | Verify diffusion/flow formulation and mass conservation; test area error. |
| S09-CM-19 | Flow-map edge bundling (FDEB) | Flow visualisation algorithm | Verify | Verify force-directed edge bundling and parameters; test directional legibility. |
| S09-CM-20 | Hexbin maps | Aggregation/visualisation | Not applicable | Distinguish binning from hexagon tile maps; define count/density semantics. |
| S09-CM-21 | Schematic/metro map layout | Network cartography | Open | Define topology preservation, angular resolution and route constraints; evaluate readability. |
| S09-CM-22 | Isosurface rendering | 3D visualisation algorithm | Open | Define scalar interpolation and surface extraction (e.g. marching cubes); test topology. |
| S09-CM-23 | Streamline rendering | Vector-field visualisation | Open | Define integration and seeding; test stagnation/boundary handling. |
| S09-CM-24 | Line Integral Convolution (LIC) | Vector-field visualisation | Verify | Verify convolution kernel and noise texture; test direction encoding. |
| S09-CM-25 | Ray marching | Volume rendering algorithm | Open | Define sampling, transfer function and acceleration; test step-size artefacts. |
| S09-CM-26 | Hillshade variants | Terrain visualisation | Partial | Define single/multidirectional/ambient methods; test illumination and aspect. |
| S09-CM-27 | Vector tile styling | Cartographic rendering workflow | Not applicable | Define style specification/version and data schema; test rendering parity. |
| S09-CM-28 | Tile pyramids | Multiscale data structure | Not applicable | Define tile matrix set, zoom and resampling; test seams/overviews. |
| S09-CM-29 | Level-of-detail rendering | Rendering strategy | Open | Define screen-space error and refinement; test view stability. |
| S09-CM-30 | WebGL pipeline | Graphics API/workflow | Not applicable | Document supported version, shader pipeline and resource limits. |
| S09-CM-31 | WebGPU pipeline | Graphics API/workflow | Not applicable | Document current specification and browser/device support. |

### Data formats, distributed computing and pipelines — page 19

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S09-IF-01 | Cloud Optimized GeoTIFF (COG) | Raster format/layout standard | Verify | Verify OGC/GeoTIFF specs and range-read conformance; test overview and metadata. |
| S09-IF-02 | Zarr | Chunked array format | Verify | Identify format version and codecs; test metadata interoperability. |
| S09-IF-03 | GeoParquet | Geospatial columnar format | Verify | Verify current spec and geometry encoding; test CRS/bbox metadata. |
| S09-IF-04 | FlatGeobuf | Geospatial vector format | Verify | Verify version and spatial index; test streaming/interoperability. |
| S09-IF-05 | STAC | Spatiotemporal asset catalogue standard | Verify | Verify current API/item/catalog spec; test extension and asset semantics. |
| S09-IF-06 | Mapbox Vector Tile (MVT) | Vector tile encoding | Verify | Verify specification/version and extent/quantisation; test clipping and attributes. |
| S09-IF-07 | TopoJSON | Topological encoding format | Verify | Verify transform/arcs semantics and licence; test shared boundary round-trip. |
| S09-IF-08 | Well-Known Binary (WKB) | Geometry encoding | Verify | Verify OGC/ISO variant, endian and dimensional flags. |
| S09-IF-09 | Well-Known Text (WKT) | Geometry text encoding | Verify | Verify version, dimensional/CRS extensions and parser behaviour. |
| S09-IF-10 | Google encoded polyline | Line encoding | Verify | Verify precision and signed delta encoding; test round-trip. |
| S09-IF-11 | Draco compression | 3D geometry compression | Verify | Identify version and licence; test quantisation and attribute loss. |
| S09-IF-12 | Spatial data deduplication | Data quality/compaction method | Open | Define geometry and semantic equivalence; test temporal/source distinctions. |
| S09-IF-13 | Apache Sedona | Distributed spatial analytics software | Verify | Verify release, SQL API and Spark compatibility. |
| S09-IF-14 | GeoMesa | Distributed geospatial datastore | Verify | Verify version, backend and query semantics. |
| S09-IF-15 | Dask | Parallel computing framework | Verify | Document version and distributed scheduling; identify exact spatial extension. |
| S09-IF-16 | Apache Spark | Distributed computing framework | Verify | Document version and execution model; not a spatial algorithm. |
| S09-IF-17 | cuSpatial | GPU spatial analytics library | Verify | Verify version, operations and hardware support. |
| S09-IF-18 | GPU raster algebra | Parallel raster processing | Open | Define kernel and boundary/NoData semantics; compare CPU/GPU results. |
| S09-IF-19 | Parallel viewshed | Parallel terrain algorithm | Open | Define line-of-sight model, curvature/refraction and parallel partitioning; test exactness. |
| S09-IF-20 | Parallel flow accumulation | Parallel hydrology algorithm | Open | Define D8/D-infinity and dependency resolution; test mass conservation. |
| S09-IF-21 | Out-of-core raster algorithms | Scalable processing family | Open | Define windowing/halo and IO strategy; test equivalence with in-memory oracle. |
| S09-IF-22 | Streaming raster algorithms | Streaming processing family | Open | Define event ordering, state and boundary handling; test chunk invariance. |
| S09-IF-23 | openEO | EO processing API/platform | Verify | Verify API version and backend-specific behaviour. |
| S09-IF-24 | xarray | N-dimensional labelled array library | Verify | Verify version and data model; distinguish library from geospatial extension. |
| S09-IF-25 | Rasterio | Raster IO library | Verify | Verify version, GDAL compatibility and metadata semantics. |
| S09-IF-26 | Snakemake | Workflow engine | Verify | Verify version and reproducibility features; document execution configuration. |
| S09-IF-27 | Apache Airflow | Workflow orchestrator | Verify | Verify version and DAG semantics; not an algorithm. |
| S09-IF-28 | Spatial process graphs | Workflow representation | Not applicable | Define node/edge schema, execution and provenance. |
| S09-IF-29 | Data lineage tracking | Provenance workflow | Not applicable | Define immutable identifiers, parentage and reproducibility. |
| S09-IF-30 | Data versioning | Data management workflow | Not applicable | Define content hashes, schema migration and retention. |

### Numerical methods and collision detection — page 19

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S09-NM-01 | Finite difference methods | Numerical discretisation | Open | Define PDE, stencil, order and boundary; test convergence. |
| S09-NM-02 | Finite volume methods | Numerical discretisation | Open | Define control volumes and fluxes; test conservation. |
| S09-NM-03 | Finite element methods | Numerical discretisation | Open | Define weak form, basis and mesh; test convergence and conditioning. |
| S09-NM-04 | Spectral methods | Numerical discretisation | Open | Define basis and boundary periodicity; test spectral convergence. |
| S09-NM-05 | Semi-Lagrangian methods | Advection solver | Open | Define characteristic tracing and interpolation; test stability/mass conservation. |
| S09-NM-06 | Multigrid | Numerical solver | Open | Define smoother, restriction/prolongation and coarse solve; test convergence rates. |
| S09-NM-07 | Conjugate gradient | Iterative linear solver | Open | Define SPD conditions and stopping; test residual and preconditioning. |
| S09-NM-08 | FFT solvers | Spectral solver family | Open | Define periodic/boundary conditions and normalisation; test against direct solver. |
| S09-NM-09 | Lattice Boltzmann methods | Fluid simulation family | Open | Identify collision model, lattice and boundary; test conservation/stability. |
| S09-NM-10 | Level-set methods | Interface evolution | Open | Define signed-distance reinitialisation and velocity; test curvature and topology changes. |
| S09-CD-01 | Sweep-and-prune collision detection | Broad-phase collision algorithm | Partial | Existing 2D AABB baseline tested; add incremental updates and 3D. |
| S09-CD-02 | Bounding-volume hierarchy (BVH) collision detection | Broad-phase spatial structure | Partial | Existing static median-split BVH tested; add dynamic refit/rebuild and continuous collision. |
| S09-CD-03 | Spatial hash-grid collision detection | Broad-phase collision algorithm | Partial | Existing 2D uniform grid tested; define cell-size and duplicate suppression. |
| S09-CD-04 | Continuous collision detection | Collision detection family | Open | Define swept volumes/time-of-impact; test tunnelling and degenerate motion. |
| S09-CD-05 | Narrow-phase polygon/mesh collision | Geometric predicate family | Open | Define exact intersection/contact and robustness; compare with trusted geometry kernel. |

### Procedural terrain and synthetic worlds — page 20

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S09-PT-01 | Perlin noise | Procedural noise | Verify | Verify gradient/hash convention and implementation; test continuity and spectrum. |
| S09-PT-02 | Simplex noise | Procedural noise | Verify | Verify simplex construction and patent/licence status historically; test continuity. |
| S09-PT-03 | Fractional Brownian motion (fBm) | Stochastic terrain model | Open | Define octave amplitudes/frequencies and seed; test spectral slope. |
| S09-PT-04 | Diamond-square algorithm | Procedural terrain generation | Verify | Verify boundary/roughness schedule and randomisation; test grid-size constraints. |
| S09-PT-05 | Poisson disk sampling | Spatial sampling algorithm | Partial | Existing sampling baselines require source-entry identity review; test minimum-distance and unbiasedness. |
| S09-PT-06 | Wave Function Collapse | Procedural constraint propagation | Verify | Identify exact implementation/entropy heuristic and adjacency constraints; test contradiction/backtracking. |
| S09-PT-07 | L-systems | Formal grammar/generative model | Verify | Define grammar, rewriting and interpretation; test deterministic/stochastic variants. |
| S09-PT-08 | Synthetic city generation | Procedural urban simulation | Open | Define street/building grammar and target statistics; validate morphology and provenance. |

### Quality assurance and geographic validity — page 20

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S09-QA-01 | Topology checks | Data validation workflow | Partial | Existing topological relation predicates cover selected cases; define dataset-level rules. |
| S09-QA-02 | DE-9IM validation rules | Geometry validation standard/rules | Partial | Existing GEOS-backed relations tested; specify geometry-type validity and application rules. |
| S09-QA-03 | Temporal consistency checks | Data QA workflow | Open | Define valid-time, event ordering and lifecycle constraints; test late updates. |
| S09-QA-04 | Automated QA/QC | Data quality workflow | Open | Define rule registry, severity and adjudication; measure false alerts. |
| S09-QA-05 | Outlier rules | Data quality method family | Open | Split statistical/physical/spatial rules; document detection vs correction. |
| S09-QA-06 | Benchmark design for GeoAI | Evaluation protocol | Open | Define geography, temporal/sensor split and representativeness; prevent leakage. |
| S09-QA-07 | Geographic bias audits | Model/data evaluation | Open | Define population/region support and metrics; report confidence intervals. |

### Location privacy — page 20

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S09-PRIV-01 | Random perturbation geomasking | Location privacy method | Open | Define noise distribution and geographic constraints; quantify disclosure/utility. |
| S09-PRIV-02 | Donut masking | Location privacy method | Open | Define exclusion radius and outer distribution; assess re-identification risk. |
| S09-PRIV-03 | Spatial k-anonymity | Location privacy method | Partial | Existing adaptive quadtree generalisation bounded; assess linkage attacks and utility. |
| S09-PRIV-04 | Spatial cloaking | Location privacy method | Open | Define cloaking region and adversary; test population/road constraints. |
| S09-PRIV-05 | Geo-indistinguishability | Formal location privacy model | Verify | Verify metric privacy definition and planar Laplace mechanism; document assumptions. |
| S09-PRIV-06 | Differential privacy for location data | Formal privacy method | Partial | Existing bounded Laplace mechanism/accountant; verify adjacency, composition and privacy budget. |
| S09-PRIV-07 | Synthetic spatial microdata | Privacy-preserving synthesis | Partial | Existing IPF donor resampling is not a complete synthesiser; add generative method and disclosure evaluation. |
| S09-PRIV-08 | Synthetic trajectory generation | Privacy-preserving trajectory synthesis | Open | Define temporal/spatial fidelity and adversary; evaluate membership/re-identification. |
| S09-PRIV-09 | Federated learning on spatial data | Distributed learning architecture | Open | Define client geography, non-IID data and privacy threat; test communication and leakage. |

### Text, social and semantic geography — page 20

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S09-TX-01 | Geoparsing | NLP workflow | Open | Define entity/place extraction and coordinate grounding; evaluate multilingual text. |
| S09-TX-02 | Place named-entity recognition | NLP task | Open | Define place taxonomy and nested entities; annotate geographically diverse corpus. |
| S09-TX-03 | Toponym resolution | Geographic entity linking | Open | Define gazetteer, context and candidate ranking; test ambiguity and historical names. |
| S09-TX-04 | Spatial relation extraction | NLP task | Open | Define relation ontology and argument roles; evaluate relation direction. |
| S09-TX-05 | RCC-8 qualitative spatial reasoning | Qualitative reasoning calculus | Verify | Verify composition tables and region assumptions; test consistency networks. |
| S09-TX-06 | Allen interval algebra | Temporal relation calculus | Verify | Verify 13 base relations and composition; test temporal reasoning. |
| S09-TX-07 | Cone-based direction relations | Qualitative directional calculus | Open | Define reference object and angular sectors; test converse/composition. |
| S09-TX-08 | Natural-language route instructions | Language-to-navigation workflow | Open | Define landmarks, turn instructions and graph grounding; evaluate ambiguity and safety. |
| S09-TX-09 | Spatial keyword search | Information retrieval method | Open | Define spatial/text relevance and top-k semantics; compare with exhaustive baseline. |
| S09-TX-10 | Geographic query understanding | Search/NLP workflow | Open | Define intent, spatial filters and entity grounding; test query coverage. |
| S09-TX-11 | Map search ranking | Geographic information retrieval | Open | Define relevance, spatial proximity and freshness; evaluate with judged queries. |
| S09-TX-12 | Geographic topic models | Spatial text model | Open | Identify spatial LDA/topic variants; define spatial prior and inference. |
| S09-TX-13 | Social-post geolocation | Social sensing workflow | Open | Define location granularity and consent/privacy; audit geographic sampling bias. |
| S09-TX-14 | Social-media burst detection | Event detection | Open | Define temporal baseline and spatial clustering; test false alarms. |
| S09-TX-15 | Volunteered geographic information validation | Data quality workflow | Open | Define authoritative reference and contributor bias; evaluate completeness/accuracy. |
| S09-TX-16 | Tourist trajectory mining from photo sharing | Mobility/social sensing | Open | Define temporal sequence and sampling bias; protect identifiable travel traces. |
| S09-TX-17 | GeoSPARQL | Geospatial semantic standard | Verify | Verify current OGC version, functions and entailment; test conformance. |
| S09-TX-18 | Spatial RDF | Semantic data model | Verify | Identify vocabularies and geometry serialisation; test CRS semantics. |
| S09-TX-19 | Ontology alignment | Knowledge representation method | Open | Define matching, consistency and human adjudication; test with known ontologies. |
| S09-TX-20 | Entity linking | Information extraction method | Open | Define candidate generation and disambiguation; evaluate geographic names. |
| S09-TX-21 | GeoQA | Geographic question-answering task/system family | Verify | Disambiguate datasets and systems; document grounding and evaluation. |
| S09-TX-22 | SWRL ontology-driven reasoning | Rule-based reasoning language | Verify | Verify specification and execution semantics; document spatial built-ins. |

### Indoor, sports and retail analytics — page 20

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S09-IN-01 | IndoorGML | Indoor spatial data standard | Verify | Verify current OGC version and navigation model; test conformance. |
| S09-IN-02 | Indoor routing | Network routing workflow | Open | Define floor connectors, accessibility and restrictions; test 3D/vertical paths. |
| S09-IN-03 | Floor-plan reconstruction | Image/geometry reconstruction | Open | Define wall/door detection and topology; validate with surveyed plans. |
| S09-IN-04 | Indoor SLAM | Robotics localisation/mapping | Open | Split lidar/visual/inertial variants; test drift and loop closure. |
| S09-SP-01 | Voronoi pitch control | Sports spatial metric | Open | Define player influence, speed and direction; validate against tracking data. |
| S09-SP-02 | Expected threat (xT) | Sports possession value model | Open | Define pitch discretisation and transition probabilities; calibrate on event data. |
| S09-SP-03 | Passing networks | Sports network analysis | Open | Define pass events, nodes and edge weights; assess time/possession aggregation. |
| S09-SP-04 | Player tracking | Sports tracking workflow | Open | Define sensor fusion, identity and uncertainty; validate trajectories. |
| S09-RT-01 | Customer flow analysis | Retail movement analytics | Open | Define anonymous sensor observations and flow metrics; assess privacy. |
| S09-RT-02 | Indoor heatmaps | Retail spatial analytics | Open | Define sampling density, smoothing and floor geometry; avoid identifying individuals. |
| S09-RT-03 | Dwell-time analysis | Movement analytics | Open | Define visit/stop detection and censoring; test sensor outages and privacy. |

### Topological, graph and geometric data analysis — page 20

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S09-TDA-01 | Persistent homology | Topological data analysis | Open | Define filtration and coefficient field; test known topological spaces. |
| S09-TDA-02 | Mapper algorithm | Topological data analysis | Verify | Verify cover/lens/clustering construction; test parameter stability. |
| S09-TDA-03 | Reeb graphs | Topological structure | Open | Define scalar function and graph construction; test critical points. |
| S09-TDA-04 | Morse–Smale complexes | Topological decomposition | Verify | Verify gradient flow/critical point construction; test triangulated surfaces. |
| S09-OT-01 | Wasserstein optimal transport | Optimal transport method | Open | Define cost and measure normalisation; test 1D exact cases. |
| S09-OT-02 | Sinkhorn algorithm | Entropic OT solver | Open | Define entropy regularisation and convergence; test bias as epsilon varies. |
| S09-OT-03 | Gromov–Wasserstein distance | Relational optimal transport | Open | Define structural cost and solver; test isomorphic finite metric spaces. |
| S09-ML-01 | t-SNE | Manifold visualisation method | Verify | Verify objective, perplexity and stochastic optimisation; avoid interpreting axes metrically. |
| S09-ML-02 | UMAP | Manifold learning method | Verify | Verify fuzzy simplicial set and optimisation; document reproducibility. |
| S09-ML-03 | Isomap | Manifold learning method | Partial | Define neighbourhood graph and geodesic approximation; test disconnected data. |
| S09-GSP-01 | Graph signal processing | Research field/method family | Not applicable | Split graph Fourier, filtering and sampling into concrete records. |
| S09-GSP-02 | Spectral clustering | Graph clustering | Partial | Link exact Laplacian variants; avoid duplicate canonical records. |
| S09-GSP-03 | Graph kernels | Graph similarity family | Open | Split random-walk, Weisfeiler–Lehman and diffusion kernels; define PSD properties. |
| S09-GSP-04 | Random walk with restart | Graph ranking/diffusion | Open | Define restart probability and dangling nodes; test convergence. |
| S09-GSP-05 | HITS | Link analysis algorithm | Verify | Verify hub/authority iteration and normalisation; test bipartite examples. |
| S09-GSP-06 | Heat-kernel diffusion | Graph diffusion method | Open | Define Laplacian and time parameter; test spectral/series equivalence. |
| S09-GSP-07 | Graph Laplacian smoothing | Graph signal processing | Open | Define normalised/unnormalised Laplacian and regularisation; test oversmoothing. |
| S09-GSP-08 | Motif mining | Graph pattern mining | Open | Define motif classes and directed/weighted handling; test exact small graphs. |

### Spatial causal inference — page 20

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S09-CA-01 | Spatial difference-in-differences | Causal design | Open | Define treatment assignment, spillovers and spatial interference; test parallel-trend diagnostics. |
| S09-CA-02 | Synthetic control | Causal estimation method | Open | Define donor pool, pre-fit and inference; test placebo/permutation inference. |
| S09-CA-03 | Geographic regression discontinuity | Causal design | Open | Define boundary treatment, distance and spatial sorting; test bandwidth/robustness. |
| S09-CA-04 | Spatial instrumental variables | Causal econometric method | Open | Define instrument exclusion/relevance and spatial spillovers; assess weak instruments. |

## Completion gates

1. Verify projections, standards, formats, models and software against authoritative current specifications; record version, datum/ellipsoid, licence and validity dates.
2. For coordinate/geodetic methods, specify frame, epoch, ellipsoid, height type, axis order, units and transformation grids.
3. For map design, distinguish computational methods from visual communication choices and document perceptual evaluation.
4. For data infrastructure, test conformance/interoperability and record versioned dependencies rather than reimplementing formats.
5. For privacy, require an explicit threat model, privacy budget where applicable, utility analysis and review before exposing location data.
6. For semantic/causal methods, define ontology/estimand, assumptions and failure modes; do not overstate causal conclusions.
7. Add independent tests and canonical lessons only after exact method identity is resolved; reconcile dashboard and cross-links after evidence changes.

**Current conclusion:** Section 9 is decomposed into atomic review items. It remains open; this register is not an authoritative implementation of the standards, models or workflows listed.
