# Section 22 atomic completion register

**Purpose:** convert every grouped entry in source pages 45–47 (original compendium section 22) into individually auditable work items. This is a tracking and acceptance artifact, not a claim that the listed methods have been verified or implemented.

**Source:** [faithful transcription, pages 41–47](../source-inventory/pages-41-47.md); source section 22 begins on page 45 and continues through page 47. The source itself warns that names are memory-based and require verification. Preserve that qualification until primary references and exact method identities are checked.

## Status vocabulary

- **Implemented (scoped):** a linked implementation exists, with tests; its stated limitations still apply.
- **Partial:** related work exists but does not satisfy the full source item.
- **Open:** no qualifying item-level verification/implementation is recorded in the section register.
- **Verify:** source identity, mathematical conditions, provenance, or exact variant must be checked before implementation.
- **Not applicable:** use only with a documented reason; never use to hide an unworked item.

A method is complete only when its canonical record names the exact variant and assumptions, cites authoritative sources, documents input/output and failure semantics, has independent analytical or differential tests (including edge cases), has an executable implementation where appropriate, and is linked from the catalogue. Domain workflows and software platforms must not be mislabeled as algorithms.

## Item-level register

### Inference engines and optimisation (source page 45)

| ID | Atomic item | Kind | Current evidence / status | Acceptance work |
|---|---|---|---|---|
| S22-INF-01 | Gibbs sampling for CAR models | Bayesian sampler | Proper Gaussian CAR fixed-hyperparameter Gibbs sampler exists; **Partial** | Verify full conditionals and precision parameterisation against independent reference; document scan order and convergence diagnostics |
| S22-INF-02 | Metropolis-within-Gibbs for CAR models | Bayesian sampler | **Open** | Define target and proposal; test detailed balance and posterior moments |
| S22-INF-03 | Metropolis-within-Gibbs for SAR models | Bayesian sampler | **Open** | Specify SAR likelihood/Jacobian and parameter constraints; compare with trusted implementation |
| S22-INF-04 | Slice sampling | Bayesian sampler | Componentwise stepping-out slice sampler exists; **Partial** | Verify shrinkage/stepping-out invariance, bounded-support behaviour and multimodal examples |
| S22-INF-05 | Sequential Monte Carlo | Bayesian sampler | **Open** | Specify tempering/resampling variant, ESS and evidence estimator; test against conjugate targets |
| S22-INF-06 | Pseudo-marginal methods | Bayesian sampler | **Open** | Specify unbiased nonnegative likelihood estimator and auxiliary-variable MH kernel; test invariance |
| S22-INF-07 | Laplace approximation | Approximate inference | Numerical mode/covariance/log-evidence baseline exists; **Partial** | Verify Hessian sign/conditioning, coordinate scaling and evidence against analytic Gaussian and non-Gaussian references |
| S22-INF-08 | Expectation propagation | Approximate inference | **Open** | Define factor/site updates and damping; test Gaussian exactness and convergence failure reporting |
| S22-INF-09 | Variational Bayes | Approximate inference | **Open** | Select explicit factorisation/objective; test ELBO monotonicity where guaranteed and posterior-moment error |
| S22-INF-10 | EM for spatial mixtures | Optimisation/inference | **Open** | Specify mixture likelihood and spatial dependence; test likelihood behaviour, label switching and degeneracy |
| S22-INF-11 | L-BFGS for GP hyperparameters | Optimiser | **Open** | Implement bounded parameter transforms and stable log marginal likelihood; gradient-check finite differences |
| S22-INF-12 | Adam for GP hyperparameters | Optimiser | **Open** | Specify objective/gradient and stopping; test reproducibility and convergence diagnostics |
| S22-INF-13 | Natural gradient for GP hyperparameters | Optimiser | **Open** | Define metric/Fisher approximation and damping; verify coordinate behaviour and positive-definite steps |
| S22-INF-14 | Stan | Probabilistic programming platform | Platform named, not an algorithm; **Verify** | Document supported spatial model patterns, code example, version and reproducibility; do not duplicate Stan internals |
| S22-INF-15 | NIMBLE | Probabilistic programming platform | Platform named, not an algorithm; **Verify** | Document spatial model and custom sampler workflow with versioned example |
| S22-INF-16 | PyMC | Probabilistic programming platform | Platform named, not an algorithm; **Verify** | Document spatial model and inference configuration with versioned example |
| S22-INF-17 | INLA-style nested approximations | Approximation framework | **Verify** | Distinguish INLA methodology from software; document latent Gaussian model assumptions and supported likelihoods |

