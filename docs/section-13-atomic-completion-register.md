# Section 13 atomic completion register

**Source:** *Spatial Analysis Algorithms: Complete Compendium*, Section 13, pages 26–28.  
**Intake:** [preserved pages 26–30 transcription](../source-inventory/pages-26-30.md).  
**Section index:** [Section 13 catalogue record](../catalog/sections/13-geofm-workflows-urban-mobility-llms.md).

> The source explicitly says model names are representative and from memory. Treat every named model, dataset, benchmark and tool as an unverified research lead until the exact paper, model card, code, release, training data and licence are resolved.

## Status policy

Apply the [verification protocol](../catalog/verification-protocol.md) and [completion standard](compendium-completion-standard.md). Distinguish workflow patterns, architectures, checkpoints, datasets, evaluation protocols and software systems. No model is considered complete merely because a similarly named package exists.

| Status | Meaning |
|---|---|
| Open | No item-specific verification or implementation evidence recorded. |
| Verify | Exact identity, release, checkpoint, data or licence must be established. |
| Partial | A related generic method exists, but the named GeoFM workflow/model remains unverified. |
| Not applicable | A modality, platform pattern or broad workflow is not one standalone algorithm. |

## Atomic source register

### Embedding-based GeoFM workflows — page 27

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S13-EM-01 | Query-by-example similarity search over embedding indexes | Retrieval workflow | Open | Define embedding model, index metric, metadata filters and candidate evaluation; test spatial/temporal filtering. |
| S13-EM-02 | Prototype-based few-shot land-cover mapping | Few-shot classification workflow | Open | Define prototype construction, support labels and class imbalance; evaluate label-efficiency and geographic transfer. |
| S13-EM-03 | Linear probe on annual embedding fields | Representation evaluation | Open | Define frozen encoder, sampling and regularisation; use region/time-disjoint validation. |
| S13-EM-04 | k-NN probe on annual embedding fields | Representation evaluation | Open | Define metric, k, class weighting and embedding normalisation; compare with linear probe. |
| S13-EM-05 | Unsupervised embedding clustering for land-cover discovery | Clustering workflow | Open | Define clustering algorithm, temporal support and cluster interpretation; evaluate stability and label alignment. |
| S13-EM-06 | Embedding-difference change detection | Change detection workflow | Open | Define embedding alignment and difference metric; test sensor/season nuisance effects. |
| S13-EM-07 | Anomaly detection in embedding space | Anomaly detection workflow | Open | Define reference distribution and score calibration; test rare-class and domain-shift behaviour. |
| S13-EM-08 | Temporal trajectory analysis of embeddings | Time-series representation workflow | Open | Define temporal encoder, missing acquisitions and trajectory distance; validate against known transitions. |
| S13-EM-09 | HNSW approximate nearest-neighbour retrieval | ANN index | Verify | Verify HNSW implementation/version and recall/ef parameters; measure recall-latency-memory. |
| S13-EM-10 | IVF-PQ retrieval | ANN/compressed vector index | Verify | Verify coarse quantiser, product quantisation and training procedure; measure recall and reconstruction error. |
| S13-EM-11 | Spatial metadata filtering for vector retrieval | Retrieval/query method | Open | Define pre/post-filter semantics and recall impact; test boundary and temporal predicates. |
| S13-EM-12 | Frozen versus full fine-tune evaluation | Evaluation protocol | Not applicable | Define controlled comparison, compute budget and leakage prevention; report uncertainty. |
| S13-EM-13 | Label-efficiency curves | Evaluation protocol | Not applicable | Define label budget, sampling policy and repeated seeds; report confidence intervals. |
| S13-EM-14 | Cross-sensor transfer evaluation | Evaluation protocol | Not applicable | Define source/target sensors and harmonisation; hold out sensor domains. |
| S13-EM-15 | Resolution generalisation evaluation | Evaluation protocol | Not applicable | Define GSD/resampling shifts and target metric; test scale robustness. |
| S13-EM-16 | Spectral generalisation evaluation | Evaluation protocol | Not applicable | Define band mismatch and spectral response; test sensor transfer. |
| S13-EM-17 | Cross-region evaluation splits | Evaluation protocol | Not applicable | Define spatial blocks/buffers and independent regions; prevent adjacent-tile leakage. |

