# Algorithm collection

## Optimisation

- [Metaheuristics for spatial optimisation](optimization/metaheuristics.md) — a source-linked taxonomy of evolutionary, trajectory, swarm, memory-based, multi-start and mathematical-programming hybrid search families.

Each record explains one method or operation, its assumptions, where it is useful, and what can go wrong. The collection is growing from the supplied [source inventory](../source-inventory/README.md); an entry is not treated as verified merely because it appears in that inventory.

## Compositional statistics

- [Compositional data geometry](statistics/compositional-data-geometry.md) — closure, centred log-ratio coordinates, multiplicative zero replacement and Aitchison distance.

## Statistical surveillance

- [Syndromic surveillance](statistics/syndromic-surveillance.md) — two-sided CUSUM and explicit EARS-style C1/C2/C3 aberration scores for count series.

## Networks and mobility

- [Flow-capturing location](networks/flow-capturing-location.md) — select a cardinality-constrained set of sites to maximize unique weighted path coverage.

- [Network algorithms index](networks/README.md) — graph search, shortest paths, transit routing, network structure, optimisation and stable matching.

## Raster and terrain

- [SLIC superpixels](remote-sensing/slic-superpixels.md) — compactness-controlled local clustering in joint feature and image-coordinate space.

- [Manning open-channel flow](raster/manning-open-channel.md) — calculate uniform-flow discharge and invert for normal depth in rectangular/trapezoidal channels.

- [Muskingum channel routing](raster/muskingum-routing.md) — linear reach routing with explicit coefficient stability conditions and storage diagnostics.

- [Brovey pan-sharpening](remote-sensing/brovey-pan-sharpening.md) — inject a co-registered panchromatic intensity into multispectral bands with an explicit NoData policy.

- [DEM void filling](raster/dem-void-filling.md) — bounded synchronous inverse-distance interpolation for missing elevation cells.

- [Stumpf bathymetry and SeaWiFS OC4v4 chlorophyll](remote-sensing/stumpf-bathymetry-and-oc4v4.md) — local log-band-ratio depth calibration and the sensor-specific OC4v4 chlorophyll polynomial.

- [Solar geometry](raster/solar-geometry.md) — estimate solar elevation, zenith, azimuth and top-of-atmosphere irradiance from timezone-aware timestamps.

- [Local raster map algebra](raster/local-map-algebra.md) — aligned cellwise arithmetic, reducers, comparisons and categorical lookup with explicit NoData policies.

- [Marching squares](raster/marching-squares.md) — extract line-segment isolines from a rectilinear scalar grid with explicit saddle and NoData handling.

## Sampling and experimental design

- [Space-filling sampling designs](statistics/space-filling-sampling.md) — Latin hypercube, centered LHS, multi-start maximin selection and k-means coverage for bounded continuous domains.

## Interpolation and geostatistics

- [Mann-Kendall and Sen trend methods](statistics/mann-kendall-sen.md) — non-parametric monotonic trend test and median pairwise slope estimator.
- [Fay-Herriot area-level model](statistics/fay-herriot.md) — REML area-level small-area estimation with empirical BLUP prediction.
- [Horvitz-Thompson estimation](statistics/horvitz-thompson.md) — design-based population total and mean using first- and second-order inclusion probabilities.

- [Inverse-distance weighting](interpolation/inverse-distance-weighting.md) — deterministic point interpolation with exact-sample, radius and nearest-neighbour policies.

- [Sibson natural-neighbour interpolation](interpolation/natural-neighbour.md) — interpolate from Voronoi-cell areas stolen when a query is inserted; the reference implementation rejects extrapolation.
- [Whittaker-Eilers smoothing](interpolation/whittaker-smoother.md) — smooth ordered sequences with a weighted finite-difference penalty and explicit missing-observation handling.

## Geometry

- [Point in polygon](geometry/point-in-polygon.md) — classify a point as inside, outside or on a polygon boundary.
- [Polygon intersection](geometry/polygon-intersection.md) — construct the geometry shared by two inputs.
- [Convex hull](geometry/convex-hull.md) — find the smallest convex set containing a finite planar point set, with Graham scan, Jarvis march (gift wrapping) and Quickhull implementations.
- [Voronoi and Delaunay](geometry/voronoi-delaunay.md) — nearest-site regions and their Delaunay dual.
- [Laplacian and Taubin mesh smoothing](geometry/mesh-smoothing.md) — smooth triangular surface meshes with uniform one-ring Laplacian and shrinkage-compensating Taubin passes.
- [Alpha shapes](geometry/alpha-shapes.md) — parameterise a non-convex point-set envelope using Delaunay triangle circumradii.
- [Segment intersection](geometry/segment-intersection.md) — determine whether two line segments cross, touch or overlap.
- [Bentley–Ottmann](geometry/bentley-ottmann.md) — find intersecting pairs across a set of segments using a plane sweep.
- [Polygon validity](geometry/polygon-validity.md) — check whether rings, shells, holes and multi-part geometries satisfy the chosen geometry model; includes a tested Shapely inspection and explicit-repair workflow.
- [Polygon clipping](geometry/polygon-clipping.md) — compare clipping algorithm families, choose an appropriate tool and study a tested convex Sutherland–Hodgman teaching implementation.
- [Polygon overlay operations](geometry/overlay-operations.md) — understand intersection, union, difference, symmetric difference and precision, with a tested Shapely/GEOS package and visual notebook.
- [Line simplification](geometry/simplification.md) — compare Douglas–Peucker maximum-deviation and Visvalingam–Whyatt effective-area generalisation, with tested baselines.
- [Polygon coverage simplification](geometry/coverage-simplification.md) — preserve shared boundaries when simplifying an edge-matched polygon coverage.
- [Precision models and snap rounding](geometry/precision-models.md) — distinguish coordinate precision reduction, fixed-grid overlay and snap-rounding noding.
- [Snap rounding noder](geometry/snap-rounding.md) — understand hot pixels, exact arrangement vertices and fixed-grid rerouting, with a tested teaching baseline.
- [Polygon offsetting](geometry/offsetting.md) — distinguish geometric offsets from clipping and compare join, cap and precision behaviour.
- [Proximity graphs](geometry/proximity-graphs.md) — compare Gabriel, relative-neighbourhood and Euclidean minimum-spanning graphs.
- [Planar point location](geometry/point-location.md) — understand slab decompositions and randomized trapezoidal maps, with a tested restricted static slab locator.