### Covariance functions and basis expansions (source pages 45–46)

| ID | Atomic item | Kind | Current evidence / status | Acceptance work |
|---|---|---|---|---|
| S22-COV-01 | Matérn covariance | Covariance | Related stationary covariance record; **Partial** | Verify parameterisation, smoothness, dimension and limiting cases; test PSD matrices |
| S22-COV-02 | Exponential covariance | Covariance | Related stationary record; **Partial** | Verify as Matérn special case and test anisotropic/scaled distances |
| S22-COV-03 | Spherical covariance | Covariance | Related stationary record; **Partial** | Verify compact support and dimension restrictions; PSD tests |
| S22-COV-04 | Gaussian covariance | Covariance | Related stationary record; **Partial** | Verify parameter convention and PSD construction |
| S22-COV-05 | Cauchy covariance | Covariance | Related stationary record; **Partial** | Verify admissible parameter constraints and PSD |
| S22-COV-06 | Powered-exponential covariance | Covariance | Related stationary record; **Partial** | Verify exponent range and limiting cases |
| S22-COV-07 | Wendland compactly supported covariance | Covariance | **Open** | Specify smoothness/dimension family and admissible polynomial; PSD tests |
| S22-COV-08 | Valid covariance on the sphere (Gneiting/Schoenberg class) | Spherical covariance theory | Spherical Legendre-coefficient construction exists; **Partial** | Verify coefficient conditions, normalisation and convergence; distinguish isotropic scalar fields |
| S22-COV-09 | Valid covariance on networks (Anderes-style) | Network covariance theory | **Open** | Identify exact cited construction and graph/network assumptions; do not substitute graph-Laplacian covariance |
| S22-COV-10 | Graph kernels | Graph covariance | Graph-Laplacian spectral covariance exists; **Partial** | Document graph class, nullspace/connectedness, PSD conditions and why it is not directed-flow stationarity |
| S22-COV-11 | Failure of geodesic-distance Gaussian kernels | Validity diagnostic | **Open** | Construct counterexample and state metric/space conditions; cite proof/source |
| S22-COV-12 | Cressie–Huang nonseparable space-time covariance | Space-time covariance | One Gneiting-class implementation exists; **Partial** | Verify exact family and admissible parameter constraints; implement/compare selected Cressie–Huang model |
| S22-COV-13 | Gneiting nonseparable space-time covariance | Space-time covariance | One Gneiting-class implementation exists; **Partial** | Verify theorem conditions and numerical PSD tests over space-time designs |
| S22-COV-14 | Product-sum space-time covariance | Space-time covariance | **Open** | Define component covariance and interaction constraints; PSD tests |
| S22-COV-15 | Metric space-time covariance models | Space-time covariance | **Open** | Define metric construction and valid parameter range; counterexample tests for invalid choices |
| S22-BAS-01 | Thin-plate spline basis | Basis / smoother | Tested component exists; **Partial** | Verify polynomial nullspace, side constraints and coordinate scaling |
| S22-BAS-02 | B-spline basis | Basis / smoother | B-spline curves component exists; **Partial** | Verify knot multiplicity, partition of unity and boundary behaviour |
| S22-BAS-03 | Tensor-product spline basis | Basis / smoother | **Open** | Implement separable basis construction and test indexing/partition properties |
| S22-BAS-04 | Wavelet basis | Multiscale basis | **Open** | Specify wavelet family, boundary extension and 2-D/irregular-grid scope |
| S22-BAS-05 | Slepian functions | Concentration basis | **Open** | Define region/bandlimit eigenproblem; verify orthogonality and concentration |
| S22-BAS-06 | Zernike basis | Orthogonal disk basis | **Open** | Define radial polynomial convention and disk normalisation; test orthogonality |
| S22-BAS-07 | Radial basis functions | Basis / interpolator | **Open** | Separate RBF families and polynomial augmentation; test conditioning |
| S22-BAS-08 | Multiresolution Haar basis | Wavelet basis | **Open** | Define dyadic grid and boundary policy; test orthonormality/reconstruction |
| S22-BAS-09 | Fixed-rank kriging (FRK) basis functions | Low-rank spatial model | **Open** | Verify basis construction, covariance approximation and identifiability |
| S22-BAS-10 | Moran eigenvector basis | Spatial filtering basis | Tested Moran eigenvector filtering exists; **Partial** | Verify weights/centering/eigenspace conventions and residual confounding caveats |