### Physics-informed and simulation-based GeoAI — page 27

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S13-PI-01 | PROSAIL-driven pretraining | Physics/ML workflow | Verify | Identify PROSAIL version and synthetic parameter distributions; document sensor response and domain gap. |
| S13-PI-02 | SCOPE-driven pretraining | Physics/ML workflow | Verify | Identify SCOPE version and coupled process assumptions; verify data and code licence. |
| S13-PI-03 | Neural-network inversion of radiative transfer models | Inverse modelling method | Open | Define forward model, parameter space and training prior; evaluate posterior ambiguity and extrapolation. |
| S13-PI-04 | Gaussian-process emulators of radiative transfer models | Surrogate modelling | Open | Define input/output space, kernel and uncertainty; compare with direct simulator. |
| S13-PI-05 | Simulation-based inference | Bayesian inference family | Open | Specify simulator, prior, likelihood-free objective and calibration; test simulation-based calibration. |
| S13-PI-06 | Amortized Bayesian inference for retrieval | Bayesian inference method | Open | Define amortised posterior/likelihood estimator and training distribution; test coverage under shift. |
| S13-PI-07 | Mass-conservation physics-guided loss | Learning constraint | Open | Define conserved quantity, numerical discretisation and boundary flux; test conservation residual. |
| S13-PI-08 | Energy-balance physics-guided loss | Learning constraint | Open | Define energy budget and terms; test units, closure and uncertainty. |
| S13-PI-09 | Monotonicity constraints in hydrology | Shape constraint | Open | Define variables and physical monotonic relation; test constrained optimisation and violations. |
| S13-PI-10 | Monotonicity constraints in climate emulators | Shape constraint | Open | Specify physical regime and variable domain; avoid imposing false global monotonicity. |
| S13-PI-11 | Differentiable simulators | Differentiable modelling family | Open | Identify simulator and gradient method; validate gradients against finite differences. |
| S13-PI-12 | Differentiable hydrology | Process-ML model family | Verify | Identify model/code and state equations; test mass balance and gradient stability. |
| S13-PI-13 | Differentiable parameter learning | Model calibration method | Open | Define objective, constraints and optimisation; compare to conventional calibration. |

### Multimodal inputs beyond imagery — page 27

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S13-MM-01 | LiDAR–optical fusion | Multimodal fusion workflow | Open | Define spatial alignment, feature representation and missing-modality handling. |
| S13-MM-02 | GEDI–optical fusion | Multimodal fusion workflow | Open | Define footprint matching, waveform metrics and temporal mismatch; quantify sampling bias. |
| S13-MM-03 | ICESat-2–optical/SAR fusion | Multimodal fusion workflow | Open | Define track/footprint matching, geolocation and temporal alignment. |
| S13-MM-04 | Street-view imagery as a modality | Data modality/workflow | Not applicable | Document capture date, location privacy, coverage and view-direction bias. |
| S13-MM-05 | POIs as a modality | Data modality/workflow | Not applicable | Define source, taxonomy, temporal validity and completeness. |
| S13-MM-06 | Building footprints as a modality | Data modality/workflow | Not applicable | Define geometry quality, age and provenance; test boundary alignment. |
| S13-MM-07 | Road graphs as a modality | Graph data modality | Not applicable | Define topology, direction, attributes and version; assess map completeness. |
| S13-MM-08 | Soundscapes as a modality | Audio data modality | Not applicable | Define audio labels, temporal support, recording bias and sensitive content. |
| S13-MM-09 | CDR mobility data as a modality | Sensitive mobility data | Not applicable | Require legal basis, aggregation and privacy threat model before use. |
| S13-MM-10 | GPS traces as a modality | Sensitive mobility data | Not applicable | Require consent/legitimate basis, location privacy and sampling-bias audit. |
| S13-MM-11 | Check-ins as a modality | Social/mobility data | Not applicable | Document platform selection bias and privacy; avoid individual-level inference. |
| S13-MM-12 | Transit smart-card data as a modality | Sensitive mobility data | Not applicable | Define anonymisation, trip inference uncertainty and data access restrictions. |
| S13-MM-13 | Text conditioning for place understanding | Multimodal conditioning | Open | Define text encoder, grounding and geographic disambiguation; evaluate hallucination. |
| S13-MM-14 | Knowledge-graph conditioning | Structured representation method | Open | Define ontology, graph construction and message passing/retrieval; test stale/conflicting facts. |
| S13-MM-15 | Geographic hierarchies as inductive bias | Representation design | Open | Define hierarchy (cell/admin/place) and leakage controls; compare flat baselines. |

