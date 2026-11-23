# Section 15 atomic completion register

**Source:** *Spatial Analysis Algorithms: Complete Compendium*, Section 15, pages 31–33.  
**Intake:** [preserved pages 31–35 transcription](../source-inventory/pages-31-35.md).  
**Section index:** [Section 15 catalogue record](../catalog/sections/15-vision-registration-vector-extraction.md).

> The source says names are representative and from memory. Architecture names, dataset names and software variants must be resolved to exact papers/releases before citation. This register is a decomposition, not a verified model zoo.

## Status policy

Apply the [source-entry verification protocol](../catalog/verification-protocol.md) and [compendium completion standard](compendium-completion-standard.md). Separate architectures, trained checkpoints, datasets, metrics, workflows and algorithms. A library integration or primitive is not evidence that a whole research family is complete.

| Status | Meaning |
|---|---|
| Open | No item-specific evidence recorded here. |
| Partial | A bounded related implementation exists; variants or validation remain open. |
| Verify | Exact method, project, version, checkpoint or benchmark must be resolved. |
| Not applicable | Dataset, hardware, platform or workflow is not a standalone algorithm. |

## Atomic source register

### Vision backbones, promptable and open-vocabulary tools — page 31

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S15-VI-01 | SegFormer | Vision architecture | Verify | Identify paper/repository and variant; document pretraining, decoder and licence. |
| S15-VI-02 | HRNet | Vision architecture | Verify | Identify exact HRNet variant and task head; verify remote-sensing adaptation separately. |
| S15-VI-03 | Mask DINO | Detection/segmentation architecture | Verify | Identify exact paper/release and task configuration; record checkpoint provenance. |
| S15-VI-04 | Video Swin Transformer | Video architecture | Verify | Identify model variant, temporal sampling and pretraining; assess satellite time-series suitability. |
| S15-VI-05 | TimeSformer | Video architecture | Verify | Verify divided space-time attention variant and input protocol. |
| S15-VI-06 | ViViT | Video architecture family | Verify | Split variants and tokenisation; identify exact architecture/checkpoint. |
| S15-VI-07 | VideoMAE for satellite image time series | Self-supervised video model/adaptation | Verify | Identify satellite-specific adaptation and training data; do not infer from generic VideoMAE. |
| S15-VI-08 | Perceiver IO | General architecture | Verify | Verify paper/release and task-specific input/output structure. |
| S15-VI-09 | MLP-Mixer | Vision architecture | Verify | Identify variant and patch embedding; document limitations relative to convolution/attention. |
| S15-VI-10 | ConvMixer | Vision architecture | Verify | Verify architecture and training protocol; identify remote-sensing adaptation if claimed. |
| S15-VI-11 | Segment Anything Model (SAM) | Promptable segmentation foundation model | Verify | Identify official model version, prompts and checkpoint licence; test geospatial raster workflow. |
| S15-VI-12 | SAM-HQ | SAM adaptation | Verify | Verify project and checkpoint; distinguish from official SAM. |
| S15-VI-13 | MobileSAM | Lightweight SAM adaptation | Verify | Verify distillation/backbone and licence; benchmark resolution and accuracy. |
| S15-VI-14 | EfficientSAM | Efficient segmentation model | Verify | Identify exact paper/repository and checkpoint; record efficiency/accuracy trade-off. |
| S15-VI-15 | Grounded-SAM | Detection-plus-segmentation workflow | Verify | Resolve component versions and prompt semantics; document chained failure modes. |
| S15-VI-16 | CLIPSeg | Text-conditioned segmentation model | Verify | Identify model/checkpoint and training data; test prompt sensitivity. |
| S15-VI-17 | Grounding DINO | Open-set grounding detector | Verify | Verify official model/version and prompt pipeline; assess remote-sensing scale limits. |
| S15-VI-18 | OWL-ViT | Open-vocabulary detector | Verify | Identify model variants and checkpoint; record zero-shot label protocol. |
| S15-VI-19 | Florence-2 | Vision-language foundation model | Verify | Identify exact release/checkpoint and task tokens; review licence and output constraints. |
| S15-VI-20 | LAE-DINO | Remote-sensing detection adaptation | Verify | Resolve exact acronym, paper and checkpoint; avoid treating shorthand as canonical. |
| S15-VI-21 | OpenRSD | Remote-sensing open-set model/project | Verify | Resolve exact project identity, release and task; confirm availability and licence. |
| S15-VI-22 | Depth Anything-style overhead depth models | Monocular depth architecture/adaptation | Verify | Identify exact model and overhead fine-tuning; validate metric scale, height bias and domain shift. |