## Query processing

- [Spatial skyline queries](query-processing/spatial-skyline.md) — return objects not dominated across distance to a query location and selected attributes.

## Approximate inference

- [Laplace approximation and slice sampling](statistics/laplace-and-slice-inference.md) — posterior mode, local Gaussian approximation and componentwise slice sampling.

## Volumetric raster analysis

- [Three-dimensional connected components](raster/3d-connected-components.md) — label voxel objects under 6-, 18- or 26-neighbour connectivity with invalid voxels as barriers.

## Ellipsoidal geodesy

- [Ellipsoidal geodesic operations](geodesy/ellipsoidal-geodesic-operations.md) — solve direct and inverse geodesics, polygon area/perimeter and sampled geodesic-radius buffers with an explicit ellipsoid.

## Network point-pattern analysis

- [Network Ripley's K](statistics/network-ripley-k.md) — summarize event clustering by shortest-path distance on a finite linear network.

## Circular and directional statistics

- [Circular and directional statistics](statistics/circular-directional-statistics.md) — summarize directions, test circular uniformity, evaluate the von Mises density and construct weighted rose histograms.

## Spatial Bayesian inference

- [Proper Gaussian CAR Gibbs sampling](statistics/proper-car-gibbs-sampling.md) — fixed-hyperparameter latent Gaussian posterior sampling.

## Competitive facility location

- [Huff competitive location](spatial-interaction/huff-competitive-location.md) — probabilistic facility choice and expected market shares.

## Scalable density estimation

- [FFT-grid KDE](statistics/fft-grid-kde.md) — weighted binned Gaussian KDE using FFT convolution.

## Information theory

- [Spatial information-theoretic measures](statistics/spatial-information-theory.md) — Shannon, Renyi, Tsallis and permutation entropy.

## Route choice

- [Path-size logit](networks/path-size-logit.md) — overlap-corrected route-choice probabilities for alternatives sharing network edges.

## Spectral continuum removal

- [Spectral continuum removal](remote-sensing/continuum-removal.md) — upper-convex-hull normalization, absorption depth and integrated absorption area.

## Empirical optical and terrain corrections

- [Empirical corrections](remote-sensing/empirical-corrections.md) — dark-object subtraction, C-correction, SCS+C, Minnaert, histogram matching, pseudo-invariant-feature affine normalization and empirical-line DN-to-reflectance calibration.
- [IR-MAD](remote-sensing/ir-mad.md) — iteratively reweighted canonical variates and chi-square no-change scores for bitemporal imagery.

## Temporal image compositing

- [Optical temporal compositing](remote-sensing/temporal-compositing.md) — best-pixel quality selection, observed-spectrum medoid and maximum-NDVI compositing.

## Spatiotemporal object tracking

- [Raster object tracking](raster/object-tracking.md) — associate segmented raster objects through overlap graphs, retaining split/merge links and deterministic primary track IDs.

## Hyperspectral candidate extraction

- [Pixel Purity Index (PPI)](remote-sensing/pixel-purity-index.md) — rank candidate endmembers by repeated random-projection extrema; scores are screening votes, not purity probabilities.

## Threshold-run event detection

- [Run-theory drought events](remote-sensing/run-theory-drought-events.md) — threshold runs, gap bridging and event severity.

## Drought indices

- [Drought condition indices](remote-sensing/drought-condition-indices.md) — VCI, TCI, VHI and gamma SPI.

## Land-change accounting

- [Land-change accounting](statistics/land-change-accounting.md) — transition matrices, gains/losses, disagreement and intensity summaries.

## Terrain travel time

- [Directional terrain travel-time models](raster/terrain-travel-time.md) — Tobler's hiking function, Naismith's rule, Langmuir's descent correction and raster Dijkstra accumulation.

## Spatial interaction

- [Constrained gravity-flow models](spatial-interaction/gravity-flow-models.md) — compare unconstrained, production-constrained, attraction-constrained, doubly constrained and entropy-maximising flow allocation.

## Cartographic classification

- [Classification breaks](cartography/classification-breaks.md) — compare geometric, standard-deviation, box-plot, head/tail, Dalenius–Hodges and exact 1D ckmeans breaks.

## Streaming and sketching

- [Streaming sketches for spatial data](streaming/streaming-sketches.md) — approximate distinct counts, event frequencies, membership screening and uniform reservoir samples.

## Optimization and location science

- [The p-median problem](optimization/p-median.md) — choose a fixed number of candidate facilities to minimise weighted assignment cost.
- [Capacitated p-median](optimization/capacitated-p-median.md) — minimise assignment cost while respecting finite facility capacities and indivisible demand.
- [Accessibility equity diagnostics](optimization/accessibility-equity.md) — inspect population-weighted accessibility distributions, lower-tail outcomes and group gaps without treating one metric as a fairness verdict.
- [Equity-constrained maximal covering](optimization/equity-constrained-covering.md) — maximise covered demand while enforcing explicit minimum coverage shares for caller-defined groups.
- [Maximal covering location](optimization/maximal-covering.md) — maximise weighted demand reached by at least one selected facility within a service threshold.
- [Backup coverage (r-covering)](optimization/backup-coverage.md) — require demand to have multiple distinct selected facilities within the threshold.
- [Maximum expected covering (MEXCLP)](optimization/mexclp.md) — discount coverage according to the probability that nearby units are busy.
- [M/M/c queueing](optimization/mmc-queue.md) — estimate waiting and system performance for a stable multi-server FCFS queue.
- [Two-step floating catchment area](optimization/two-step-fca.md) — estimate potential service accessibility by combining provider supply and population demand within travel catchments.

## Remote sensing

- [N-FINDR](remote-sensing/nfindr-endmembers.md) — iteratively maximise simplex volume to identify candidate hyperspectral endmembers.
- [Automatic Target Generation Process (ATGP)](remote-sensing/atgp-endmembers.md) — select candidate spectra by iterative orthogonal residual-energy projection.
- [Vertex Component Analysis (VCA)](remote-sensing/vca-endmembers.md) — extract candidate hyperspectral endmembers under a pure-pixel linear-mixture assumption.
- [Fully Constrained Least Squares (FCLS)](remote-sensing/fcls-unmixing.md) — estimate nonnegative per-pixel abundance fractions constrained to sum to one.
- [Constrained Energy Minimisation (CEM)](remote-sensing/cem-detection.md) — construct a unit-target-response filter that minimises output energy.
- [Adaptive Coherence Estimator (ACE)](remote-sensing/ace-detection.md) — score target similarity in a background-whitened spectral space.
- [Spectral matched filter](remote-sensing/spectral-matched-filter.md) — detect a known target signature against a global covariance model of background spectra.
- [Spectral Angle Mapper and Spectral Information Divergence](remote-sensing/spectral-similarity.md) — compare pixel spectra with reference signatures using angular and information-theoretic distances.
- [Reed–Xiaoli anomaly detection](remote-sensing/rx-anomaly.md) — score spectrally unusual pixels using global background Mahalanobis distance.
- [Minimum Noise Fraction (MNF)](remote-sensing/mnf-transform.md) — whiten estimated noise covariance before ordering spectral components by signal-to-noise.
- [2-D Haar wavelet transform](remote-sensing/haar-wavelet.md) — decompose imagery into multiscale approximation and directional detail subbands with inverse reconstruction.
- [Radon transform](remote-sensing/radon-transform.md) — calculate approximate line integrals over angle and offset to form a sinogram.
- [2-D Fourier transforms and frequency filtering](remote-sensing/fourier-filtering.md) — transform imagery into spatial-frequency space and apply radial low-, high- or band-pass filters.
- [Adaptive thresholding](remote-sensing/adaptive-thresholding.md) — derive local mean or Gaussian threshold surfaces for spatially varying backgrounds.
- [Hough line transform](remote-sensing/hough-transform.md) — accumulate edge-pixel votes in rho-theta space and extract straight-line peaks.
- [Sobel and Canny edge detection](remote-sensing/edge-detection.md) — gradient estimation, non-maximum suppression and hysteresis.
- [Mathematical morphology](remote-sensing/mathematical-morphology.md) — binary dilation, erosion, opening, closing and boundary extraction.
- [Gabor filters](remote-sensing/gabor-filters.md) — oriented, frequency-selective filter banks for texture analysis.
- [PCA transform](remote-sensing/pca-transform.md) — reduce correlated multispectral bands with covariance or correlation principal components; distinct from MNF.
- [GLCM texture](remote-sensing/glcm-texture.md) — build offset-specific gray-level co-occurrence matrices and calculate common texture features.
- [Optical spectral-index family](remote-sensing/spectral-index-family.md) — calculate vegetation, moisture, water, built-up, burn and snow indices with explicit band conventions.
- [Otsu thresholding](remote-sensing/otsu-thresholding.md) — select a global two-class intensity threshold by maximising between-class variance.
- [Normalised Difference Vegetation Index (NDVI)](remote-sensing/ndvi.md) — calculate a red/NIR spectral contrast while preserving invalid pixels and preprocessing caveats.

## Raster operations

- [Raster range reclassification](raster/raster-reclassification.md) — apply explicit non-overlapping half-open intervals to raster values while preserving NoData.

- [Euclidean distance transform](raster/euclidean-distance-transform.md) — calculate centre-to-centre distance from every grid cell to the nearest target cell.
- [Focal raster statistics](raster/focal-statistics.md) — calculate NoData-aware square-window means efficiently using integral images.
- [Priority-Flood](raster/priority-flood.md) — fill DEM depressions to their lowest spill elevation and inspect the fill-depth surface.
- [D8 flow direction](raster/d8-flow-direction.md) — assign each DEM cell to its steepest downslope neighbour.
- [D8 flow accumulation](raster/d8-flow-accumulation.md) — propagate upstream cell counts or weighted contributions through an existing D8 direction grid.
- [Watershed delineation](raster/watershed-delineation.md) — trace the contributing area of a selected outlet through a D8 flow network.
- [Stream ordering](raster/stream-order.md) — compare Strahler order and Shreve magnitude on a connected D8 channel network.
- [Terrain slope and aspect](raster/slope-aspect.md) — estimate local derivatives with Horn's 3×3 operator.
- [Local hillshade](raster/hillshade.md) — derive normalized illumination from slope, aspect and a declared sun position.
- [Topographic wetness index](raster/topographic-wetness-index.md) — combine specific catchment area and slope into a relative terrain index.
- [Raster resampling](raster/resampling.md) — compare nearest-neighbour and bilinear interpolation, including NoData policies.
- [Zonal statistics](raster/zonal-statistics.md) — summarize aligned raster values by integer zone labels.
- [Connected-component labeling](raster/connected-components.md) — identify connected foreground regions under 4/8-neighbour rules.
- [Raster cost distance](raster/cost-distance.md) — calculate multi-source least accumulated cost through a weighted raster graph.

## Geostatistics

- [Spatial interpolation](geostatistics/interpolation.md) — compare inverse-distance weighting with ordinary kriging, a variogram model and conditional prediction variance.

## Networks and routing

- [Shortest paths](networks/shortest-paths.md) — understand graph cost models and shortest-path families, with tested Dijkstra, A*, bidirectional Dijkstra and ALT baselines.
- [Turn-aware and time-dependent routing](networks/turn-aware-time-dependent-routing.md) — model prohibited turns, turn penalties and FIFO travel-time functions, with tested edge-based and earliest-arrival examples.

## Spatial indexing

- [STR-packed R-tree](indexing/str-packed-rtree.md) — organise geometry bounding boxes into a packed hierarchy so queries can skip groups that cannot match.
- [Hilbert-packed R-tree](indexing/hilbert-rtree.md) — bulk-load bounding boxes in Hilbert curve order to improve spatial locality in a static hierarchy.
- [Quadtree](indexing/quadtree.md) — recursively partition a two-dimensional space; this record focuses on bucket point-region trees and distinguishes them from region and other variants.
- [k-d tree nearest-neighbour search](indexing/kd-tree-nearest-neighbour.md) — partition point data along coordinate axes and prune branches using distance lower bounds.
- [Choosing a spatial index](indexing/choosing-spatial-index.md) — match R-trees, point-region quadtrees and k-d trees to the data model, query, update pattern and coordinate metric.

## Methods and analytical foundations

Not every spatial method is a standalone algorithm. See the [methods collection](../methods/README.md) for foundational objects and modelling choices, beginning with the spatial weights matrix.

## Query processing

- [Filter-and-refine spatial join](query-processing/filter-refine-spatial-join.md) — use a spatial index to find candidate geometry pairs, then apply the exact spatial predicate.

## Spatial statistics
- [Lee's L](statistics/lees-l.md) — integrate the spatial smoothing of two variables with their lagged correlation.
- [Mantel and partial Mantel tests](statistics/mantel-tests.md) — test association between aligned distance matrices and examine the limits of the conventional permutation null.
- [Bivariate Moran's I](statistics/bivariate-morans-i.md) — relate one variable at each location to the spatial lag of a second variable, with an explicitly scoped conditional permutation baseline.

- [Ripley's K and L](statistics/ripley-k.md) — compare uncorrected pair-count summaries with the homogeneous Poisson reference across distance scales.
- [Cross-type point-pattern summaries](statistics/cross-type-point-pattern-summaries.md) — compare nearest-neighbour, K, pair-correlation and J functions between two marked event types.
- [Homogeneous Poisson and Thomas processes](statistics/poisson-and-thomas-processes.md) — simulate a complete-spatial-randomness baseline and a Gaussian Neyman–Scott cluster process.
- [Matérn cluster process](statistics/matern-cluster-process.md) — simulate a Neyman–Scott process with Poisson parents and compact-support uniform-disc offspring.
- [Log-Gaussian Cox process](statistics/log-gaussian-cox-process.md) — simulate a Cox process driven by a discretised correlated Gaussian log-intensity field.
- [Flexible spatial scan statistic](statistics/flexible-spatial-scan.md) — exhaustively score connected irregular zones inside a bounded nearest-neighbour candidate universe, with global Monte Carlo inference.
- [Elliptical spatial scan statistic](statistics/elliptical-spatial-scan.md) — scan a finite grid of centroid-centred ellipse shapes and orientations with a Poisson likelihood ratio and global Monte Carlo inference.
- [Tango's general spatial clustering test](statistics/tango-clustering-test.md) — measure global spatial concentration in population-adjusted case-proportion deviations with a distance-decay quadratic form.
- [Besag–Newell cluster detection](statistics/besag-newell.md) — find compact nearest-area neighbourhoods reaching a fixed case count and calibrate local/global significance.
- [Strauss point process](statistics/strauss-point-process.md) — model repulsive interactions with a finite-window Gibbs density and a birth-death Metropolis–Hastings teaching sampler.
- [Clark–Evans nearest-neighbour index](statistics/clark-evans.md) — compare observed mean nearest-neighbour spacing with a homogeneous Poisson reference.
- [Kernel density estimation for point patterns](statistics/point-pattern-kde.md) — estimate a fixed-bandwidth planar Gaussian intensity surface and understand bandwidth and edge effects.
- [Inhomogeneous Ripley's K](statistics/inhomogeneous-ripley-k.md) — adjust second-order pair counts for supplied spatially varying event intensities.


- [DBSCAN](statistics/dbscan.md) — identify density-connected clusters and noise in planar point data.


- [Global Moran's I](statistics/global-morans-i.md) — measure global spatial autocorrelation by comparing deviations from the mean across neighbouring units.
- [Global Moran's I permutation inference](statistics/global-morans-i-permutation.md) — calibrate the global statistic against a seeded randomization distribution with one- or two-sided alternatives.
- [Local Moran's I conditional permutation inference](statistics/local-morans-i-permutation.md) — identify local clusters and spatial outliers with conditional randomization and FDR-adjusted p-values.
- [Heteroskedasticity diagnostics](statistics/heteroskedasticity-diagnostics.md) — run Koenker studentized Breusch–Pagan and White auxiliary-regression tests after OLS.
- [Ramsey RESET](statistics/ramsey-reset.md) — test whether powers of fitted values improve an OLS specification using a nested partial F test.
- [SAR/SEM/SDM profile-likelihood intervals](statistics/spatial-mle-profile-intervals.md) — invert a concentrated Gaussian likelihood-ratio test to quantify uncertainty in the spatial lag or error parameter, including the SDM.
- [Spatial-lag Anderson–Rubin confidence sets](statistics/spatial-lag-ar-confidence-set.md) — invert candidate-value AR tests over a grid, preserving empty, disconnected and grid-limited sets.
- [Geary's C](statistics/gearys-c.md) — measure global spatial autocorrelation through squared differences between neighbouring values.
- [Spatial LM diagnostics](statistics/spatial-lm-diagnostics.md) — test classic and Bera-Yoon robust spatial lag and spatial error alternatives after an OLS null model.
- [Spatial impacts](statistics/spatial-impacts.md) — decompose SAR/SDM marginal effects into average direct, indirect and total impacts.
- [Spatial impact uncertainty](statistics/spatial-impact-uncertainty.md) — propagate a supplied joint parameter covariance into analytic delta-method or parametric Monte Carlo intervals for direct, indirect and total impacts.
- [Spatial lag 2SLS](statistics/spatial-lag-2sls.md) — instrument the endogenous spatially lagged response with exogenous covariates and their spatial lags.
- [Two-step spatial-lag GMM](statistics/spatial-lag-gmm.md) — update the 2SLS weighting matrix with a heteroskedasticity-robust instrument-moment covariance and report robust standard errors and an overidentification statistic.
- [Spatial-lag instrument diagnostics](statistics/spatial-lag-instrument-diagnostics.md) — assess excluded spatial-lag relevance with partial R-squared, classical partial F and an HC1 robust first-stage Wald F.
- [Spatial-lag Anderson–Rubin inference](statistics/spatial-lag-anderson-rubin.md) — test a candidate spatial autoregressive coefficient with classical and HC1 robust joint-exclusion tests that do not require strong instruments.
- [Spatial HAC covariance for 2SLS](statistics/spatial-2sls-hac.md) — calculate a Conley-style compact-support spatial HAC sandwich using projected IV regressors.
- [Kelejian–Prucha spatial-error GMM](statistics/kelejian-prucha-spatial-error-gmm.md) — estimate spatial error dependence from three innovation moments, then apply feasible GLS under homoskedastic innovations.
- [Heteroskedastic spatial-error GM](statistics/heteroskedastic-spatial-error-gm.md) — estimate the spatial-error coefficient from two zero-diagonal quadratic moments that accommodate unknown diagonal innovation variances.
- [Heteroskedastic SARAR GTSLS](statistics/heteroskedastic-sarar-gtsls.md) — estimate the SARAR(1,1) model in three steps: initial spatial 2SLS, heteroskedastic disturbance GM, and transformed 2SLS.
- [Joint heteroskedastic SARAR inference](statistics/heteroskedastic-sarar-joint-inference.md) — estimate the Kelejian–Prucha joint covariance for final GTSLS regression coefficients and the spatial-error parameter, including generated-residual uncertainty.
- [Spatial Durbin 2SLS](statistics/spatial-durbin-2sls.md) — estimate the endogenous spatial lag alongside spatially lagged covariates using higher-order spatial instruments.
- [Concentrated SAR/SEM maximum likelihood](statistics/spatial-maximum-likelihood.md) — estimate spatial lag and spatial error parameters by profiling the Gaussian likelihood over a conservative interval.
- [Spatial Durbin maximum likelihood](statistics/spatial-durbin-mle.md) — estimate response feedback and lagged-covariate effects by concentrated Gaussian maximum likelihood.
- [Spatial Durbin common-factor test](statistics/spatial-durbin-common-factor.md) — test whether lagged-covariate coefficients satisfy the restriction that nests the spatial-error model.
- [SARAR/SAC maximum likelihood](statistics/spatial-sarar-mle.md) — jointly estimate spatial response feedback and spatially correlated disturbances by concentrated Gaussian maximum likelihood.
- [SLX and SDEM](statistics/slx-and-sdem.md) — estimate spatially lagged covariate effects by OLS or with a spatial-error process by concentrated ML.
- [Gaussian proper-CAR regression](statistics/proper-car-gaussian-regression.md) — fit a Gaussian conditional autoregressive covariance model using an eigenvalue-constrained precision matrix.
- [Intrinsic CAR Gaussian fields](statistics/icar-gaussian-fields.md) — simulate a constrained intrinsic Gaussian field with one sum-to-zero condition per connected graph component.
- [Spatial HAC covariance for OLS](statistics/spatial-hac-covariance.md) — estimate a distance-weighted sandwich covariance for OLS under local heteroskedasticity and spatial residual dependence.
- [Local Moran's I](statistics/local-morans-i.md) — locate local clusters of similar values and spatial outliers, with conditional permutation inference.
- [Local Geary](statistics/local-geary.md) *(supplementary)* — measure local similarity and dissimilarity directly between a unit and its neighbours.
- [Getis-Ord Gi*](statistics/getis-ord-gi-star.md) — identify local concentrations of high values (hotspots) and low values (coldspots).

### Supplementary companion method

- [Global Getis-Ord G](statistics/global-getis-ord-g.md) — a supplementary global concentration statistic added to explain the source-listed local Gi* method; it is not a separate entry in the original compendium.

## Geodesy and coordinate systems

- [Coordinate transformation and CRS axis order](geodesy/crs-transformation.md) — transform point coordinates with explicit longitude/latitude and x/y conventions.
- [Geodetic, ECEF and local ENU coordinates](geodesy/ecef-enu.md) — move between ellipsoidal longitude/latitude/height, Earth-centred Cartesian coordinates and a local East-North-Up frame.

## GeoAI

- [Contrastive representation learning with NT-Xent](geoai/contrastive-info-nce.md) — derive a self-supervised objective and examine geospatial positive-pair design.

## A connected place to start

The [geometry foundations path](../learning-paths/geometry-foundations.md) connects the first four geometry lessons and continues into validity, clipping and overlay. The [Core GIS continuation path](../learning-paths/core-gis-continuation.md) adds simplification, offsetting, proximity graphs and point location; [network routing foundations](../learning-paths/network-routing-foundations.md) connects graph models with shortest-path methods. The [spatial indexing path](../learning-paths/spatial-indexing.md) connects the packed R-tree, spatial joins, quadtree and k-d tree, with a new selection guide to help match an index to a workload. The [spatial autocorrelation path](../learning-paths/global-spatial-autocorrelation.md) connects global and local Moran, Geary and Getis-Ord methods, with six interactive notebooks. The [spatial indexing path](../learning-paths/spatial-indexing.md) starts with bounding boxes and the STR-packed R-tree.

## How to read a record

Start with the practical question, then follow the explanation into the formal definition, method, guarantees, complexity, numerical issues and references. Where a runnable implementation exists, it is linked from the record.

Records may have different evidence and implementation status. Check the status and version before relying on them.

- [Ear clipping](geometry/ear-clipping.md) — triangulate one simple polygon ring, with a tested exact-predicate teaching baseline.

- [Convex decomposition](geometry/convex-decomposition.md) — compare triangulation-based merging, optimal partitioning and approximate convex decomposition.

- [Minkowski sums](geometry/minkowski-sum.md) — combine geometric sets through pointwise addition and apply the result to offsets and collision planning.

- [Medial axis](geometry/medial-axis.md) — represent a region through centres of maximal inscribed discs.
- [Straight skeleton](geometry/straight-skeleton.md) — construct the polygon skeleton from inward parallel wavefronts.

- [Convex Minkowski-sum implementation](../implementations/python/minkowski-convex/README.md) — a tested linear-time edge merge for convex rings.

- [Convex decomposition implementation](../implementations/python/convex-decomposition/README.md) — a tested greedy triangulate-and-merge teaching baseline.

- [Delaunay-filtered proximity graphs](../implementations/python/proximity-graphs/README.md) — compare sparse candidate filtering with all-pairs reference methods.









## Recurrence analysis

- [Recurrence plots and quantification](statistics/recurrence-analysis.md) — calculate fixed-threshold recurrence matrices and RR, DET, line-length, entropy and laminarity measures.


## Coastal processes

- [Coastal empirical processes and shoreline change](coastal/coastal-processes.md) — Stockdon wave runup, scoped CERC transport, Bruun recession, Dean equilibrium profile, EPR/OLS/WLR rates, six-variable CVI aggregation, empirical satellite-derived bathymetry calibration and multibeam sounding gridding.


- [Local terrain extrema](raster/local-terrain-extrema.md) — identify local raster peaks and pits with complete-neighbourhood and prominence rules.
- [Reservoir stage-storage curves](raster/reservoir-stage-storage.md) — derive DEM-based inundated area and storage over supplied water stages.

- [SCS curve-number runoff](raster/scs-curve-number-runoff.md) — estimate event direct-runoff depth and convert AMC-II curve numbers to dry/wet antecedent conditions.

- [Green-Ampt infiltration](raster/green-ampt-infiltration.md) — advance a homogeneous soil-column infiltration state through constant-intensity rainfall steps, including ponding onset.
- [Unit-hydrograph convolution](raster/unit-hydrograph-convolution.md) — route rainfall-excess depth through supplied discrete unit-hydrograph ordinates.

- [Raster viewshed and cumulative visibility](raster/viewshed.md) — calculate discrete line-of-sight visibility from one or more raster observer cells, with optional curvature/refraction correction.

- [Flood-frequency analysis](raster/flood-frequency-analysis.md) — estimate annual-maximum return levels using Weibull plotting positions and Gumbel/GEV L-moment fits.

- [Positive and negative terrain openness](raster/terrain-openness.md) — summarize radial horizon openness above and below terrain cells using explicit search and sampling parameters.

- [Channel chi, slope-area and knickpoint analysis](raster/channel-morphometry.md) — calculate chi coordinates, fit log slope-area relationships and screen longitudinal profiles for chord-residual knickpoints.

- [USLE/RUSLE soil-loss factors](raster/usle-rusle-erosion.md) — calculate the empirical R×K×LS×C×P product and a conventional slope-length/steepness factor.

- [DRASTIC and landslide susceptibility baselines](raster/susceptibility-indices.md) — calculate weighted DRASTIC ratings, categorical frequency ratios and ridge-regularized logistic susceptibility probabilities.

- [Image co-registration](remote-sensing/image-coregistration.md) — estimate global translation by phase correlation and robust affine transforms from matched point correspondences.


- [Bitemporal change detection: CVA and post-classification comparison](remote-sensing/change-vector-analysis.md) — compare aligned multispectral dates with spectral change vectors and summarize categorical transitions.

- [Empirical atmospheric, terrain and relative radiometric corrections](remote-sensing/empirical-corrections.md) — dark-object subtraction, C-correction, Minnaert, histogram matching and a pseudo-invariant-feature normalization baseline.
- [IR-MAD](remote-sensing/ir-mad.md) — weighted canonical correlation analysis for relative radiometric normalization and change screening.

- [Tasseled Cap transform](remote-sensing/tasseled-cap.md) — apply caller-supplied sensor-specific brightness/greenness/wetness coefficient matrices to multispectral pixels.

- [Thermal land-surface temperature](remote-sensing/thermal-land-surface-temperature.md) — invert Planck and single-channel radiative-transfer equations and apply a sensor-calibrated generalized split-window model.

- [Classical multispectral classification](remote-sensing/classical-classification.md) — Gaussian maximum-likelihood pixel classification and k-means++ clustering baselines.

- [RossThick-LiSparseR BRDF normalization](remote-sensing/ross-li-brdf.md) — fit kernel-driven volumetric/geometric reflectance terms and normalize multi-angle observations to a declared reference geometry.

- [Point-cloud registration and geometric comparison](geometry/point-cloud-registration.md) — point-to-point, point-to-plane and generalized ICP, voxel-Gaussian NDT, plus symmetric Chamfer/Hausdorff and threshold F-score metrics.


- [Climate analogs and velocity](remote-sensing/climate-analogs-velocity.md) — Mahalanobis climate analog ranking and gradient-derived climate velocity.

- [Mogi point-source deformation](geodesy/mogi-point-source.md) — elastic half-space surface displacement from a point source.


- [Intervening-opportunities spatial interaction](spatial-interaction/intervening-opportunities.md) — cumulative opportunity-acceptance allocation by increasing generalized cost, with explicit unallocated mass.


- [Biodiversity occurrence and grid metrics](biodiversity/range-metrics.md) — convex-hull extent of occurrence, grid-based area of occupancy, species richness and weighted endemism.


- [Fay-Herriot area-level model](statistics/fay-herriot.md) — REML small-area estimation with empirical BLUP prediction.
- [Horvitz-Thompson estimator](statistics/horvitz-thompson.md) — design-based population total and mean with pairwise inclusion-probability variance.
- [Statistical downscaling](statistics/statistical-downscaling.md) — empirical quantile mapping and additive/multiplicative delta-change baselines.


- [Iterative proportional fitting](statistics/iterative-proportional-fitting.md) — raking of nonnegative tables to supplied row and column margins.


- [HANTS harmonic time-series fitting](statistics/hants.md) — iterative Fourier fitting with directional residual rejection and gap reconstruction.


- [Soft-Impute matrix completion](statistics/soft-impute-matrix-completion.md) — low-rank matrix completion by iterative singular-value thresholding.


- [QA-based cloud and shadow masks](remote-sensing/qa-cloud-masks.md) — Landsat QA_PIXEL, Sentinel-2 SCL and supplied cloud-probability thresholding.


- [Districting compactness metrics](optimization/districting-compactness.md) — Polsby–Popper, Reock and Schwartzberg with a minimum enclosing circle.


- [K-means](statistics/k-means.md) — Lloyd assignment/update with k-means++ seeding, multiple starts and empty-cluster repair.
- [K-medoids and CLARA](statistics/k-medoids.md) — deterministic PAM BUILD/SWAP and sample-based CLARA for symmetric dissimilarities.


- [Ward hierarchical clustering](statistics/ward-clustering.md) — exact dense Ward merge objective, deterministic linkage and flat-tree cutting.


- [SKATER spatial regionalization](statistics/skater-regionalization.md) — deterministic MST construction and greedy edge pruning for connected k-regions.


- [Principal component analysis](statistics/pca.md) — covariance/correlation PCA fitting and component projection for multiband observations.


## Record linkage

- [String similarity and probabilistic record linkage](statistics/string-linkage.md) — edit distance, Jaro-Winkler, character n-gram cosine, Soundex, candidate blocking and Fellegi-Sunter log weights.

- [Numeric map classification](statistics/map-classification.md) — equal interval, quantile and Fisher-Jenks natural breaks with explicit interval assignment.

- [Broad-phase collision detection](statistics/collision-broadphase.md) — sweep-and-prune, uniform spatial hashing and a static AABB BVH.

- [Classification accuracy assessment](statistics/accuracy-assessment.md) — confusion matrices, producer/user accuracy, kappa and disagreement measures.

- [Positional accuracy and uncertainty propagation](statistics/uncertainty-propagation.md) — coordinate RMSE, Monte Carlo propagation and first-/total-order Sobol indices.

- [Geohash encoding](geodesy/geohash.md) — WGS84 geohash encode/decode and cell bounds.

## Remote sensing time series

- [Dynamic and time-weighted DTW](remote-sensing/time-series-dtw.md) — sequence alignment with optional temporal mismatch penalties.

## SAR filtering

- [Adaptive Lee speckle filter](remote-sensing/lee-speckle-filter.md) — local adaptive filtering of single-channel SAR intensity.

- [Cell-averaging CFAR](remote-sensing/sar-cfar.md) — square-window 2D detection under an exponential intensity model.

- [OBIA object features](remote-sensing/obia-object-features.md) — object geometry, spectral summaries and region adjacency from supplied segmentation labels.

- [SAR CA-CFAR and OS-CFAR](remote-sensing/sar-cfar.md) — local clutter thresholding with cell-averaging and ordered-statistics reference detectors.

- [Lee local-statistics speckle filter](remote-sensing/lee-speckle-filter.md) — adaptive local-mean shrinkage under an explicit noise-variance model, with a tested NumPy baseline.

- [Open Location Code (Plus Codes)](geodesy/open-location-code.md): full-code WGS84 encoding/decoding and decoded cell bounds; short-code recovery and geocoding remain out of scope.

- [Fractional-cover regression tree](remote-sensing/fractional-cover-regression-tree.md): deterministic CART baseline for field-labelled fractional-cover estimation.

- [Brown-Conrady lens distortion](photogrammetry/brown-conrady-distortion.md): radial/tangential camera-plane distortion and Newton inverse.

- [Progressive morphological ground filtering](photogrammetry/progressive-morphological-ground-filter.md): rasterised progressive opening and height-threshold baseline for XYZ point clouds.

- [RANSAC plane fitting](photogrammetry/ransac-plane-fitting.md): robust single-plane estimation with SVD consensus refinement.

- [CHM watershed crown segmentation](photogrammetry/chm-watershed-crown-segmentation.md): local-maximum markers and watershed segmentation on a canopy height model.

- [Marching cubes](geometry/marching-cubes.md): validated Lewiner isosurface extraction from a 3-D scalar field.

- [Contextual thermal-hotspot screening](remote-sensing/contextual-thermal-hotspot.md): local-median/MAD anomaly baseline with an absolute temperature threshold.

- [Point-cloud voxelization](photogrammetry/point-cloud-voxelization.md): sparse XYZ voxel indexing and per-cell summaries.

- [Vecchia Gaussian-process approximation](geostatistics/vecchia-approximation.md): nearest-predecessor Gaussian likelihood factorisation with an exact all-neighbour check.

- [Knox space-time interaction test](geostatistics/knox-space-time-test.md): pair-count statistic with a plus-one temporal-label permutation p-value.


## Domain modeling

- [Spatial cellular automata](domain-modeling/cellular-automata.md) — synchronous B/S rules, site-percolation crossing, a stochastic forest-fire automaton and a bounded Schelling-style relocation example.


- [Spatial random graphs](domain-modeling/spatial-random-graphs.md) — degree- and distance-weighted preferential attachment plus Watts–Strogatz small-world rewiring.


- [Network SIR simulation](domain-modeling/network-sir.md) — discrete-time transmission and recovery on a static undirected contact graph, with explicit synchronous update semantics.


- [Markov land-change simulation](domain-modeling/markov-land-change.md) — estimate categorical transition probabilities from aligned rasters and simulate independent per-cell transitions.


- [Drought and vegetation-condition indicators](domain-modeling/drought-condition-indices.md) — distinguish SPI, VCI, TCI and VHI from SPEI, PDSI and growing degree days.


- [Categorical landscape patch metrics](biodiversity/landscape-patch-metrics.md) — connected patches, largest-patch index, internal edge density and Shannon class diversity.


- [Random-hyperplane locality-sensitive hashing](indexing/locality-sensitive-hashing.md) — multi-table approximate cosine search with exact candidate reranking.

- [Greedy VRPTW insertion](optimization/vrptw-greedy-insertion.md) — construct capacity-feasible depot routes with service windows, waiting and explicit unserved customers.

### 3D geometry

- [Möller–Trumbore ray/triangle intersection](geometry/ray-triangle-intersection.md) — barycentric ray hit testing with explicit tolerance, interval and back-face policies.