### Urban and spatiotemporal foundation models — pages 27–28

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S13-UR-01 | UrbanCLIP | Urban vision-language model | Partial | Identity and initial bibliographic evidence are recorded in [the Section 13 identity audit](../research/section-13-identity-audit.md); resolve versioned checkpoints, code/data provenance, licences and technical claims before completion. |
| S13-UR-02 | UrbanVLP | Urban vision-language model | Partial | Identity and initial bibliographic evidence are recorded in [the Section 13 identity audit](../research/section-13-identity-audit.md); resolve versioned checkpoints, code/data provenance, licences and technical claims before completion. |
| S13-UR-03 | Region embedding models | Model family | Open | Split by architecture, region definition and supervision; benchmark spatial transfer. |
| S13-UR-04 | Street-view/satellite fusion for socioeconomic prediction | Multimodal prediction workflow | Open | Define target, spatial unit and temporal alignment; audit privacy, bias and ecological inference. |
| S13-UR-05 | UniST | Spatiotemporal foundation model | Partial | Identity and initial bibliographic evidence are recorded in [the Section 13 identity audit](../research/section-13-identity-audit.md); resolve versioned checkpoints, code/data provenance, licences and technical claims before completion. |
| S13-UR-06 | UrbanGPT | Urban language/model system | Partial | Identity and initial bibliographic evidence are recorded in [the Section 13 identity audit](../research/section-13-identity-audit.md); resolve versioned checkpoints, code/data provenance, licences and technical claims before completion. |
| S13-UR-07 | OpenCity | Urban/traffic model system | Verify | Resolve exact project and version; verify data, architecture and licence. |
| S13-UR-08 | UrbanDiT | Urban diffusion/forecasting model | Partial | Identity and initial bibliographic evidence are recorded in [the Section 13 identity audit](../research/section-13-identity-audit.md); resolve versioned checkpoints, code/data provenance, licences and technical claims before completion. |
| S13-UR-09 | STFM-style universal forecasters | Model family | Open | Identify concrete models and task definitions; do not cite generic acronym as a specific method. |
| S13-UR-10 | TrajFM | Trajectory foundation model | Partial | Identity and initial bibliographic evidence are recorded in [the Section 13 identity audit](../research/section-13-identity-audit.md); resolve versioned checkpoints, code/data provenance, licences and technical claims before completion. |
| S13-UR-11 | UniTraj | Trajectory model/framework | Partial | Identity and initial bibliographic evidence are recorded in [the Section 13 identity audit](../research/section-13-identity-audit.md); resolve versioned checkpoints, code/data provenance, licences and technical claims before completion. |
| S13-UR-12 | Trajectory tokenizers | Representation method family | Open | Split discrete/continuous tokenisation methods; test reconstruction and temporal fidelity. |
| S13-UR-13 | Mobility LLM next-location prediction | Language/mobility model family | Open | Define sequence, location vocabulary and uncertainty; audit re-identification risk. |
| S13-UR-14 | Mobility LLM mode prediction | Language/mobility model family | Open | Define mode labels, context and sampling bias; validate across regions. |
| S13-UR-15 | TimesFM for spatial sensors | Time-series foundation model adaptation | Verify | Identify model version and adaptation; compare with local baselines. |
| S13-UR-16 | Chronos for spatial sensors | Time-series foundation model adaptation | Verify | Identify model/checkpoint and tokenisation; test spatial/temporal shift. |
| S13-UR-17 | Moirai for spatial sensors | Time-series foundation model adaptation | Verify | Identify model version and task; verify probabilistic outputs. |
| S13-UR-18 | Lag-Llama for spatial sensors | Time-series foundation model adaptation | Verify | Identify model version/checkpoint; document covariates and horizon. |
| S13-UR-19 | Spatial adapters for general time-series models | Adaptation method family | Open | Define adapter architecture and spatial context; compare frozen/fine-tuned baselines. |
| S13-UR-20 | Hypergraph neural networks for urban knowledge graphs | Graph architecture | Open | Define hyperedge construction and semantics; test sensitivity to POI/region aggregation. |
| S13-UR-21 | Heterogeneous graph neural networks for urban knowledge graphs | Graph architecture | Open | Define node/edge types and relation-specific aggregation; test missing-type robustness. |
| S13-UR-22 | HGI | Graph representation model | Verify | Resolve exact acronym, paper and model; identify graph schema. |
| S13-UR-23 | ReMVC | Graph representation model | Verify | Resolve exact acronym and paper; verify method and release. |
| S13-UR-24 | Region embeddings | Urban representation | Open | Define region unit, pooling and labels; evaluate boundary/scale sensitivity. |
| S13-UR-25 | POI embeddings | Place representation | Open | Define POI taxonomy, temporal freshness and graph context; assess coverage bias. |