### Hyperspectral deep learning — page 31

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S15-HS-01 | 3D-CNN hyperspectral classification | Architecture family | Open | Specify spectral-spatial kernel, patch size and label protocol; test leakage-safe spatial splits. |
| S15-HS-02 | HybridSN | Hyperspectral architecture | Verify | Verify original architecture and benchmark protocol; reproduce published result before comparison. |
| S15-HS-03 | SSRN | Hyperspectral architecture | Verify | Resolve exact Spectral–Spatial Residual Network paper and architecture; document preprocessing. |
| S15-HS-04 | SpectralFormer | Hyperspectral transformer | Verify | Verify architecture/checkpoint and spectral tokenisation; assess sensor transfer. |
| S15-HS-05 | Spectral-spatial transformers | Architecture family | Open | Split by attention axis, token design and spectral sampling; do not use as one canonical model. |
| S15-HS-06 | Graph convolution on superpixels | Graph-based classification | Open | Define superpixel construction, graph edges and feature aggregation; test segmentation sensitivity. |
| S15-HS-07 | EndNet unmixing autoencoder | Spectral unmixing model | Verify | Verify paper, constraints and loss; test abundance nonnegativity/sum-to-one. |
| S15-HS-08 | DAEN unmixing model | Spectral unmixing model | Verify | Resolve exact acronym and paper; document endmember assumptions. |
| S15-HS-09 | uDAS-style unmixing models | Spectral unmixing family | Verify | Resolve exact model identity and acronym; separate variants. |
| S15-HS-10 | Physically constrained unmixing networks | Model family | Open | Define mixing model, abundance constraints and spectral response; compare with linear unmixing oracle. |
| S15-HS-11 | Low-rank hyperspectral denoising | Denoising method family | Open | Specify tensor/matrix rank model and noise assumptions; evaluate spectral distortion. |
| S15-HS-12 | Tensor-based hyperspectral denoising | Denoising method family | Open | Define tensor representation and regulariser; test signal/noise recovery. |
| S15-HS-13 | HSI-DeNet | Denoising architecture | Verify | Verify exact paper/repository/checkpoint and sensor setup. |
| S15-HS-14 | Hyperspectral–multispectral fusion networks | Fusion architecture family | Open | Split by fusion model and resolution protocol; test spectral and spatial fidelity. |
| S15-HS-15 | Complex-valued CNNs for PolSAR | Complex neural architecture | Open | Define complex convolution/normalisation and polarimetric representation; test phase equivariance. |
| S15-HS-16 | PolSAR classification networks | Radar classification family | Open | Split architecture and input representation; validate across incidence/terrain domains. |

