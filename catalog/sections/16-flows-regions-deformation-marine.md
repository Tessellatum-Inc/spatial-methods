# Section 16 — Additions: flows, regions, deformation, marine, biodiversity, humanitarian

- **Original source section:** 16
- **Source pages:** 33–34
- **Source transcription:** [pages 31–35](../../source-inventory/pages-31-35.md)
- **Review state:** source entries extracted into this index; not every entry independently verified
- **Current canonical records:** [Constrained gravity-flow models](../../algorithms/spatial-interaction/gravity-flow-models.md), including the four constraint forms and an exponential-cost entropy-maximising IPF baseline; [classification breaks](../../algorithms/cartography/classification-breaks.md), with six tested one-dimensional methods including exact dynamic-programming ckmeans; other flow, regionalisation, movement, geophysical, marine, biodiversity and humanitarian entries remain to be verified

This section groups applied methods across spatial interaction, functional regions, classification, movement, geophysics, marine systems, biodiversity and humanitarian analysis.

## Spatial interaction models (advanced)

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Entropy-maximizing models (Wilson), production, attraction and doubly constrained forms, Poisson and negative binomial gravity models | Spatial interaction models / statistical specifications | 33 | Partially implemented: unconstrained, production-constrained, attraction-constrained and doubly constrained flows plus an exponential-cost entropy-maximising IPF variant; PPML regression already exists. Negative-binomial estimation and calibrated impedance/parameter estimation remain open |
| Competing destinations, intervening opportunities variants, spatial autocorrelation in flows (Griffith eigenvector filtering, LeSage-Pace origin-destination models) | Interaction models / flow autocorrelation and econometric methods | 33 | Partial — a cumulative exponential intervening-opportunities allocation baseline is implemented with tied-cost handling and explicit unallocated mass; competing-destinations specifications and Griffith/LeSage–Pace flow-autocorrelation models remain open |
| Flow clustering and flow mapping: flow-based community detection, flow KDE, OD flow hotspot detection | Flow clustering / density estimation / hotspot methods | 33 | Partial — DBSCAN clustering in origin-destination feature space, line-integrated Gaussian flow KDE and grid-cell hotspot extraction are implemented and tested; network-constrained community detection and inferential hotspot significance remain open |

## Functional regions and urban boundaries

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Functional region delineation from flows: Intramax, CURDS, Louvain and Leiden on flow networks, commuting zone definition | Functional regionalisation algorithms / network clustering | 33 | Partial — reciprocal OD-flow weighted Louvain communities with optional contiguity-constrained edges are implemented and tested; Intramax, CURDS, Leiden and commuting-zone calibration remain open |
| Urban boundary delineation: city clustering algorithm (CCA), DBSCAN on building density, percolation-based clustering, natural cities via head/tail breaks | Urban boundary detection / clustering and classification methods | 33 | Partial — building-point DBSCAN, density-grid aggregation, connected density-component extraction and recursive head/tail natural-city thresholds are implemented and tested; full CCA, stochastic percolation and boundary calibration remain open |
| Home and work location inference from traces, activity space delineation, co-location and contact pattern extraction | Mobility inference / activity-space and contact analysis | 33 | Partial — sequential staypoint detection, time-window home/work cluster inference and radius-of-gyration/convex-hull activity-space summaries are implemented and tested; co-location/contact extraction and robust longitudinal home/work validation remain open |

## Classification schemes and aggregation

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Head/tail breaks, maximum breaks, geometric interval, standard deviation, box plot, pretty breaks, Dalenius-Hodges, optimal 1D k-means (ckmeans) | Classification and binning methods | 33 | Partially implemented: head/tail, geometric interval, standard deviation, box plot, Dalenius–Hodges and exact 1D ckmeans are tested; “maximum breaks” and “pretty breaks” remain unresolved names |
| Zone design and aggregation: AMOEBA, automated zoning procedures, scale-effect analysis, variance by aggregation level | Spatial regionalisation / aggregation and scale analysis | 33 | Not checked — intake only |