### Geospatial LLMs and agents — page 28

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S13-LL-01 | GeoGalactica | Domain language model | Partial | Identity and initial bibliographic evidence are recorded in [the Section 13 identity audit](../research/section-13-identity-audit.md); resolve versioned checkpoints, code/data provenance, licences and technical claims before completion. |
| S13-LL-02 | K2 geospatial model | Domain language model | Partial | Identity and initial bibliographic evidence are recorded in [the Section 13 identity audit](../research/section-13-identity-audit.md); resolve versioned checkpoints, code/data provenance, licences and technical claims before completion. |
| S13-LL-03 | GeoGPT | Domain language model/system | Partial | Identity and initial bibliographic evidence are recorded in [the Section 13 identity audit](../research/section-13-identity-audit.md); resolve versioned checkpoints, code/data provenance, licences and technical claims before completion. |
| S13-LL-04 | GeoLLM | Geospatial language model | Partial | Identity and initial bibliographic evidence are recorded in [the Section 13 identity audit](../research/section-13-identity-audit.md); resolve versioned checkpoints, code/data provenance, licences and technical claims before completion. |
| S13-LL-05 | Map-aware instruction-tuned models | Model family | Open | Identify concrete checkpoints and map grounding; test coordinate/topology correctness. |
| S13-LL-06 | Map visual question answering | Multimodal task | Open | Define map type, question taxonomy and answer evidence; benchmark spatial reasoning. |
| S13-LL-07 | Map reading | Vision-language task | Open | Define symbol/scale/orientation tasks and ground truth. |
| S13-LL-08 | Georeferenced map OCR | OCR/georeferencing workflow | Open | Define text extraction, coordinate calibration and uncertainty; test map distortions. |
| S13-LL-09 | Chart/cartographic-style question answering | Multimodal reasoning task | Open | Define chart grammar and spatial reference; evaluate evidence-grounded responses. |
| S13-LL-10 | GeoLLM-Engine | Agent evaluation/tool system | Verify | Resolve exact project and release; document benchmark and tool APIs. |
| S13-LL-11 | GeoBenchX | Geospatial benchmark | Partial | Identity and initial bibliographic evidence are recorded in [the Section 13 identity audit](../research/section-13-identity-audit.md); resolve versioned checkpoints, code/data provenance, licences and technical claims before completion. |
| S13-LL-12 | GIS Copilot-style agents | Agent workflow family | Open | Identify actual systems and tool scopes; test deterministic execution and permissions. |
| S13-LL-13 | SpatialEval | Spatial reasoning benchmark | Verify | Resolve exact benchmark version and task definitions; audit data contamination. |
| S13-LL-14 | GeoQA | Geospatial QA benchmark family | Verify | Disambiguate datasets/projects; document geographic coverage and licence. |
| S13-LL-15 | Natural language to spatial SQL | Agent/compiler workflow | Open | Define schema grounding, SQL validation and query safety; test against exact result oracles. |
| S13-LL-16 | Natural language to PyQGIS | Agent/code-generation workflow | Open | Define API version and sandbox; test generated scripts on synthetic projects. |
| S13-LL-17 | Natural language to GeoPandas | Agent/code-generation workflow | Open | Define supported operations and schema context; execute safely with reproducible fixtures. |
| S13-LL-18 | Natural language to GDAL | Agent/code-generation workflow | Open | Define command allowlist, file safety and CRS checks; validate outputs. |
| S13-LL-19 | Validation and execution sandboxes | Agent safety architecture | Open | Define filesystem/network/resource boundaries and data permissions; test escape attempts. |
| S13-LL-20 | Self-repair loops | Agent control pattern | Open | Define error classification, retry limits and verification; prevent unbounded execution. |
| S13-LL-21 | GeoRAG over STAC catalogs | Retrieval workflow | Open | Define STAC metadata, spatial/time filters and citation grounding; test catalogue updates. |
| S13-LL-22 | Metadata-aware retrieval | Retrieval method | Open | Define metadata ranking and hard filters; evaluate recall/precision. |
| S13-LL-23 | OSM tag reasoning | Geographic knowledge reasoning | Open | Define tag schema/version and geographic context; handle incomplete/conflicting tags. |
| S13-LL-24 | Gazetteer-augmented generation | Geographic entity grounding | Open | Define gazetteer provenance, entity resolution and ambiguity; test hallucination rate. |