### Point-cloud learning, registration and building reconstruction — page 31

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S15-PC-01 | Point-BERT | Point-cloud architecture | Verify | Identify paper/repository/checkpoint and pretraining corpus; record point sampling. |
| S15-PC-02 | Point-MAE | Point-cloud architecture | Verify | Verify masked autoencoder formulation and checkpoint; test point density sensitivity. |
| S15-PC-03 | PointMLP | Point-cloud architecture | Verify | Verify exact variant and input normalisation; record training data/licence. |
| S15-PC-04 | PointNeXt | Point-cloud architecture | Verify | Identify model scale and training protocol; benchmark transfer to aerial LiDAR. |
| S15-PC-05 | SPVCNN | Sparse voxel point-cloud architecture | Verify | Verify architecture/release and voxel resolution; assess memory and spatial quantisation. |
| S15-PC-06 | Cylinder3D | Point-cloud segmentation architecture | Verify | Identify cylindrical partition and task; document domain assumptions. |
| S15-PC-07 | Point Transformer V3 | Point-cloud transformer | Verify | Identify exact version and checkpoint; record preprocessing and licence. |
| S15-PC-08 | Sonata | Point-cloud foundation/self-supervised model | Verify | Resolve exact project/version and objective; confirm model-weight rights. |
| S15-PC-09 | DALES dataset | Aerial LiDAR benchmark | Verify | Verify dataset version, classes, split and licence; prevent spatial leakage. |
| S15-PC-10 | SensatUrban dataset | Urban point-cloud benchmark | Verify | Verify release, label taxonomy and split; document coverage and bias. |
| S15-PC-11 | Toronto-3D dataset | Urban point-cloud benchmark | Verify | Verify release, acquisition and split; document spatial/temporal coverage. |
| S15-PC-12 | Point-to-point ICP | Registration algorithm | Partial | Existing baseline is tested; verify convergence conditions, correspondence and robust variants. |
| S15-PC-13 | Point-to-plane ICP | Registration algorithm | Partial | Existing baseline is tested; verify normal estimation and conditioning. |
| S15-PC-14 | Generalized ICP | Registration algorithm | Partial | Existing baseline is tested; verify covariance weighting and objective. |
| S15-PC-15 | Normal Distributions Transform (NDT) | Registration algorithm | Partial | Existing hard-voxel Gaussian baseline is bounded; verify canonical continuous NDT and optimisation. |
| S15-PC-16 | Colored ICP | Registration algorithm | Open | Define photometric/geometric objective and colour calibration; test illumination sensitivity. |
| S15-PC-17 | FPFH descriptors | Local geometric descriptor | Open | Verify descriptor construction and normal/radius parameters; test rotation invariance. |
| S15-PC-18 | RANSAC correspondence registration | Robust registration method | Partial | Existing RANSAC plane fitting is not a full feature-correspondence registration; implement separately with degeneracy checks. |
| S15-PC-19 | TEASER++ | Robust registration algorithm/software | Verify | Identify version and truncated least-squares guarantees; document certifiable stage and assumptions. |
| S15-PC-20 | DCP | Deep point-cloud registration | Verify | Identify exact Deep Closest Point version/checkpoint and input assumptions. |
| S15-PC-21 | PointNetLK | Deep registration architecture | Verify | Verify Lucas–Kanade-style formulation and checkpoint; test pose range. |
| S15-PC-22 | GeoTransformer | Learned geometric registration | Verify | Identify paper/release and feature matching pipeline; document training domain. |
| S15-PC-23 | PolyFit building reconstruction | Building reconstruction method | Verify | Verify exact method and planar-face assumptions; test roof topology and constraints. |
| S15-PC-24 | City3D | Building reconstruction software/method | Verify | Identify exact project/version and supported inputs; document integration/licence. |
| S15-PC-25 | 2.5D dual contouring | Surface reconstruction method | Verify | Define height-field constraints and vertex placement; test feature preservation. |
| S15-PC-26 | RANSAC roof-plane segmentation | Geometric segmentation | Partial | Existing single-plane primitive is bounded; implement multi-plane extraction, residual reassignment and stopping. |
| S15-PC-27 | Region-growing roof-plane segmentation | Point-cloud segmentation | Open | Define adjacency, normal/curvature thresholds and seed selection; test roof topology. |
| S15-PC-28 | LoD2 building generation | 3D building workflow | Open | Define LoD2 semantics and roof reconstruction; validate against authoritative models. |
| S15-PC-29 | DeepSDF | Neural implicit surface model | Verify | Verify paper/repository and signed-distance assumptions; record checkpoint and licence. |
| S15-PC-30 | Occupancy networks | Neural implicit representation | Verify | Identify exact architecture and occupancy objective; document extraction resolution. |