## Cost surfaces and movement through terrain

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Anisotropic cost surfaces (Tobler hiking function, Naismith, Langmuir), path distance with vertical factors, backlink rasters | Cost-surface construction / terrain travel models | 33 | Partially implemented: directional raster travel-time Dijkstra with Tobler, Naismith and per-edge Langmuir models; vertical-factor variants, backlink rasters, turn penalties and continuous path-distance solvers remain open |
| Least-cost corridors, cost-weighted distance with turning penalties, energy-expenditure models for walking and loaded travel | Corridor analysis / movement cost models | 33 | Partial — additive-tolerance raster least-cost corridors now implemented and tested; turn penalties and calibrated energy-expenditure models remain open |

## SAR geometry, InSAR time series and crustal deformation

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| SAR geometry: radiometric terrain correction (RTC), geocoding, multilooking, calibration, enhanced spectral diversity (ESD) coregistration | SAR geometry and preprocessing workflows | 34 | Not checked — intake only |
| Phase corrections: atmospheric phase screen estimation, GACOS and ERA5-based tropospheric correction, orbital ramp removal, DEM error correction | Interferometric phase correction methods | 34 | Not checked — intake only |
| Time-series InSAR workflows: SBAS variants, NSBAS, MintPy-style and LiCSBAS-style pipelines, GNSS-InSAR integration for 3D velocity decomposition | InSAR time-series processing / geodetic data integration | 34 | Not checked — intake only |
| Source modeling: Okada dislocation, Mogi source, finite fault slip inversion, elastic and viscoelastic deformation models | Geophysical source and deformation models | 34 | Partial — tested Mogi point-source elastic half-space displacement is implemented; Okada finite dislocations, finite-fault inversion and viscoelastic models remain open |

## Marine and fisheries spatial analysis

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| CPUE standardization (GAM and spatiotemporal models such as VAST-style vector autoregressive models), spatial stock assessment, fishing effort allocation | Fisheries statistical models / stock assessment / allocation | 34 | Partial — effort-offset Poisson and NB2 log-linear standardization models with reference-condition CPUE predictions are implemented and tested; GAM smooths, VAST spatiotemporal random fields, stock assessment and effort-allocation optimization remain open |
| Larval dispersal and ocean connectivity: Lagrangian tools (Parcels, OpenDrift), connectivity matrices, marine protected area network design | Particle tracking / connectivity analysis / reserve design | 34 | Partial — steady-field RK4 particle advection and weighted source-to-destination connectivity matrices are implemented and tested; time-varying currents, diffusion, vertical motion and reserve-design optimisation remain open |
| Marine spatial planning with Marxan and Zonation, benthic habitat mapping from multibeam backscatter | Spatial planning software / habitat mapping workflows | 34 | Not checked — intake only |

## Biodiversity assessment and conservation planning

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| IUCN range metrics: extent of occurrence (convex hull, alpha hull), area of occupancy, range fragmentation indices | Range metrics / spatial biodiversity measures | 34 | Partial — planar convex-hull EOO and aligned-grid AOO are implemented; alpha hulls and range-fragmentation indices remain open |
| Essential biodiversity variables, protected area gap analysis, key biodiversity area delineation, species richness and endemism indices (weighted endemism, phylogenetic diversity) | Biodiversity indicators / conservation planning and assessment | 34 | Partial — cellwise species richness and weighted endemism are implemented from binary presence matrices; phylogenetic diversity, essential-variable frameworks, protected-area gap analysis and KBA delineation remain open |
| Wildlife crime and anti-poaching: green security games, learned patrol planning, risk maps from patrol data | Security games / patrol optimisation / risk mapping | 34 | Not checked — intake only |

