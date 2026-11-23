# Section 11 atomic completion register

**Source:** *Spatial Analysis Algorithms: Complete Compendium*, Section 11, pages 23–24.  
**Intake:** [preserved pages 21–25 transcription](../source-inventory/pages-21-25.md).  
**Section index:** [Section 11 catalogue record](../catalog/sections/11-geoai-computer-vision-additions.md).

> The source says model names are representative and not verified against current releases. The rows below are research leads, not a verified model zoo. Verify identity, publication, release, checkpoint, training data, benchmark and licence before use.

## Status policy

Apply the [source-entry verification protocol](../catalog/verification-protocol.md) and [compendium completion standard](compendium-completion-standard.md). Separate model architectures, trained weights, datasets, evaluation protocols, software and workflows. Existing generic components do not verify named models.

| Status | Meaning |
|---|---|
| Open | No item-specific independent evidence recorded. |
| Verify | Exact model, project, dataset, release or benchmark must be identified. |
| Partial | A related generic implementation exists, but the named family remains only partly covered. |
| Not applicable | A task, dataset or operational workflow is not a standalone algorithm. |

## Atomic source register

### Optical and multispectral GeoFM families — page 23

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S11-FM-01 | Prithvi-EO-2.0 | Earth-observation foundation model | Verify | Identify exact release/checkpoint, architecture, training data and licence; document task support. |
| S11-FM-02 | SatMAE++ | Self-supervised EO model | Verify | Resolve exact paper/release and distinction from SatMAE; verify checkpoint. |
| S11-FM-03 | RingMo | EO foundation model | Verify | Identify exact version and pretraining objective; document sensor/data provenance. |
| S11-FM-04 | RVSA | Remote-sensing vision architecture | Verify | Resolve acronym, paper and exact architecture; avoid name collision. |
| S11-FM-05 | SatViT | Satellite vision transformer | Verify | Identify exact model/release and training data; confirm project identity. |
| S11-FM-06 | USat | EO model/project | Verify | Resolve exact project, paper and acronym; verify weights/licence. |
| S11-FM-07 | SMARTIES | EO model/project | Verify | Resolve exact identity and release; record model card and supported sensors. |
| S11-FM-08 | DeCUR | EO representation/pretraining model | Verify | Verify exact acronym, paper and pretraining task; distinguish model from training recipe. |
| S11-FM-09 | FoMo | EO model/project | Verify | Resolve exact project/version and architecture; confirm acronym expansion from primary source. |
| S11-FM-10 | THOR | EO model/project | Verify | Resolve exact paper/repository; avoid acronym ambiguity. |
| S11-FM-11 | RoMA | EO model/project | Verify | Identify exact model and distinguish from similarly named registration models. |
| S11-FM-12 | SkySense++ | EO foundation model | Verify | Verify release/checkpoint and multimodal scope; document licence. |

### Multimodal and multi-sensor models — page 23

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S11-MM-01 | OmniSat | Multimodal satellite model | Verify | Resolve exact paper/project, modality set and release; validate missing-modality handling. |
| S11-MM-02 | MMEarth | Multimodal EO dataset/model family | Verify | Separate dataset from model/pretext tasks; verify release, modalities and licence. |
| S11-MM-03 | Auxiliary geographic-data pretext tasks | Self-supervised learning method family | Open | Identify concrete pretext tasks and data sources; test leakage and geographic transfer. |
| S11-MM-04 | SSL4EO-S12 | EO pretraining dataset | Verify | Verify dataset release, sensor bands, splits and terms; not an algorithm. |
| S11-MM-05 | DOFA-CLIP | Multimodal EO model | Verify | Resolve exact model version and modality-specific adaptation; verify training data and weights. |
| S11-MM-06 | Hydra-style multi-head pretraining | Multi-task architecture/training pattern | Open | Identify concrete implementation and head objectives; distinguish generic pattern from named model. |

### Time-series and temporal models — page 23

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S11-TS-01 | EarthPT | EO time-series model | Verify | Identify exact paper/release and temporal input protocol; validate spatial/time transfer. |
| S11-TS-02 | TESSERA | EO representation model/project | Verify | Resolve exact project and release; verify model/data licence. |
| S11-TS-03 | Presto | EO time-series foundation model | Verify | Identify exact version/checkpoint and input bands/time encoding; document missing data handling. |
| S11-TS-04 | SITS-Former | Satellite image time-series architecture | Verify | Verify paper/repository and tokenisation; test temporal gaps and irregular sampling. |
| S11-TS-05 | Pixel-wise transformers for satellite time series | Architecture family | Open | Split by temporal attention, spatial context and token design; define leakage-safe evaluation. |