### Image matching and multimodal registration — pages 31–32

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S15-IM-01 | SIFT | Local image feature | Partial | Existing implementation/integration is bounded; verify version and scale/orientation semantics. |
| S15-IM-02 | ORB | Local image feature | Partial | Existing feature matching is tested; document binary descriptor and rotation/scale limits. |
| S15-IM-03 | AKAZE | Local image feature | Partial | Existing feature matching is tested; verify nonlinear scale-space and descriptor variant. |
| S15-IM-04 | Phase correlation | Image registration algorithm | Partial | Existing FFT translation baseline is tested; document windowing, periodicity and subpixel refinement. |
| S15-IM-05 | Enhanced Correlation Coefficient (ECC) registration | Image registration algorithm | Partial | Existing parametric baseline is tested; document warp model, convergence and masking. |
| S15-IM-06 | Mutual-information registration | Multimodal registration metric/optimisation | Partial | Existing translation baseline is bounded; add transform models, histogram estimator and independent oracle. |
| S15-IM-07 | SuperPoint | Learned feature detector/descriptor | Verify | Identify checkpoint and training data; document repeatability and licence. |
| S15-IM-08 | SuperGlue | Learned feature matcher | Verify | Verify exact model and graph matching; test out-of-domain imagery. |
| S15-IM-09 | LightGlue | Learned feature matcher | Verify | Identify version/checkpoint and supported descriptors; benchmark matching reliability. |
| S15-IM-10 | LoFTR | Detector-free matcher | Verify | Verify model variant and coarse/fine matching; document image-scale limits. |
| S15-IM-11 | DKM | Dense matching model | Verify | Identify exact paper/release and checkpoint; test geometric consistency. |
| S15-IM-12 | RoMa | Robust dense matching model | Verify | Identify model version/checkpoint and licence; validate on aerial imagery. |
| S15-IM-13 | MINIMA multimodal matcher | Multimodal matching model | Verify | Resolve exact project identity and acronym; verify optical/SAR support. |
| S15-IM-14 | RIFT | Optical–SAR matching method | Verify | Verify exact method/version and phase-congruency features; test sensor/terrain conditions. |
| S15-IM-15 | HOPC | Optical–SAR matching descriptor | Verify | Resolve acronym and exact formulation; test invariance and matching precision. |
| S15-IM-16 | CFOG | Optical–SAR matching descriptor | Verify | Verify descriptor definition and parameterisation; compare with RIFT/HOPC. |
| S15-IM-17 | OS-SIFT | Optical–SAR matching method | Verify | Verify exact paper and descriptor modification; test cross-modal robustness. |
| S15-IM-18 | Deep cross-modal descriptors | Model family | Open | Split by architecture/training objective; validate on sensor-disjoint and geographic splits. |
| S15-IM-19 | COSI-Corr-style correlation | Displacement estimation workflow | Verify | Identify exact COSI-Corr method/version; distinguish correlation windowing and georeferencing. |
| S15-IM-20 | Deep optical flow for glacier motion | Dense motion estimation | Open | Define model and temporal sampling; validate against stable control and independent displacement. |
| S15-IM-21 | Deep optical flow for landslide motion | Dense motion estimation | Open | Define model and change conditions; quantify occlusion, decorrelation and displacement uncertainty. |