### Data-centric GeoAI — page 28

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S13-DC-01 | Label refinement from coarse land cover | Label refinement workflow | Open | Define source/target taxonomy and uncertainty; compare with expert labels. |
| S13-DC-02 | OSM-assisted label refinement | Weak supervision workflow | Open | Define tag mapping, temporal mismatch and coverage bias; audit false labels. |
| S13-DC-03 | Noisy-label correction | Learning method family | Open | Split algorithms by noise model and assumptions; test synthetic corruption. |
| S13-DC-04 | Confident learning for segmentation | Label quality method | Verify | Verify exact confident-learning adaptation; define pixel/instance dependence and calibration. |
| S13-DC-05 | Physically based rendering for synthetic data | Simulation workflow | Not applicable | Define scene/physics/sensor model and provenance; distinguish renderer from data generator. |
| S13-DC-06 | Procedural city generation | Synthetic data workflow | Open | Define grammar/parameters and urban realism; test spatial statistics and licence. |
| S13-DC-07 | Domain randomisation | Simulation/training method | Open | Define randomised factors/distributions; test transfer to real sensor data. |
| S13-DC-08 | Diffusion-generated training tiles | Generative data workflow | Open | Identify model/checkpoint and conditioning; evaluate geographic realism, bias and rights. |
| S13-DC-09 | Dataset distillation | Dataset compression method | Open | Define objective and distilled set; test downstream performance/reproducibility. |
| S13-DC-10 | Core-set selection for imagery | Data selection method | Open | Define diversity/coverage criterion; test label efficiency and spatial leakage. |
| S13-DC-11 | Geographic diversity sampling | Sampling design | Open | Define geographic strata and representation target; quantify omitted regions. |
| S13-DC-12 | Long-tail class handling | Learning strategy family | Open | Split reweighting, resampling and calibration methods; evaluate rare-class recall. |
| S13-DC-13 | SAM-assisted annotation | Annotation workflow | Verify | Resolve SAM model version and human review process; track prompt and edit provenance. |
| S13-DC-14 | Superpixel scribble annotation | Interactive labelling method | Open | Define superpixel algorithm and scribble propagation; test boundary leakage. |
| S13-DC-15 | Interactive segmentation annotation | Annotation workflow | Not applicable | Document human-in-loop interface and quality assurance; evaluate annotator effort. |
| S13-DC-16 | Consensus labelling across annotators | Annotation aggregation | Open | Define adjudication/latent-label model and disagreement; report inter-annotator reliability. |