### Mamba and linear-attention variants — page 23

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S11-EF-01 | Mamba EO encoder variants | State-space architecture family | Open | Identify concrete model and token order; test long-range spatial/temporal behaviour. |
| S11-EF-02 | Linear-attention hyperspectral encoders | Efficient attention family | Open | Split by kernel/normalisation variant; evaluate spectral fidelity and numerical stability. |
| S11-EF-03 | HyperSIGMA | Hyperspectral foundation model | Verify | Verify paper, architecture, checkpoint and sensor/training corpus. |
| S11-EF-04 | Samba | Hyperspectral/large-scene model | Verify | Resolve exact project and model variant; confirm acronym and checkpoint. |

### Pretraining datasets — page 23

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S11-DATA-01 | SSL4EO-S12 dataset | Pretraining dataset | Verify | Verify official release/version, sensor data and licence. |
| S11-DATA-02 | MMEarth dataset | Multimodal dataset | Verify | Verify dataset scope, modalities, collection and licence. |
| S11-DATA-03 | Satlas dataset | EO dataset/benchmark | Verify | Identify exact dataset release and annotation terms. |
| S11-DATA-04 | fMoW dataset | EO benchmark dataset | Verify | Verify version, class labels, split and use restrictions. |
| S11-DATA-05 | BigEarthNet | EO benchmark dataset | Verify | Verify version, label hierarchy, sensor bands and licence. |
| S11-DATA-06 | SEN12MS | EO benchmark dataset | Verify | Verify release, paired SAR/optical semantics and licence. |
| S11-DATA-07 | Major TOM | EO dataset | Verify | Resolve exact release, imagery sources and terms. |
| S11-DATA-08 | GeoPile | EO pretraining corpus | Verify | Identify exact project/release and data mixture; audit upstream licences. |

### Oriented detection — page 23

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S11-OD-01 | Gliding Vertex | Oriented object detector | Verify | Verify paper/model and rotated-box representation; benchmark angle conventions. |
| S11-OD-02 | S2A-Net | Oriented object detector | Verify | Verify exact architecture/checkpoint and angle definition. |
| S11-OD-03 | R3Det | Oriented object detector | Verify | Verify refinement stages and box parameterisation; test small/elongated objects. |
| S11-OD-04 | LSKNet | Large-kernel vision architecture/detector backbone | Verify | Identify exact variant and task head; verify checkpoint. |
| S11-OD-05 | Oriented RepPoints | Oriented detection architecture | Verify | Verify point-set representation and training targets; test geometric decoding. |
| S11-OD-06 | ReDet | Rotation-equivariant detector | Verify | Verify architecture/release and rotation-equivariance claims; benchmark orientation error. |

### Small-object detection and slicing — page 23

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S11-SO-01 | SAHI | Sliced-aided inference software/method | Verify | Identify version, slicing/merge semantics and licence; evaluate seam and duplicate detections. |
| S11-SO-02 | Tile-based inference | Large-scene inference workflow | Not applicable | Define tile size, overlap, context and merge; test boundary omissions. |
| S11-SO-03 | Multi-scale feature fusion | Detection architecture method | Open | Identify concrete fusion architecture; test scale-specific recall. |

### Video, tracking and counting — page 23

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S11-VT-01 | SORT | Multi-object tracking algorithm | Verify | Verify Kalman/assignment formulation and version; test ID switches and occlusion. |
| S11-VT-02 | DeepSORT | Multi-object tracking algorithm | Verify | Verify appearance embedding and association; document checkpoint. |
| S11-VT-03 | ByteTrack | Multi-object tracking algorithm | Verify | Verify two-stage association and score thresholds; test low-confidence detections. |
| S11-VT-04 | Satellite video object tracking | Application/task family | Open | Identify data and tracking methods; handle parallax, revisit and georegistration. |
| S11-VT-05 | Vehicle counting | Object counting workflow | Open | Define line/area counting and direction; validate with annotated trajectories. |
| S11-VT-06 | Crowd density estimation | Density estimation task | Open | Define point/density labels and scale; evaluate count bias and domain shift. |