### Road, building and polygon extraction — page 32

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S15-RD-01 | Sat2Graph | Road graph extraction model | Verify | Verify paper/checkpoint and graph representation; evaluate topology and connectivity. |
| S15-RD-02 | RNGDet | Road network extraction model | Verify | Identify exact model and graph decoding; test junction and connectivity errors. |
| S15-RD-03 | iCurb | Curb/road boundary extraction model | Verify | Verify task definition, checkpoint and input resolution; validate geometric offsets. |
| S15-RD-04 | RoadTracer | Road graph extraction algorithm | Verify | Verify original method and iterative tracing; test graph completeness and loops. |
| S15-RD-05 | Lane graph inference | Road topology inference family | Open | Define lane-level graph semantics, direction and intersection handling; test topology separately from pixels. |
| S15-RD-06 | PolyRNN | Polygon prediction architecture | Verify | Identify exact paper/model and vertex sequence protocol; test closure and topology. |
| S15-RD-07 | Pix2Poly | Polygon extraction model | Verify | Verify model/version and polygon decoding; evaluate shape/topology. |
| S15-RD-08 | Frame-field learning | Vectorisation/geometry representation | Verify | Verify exact frame-field formulation and singularity handling; test orientation consistency. |
| S15-RD-09 | HiSup | Polygon extraction model | Verify | Identify exact paper/checkpoint and output representation; test topology. |
| S15-RD-10 | P2PFormer | Polygon extraction architecture | Verify | Resolve exact project/model and training data; verify acronym. |
| S15-RD-11 | APLS metric | Road-network evaluation metric | Verify | Verify exact path-based score and implementation version; test graph edit cases. |
| S15-RD-12 | TOPO metric | Topological evaluation metric | Verify | Resolve exact benchmark definition; test connectivity and junction errors. |
| S15-RD-13 | Junction F1 | Network extraction metric | Open | Define junction matching tolerance and class balance; test split/merge errors. |
| S15-RD-14 | Boundary IoU | Segmentation metric | Open | Define boundary tolerance and geometry rasterisation; test resolution sensitivity. |
| S15-RD-15 | Polygon similarity metrics | Geometry evaluation family | Open | Split by metric (IoU, shape, topology, vertex correspondence); define invariances. |
| S15-RD-16 | Vertex-based metrics | Polygon evaluation family | Open | Define matching, ordering and tolerance; handle different vertex densities. |
| S15-RD-17 | KDE map inference from GPS traces | Map inference method | Open | Define trace sampling, bandwidth and network constraints; validate against authoritative roads. |
| S15-RD-18 | GPS trace merging | Map inference workflow | Open | Define conflation and alignment; test parallel roads and intersections. |
| S15-RD-19 | Clustering-based map inference | Map inference family | Open | Identify exact clustering method and graph construction; test density variation. |
| S15-RD-20 | Incremental map generation | Online map inference | Open | Define update/decay and conflict resolution; test stream order and drift. |
| S15-RD-21 | DeepMG | Deep map-generation model | Verify | Resolve exact paper/repository and output graph; validate on held-out regions. |
| S15-RD-22 | kharita | Deep map-generation project/model | Verify | Identify exact project/version and acronym; verify data and model availability. |

### Bayesian spatial clustering and partition models — page 32

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S15-BC-01 | Potts-model spatial prior | Bayesian spatial prior | Open | Define neighbourhood graph, coupling and normalising constant; test limiting independent case. |
| S15-BC-02 | Voronoi tessellation prior | Spatial partition prior | Open | Define seed process and partition likelihood; test geometry and prior sensitivity. |
| S15-BC-03 | Product partition model | Bayesian partition model | Verify | Verify cohesion function and exchangeability assumptions; test posterior partition recovery. |
| S15-BC-04 | Spatial Dirichlet process mixture | Bayesian nonparametric model | Open | Define spatial dependence in mixture weights/atoms; document identifiability and inference. |
| S15-BC-05 | BaySTDetect | Bayesian spatiotemporal cluster detection | Verify | Resolve exact model/software and version; document prior, scan and posterior interpretation. |
| S15-BC-06 | Spatially varying finite mixtures | Spatial mixture model | Open | Define spatially varying weights/parameters and identifiability; test synthetic clusters. |
| S15-BC-07 | Reversible-jump MCMC for partition changes | Bayesian model selection | Open | Define dimension-changing moves and detailed balance; test posterior on known partitions. |
| S15-BC-08 | Bayesian spatial change-point models | Bayesian change-point model | Open | Define spatial/temporal boundary and likelihood; test known synthetic transitions. |
| S15-BC-09 | Bayesian boundary detection | Spatial boundary model | Open | Define adjacency, contrast prior and posterior boundary probability; assess resolution dependence. |