### Spherical and Riemannian statistics (source page 46)

| ID | Atomic item | Kind | Current evidence / status | Acceptance work |
|---|---|---|---|---|
| S22-SPH-01 | Fréchet/Karcher mean on sphere | Intrinsic statistic | Tested implementation exists; **Partial** | Verify objective, cut-locus handling, initialisation and non-unique minima |
| S22-SPH-02 | Spherical k-means | Clustering | Tested implementation exists; **Partial** | Verify objective/normalisation, empty clusters and antipodal inputs |
| S22-SPH-03 | von Mises–Fisher density | Directional distribution | Tested 3-D density exists; **Partial** | Verify normalising constant, stable large-concentration evaluation and dimensions |
| S22-SPH-04 | von Mises–Fisher mixture EM | Mixture estimation | Tested finite-mixture EM exists; **Partial** | Verify responsibilities, concentration estimation, degeneracy and label switching |
| S22-SPH-05 | Spherical kernel density estimation | Density estimation | Weighted vMF KDE exists; **Partial** | Verify bandwidth/weight normalisation and leave-one-out diagnostics |
| S22-SPH-06 | Spherical spline interpolation | Interpolation | **Open** | Select intrinsic/extrinsic formulation and validate interpolation conditions |
| S22-SPH-07 | Geodesic regression | Regression | **Open** | Define response manifold, loss and optimiser; test known geodesic trajectories |
| S22-SPH-08 | Spherical Gaussian processes | Probabilistic model | Isotropic spherical covariance exists; **Partial** | Implement conditioning/prediction and uncertainty; test against finite Gaussian reference |

### Ellipsoidal geodesy (source page 46)

| ID | Atomic item | Kind | Current evidence / status | Acceptance work |
|---|---|---|---|---|
| S22-GEO-01 | Karney direct geodesic | Geodesic algorithm | PROJ/Karney-backed tested operation; **Partial** | Record library/version and compare independent known fixtures including near-antipodal cases |
| S22-GEO-02 | Karney inverse geodesic | Geodesic algorithm | PROJ/Karney-backed tested operation; **Partial** | Verify azimuth conventions, coincident points and near-antipodal fixtures |
| S22-GEO-03 | Karney ellipsoidal polygon area | Geodesic geometry | Tested signed/unsigned area; **Partial** | Verify orientation, dateline, pole-enclosing and large-polygon conventions |
| S22-GEO-04 | Geodesic point buffers | Geodesic geometry | Sampled point buffers tested; **Partial** | Quantify approximation error and segment resolution; do not imply exact buffer topology |
| S22-GEO-05 | Azimuthal-equidistant buffers | Projection-based geometry | **Open** | Specify centre/ellipsoid and distortion/extent limitations; compare with geodesic distances |
| S22-GEO-06 | Antipodal and dateline handling | Edge-case policy | Some handling in geodesic package; **Partial** | Add independent adversarial fixtures for wrap, poles, antipodes and ring closure |
| S22-GEO-07 | Geodesic polygon topology operations | Geometry operations | **Open** | Define split/wrap/topology semantics; validate against trusted geodesic library |

### Sensor artifact correction and restoration (source page 46)