### Instance, panoptic and keypoint tasks — page 23

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S11-IP-01 | Mask R-CNN | Instance segmentation architecture | Verify | Verify exact version/backbone and training recipe; record checkpoint licence. |
| S11-IP-02 | Mask2Former | Universal segmentation architecture | Verify | Identify version and task head; verify benchmark and checkpoint. |
| S11-IP-03 | Panoptic FPN | Panoptic segmentation architecture | Verify | Verify original formulation and instance/semantic fusion; test PQ components. |
| S11-IP-04 | Building roof keypoints | Geometric keypoint task | Open | Define semantic keypoint taxonomy and geometry; validate geometric reconstruction. |
| S11-IP-05 | Centerline extraction | Vector extraction task | Open | Define skeleton/graph representation and topology metrics; test connectivity. |
| S11-IP-06 | Road graph extraction | Network extraction task | Partial | Existing classical/other source families do not verify this section's GeoAI architectures; define graph topology and benchmark independently. |

### Vision-language and multimodal additions — page 23

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S11-VL-01 | SkySenseGPT | Remote-sensing vision-language model | Verify | Identify exact project/release and model card; verify image/text training data. |
| S11-VL-02 | GeoPixel | Geospatial vision-language model | Verify | Resolve exact paper/project and checkpoint; confirm grounding/task scope. |
| S11-VL-03 | GeoGround | Geospatial grounding model | Verify | Resolve exact identity, output format and release; test spatial grounding. |
| S11-VL-04 | EarthMind | Earth-observation multimodal model | Verify | Identify exact paper/model and supported modalities; verify licence. |
| S11-VL-05 | GeoLLaVA-style models | Model family | Open | Identify concrete implementations; distinguish model weights and prompt formats. |
| S11-VL-06 | RS5M | Image-text corpus | Verify | Verify dataset release, caption provenance and licence. |
| S11-VL-07 | Pixel-level grounding | Vision-language task | Open | Define grounding target and spatial accuracy metric; evaluate dense correspondence. |
| S11-VL-08 | Change captioning | Vision-language task | Open | Define temporal pair, change taxonomy and factuality; evaluate hallucinations. |
| S11-VL-09 | Multi-temporal visual question answering | Multimodal task | Open | Define temporal evidence and answer grounding; test time ordering. |
| S11-VL-10 | VQA over multispectral inputs | Multimodal task | Open | Define band availability and sensor context; test spectral reasoning. |
| S11-VL-11 | VQA over SAR inputs | Multimodal task | Open | Define polarisation/geometry metadata and task labels; test SAR-specific reasoning. |
| S11-VL-12 | Multimodal LLM agents calling segmentation/detection tools | Agent architecture/workflow | Open | Define tool contracts, permissions and result verification; test execution sandbox and hallucination. |

### Neural combinatorial optimisation and reinforcement learning — page 24

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S11-NO-01 | Attention models for TSP | Neural combinatorial optimisation | Verify | Identify exact architecture/training objective; compare with exact/heuristic TSP baselines. |
| S11-NO-02 | POMO for TSP | Neural combinatorial optimisation | Verify | Verify POMO formulation and multi-start sampling; benchmark optimality gap. |
| S11-NO-03 | Attention models for VRP | Neural combinatorial optimisation | Verify | Identify capacity/time-window variant; compare with classical solvers. |
| S11-NO-04 | POMO for VRP | Neural combinatorial optimisation | Verify | Verify exact VRP constraints and objective; benchmark feasibility and gap. |
| S11-NO-05 | GNN-based routing heuristics | Learned optimisation | Open | Define graph encoding and decoder; compare with OR-Tools/exact small instances. |
| S11-NO-06 | Learned neighbourhood search | Learned optimisation | Open | Define move set, acceptance and training; measure feasible improvement. |
| S11-RL-01 | Max-pressure traffic signal control | Traffic control baseline | Verify | Verify pressure definition and network assumptions; compare with fixed-time control. |
| S11-RL-02 | DQN traffic signal control | Reinforcement learning | Open | Define state/action/reward and simulator; test multiple seeds and transfer. |
| S11-RL-03 | PPO traffic signal control | Reinforcement learning | Open | Define policy/action constraints and simulator; test safety and stability. |
| S11-RL-04 | Ride-hailing dispatch RL | Reinforcement learning application | Open | Define supply/demand, fairness and reward; simulate demand uncertainty. |
| S11-RL-05 | Spatial crowdsourcing assignment RL | Reinforcement learning application | Open | Define worker/task matching, travel and deadlines; compare with assignment optimisation. |
| S11-RL-06 | Ambulance relocation RL | Reinforcement learning application | Open | Define demand, coverage and response-time reward; evaluate rare-event performance and equity. |
| S11-LR-01 | GNN-based travel-time prediction | Learned routing/ETA | Open | Define graph/time features and leakage-safe splits; compare with speed/profile baselines. |
| S11-LR-02 | Transformer route recommendation | Learned routing | Open | Define candidate routes, choice labels and constraints; assess calibration and safety. |