### Hydrology machine learning — page 32

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S15-HY-01 | Streamflow LSTM | Hydrological forecasting architecture | Verify | Identify exact architecture/data protocol; compare against persistence and process baselines. |
| S15-HY-02 | CAMELS-based training | Benchmark dataset/workflow | Verify | Identify CAMELS version/region and licence; define basin split and covariates. |
| S15-HY-03 | Regional models for ungauged basins | Hydrological regionalisation | Open | Define donor basins, similarity and transfer; evaluate leave-one-basin-out. |
| S15-HY-04 | Transformer flood forecasting | Hydrological forecasting architecture | Open | Identify model and forecast horizon; use temporal and basin-held-out evaluation. |
| S15-HY-05 | Graph-based flood forecasting | Graph ML workflow | Open | Define graph nodes/edges and routing lags; test spatial transfer and missing gauges. |
| S15-HY-06 | Differentiable HBV-style model | Differentiable process model | Verify | Identify exact HBV variant and differentiable implementation; test mass balance and gradients. |
| S15-HY-07 | Differentiable parameter learning | Process-model calibration | Open | Define loss, constraints and gradient method; compare with derivative-free calibration. |
| S15-HY-08 | Neural ODE catchment models | Neural differential equation | Verify | Identify exact model and state variables; test numerical solver and physical constraints. |
| S15-HY-09 | Operational flood forecasting pipeline | Forecasting system | Not applicable | Document components, latency, data assimilation and monitoring; do not represent as one algorithm. |
| S15-HY-10 | Hybrid process–ML models | Hybrid modelling family | Open | Specify process model, learned residual/corrector and conservation constraints. |
| S15-HY-11 | Learned-corrector data assimilation | Data assimilation method | Open | Define state/observation operator and update; test stability and uncertainty calibration. |
| S15-HY-12 | Ocean surrogate models | Numerical model emulation | Open | Define target solver, forcing and generalisation domain; compare against held-out simulations. |
| S15-HY-13 | Ocean forecasting models | Forecasting model family | Open | Split by state variables and model architecture; validate long-horizon physical consistency. |
| S15-HY-14 | Learned wave emulators | Wave model emulation | Open | Define spectral/state representation and boundary conditions; test extremes. |
| S15-HY-15 | Storm-surge emulators | Coastal hazard emulation | Open | Define hydrodynamic solver, tide/forcing and inundation outputs; validate extreme-event tails. |

### Image geolocation — page 32

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S15-GL-01 | S2-cell image classification with hierarchical heads | Image geolocation model | Open | Define cell hierarchy, target resolution and uncertainty; test spatially disjoint splits. |
| S15-GL-02 | H3-cell image classification with hierarchical heads | Image geolocation model | Open | Define H3 resolution hierarchy and label aggregation; test cell-boundary ambiguity. |
| S15-GL-03 | Contrastive image–location training | Representation learning method | Open | Define positive/negative sampling and geographic leakage controls; test calibration. |
| S15-GL-04 | Retrieval-plus-refinement geolocation | Image retrieval workflow | Open | Define retrieval index, candidate reranking and uncertainty; test coverage and failure modes. |
| S15-GL-05 | PIGEON | Image geolocation model/system | Verify | Identify exact paper/version and evaluation dataset; document geographic bias and privacy. |
| S15-GL-06 | G3 | Image geolocation model/system | Verify | Resolve exact model identity, paper and checkpoint; avoid acronym ambiguity. |
| S15-GL-07 | StreetCLIP | Geospatial vision-language model | Verify | Identify project/checkpoint and training corpus; review licence and location bias. |
| S15-GL-08 | Distance-threshold geolocation accuracy | Evaluation metric | Open | Define distance thresholds, geodesic metric and aggregation; report full error distribution. |
| S15-GL-09 | Geographic bias audit | Fairness evaluation | Open | Define regions/populations and sampling; report support and uncertainty. |
| S15-GL-10 | Adversarial robustness evaluation | Robustness evaluation | Open | Define threat model and perturbations; test location-specific failure modes. |
| S15-GL-11 | Geolocation privacy-risk analysis | Privacy assessment | Open | Define re-identification threat and sensitive location; establish mitigation and disclosure policy. |