| ID | Atomic item | Kind | Status | Acceptance work |
|---|---|---|---|---|
| S22-SEN-01 | Fourier destriping | Image restoration | Partial | A user-guided conjugate-symmetric Gaussian/ideal notch-reject filter and periodic destriping helper now attenuate specified stripe frequencies; synthetic vertical-stripe recovery, conjugate symmetry and DC-preservation tests are included: [package](../implementations/python/fourier-filtering/README.md), [verification](../catalog/verification/fourier-destriping.md). Automatic peak detection, real-scene signal-preservation review, NoData-aware processing and wavelet methods remain open. |
| S22-SEN-02 | Wavelet destriping | Image restoration | Open | Specify wavelet/threshold strategy; compare against clean synthetic scenes |
| S22-SEN-03 | Sensor noise estimation | Estimation | Partial | A scoped Haar diagonal-detail MAD estimator now estimates per-band additive white-Gaussian sigma; seeded synthetic tests cover known noise levels, smooth trends, band separation, odd dimensions and invalid inputs. It does not model correlated, periodic, signal-dependent or full physical sensor noise: [lesson](../algorithms/remote-sensing/sensor-noise-estimation.md), [package](../implementations/python/sensor-noise-estimation/README.md), [verification](../catalog/verification/sensor-noise-estimation.md). Broader noise models and independent source-variant review remain open. |
| S22-SEN-04 | Modulation transfer function compensation | Image restoration | Open | Define sensor MTF/deconvolution regularisation; stability and ringing tests |
| S22-SEN-05 | Image deblurring | Inverse problem | Open | Specify blur kernel and regulariser; quantify reconstruction and noise amplification |
| S22-SEN-06 | Jitter correction | Geometric correction | Open | Define platform/sensor motion model; synthetic displacement recovery |
| S22-SEN-07 | Line-scan geometric model | Sensor geometry | Open | Derive time/trajectory/attitude mapping; validate simulated scan geometry |
| S22-SEN-08 | Rolling-shutter geometric model | Sensor geometry | Open | Model row-time and platform motion; validate synthetic moving-camera cases |
| S22-SEN-09 | Attitude processing | Calibration workflow | Open | Specify frame conventions, interpolation and uncertainty |
| S22-SEN-10 | Star-tracker processing | Sensor processing | Open | Identify centroid/catalogue/attitude pipeline and exact source |
| S22-SEN-11 | Boresight refinement | Calibration | Open | Define joint calibration observations and parameter estimation; independent residual tests |
| S22-SEN-12 | SAR-guided cloud removal | Multisensor restoration | Open | Specify fusion assumptions and preserve optical/SAR provenance |
| S22-SEN-13 | SAR-optical fusion | Multisensor fusion | Open | Separate pixel-, feature- and decision-level fusion; quantitative validation |
| S22-SEN-14 | Hyperspectral destriping | Image restoration | Open | Model band-dependent artifacts; spectral-shape preservation tests |

### Road and roadway asset mapping (source page 46)

| ID | Atomic item | Kind | Status | Acceptance work |
|---|---|---|---|---|
| S22-ROAD-01 | Traffic-sign detection from street imagery | Detection | Open | Define classes, georeferencing and confidence; spatially separated validation |
| S22-ROAD-02 | Pole detection from imagery/point clouds | Detection | Open | Define pole geometry and occlusion handling; precision/recall and positional error |
| S22-ROAD-03 | Lane-marking detection | Detection | Open | Define marking taxonomy and geometry; occlusion/wear tests |
| S22-ROAD-04 | Sidewalk inventory | Asset inventory | Open | Define completeness, topology and positional accuracy |
| S22-ROAD-05 | Curb-ramp inventory | Asset inventory | Open | Define accessibility attributes and positional accuracy; field-check protocol |
| S22-ROAD-06 | Pavement distress detection | Condition assessment | Open | Define distress taxonomy/severity; spatially independent validation |
| S22-ROAD-07 | Road roughness from accelerometers / IRI estimation | Estimation | Open | Specify calibration, speed dependence and reference profilometer comparison |
| S22-ROAD-08 | Crowdsourced street-imagery pipeline | Workflow | Open | Document acquisition, coverage, privacy, temporal freshness and QA |
| S22-ROAD-09 | Mapillary-style imagery processing | Platform workflow | Open | Treat as workflow/platform integration, not a single algorithm; version and licence checks |
| S22-ROAD-10 | OSM feature conflation | Data integration | Open | Define matching, conflict resolution and provenance; precision/recall against adjudicated pairs |

### Utilities, rail and power networks (source page 46)