### Generative and probabilistic EO models — page 24

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S11-GE-01 | Diffusion cloud removal | Generative restoration | Open | Define cloud mask, conditional inputs and radiometric consistency; test against cloud-free references. |
| S11-GE-02 | Diffusion super-resolution | Generative restoration | Open | Define scale factor and spectral consistency; evaluate hallucination risk. |
| S11-GE-03 | Diffusion gap filling | Generative reconstruction | Open | Define missing-data mask and temporal context; preserve uncertainty and observations. |
| S11-GE-04 | Controllable synthetic EO scene generation | Generative simulation workflow | Open | Define geographic/semantic controls and provenance; audit realism and training data rights. |
| S11-GE-05 | Flow matching | Generative modelling method | Verify | Identify exact flow-matching formulation and objective; distinguish from diffusion. |
| S11-GE-06 | Consistency models | Generative modelling method | Verify | Identify consistency training/sampling variant; test speed-quality trade-off. |
| S11-GE-07 | Latent diffusion with learned EO tokenizers | Generative architecture workflow | Open | Define tokenizer, latent geometry and spectral reconstruction; verify spatial fidelity. |
| S11-GE-08 | Mixture density networks | Probabilistic prediction method | Open | Define mixture likelihood and calibration; test multimodal uncertainty. |
| S11-GE-09 | Normalizing flows | Probabilistic density model | Open | Specify invertible architecture and Jacobian; test likelihood and calibration. |
| S11-GE-10 | Quantile regression networks | Probabilistic prediction method | Open | Define quantile loss and crossing correction; test coverage and sharpness. |

### Benchmarks and datasets — page 24

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S11-BM-01 | LoveDA | Segmentation dataset | Verify | Verify release, labels, splits and licence; document urban/rural coverage. |
| S11-BM-02 | iSAID | Instance segmentation dataset | Verify | Verify version, classes, splits and terms. |
| S11-BM-03 | Open-Earth-Map | Mapping dataset/project | Verify | Resolve exact dataset/release and annotation licence. |
| S11-BM-04 | SpaceNet | Benchmark family | Verify | Split by challenge/version; document imagery, labels and evaluation protocol. |
| S11-BM-05 | FLAIR | Land-cover dataset | Verify | Verify version, geographic coverage, labels and terms. |
| S11-BM-06 | Sen1Floods11 | Flood mapping dataset | Verify | Verify release, sensor/time pairing and split. |
| S11-BM-07 | HLS Burn Scars | Burn-scar dataset/product | Verify | Identify exact dataset version and label provenance; distinguish HLS product from benchmark. |
| S11-BM-08 | So2Sat LCZ42 | Local climate zone dataset | Verify | Verify version, label protocol, sensor and licence. |
| S11-BM-09 | DynamicEarthNet | Multi-temporal dataset | Verify | Verify release, temporal labels and evaluation protocol. |
| S11-BM-10 | DOTA | Oriented detection dataset | Verify | Verify version, annotation conventions and licence. |
| S11-BM-11 | DIOR | Object detection dataset | Verify | Verify release, class labels and licence. |
| S11-BM-12 | xView | Object detection dataset | Verify | Verify challenge/version, labels and restrictions. |
| S11-BM-13 | FAIR1M | Fine-grained aerial dataset | Verify | Verify release, category taxonomy and licence. |
| S11-BM-14 | PANGAEA | Geospatial benchmark suite | Verify | Resolve exact benchmark version/tasks; document evaluation. |
| S11-BM-15 | GEO-Bench | GeoFM benchmark | Verify | Verify release, tasks, splits and data rights. |
| S11-BM-16 | Copernicus-Bench | EO benchmark suite | Verify | Identify exact release and evaluation tasks; document product provenance. |
| S11-BM-17 | WeatherBench 2 | Weather benchmark | Verify | Verify dataset/benchmark version and spatial/temporal split. |
| S11-BM-18 | SEVIR | Severe-weather dataset | Verify | Verify release, sensor/event structure and licence. |
| S11-BM-19 | ClimateBench | Climate benchmark | Verify | Verify target tasks, model inputs and version. |
| S11-BM-20 | ERA5-based training sets | Data collection family | Open | Identify exact derived datasets, processing and licence; ERA5 is not one benchmark definition. |