### Onboard and edge intelligence — page 32

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S15-ED-01 | CloudScout-style onboard cloud screening | Onboard inference workflow | Verify | Identify exact model/system and sensor; verify onboard constraints and product performance. |
| S15-ED-02 | Low-power satellite CNN accelerators | Hardware/platform family | Not applicable | Document hardware architectures, power/throughput and software stack; not an algorithm. |
| S15-ED-03 | Event-triggered downlink | Data acquisition/communications policy | Open | Define event score, threshold, bandwidth and missed-event cost; simulate trade-offs. |
| S15-ED-04 | In-orbit model update strategies | Model deployment workflow | Open | Define update channel, validation, rollback and fault tolerance; assess security. |
| S15-ED-05 | Quantized models for UAV payloads | Model compression/deployment | Open | Define quantisation scheme, calibration and hardware; measure accuracy/latency/power. |

### Renewable energy forecasting — page 33

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S15-RE-01 | Solar nowcasting from satellite imagery | Solar forecasting workflow | Open | Define cloud-motion model, spatial support and lead time; compare with persistence. |
| S15-RE-02 | Solar nowcasting from sky cameras | Solar forecasting workflow | Open | Define camera calibration, cloud segmentation and temporal lead; validate against irradiance. |
| S15-RE-03 | Irradiance forecasting | Forecasting model family | Open | Define GHI/DNI/DHI target and horizon; assess probabilistic calibration. |
| S15-RE-04 | PV power estimation | Energy prediction model | Open | Define module/inverter and weather inputs; validate across sites and seasons. |
| S15-RE-05 | Wind power forecasting with graph neural networks | Forecasting architecture | Open | Define turbine graph, wake/meteorological inputs and forecast horizon; spatially blocked evaluation. |
| S15-RE-06 | Spatiotemporal wind ensembles | Ensemble forecasting | Open | Define ensemble generation and dependence; test calibration and diversity. |
| S15-RE-07 | Probabilistic wind forecasting for grid operations | Probabilistic forecasting workflow | Open | Define quantiles/distributions and operational decision metric; test reliability and sharpness. |

## Completion gates

1. Verify exact paper, repository, release, checkpoint, training data and licence for every named model or dataset.
2. Separate architectures from trained weights, benchmark datasets, evaluation metrics and end-to-end workflows.
3. For remote sensing, record sensor, bands, ground sampling distance, acquisition geometry, preprocessing and spatial/temporal splits.
4. For registration, test geometric accuracy, residual distributions, outliers, degenerate geometry and independent synthetic transformations.
5. For road/building extraction, evaluate topology and geometry in addition to pixel overlap.
6. For hydrology and energy forecasting, prevent temporal/basin/site leakage and compare against transparent persistence/process baselines.
7. Document uncertainty, domain shift, privacy and geographic bias; review rights for model weights, imagery and datasets.
8. Reconcile lessons, model integrations, tests, notebooks, catalogue and dashboard only after evidence changes.

**Current conclusion:** Section 15 is decomposed into atomic review items. It remains open; the register is not a verification of the named architectures, benchmarks or software projects.