| ID | Atomic item | Kind | Status | Acceptance work |
|---|---|---|---|---|
| S22-UTIL-01 | EPANET hydraulic simulation | Network simulation | Open | Document hydraulic equations, solver assumptions and validation dataset; software integration distinct from algorithm |
| S22-UTIL-02 | Water-network leak detection | Anomaly detection | Open | Define pressure/flow signals, detection latency and false-alarm metrics |
| S22-UTIL-03 | District-metered-area sectorisation | Network partitioning | Open | Define constraints/objective and hydraulic feasibility checks |
| S22-UTIL-04 | Water-loss analysis | Accounting/estimation | Open | Define water balance, uncertainty and reporting period |
| S22-UTIL-05 | Geographic power-flow analysis | Network simulation | Open | Define electrical model and spatial coupling; compare with trusted solver |
| S22-UTIL-06 | Power outage detection | Event detection | Open | Define data sources, outage labels and detection latency |
| S22-UTIL-07 | Power restoration routing | Routing/optimisation | Open | Include crew skills, precedence, travel time and network constraints |
| S22-UTIL-08 | LiDAR vegetation encroachment along power lines | Clearance analysis | Open | Define conductor corridor, point classification and clearance uncertainty |
| S22-UTIL-09 | Conductor sag estimation | Engineering model | Open | Define catenary/temperature/loading assumptions and survey inputs |
| S22-UTIL-10 | Conductor clearance analysis | Safety/geometry | Open | Define statutory clearance reference and uncertainty margin |
| S22-UTIL-11 | Power-pole detection | Detection | Open | Define sensor modality, asset taxonomy and positional validation |
| S22-UTIL-12 | Rail-track geometry from LiDAR | Survey/estimation | Open | Define rail-head extraction, alignment and gauge/cant accuracy |
| S22-UTIL-13 | Rail asset inventories | Asset inventory | Open | Define asset schema, completeness and update protocol |
| S22-UTIL-14 | Rail vegetation encroachment | Clearance analysis | Open | Define corridor and clearance criteria; validate against surveyed cases |

### Engineering geodesy and structural monitoring (source page 46)

| ID | Atomic item | Kind | Status | Acceptance work |
|---|---|---|---|---|
| S22-ENG-01 | Stockpile volume estimation | Survey/volume | Open | Define base surface, boundary and uncertainty; compare synthetic/reference solids |
| S22-ENG-02 | Earthwork cut-and-fill | Surface comparison | Open | Define design/existing surfaces, sign convention and NoData policy |
| S22-ENG-03 | Construction progress monitoring | Monitoring workflow | Open | Define temporal baseline, measurable quantities and uncertainty |
| S22-ENG-04 | As-built versus design comparison | Deviation analysis | Open | Define registration, tolerance and signed distance |
| S22-ENG-05 | Total-station network adjustment | Geodetic adjustment | Open | Define observation equations, stochastic model and datum constraints |
| S22-ENG-06 | Tunnel convergence monitoring | Deformation monitoring | Open | Define epoch registration, reference points and uncertainty |
| S22-ENG-07 | Bridge deformation monitoring | Structural monitoring | Open | Define sensor/epoch model, temperature effects and alert thresholds |
| S22-ENG-08 | Dam deformation monitoring | Structural monitoring | Open | Define geodetic network, reference stability and safety-critical review |
| S22-ENG-09 | InSAR settlement monitoring | Remote-sensing monitoring | Open | Define reference area, atmospheric correction and temporal coherence |
| S22-ENG-10 | GNSS settlement monitoring | Geodetic monitoring | Open | Define reference frame, time series and uncertainty |
| S22-ENG-11 | Terrestrial laser scanning registration | Point-cloud registration | Partial | Existing generic point-cloud registration is not TLS-specific; add target/scan geometry and calibration tests |
| S22-ENG-12 | M3C2 point-cloud change detection | 3-D change detection | Open | Implement normal-scale/distance uncertainty model; test known displacement and roughness |
| S22-ENG-13 | Dense point-cloud change detection | 3-D change detection | Partial | Existing point-cloud distance metrics are not M3C2; distinguish nearest-neighbour distance from statistically qualified change |

### Citizen science and presence-only modelling (source page 47)