### Operational GeoAI engineering — page 24

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S11-OP-01 | Tile deduplication | Data curation method | Open | Define exact/near-duplicate and overlap criteria; test across time/sensors. |
| S11-OP-02 | Label-noise audits | Data quality workflow | Open | Define audit sampling, confusion and adjudication; report class-wise uncertainty. |
| S11-OP-03 | Class-balanced geographic sampling | Sampling design | Open | Define geographic strata and class balance; quantify coverage trade-offs. |
| S11-OP-04 | Region-stratified data splits | Evaluation design | Partial | Existing spatial CV is a generic baseline; define region groups and leakage buffers. |
| S11-OP-05 | Dataset versioning | MLOps workflow | Not applicable | Define immutable manifests, lineage and reproducible versions. |
| S11-OP-06 | STAC-driven training pipelines | Data/ML workflow | Open | Define catalogue query, asset version and licence checks; make training inputs reproducible. |
| S11-OP-07 | Temporal drift monitoring | Model monitoring | Open | Define drift statistic, seasonality and alert thresholds; evaluate false alarms. |
| S11-OP-08 | Sensor-change monitoring | Model monitoring | Open | Define metadata and distribution shift; test cross-sensor calibration. |
| S11-OP-09 | Active-learning loops | Human-in-loop workflow | Partial | Existing adaptive sampling provides bounded selection components; close annotation, retraining and evaluation loop. |
| S11-OP-10 | SAM-assisted interactive segmentation | Annotation workflow | Verify | Identify exact SAM version and user workflow; track prompt/edits and human review. |
| S11-OP-11 | Quality scoring | Annotation QA | Open | Define geometry/label consistency and confidence; validate against expert review. |
| S11-OP-12 | Annotation review queues | Human-in-loop operations | Not applicable | Define prioritisation, adjudication and audit trail; measure reviewer consistency. |
| S11-OP-13 | Cross-continent evaluation splits | Generalisation protocol | Not applicable | Define continent holdout and sampling support; report regional confidence intervals. |
| S11-OP-14 | Seasonal shift tests | Generalisation protocol | Not applicable | Define season/time split and phenology effects; test calibration drift. |
| S11-OP-15 | Sensor-swap tests | Generalisation protocol | Not applicable | Define sensor holdout and spectral harmonisation; quantify degradation. |
| S11-OP-16 | Calibration-drift checks | Model monitoring/evaluation | Open | Define reliability metric and recalibration policy; test temporal changes. |

## Completion gates

1. Resolve exact names and versions against primary papers, official model cards, code and benchmark documentation.
2. Record checkpoint hashes, training datasets, sensor coverage, pretraining objective and licence.
3. For benchmark datasets, preserve split integrity, geographic/temporal separation, label taxonomy and data rights.
4. Evaluate oriented geometry, tracking identity, topology, probabilistic calibration and downstream utility—not only generic accuracy.
5. For RL/learned optimisation, compare against transparent classical baselines, report feasibility and use multiple seeds.
6. For generative models, assess observation consistency, uncertainty, hallucination and spectral/physical plausibility.
7. For operational workflows, include provenance, dataset versioning, drift monitoring, human review and rollback.
8. Reconcile canonical lessons, model integrations, tests, notebooks, catalogue and dashboard only after evidence changes.

**Current conclusion:** Section 11 is decomposed into atomic review items. It remains open; no named model, benchmark or operational GeoAI system is declared verified by this register.