## Climate analogs, velocity and refugia

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Climate analogs and novel climates (Mahalanobis distance based), climate velocity, climate-change refugia, bioclimatic envelope shifts | Climate similarity and velocity metrics / ecological modelling | 34 | Partial — global-covariance Mahalanobis analog ranking and gradient-based climate-velocity vectors are implemented and tested; climate refugia and bioclimatic envelope workflows remain open |
| Land degradation analysis: RESTREND, NPP residual methods, desertification indicators, soil salinity mapping | Land degradation assessment / remote-sensing indicators | 34 | Partial — per-pixel RESTREND rainfall-response regression and residual-trend diagnostics are implemented and tested; NPP residual variants, soil salinity retrieval and calibrated desertification indicators remain open |

## Humanitarian, food security and conflict

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Relief facility location, humanitarian logistics routing, displacement camp mapping, tent and structure counting from imagery | Humanitarian location and routing / settlement mapping | 34 | Not checked — intake only |
| Food security: IPC-style analysis, FEWS NET-style outlooks, livelihood zone delineation, market integration and price transmission models | Food-security analysis / early-warning and regional economic methods | 34 | Partial — a tested two-market Engle–Granger-style long-run relation and error-correction price-transmission model is implemented; IPC/FEWS NET workflows, livelihood-zone delineation and multi-market spatial equilibrium remain open |
| Conflict analysis: ACLED-style event analysis, conflict diffusion models, forecasting systems such as ViEWS, spatial event clustering and early warning indicators | Event analysis / diffusion and forecasting models | 34 | Not checked — intake only |

## Decisions for the next pass

1. Define the spatial unit and temporal interval for flow and regionalisation methods.
2. Distinguish interaction models from observed flow datasets and from network clustering.
3. Record uncertainty and sensor limitations in deformation and marine applications.
4. Use conservation and humanitarian examples with transparent data provenance and careful privacy review.
5. Treat named products and tools as implementations or data sources, not interchangeable with the underlying method.


### Classification implementation update

Six classification methods now have a NumPy package, tests and a canonical lesson. The ckmeans dynamic program is checked against exhaustive partition enumeration on small samples. The source's “maximum breaks” and “pretty breaks” labels remain open pending identity verification; they are not guessed to mean Jenks or ckmeans.


### Spatial-interaction implementation update

The regional-dynamics package now distinguishes aggregate flow allocation from regression estimation: unconstrained, singly constrained and doubly constrained gravity flows are implemented, and the doubly constrained form is balanced by iterative proportional fitting. The entropy-maximising wrapper uses an explicit exponential generalized-cost deterrence term. PPML remains a separate count-regression method; negative-binomial estimation, competing destinations, intervening opportunities and flow-network clustering remain open.


### Least-cost corridor implementation update

A raster-graph corridor now combines source and destination Dijkstra surfaces and retains cells whose through-cost is within an additive tolerance of the optimum. Tests include an exhaustive simple-path oracle on a small grid. This is not a probabilistic corridor, a directional travel-time corridor or a continuous-surface solver.


### Climate analogs and velocity implementation update

The new `climate-velocity` package ranks historical samples as multivariate Mahalanobis analogs of future climate vectors and estimates local climate velocity from temporal change and spatial gradients. The analog metric uses a declared reference covariance with ridge regularisation; the velocity vector follows the isocline-displacement equation. These are numerical components, not a complete climate-refugia or species-range model.


### Mogi point-source deformation implementation update

A tested Mogi elastic half-space point-source model now returns east, north and vertical surface displacement from source depth, volume change and Poisson ratio. It is an analytical point-source baseline; finite rectangular dislocations, layered or topographic media, finite-fault inversion and viscoelastic time dependence remain open.


### Intervening-opportunities implementation update

The regional-dynamics package now includes a cumulative exponential intervening-opportunities allocation model. Destinations are ordered by generalized cost; tied-cost groups share the acceptance probability in proportion to their opportunity mass. The residual probability is returned as unallocated flow, preserving origin totals without forcing all trips to be assigned. The model is a transparent Stouffer-style baseline; competing-destinations formulations and spatial filtering of OD flows remain separate open methods.


### Biodiversity range metrics implementation update