| ID | Atomic item | Kind | Status | Acceptance work |
|---|---|---|---|---|
| S22-ECO-01 | Observer-effort modelling | Observation process | Open | Define effort covariates and sampling unit; synthetic bias recovery |
| S22-ECO-02 | Detectability modelling | Observation process | Open | Specify detection probability and repeated-survey assumptions |
| S22-ECO-03 | eBird-style spatiotemporal exploratory models (STEM) | Exploratory model | Verify | Identify exact published method and acronym expansion before implementation |
| S22-ECO-04 | Target-group background | Presence-only bias correction | Open | Define target group and sampling domain; compare bias surfaces |
| S22-ECO-05 | Bias-grid correction | Presence-only bias correction | Open | Define grid construction and sensitivity to resolution |
| S22-ECO-06 | Integrated species distribution models | Integrated modelling | Open | Define joint likelihood for presence-only and structured observations |
| S22-ECO-07 | Point-process species distribution models | Point-process model | Open | Define intensity/link/offset and quadrature; test simulated inhomogeneous Poisson process |
| S22-ECO-08 | iNaturalist-style data cleaning | Data quality workflow | Open | Separate taxonomic, coordinate, captive/introduced and observer-quality filters; preserve provenance |
| S22-ECO-09 | Occupancy with false positives | Occupancy model | Open | Define validation/subsample design and false-positive/false-negative likelihood |
| S22-ECO-10 | Camera-trap density estimation | Ecological estimation | Open | Identify exact estimator family and assumptions (e.g. movement/independence); do not conflate occupancy with density |
| S22-ECO-11 | eDNA spatial sampling models | Sampling design/model | Open | Define transport, detection and spatial dependence assumptions |

### Fire danger and post-fire hazards (source page 47)

| ID | Atomic item | Kind | Status | Acceptance work |
|---|---|---|---|---|
| S22-FIRE-01 | Canadian Fire Weather Index (FWI) | Fire danger system | Open | Verify component equations, inputs, temporal carry-over and official reference fixtures |
| S22-FIRE-02 | Keetch–Byram Drought Index (KBDI) | Fire danger index | Open | Verify precipitation/temperature update, bounds and regional assumptions |
| S22-FIRE-03 | McArthur forest fire danger index | Fire danger index | Open | Verify exact variant, fuel/weather inputs and jurisdiction |
| S22-FIRE-04 | US National Fire Danger Rating System (NFDRS) | Fire danger system | Open | Identify edition/version; do not collapse distinct system revisions |
| S22-FIRE-05 | Fuel-moisture estimation | Estimation | Open | Define fuel class, equilibrium/time-lag model and validation observations |
| S22-FIRE-06 | Fuel-type mapping | Classification | Open | Define fuel taxonomy, scale and independent field validation |
| S22-FIRE-07 | Burn severity dNBR | Change metric | Open | Define pre/post compositing, NBR scaling and masking; synthetic and reference tests |
| S22-FIRE-08 | Burn severity RdNBR | Change metric | Open | Verify denominator/scaling and low-prefire-NBR handling |
| S22-FIRE-09 | Burn severity RBR | Change metric | Open | Verify formula and denominator stability |
| S22-FIRE-10 | Post-fire debris-flow empirical models | Hazard model | Open | Identify exact USGS model version, calibration domain and input units |
| S22-FIRE-11 | Smoke-dispersion coupling | Coupled model | Open | Define emissions, meteorology and transport model interface; validate conservation/units |

## Completion gates

A row must not be marked complete merely because a library exposes a similarly named function. Before changing a status to **Implemented (scoped)**, add:

1. **Identity:** exact method variant, source page, primary/authoritative reference and version where relevant.
2. **Theory:** equations, assumptions, admissible parameter space and known failure modes.
3. **Contract:** coordinate reference/units, shapes, missing values, deterministic behaviour and error semantics.
4. **Implementation:** canonical package or an explicit reason the item is a workflow/platform rather than a standalone algorithm.
5. **Independent verification:** analytical fixtures, differential comparison to an independent implementation or published benchmark, adversarial edge cases and numerical stability tests.
6. **Teaching material:** method record, implementation walkthrough, runnable example/notebook when it adds learning value.
7. **Catalogue reconciliation:** links and status consistent across source section, methods catalogue, implementation index and coverage matrix.
8. **Rights/provenance:** source and data/software licences reviewed; no copied proprietary code or undocumented datasets.

## Batch execution order

1. Close source identity and references for each item family before coding.
2. Implement compact, mathematically self-contained methods first; batch tests and documentation with each implementation.
3. Treat domain workflows, commercial platforms and sensor pipelines as reproducible workflow records where a standalone algorithm is not appropriate.
4. Keep high-stakes fire, power, water and structural-monitoring methods explicitly educational/research-only until validated by domain authorities.
5. Reconcile all rows against the full compendium and run the complete CI suite before release.

**Current conclusion:** this register decomposes the Section 22 backlog into atomic work items; it does not complete them. Section 22 remains open until each applicable row passes the gates above. The same decomposition and evidence discipline must be applied to sections 1–21.