### Scaling and efficiency — page 28

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S13-SE-01 | Neural scaling laws for EO pretraining | Empirical scaling analysis | Open | Define data/parameter/compute axes and held-out tasks; fit uncertainty-aware scaling curves. |
| S13-SE-02 | Compute-optimal pretraining budgets | Resource optimisation | Open | Define compute, data and model trade-off; reproduce scaling-law assumptions. |
| S13-SE-03 | Data pruning | Data selection method | Open | Define redundancy/utility score; measure performance and geographic coverage impact. |
| S13-SE-04 | Windowed attention | Efficient attention method | Open | Define window geometry and shift; measure memory/accuracy at scene scale. |
| S13-SE-05 | Linear attention | Efficient attention family | Open | Split kernel/normalisation variants; test approximation and stability. |
| S13-SE-06 | State-space models for spatial imagery | Sequence architecture family | Open | Identify architecture and token ordering; test long-range spatial dependency. |
| S13-SE-07 | FlashAttention | Attention kernel/software | Verify | Identify implementation/version and hardware; document exactness and memory behaviour. |
| S13-SE-08 | Resolution-adaptive patching | Tokenisation/inference method | Open | Define patch-size policy and scale transitions; test small-object preservation. |
| S13-SE-09 | Token dropping | Model efficiency method | Open | Define importance score and recovery; test accuracy/calibration under spatially clustered drops. |
| S13-SE-10 | Coarse-to-fine inference cascades | Large-scene workflow | Open | Define coarse trigger and zoom policy; measure recall/compute trade-off. |
| S13-SE-11 | Region-of-interest zoom | Large-scene inference workflow | Open | Define ROI proposal, context margin and scale; test missed-object propagation. |
| S13-SE-12 | Gigapixel streaming | Inference system workflow | Not applicable | Define tiling, overlap, memory and output stitching; validate seams and resource bounds. |

## Completion gates

1. Verify model names, exact releases, checkpoints, training corpora, evaluation papers and licences.
2. Separate foundation-model architectures from embedding workflows, retrieval indexes, evaluation protocols and agent systems.
3. Record sensor, region, temporal coverage, spatial resolution, training-data provenance and geographic split design.
4. Test cross-region, cross-sensor, cross-resolution and temporal transfer; report label-efficiency and uncertainty.
5. For mobility/social modalities, require privacy/legal review and do not expose individual trajectories.
6. For geospatial agents, enforce schema-grounded operations, deterministic validation, sandboxing, resource limits and auditable tool permissions.
7. Review rights for training data, model weights, synthetic assets, benchmark data and derived embeddings.
8. Reconcile canonical records and dashboard only after identity/evidence changes.

**Current conclusion:** Section 13 is decomposed into atomic review items. It remains open; no named model, benchmark or agent system is endorsed or declared verified by this register.