A new `biodiversity-metrics` package provides planar convex-hull extent of occurrence, aligned-grid area of occupancy, cellwise species richness and inverse-range-size weighted endemism. Analytic geometry and direct matrix oracles cover the numerical kernels. These do not constitute a complete IUCN assessment: alpha hulls, range fragmentation, sampling-bias correction, phylogenetic diversity and key-biodiversity-area criteria remain outstanding.


### Lagrangian particle advection and connectivity implementation update

A steady two-dimensional velocity-field particle integrator now uses fourth-order Runge–Kutta interpolation on a rectilinear grid. A companion connectivity aggregator converts released particle source regions and final destination regions into weighted counts and row-normalized probabilities, retaining unassigned particles separately. This is a deterministic advection baseline, not a full ocean particle framework: time-varying currents, diffusion, vertical motion, beaching, decay and uncertainty remain open.


### Flow clustering, line KDE and hotspot implementation update

The flow-analysis package now clusters OD records using DBSCAN over separately scaled origin and destination coordinates, estimates a line-integrated Gaussian kernel density surface using Gauss–Legendre quadrature along each OD segment, and extracts local grid maxima above a caller-selected quantile. These are exploratory spatial-analysis baselines: they do not implement network-constrained flow communities, inferential hotspot significance, edge effects, adaptive bandwidth selection or uncertainty estimation.


### Functional regions from origin-destination flows

The flow-analysis package converts a directed OD matrix into an undirected weighted graph by summing reciprocal movements, then applies the repository's tested Louvain modularity implementation. An optional zone-neighbour adjacency constrains graph edges. This is a flow-network community baseline, not Intramax, CURDS, Leiden or an empirically calibrated commuting-zone workflow.


### Urban boundary and natural-city baselines

The urban-boundaries package provides DBSCAN clustering of building centroids, point-to-grid building density aggregation, connected-component extraction above a density threshold, and a recursive head/tail threshold for natural-city candidate masks. These are exploratory delineation methods: they do not replace full city-clustering algorithm calibration, stochastic percolation models, building-footprint quality control or administrative boundary validation.


### Staypoints, home/work inference and activity spaces

A trace-processing baseline now detects dwell episodes by a maximum-radius/time-duration rule, infers candidate home and work clusters from night/day staypoints using DBSCAN and dwell-weighted centroids, and summarizes activity spaces by radius of gyration and convex-hull area. It does not infer social contacts, model irregular sampling or GPS uncertainty, or validate home/work roles over long periods; these outputs are candidates, not ground truth.


### CPUE standardization baseline

An effort-offset log-linear catch-rate model is now available under Poisson and NB2 negative-binomial likelihoods. It reports fitted catch, standardized predictions at mean covariates and unit effort, dispersion and coefficient diagnostics. It is not a GAM or VAST reproduction: nonlinear smooths, spatial/temporal random fields, zero inflation, stock dynamics and fishing-effort optimization remain open.


### Marine reserve-selection baseline

A Marxan-style simulated-annealing selector now minimizes zone acquisition cost, squared feature-target shortfall penalties and selected/unselected boundary length. It accepts an explicit zone-feature matrix, costs, targets and adjacency boundary lengths. This is a compact educational heuristic, not the full Marxan solver or Zonation's iterative removal algorithm; feature quality, costs, targets and connectivity constraints remain analyst-supplied. Benthic habitat classification from calibrated multibeam backscatter remains open.


### RESTREND land-degradation screening

A per-pixel RESTREND baseline now fits NDVI against precipitation, calculates rainfall-adjusted residuals and estimates the residual temporal trend with slope, R-squared and p-value. Pixels with insufficient valid paired observations are left as NoData. This is a screening statistic, not a causal degradation diagnosis; precipitation-product bias, land-cover change, irrigation, fire, sensor harmonization and NPP/soil-salinity variants remain open.


### Two-market price transmission

A two-stage error-correction baseline estimates a long-run price relation between two markets, then models short-run target-market price changes as a function of lagged disequilibrium and contemporaneous source-market changes. It reports the error-correction speed and standard errors. This is a pairwise econometric teaching model, not a complete food-security early-warning system or multi-market spatial equilibrium model.
