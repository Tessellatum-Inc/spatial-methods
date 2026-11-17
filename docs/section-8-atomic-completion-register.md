# Section 8 atomic completion register

**Source:** *Spatial Analysis Algorithms: Complete Compendium*, Section 8, pages 14–18.  
**Intake:** [pages 11–15](../source-inventory/pages-11-15.md) and [pages 16–20](../source-inventory/pages-16-20.md).  
**Section index:** [Section 8 catalogue record](../catalog/sections/08-geoai.md).

> The source explicitly describes model names as representative, not exhaustive or verified. Every model, benchmark and deployment claim is a research lead until its exact paper, release, checkpoint, training data and licence are established.

## Status policy

Use the [source-entry verification protocol](../catalog/verification-protocol.md) and [compendium completion standard](compendium-completion-standard.md). Keep architectures, objectives, checkpoints, datasets, software, tasks, metrics and workflows as separate record types. A generic objective implementation does not verify a named foundation model.

| Status | Meaning |
|---|---|
| Open | No item-specific verification/implementation evidence recorded. |
| Partial | A bounded related implementation or lesson exists; source family remains incomplete. |
| Verify | Exact model, paper, release, dataset or variant must be resolved. |
| Not applicable | A workflow, metric, task or infrastructure component is not one standalone algorithm. |

## Atomic source register

### Masked autoencoding and self-supervised objectives — page 15

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S08-SSL-01 | Masked Autoencoder (MAE) | Self-supervised objective/architecture | Partial | Existing masking/restoration teaching package is not a trained MAE; reproduce encoder/decoder objective and benchmark. |
| S08-SSL-02 | SatMAE temporal grouping | EO self-supervised model | Verify | Identify exact paper/checkpoint and temporal grouping; verify training data/licence. |
| S08-SSL-03 | SatMAE spectral grouping | EO self-supervised model | Verify | Verify band grouping and sensor assumptions; test missing bands. |
| S08-SSL-04 | Scale-MAE GSD-aware encoding | EO self-supervised model | Verify | Identify exact model version and GSD encoding; test resolution transfer. |
| S08-SSL-05 | SelectiveMAE | Self-supervised model | Verify | Resolve exact paper/release and masking policy. |
| S08-SSL-06 | S2MAE | Self-supervised model | Verify | Resolve exact project/model and checkpoint; avoid acronym ambiguity. |
| S08-SSL-07 | SpectralGPT 3D masking | Hyperspectral self-supervised model | Verify | Verify architecture, spectral tokenisation and checkpoint. |
| S08-SSL-08 | SimCLR | Contrastive learning method | Verify | Verify augmentation/objective variant; reproduce NT-Xent benchmark. |
| S08-SSL-09 | MoCo | Contrastive learning method | Verify | Split MoCo v1/v2/v3 and queue/momentum variants; test negative dictionary. |
| S08-SSL-10 | DINO | Self-distillation method | Verify | Verify teacher/student centring and sharpening; identify release. |
| S08-SSL-11 | DINOv2 | Self-distillation model | Verify | Identify official model/checkpoint and data; verify licence. |
| S08-SSL-12 | DINOv3 | Self-distillation model | Verify | Identify official release/checkpoint and training protocol; verify licence. |
| S08-SSL-13 | iBOT | Self-distillation/masked prediction | Verify | Verify online tokenizer and patch-level objective; reproduce reference. |
| S08-SSL-14 | BYOL | Self-supervised learning method | Verify | Verify predictor/target EMA and collapse prevention; test no-negative setup. |
| S08-SSL-15 | Barlow Twins | Self-supervised objective | Verify | Verify redundancy-reduction objective and normalization; test invariance. |
| S08-SSL-16 | VICReg | Self-supervised objective | Verify | Verify invariance/variance/covariance terms and scaling. |
| S08-SSL-17 | SeCo | Satellite EO self-supervised model | Verify | Identify exact paper/checkpoint and seasonal contrastive pairs. |
| S08-SSL-18 | SSL4EO | EO self-supervised dataset/model family | Verify | Separate dataset release from pretraining model; verify sensor data and terms. |
| S08-SSL-19 | CROMA | Multimodal SAR/optical model | Verify | Verify model version, modalities and cross-modal objective. |
| S08-SSL-20 | JEPA-style latent prediction | Self-supervised objective family | Open | Identify concrete JEPA variants; define target encoder/predictor and collapse diagnostics. |
| S08-SSL-21 | NT-Xent / InfoNCE | Contrastive objective | Partial | Existing lesson covers objective; verify exact normalisation, temperature and negative sampling. |

### Image-text and multi-sensor foundation models — page 15

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S08-MM-01 | RemoteCLIP | EO vision-language model | Verify | Identify exact paper/release/checkpoint and image-text corpus. |
| S08-MM-02 | GeoRSCLIP | EO vision-language model | Verify | Verify architecture, dataset and checkpoint licence. |
| S08-MM-03 | SkyCLIP | EO vision-language model | Verify | Resolve exact model release and training corpus. |
| S08-MM-04 | SatCLIP | Location-conditioned EO model | Verify | Identify exact paper/checkpoint and coordinate encoding. |
| S08-MM-05 | GeoCLIP | Image-location alignment model | Verify | Identify exact model and evaluation; document geographic bias. |
| S08-MM-06 | CSP | Cross-modal model/objective | Verify | Resolve exact acronym and source; do not infer expansion. |
| S08-MM-07 | Galileo | Multimodal EO foundation model | Verify | Identify exact version and supported modalities; verify weights/licence. |
| S08-MM-08 | DOFA | Dynamic sensor-agnostic EO model | Verify | Identify paper/release and wavelength-conditioned architecture. |
| S08-MM-09 | SkySense | Multisensor EO foundation model | Verify | Resolve exact version and sensor inputs; distinguish from SkySense++ variants. |
| S08-MM-10 | Copernicus-FM | EO foundation model | Verify | Identify official project/release, data and licence. |
| S08-MM-11 | TerraMind | Multimodal Earth observation model | Verify | Verify exact checkpoint, modalities and generation/reasoning tasks. |
| S08-MM-12 | AnySat | Multisensor EO model | Verify | Verify model architecture and modality flexibility; identify release. |
| S08-MM-13 | Panopticon | EO model/project | Verify | Resolve exact model identity and paper; verify checkpoint. |
| S08-MM-14 | AlphaEarth Foundations | Geospatial embedding model/system | Verify | Identify exact product/model release and access terms; document embedding semantics. |
| S08-MM-15 | Clay | EO foundation model | Verify | Identify exact model version and data; verify licence. |
| S08-MM-16 | TESSERA | EO embedding/model project | Verify | Resolve exact release and training data; avoid conflating similarly named projects. |
| S08-MM-17 | Presto | EO time-series model | Verify | Identify checkpoint, temporal encoding and input bands. |
| S08-MM-18 | TiMo | EO temporal model | Verify | Resolve exact project/version and task; confirm model availability. |
| S08-MM-19 | SatlasPretrain | EO pretraining model/dataset | Verify | Separate model weights, corpus and release; document licence. |
| S08-MM-20 | MTP | Multi-task pretraining | Verify | Resolve exact acronym/paper and objective. |
| S08-MM-21 | GFM continual pretraining | Training workflow | Open | Identify concrete recipes and data curation; test catastrophic forgetting. |
| S08-MM-22 | Foundation-model distillation | Model compression/training method | Open | Define teacher/student, objective and evaluation; compare compute/accuracy. |
| S08-MM-23 | Weak supervision from land-cover maps | Training-data workflow | Open | Define taxonomy mapping and label noise; audit temporal mismatch. |
| S08-MM-24 | Weak supervision from OSM | Training-data workflow | Open | Define tag-to-class mapping and coverage bias; validate regionally. |
| S08-MM-25 | Weak supervision from geotagged text | Training-data workflow | Open | Define geolocation precision and semantic labels; privacy/licence review. |
| S08-MM-26 | Deduplicated global tile sampling | Data sampling method | Open | Define overlap/deduplication, spatial strata and sampling weights. |

### Architectures, encodings and decoders — page 15

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S08-AR-01 | Vision Transformer (ViT) | Neural architecture | Verify | Identify architecture version and patch protocol; test resolution handling. |
| S08-AR-02 | Swin Transformer | Hierarchical vision architecture | Verify | Verify window/shift and hierarchy; document model variants. |
| S08-AR-03 | Hierarchical ViT | Architecture family | Open | Split by token hierarchy and pooling; identify concrete models. |
| S08-AR-04 | ConvNeXt | Convolutional architecture | Verify | Identify version and training protocol; verify checkpoint licence. |
| S08-AR-05 | Mamba/state-space encoders | Sequence architecture family | Open | Identify concrete variants and spatial token ordering; test long-range dependencies. |
| S08-AR-06 | RS-Mamba | Remote-sensing state-space model | Verify | Resolve exact paper/release and model weights. |
| S08-AR-07 | Samba | State-space/attention model | Verify | Resolve exact project and architecture; verify EO adaptation. |
| S08-AR-08 | Perceiver-style encoders | Latent bottleneck architecture family | Open | Identify exact variants; document latent query and cross-attention. |
| S08-AR-09 | Mixture-of-experts | Conditional computation architecture | Open | Define gating, expert routing and load balancing; test spatial collapse. |
| S08-AR-10 | Prithvi-EO temporal ViT | EO temporal architecture | Verify | Identify exact checkpoint/release and 3D patch embedding. |
| S08-AR-11 | U-TAE | Temporal attention architecture | Verify | Verify architecture and task; identify official implementation. |
| S08-AR-12 | L-TAE | Lightweight temporal attention | Verify | Verify temporal attention formulation and input protocol. |
| S08-AR-13 | PSE-TAE | Temporal attention architecture | Verify | Resolve exact model and spectral/spatial attention design. |
| S08-AR-14 | ChannelViT | Channel-aware ViT | Verify | Verify model/version and channel tokenisation; test missing channels. |
| S08-AR-15 | DOFA hypernetwork-generated weights | Dynamic sensor adaptation | Verify | Identify exact weight-generation mechanism and checkpoint. |
| S08-AR-16 | FiLM wavelength conditioning | Conditional feature modulation | Open | Define conditioning vector and layer placement; test spectral interpolation. |
| S08-AR-17 | Cross-attention wavelength conditioning | Spectral conditioning method | Open | Identify architecture and band metadata; test sensor transfer. |
| S08-AR-18 | Spectral-band tokens | Spectral encoding method | Open | Define wavelength/band metadata and missing-band handling. |
| S08-AR-19 | 2D sinusoidal positional encoding | Positional encoding | Open | Define coordinate normalisation and frequency scale; test translation behaviour. |
| S08-AR-20 | Learned positional encoding | Positional encoding | Open | Define interpolation to new resolutions; test geographic extrapolation. |
| S08-AR-21 | RoPE | Rotary positional encoding | Verify | Verify 2D/axial variants and coordinate scaling. |
| S08-AR-22 | ALiBi | Attention bias | Verify | Verify slope schedule and spatial extension. |
| S08-AR-23 | Relative positional encoding | Positional encoding family | Open | Split relative bias variants and spatial geometry. |
| S08-AR-24 | GSD-aware encoding | Scale-aware positional encoding | Open | Define GSD units and sensor metadata; test resolution transfer. |
| S08-AR-25 | Day-of-year embedding | Temporal encoding | Open | Define calendar and seasonal periodicity; test leap-year handling. |
| S08-AR-26 | Date embedding | Temporal encoding | Open | Define continuous/discrete time representation; test irregular sampling. |
| S08-AR-27 | U-Net decoder | Segmentation decoder | Verify | Identify variant and skip connections; test output alignment. |
| S08-AR-28 | UPerNet | Segmentation decoder | Verify | Verify pyramid pooling and feature fusion; identify implementation. |
| S08-AR-29 | ViTDet feature pyramids | Detection feature architecture | Verify | Identify exact feature pyramid and windowing implementation. |
| S08-AR-30 | Linear probe | Representation evaluation | Partial | Define frozen encoder and classifier; ensure geographic split and confidence intervals. |
| S08-AR-31 | MLP probe | Representation evaluation | Partial | Define architecture/regularisation; compare with linear probe. |
| S08-AR-32 | Windowed attention | Efficient attention | Open | Define window size/shift and boundary treatment; test seam effects. |
| S08-AR-33 | Token merging | Token efficiency | Open | Identify method and merge metric; evaluate small-object loss. |
| S08-AR-34 | Token pruning | Token efficiency | Open | Define saliency score and recovery; test spatially clustered pruning. |
| S08-AR-35 | Dynamic resolution | Adaptive inference | Open | Define scale policy and output fusion; test consistency. |
| S08-AR-36 | Register tokens | Transformer architecture component | Verify | Identify exact method and purpose; test representation effect. |

### Adaptation, transfer and efficient training — pages 15–16

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S08-AD-01 | LoRA | Parameter-efficient fine-tuning | Verify | Verify rank/target-module choices and merge semantics; test parameter counts. |
| S08-AD-02 | GeoAdapter | Geospatial adapter model | Verify | Resolve exact project/model and adapter architecture. |
| S08-AD-03 | Adapter tuning | Parameter-efficient adaptation | Open | Split adapter architectures and insertion locations; benchmark. |
| S08-AD-04 | Prompt tuning | Parameter-efficient adaptation | Open | Define soft prompt and task protocol; compare frozen/fine-tuned. |
| S08-AD-05 | Visual prompt tuning | Vision adaptation | Verify | Identify VPT shallow/deep variants; verify implementation. |
| S08-AD-06 | In-context learning | Adaptation paradigm | Not applicable | Define task/context protocol; evaluate reproducibility and leakage. |
| S08-AD-07 | Parameter-efficient fine-tuning (PEFT) | Method family | Not applicable | Split LoRA, adapters, prompts and other concrete methods. |
| S08-AD-08 | Few-shot learning | Evaluation/training setting | Not applicable | Define support/query sampling and geographic split; report variance. |
| S08-AD-09 | Zero-shot learning | Evaluation setting | Not applicable | Define label/text prompts and class set; assess geographic bias. |
| S08-AD-10 | Prototypical networks | Few-shot learning algorithm | Verify | Verify prototype distance and episodic training; test class imbalance. |
| S08-AD-11 | Model-Agnostic Meta-Learning (MAML) | Meta-learning algorithm | Verify | Verify inner/outer loop and second-order approximation; test task transfer. |
| S08-AD-12 | Open-set recognition | Recognition setting/method family | Open | Define unknown class and rejection calibration; test open-set metrics. |
| S08-AD-13 | Model merging | Model composition | Open | Identify concrete merge algorithm; test interference and task retention. |
| S08-AD-14 | Task arithmetic | Model composition method | Verify | Verify parameter-delta composition and scaling; test task conflicts. |
| S08-AD-15 | Continual learning | Learning paradigm | Not applicable | Split replay/regularisation/expansion methods; test forgetting. |
| S08-AD-16 | Pruning | Model compression | Open | Define unstructured/structured pruning and recovery; measure hardware latency. |
| S08-AD-17 | Quantization-aware training | Model compression | Verify | Verify quantisation scheme and calibration; test accuracy/hardware. |
| S08-AD-18 | Student-model distillation | Model compression | Open | Define teacher/student logits/features and loss; measure deployment trade-offs. |
| S08-AD-19 | On-board satellite inference | Deployment workflow | Not applicable | Define hardware, power, latency and fault constraints. |
| S08-AD-20 | Edge inference | Deployment workflow | Not applicable | Define device/runtime and model constraints; measure actual deployment. |
| S08-AD-21 | UAV inference | Deployment workflow | Not applicable | Define flight hardware, latency and sensor; assess safety/reliability. |
| S08-TR-01 | Mixed-precision training | Training optimisation | Verify | Verify precision formats and loss scaling; test numerical stability. |
| S08-TR-02 | Gradient checkpointing | Memory optimisation | Verify | Verify recomputation semantics and performance; test gradient parity. |
| S08-TR-03 | FSDP | Distributed training software | Verify | Identify framework/version and sharding semantics; document hardware. |
| S08-TR-04 | DeepSpeed | Distributed training software | Verify | Identify version/ZeRO stage and licence; test reproducibility. |
| S08-TR-05 | FlashAttention | Attention kernel/software | Verify | Identify version/hardware and exactness; measure memory/speed. |
| S08-TR-06 | AdamW | Optimiser | Verify | Verify decoupled weight decay and epsilon/beta conventions. |
| S08-TR-07 | LARS | Optimiser | Verify | Verify trust ratio and exclusions; test large-batch setup. |
| S08-TR-08 | Layer-wise learning-rate decay | Training strategy | Open | Define layer grouping and decay schedule; test sensitivity. |
| S08-TR-09 | EMA teacher | Self-distillation training component | Open | Define update schedule and warmup; test stability. |
| S08-TO-01 | TorchGeo | Geospatial ML software | Verify | Verify version, dataset API and licence; map exact methods to repo. |
| S08-TO-02 | TerraTorch | EO model toolkit | Verify | Verify project/release and supported model/data APIs. |
| S08-TO-03 | Tiled/sliding-window inference | Large-scene inference workflow | Partial | Existing general inference components do not close this named workflow; define tile overlap and global stitching. |
| S08-TO-04 | Gaussian blending of tile predictions | Tile aggregation method | Open | Define window weights and edge coverage; test seam-free reconstruction. |
| S08-TO-05 | Vector databases | Retrieval infrastructure | Not applicable | Document embedding schema, index metric, update and spatial filtering. |
| S08-TO-06 | Embedding caches | Retrieval infrastructure | Not applicable | Define cache key, model version and invalidation. |

### Downstream vision tasks — page 16

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S08-DT-01 | U-Net segmentation | Segmentation architecture | Verify | Identify exact variant; compare with transparent baseline. |
| S08-DT-02 | DeepLab | Segmentation architecture | Verify | Identify version/backbone and ASPP configuration. |
| S08-DT-03 | Mask2Former | Universal segmentation architecture | Verify | Identify checkpoint/version and task protocol. |
| S08-DT-04 | UPerNet | Segmentation decoder | Verify | Identify implementation and backbone. |
| S08-DT-05 | SAM geospatial adaptations | Promptable segmentation family | Verify | Split RSPrompter, SAMGeo and other adaptations; identify versions. |
| S08-DT-06 | SAM 2 geospatial adaptations | Video/promptable segmentation family | Verify | Identify SAM 2 release and temporal tracking semantics. |
| S08-DT-07 | RSPrompter | Remote-sensing SAM adaptation | Verify | Verify paper, checkpoint and prompt strategy. |
| S08-DT-08 | SAMGeo | Geospatial SAM software | Verify | Verify release, API, licence and supported outputs. |
| S08-DT-09 | Oriented R-CNN | Oriented object detection | Verify | Verify rotated-box parameterisation and code. |
| S08-DT-10 | RoI Transformer | Oriented detection architecture | Verify | Verify feature transformation and box refinement. |
| S08-DT-11 | ReDet | Rotation-equivariant detector | Verify | Verify exact release and orientation representation. |
| S08-DT-12 | DETR variants | Detection architecture family | Open | Split Deformable DETR, DINO/other variants and rotated adaptations. |
| S08-DT-13 | YOLO family | Detection architecture family | Verify | Pin version and task; avoid generic name as one algorithm. |
| S08-DT-14 | Siamese change detection | Change detection architecture family | Open | Define feature sharing, differencing and temporal pairing. |
| S08-DT-15 | ChangeFormer | Change detection model | Verify | Identify exact paper/checkpoint and input protocol. |
| S08-DT-16 | BIT | Change detection model | Verify | Resolve exact model/version and token aggregation. |
| S08-DT-17 | SNUNet | Change detection architecture | Verify | Verify nested U-Net variant and training setup. |
| S08-DT-18 | Cloud masking | EO task | Not applicable | Define cloud/shadow taxonomy, sensor and benchmark. |
| S08-DT-19 | Flood mapping | EO task | Not applicable | Define event/extent labels and water/urban context. |
| S08-DT-20 | Burn-scar mapping | EO task | Not applicable | Define spectral/temporal reference and severity. |
| S08-DT-21 | Crop-type mapping | EO task | Not applicable | Define crop taxonomy, season and label source. |
| S08-DT-22 | Canopy-height regression | EO task | Not applicable | Define target height, reference lidar and uncertainty. |
| S08-DT-23 | Building extraction | EO task | Not applicable | Define footprint geometry and topology metrics. |
| S08-DT-24 | D-LinkNet | Road extraction architecture | Verify | Identify exact paper/release and backbone. |
| S08-DT-25 | HRNet | Vision architecture | Verify | Identify exact HRNet variant/task head. |
| S08-DT-26 | RoadTracer | Road graph extraction algorithm | Verify | Verify graph-tracing method and benchmark. |
| S08-DT-27 | PolyWorld | Polygon extraction architecture | Verify | Verify vertex/edge representation and checkpoint. |
| S08-DT-28 | HiSup | Polygon extraction model | Verify | Resolve exact paper/release and output topology. |
| S08-DT-29 | Field-boundary extraction | EO task | Not applicable | Define boundary label, topology and field survey validation. |
| S08-DT-30 | Monocular height estimation | 3D attribute task | Open | Define scale reference and sensor; validate metric height. |
| S08-DT-31 | Monocular depth estimation | Vision task | Open | Define depth scale and domain; test geometric consistency. |
| S08-DT-32 | SRGAN | Super-resolution architecture | Verify | Verify generator/discriminator and loss; test spectral fidelity. |
| S08-DT-33 | Diffusion super-resolution | Generative restoration | Open | Identify exact model and scale; test hallucination/uncertainty. |
| S08-DT-34 | DiffusionSat | EO generative model | Verify | Identify paper/release and checkpoint; document task. |
| S08-DT-35 | CycleGAN | Unpaired image translation | Verify | Verify objective and cycle-consistency assumptions; test spectral drift. |
| S08-DT-36 | Pix2Pix | Conditional image translation | Verify | Verify paired-data and adversarial loss setup. |
| S08-DT-37 | Variational autoencoders (VAE) | Generative model family | Open | Specify likelihood, latent prior and objective. |
| S08-DT-38 | VQGAN | Vector-quantised generative model | Verify | Identify exact architecture/codebook and checkpoint. |
| S08-DT-39 | Cloud removal | Restoration task | Not applicable | Define cloudy input/reference and observation consistency. |
| S08-DT-40 | Sensor translation | Domain translation task | Not applicable | Define source/target sensor response and physical consistency. |
| S08-DT-41 | Synthetic EO data generation | Data synthesis workflow | Not applicable | Define scene/physics/provenance and rights. |
| S08-DT-42 | SegEarth-OV | Open-vocabulary segmentation model | Verify | Identify exact project/release/checkpoint and vocabulary. |
| S08-DT-43 | MapTR | Vectorised HD map architecture | Verify | Verify exact version, map element representation and benchmark. |
| S08-DT-44 | VectorMapNet | Vector map construction architecture | Verify | Verify paper/checkpoint and topology metrics. |
| S08-DT-45 | BEVFormer | Bird's-eye-view perception architecture | Verify | Identify version and sensor/camera setup. |
| S08-DT-46 | NetVLAD | Visual place recognition | Verify | Verify pooling architecture and training objective. |
| S08-DT-47 | MixVPR | Visual place recognition | Verify | Identify release/checkpoint and descriptor protocol. |
| S08-DT-48 | CosPlace | Visual place recognition | Verify | Verify classification-based training and geographic evaluation. |
| S08-DT-49 | SALAD | Visual place recognition | Verify | Identify exact model/version and aggregation. |
| S08-DT-50 | PlaNet | Image geolocation model | Verify | Verify original task, dataset and geographic error metrics. |
| S08-DT-51 | StreetCLIP | Geospatial vision-language model | Verify | Identify exact release and training data; audit bias. |
| S08-DT-52 | G3 | Image geolocation model | Verify | Resolve exact acronym/model and evaluation. |
| S08-DT-53 | Cross-view matching | Geolocation task family | Open | Split satellite-to-ground/aerial and model variants; evaluate pose and geographic generalisation. |

### Vision-language, agents and geographic reasoning — page 16

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S08-VL-01 | GeoChat | Remote-sensing VLM | Verify | Identify exact release/checkpoint and training data. |
| S08-VL-02 | EarthGPT | Remote-sensing VLM | Verify | Resolve exact model/paper and modalities. |
| S08-VL-03 | LHRS-Bot | Remote-sensing VLM | Verify | Identify project/release and benchmark. |
| S08-VL-04 | SkyEyeGPT | Remote-sensing VLM | Verify | Verify checkpoint, data and tasks. |
| S08-VL-05 | RSGPT | Remote-sensing VLM | Verify | Resolve exact model and release. |
| S08-VL-06 | VHM | Remote-sensing VLM | Verify | Resolve acronym and project identity. |
| S08-VL-07 | TEOChat | Remote-sensing VLM | Verify | Identify exact model/release and data. |
| S08-VL-08 | EarthDial | Remote-sensing VLM/dataset | Verify | Separate model from instruction dataset; verify release/licence. |
| S08-VL-09 | RemoteSAM | Remote-sensing segmentation system | Verify | Identify exact release and model; distinguish from SAM adaptations. |
| S08-VL-10 | GeoSAM | Geospatial segmentation model/software | Verify | Disambiguate project and version. |
| S08-VL-11 | Image captioning | Vision-language task | Not applicable | Define caption taxonomy and factuality evaluation. |
| S08-VL-12 | Visual question answering | Multimodal task | Not applicable | Define question types, evidence and benchmark. |
| S08-VL-13 | Visual grounding | Multimodal task | Not applicable | Define spatial grounding target and accuracy. |
| S08-VL-14 | Geo-VLM reasoning benchmarks | Evaluation suite family | Open | Identify concrete benchmark/task versions; audit contamination. |
| S08-VL-15 | Chain-of-thought VLM prompting | Reasoning/prompting method | Open | Define reproducible protocol and faithfulness evaluation. |
| S08-VL-16 | GRPO-style RL for geo-VLMs | Model optimisation | Verify | Identify exact implementation and reward; test reward hacking. |
| S08-AG-01 | LLM text-to-SQL agents | Agent workflow | Open | Define schema grounding, SQL safety and result validation. |
| S08-AG-02 | LLM text-to-GIS agents | Agent workflow | Open | Define GIS operation contract, CRS validation and sandbox. |
| S08-AG-03 | LLM-Geo | Geospatial agent/model | Verify | Resolve exact project and version. |
| S08-AG-04 | GeoAgent | Geospatial agent/model | Verify | Resolve exact project and tool set. |
| S08-AG-05 | GeoGPT | Geospatial language model/system | Verify | Disambiguate project name and release. |
| S08-AG-06 | PyQGIS code generation | Agent/code generation workflow | Open | Pin QGIS API version; execute in isolated project fixture. |
| S08-AG-07 | GeoPandas code generation | Agent/code generation workflow | Open | Pin library version and schema; run generated code against test data. |
| S08-AG-08 | Tool-calling agents | Agent architecture | Not applicable | Define tool schemas, permissions and audit logs. |
| S08-AG-09 | MCP-based geospatial agents | Agent integration architecture | Not applicable | Define server capabilities, scopes and deterministic validation. |
| S08-AG-10 | GeoRAG | Retrieval-augmented generation | Verify | Resolve exact project; define document/layer retrieval and citations. |
| S08-AG-11 | Dense retrieval over layers and metadata | Retrieval workflow | Open | Define embeddings, filters and relevance evaluation. |
| S08-GR-01 | Geographic knowledge probing | Model evaluation task | Open | Define factual question set, source truth and temporal validity. |
| S08-GR-02 | GeoLLM | Geographic reasoning model/system | Verify | Disambiguate exact paper/project and benchmark. |
| S08-GR-03 | LLM geolocation | Language-based geolocation task | Open | Define target granularity, uncertainty and privacy risk. |
| S08-GR-04 | Geocoding with language models | Geocoding workflow | Open | Ground outputs in gazetteer and report candidate confidence. |
| S08-GR-05 | Toponym resolution | Geographic entity linking | Open | Define candidate set, context and multilingual names. |
| S08-GR-06 | Spatial reasoning/mental-map prompting | Reasoning task | Open | Define reference frame and metric evaluation; test directional consistency. |
| S08-GR-07 | Vision-language navigation | Navigation task | Open | Define map/scene inputs, action space and safety; evaluate route completion. |

### Location encoders and representation learning — page 17

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S08-LE-01 | Space2Vec | Location encoding model | Verify | Identify exact paper and basis; test spatial generalisation. |
| S08-LE-02 | Sphere2Vec | Spherical location encoding | Verify | Verify spherical basis and coordinate convention. |
| S08-LE-03 | Theory | Location representation method | Verify | Resolve exact project/name and formulation. |
| S08-LE-04 | Grid encoding | Location encoding family | Open | Define grid scale and hierarchy; compare with continuous coordinates. |
| S08-LE-05 | Wrap encoding | Location encoding method | Verify | Resolve exact method and periodic boundary semantics. |
| S08-LE-06 | RBF location encoding | Radial basis representation | Open | Define centres, bandwidth and normalisation; test extrapolation. |
| S08-LE-07 | Spherical harmonics | Spherical representation | Verify | Verify basis normalisation/order and coordinate convention. |
| S08-LE-08 | Spherical Fourier features | Spherical representation | Open | Define spectral sampling and rotation behaviour; test approximation. |
| S08-LE-09 | SINR species-range model | Species distribution/location representation | Verify | Resolve exact model, acronym and paper; verify ecological use. |
| S08-LE-10 | Multi-scale sinusoidal features | Coordinate representation | Open | Define frequency schedule and scale; test translation/aliasing. |
| S08-LE-11 | Random Fourier features | Kernel/coordinate representation | Partial | Existing generic method may exist elsewhere; verify spatial basis and kernel assumptions. |
| S08-LE-12 | Poincaré hyperbolic embeddings | Geometric representation | Verify | Define curvature and optimisation; test distance and numerical stability. |
| S08-LE-13 | Tile2Vec | EO representation learning | Verify | Identify paper/checkpoint and tile triplet protocol. |
| S08-LE-14 | Place2Vec | Place representation | Verify | Resolve exact model and geographic context. |
| S08-LE-15 | Urban2Vec | Urban representation | Verify | Identify project/version and training data. |
| S08-LE-16 | Geo2Vec | Geographic representation | Verify | Disambiguate exact project and embedding semantics. |
| S08-LE-17 | H3 token embeddings | Spatial index embedding | Open | Define H3 version/resolution and hierarchy; test cell-boundary effects. |
| S08-LE-18 | Geohash token embeddings | Spatial index embedding | Open | Define precision and token sequence; test neighbouring-cell discontinuity. |
| S08-LE-19 | Node2Vec on geographic graphs | Graph representation | Verify | Verify random-walk bias and graph construction. |
| S08-LE-20 | DeepWalk on geographic graphs | Graph representation | Verify | Verify walk/context objective and graph semantics. |
| S08-LE-21 | LINE on geographic graphs | Graph representation | Verify | Verify first/second-order proximity objectives. |
| S08-LE-22 | TransE on geographic knowledge graphs | Knowledge graph embedding | Verify | Define relation translation and spatial predicates; test link prediction. |
| S08-LE-23 | RotatE on geographic knowledge graphs | Knowledge graph embedding | Verify | Verify complex rotation and relation patterns; test link prediction. |

### Spatiotemporal and Earth-system deep learning — page 17

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S08-ST-01 | Graph Convolutional Network (GCN) | Graph neural architecture | Verify | Verify normalisation and spectral/spatial variants; test graph transfer. |
| S08-ST-02 | Graph Attention Network (GAT) | Graph neural architecture | Verify | Verify attention normalisation and multi-head variants. |
| S08-ST-03 | GraphSAGE | Graph neural architecture | Verify | Verify sampling/aggregation and inductive setting. |
| S08-ST-04 | Temporal Graph Network (TGN) | Temporal graph architecture | Verify | Verify memory/update and event-time protocol. |
| S08-ST-05 | Spatiotemporal GCN | Graph time-series model family | Open | Split exact ST-GCN variants and adjacency construction. |
| S08-ST-06 | KCN | GNN kriging model | Verify | Resolve exact paper/model and covariance assumptions. |
| S08-ST-07 | IGNNK | GNN kriging/imputation model | Verify | Verify architecture, task and benchmark. |
| S08-ST-08 | SATCN | GNN kriging model | Verify | Resolve exact acronym and model identity. |
| S08-ST-09 | ConvLSTM | Spatiotemporal recurrent architecture | Verify | Verify convolutional state update and sequence protocol. |
| S08-ST-10 | PredRNN | Video prediction architecture | Verify | Identify exact version and memory mechanism. |
| S08-ST-11 | SimVP | Video prediction architecture | Verify | Identify model version and benchmark. |
| S08-ST-12 | Earthformer | Earth-system transformer | Verify | Verify cuboid attention architecture and release. |
| S08-ST-13 | Neural ODEs | Neural differential equation | Open | Define continuous-time dynamics and solver; test gradient accuracy. |
| S08-ST-14 | Neural fields | Continuous neural representation | Open | Define coordinate domain and conditioning; evaluate interpolation/extrapolation. |
| S08-ST-15 | Implicit neural representations | Continuous function representation | Open | Split SDF/occupancy/radiance fields; define regularisation. |
| S08-ST-16 | Neural Hawkes process | Neural point process | Verify | Verify conditional intensity and likelihood; test event simulation. |
| S08-ST-17 | FourCastNet | Weather model | Verify | Identify version/checkpoint and forecast protocol. |
| S08-ST-18 | Pangu-Weather | Weather model | Verify | Verify release and data/training assumptions. |
| S08-ST-19 | GraphCast | Weather model | Verify | Verify model release, inputs and evaluation. |
| S08-ST-20 | GenCast | Probabilistic weather model | Verify | Verify checkpoint, ensemble generation and calibration. |
| S08-ST-21 | FuXi | Weather model family | Verify | Identify exact variant and forecast horizon. |
| S08-ST-22 | FengWu | Weather model | Verify | Verify paper/release and data. |
| S08-ST-23 | Aurora | Earth-system foundation model | Verify | Identify exact version, tasks and licence. |
| S08-ST-24 | ClimaX | Climate model architecture | Verify | Verify model/checkpoint and variable conditioning. |
| S08-ST-25 | Prithvi WxC | Weather/climate model | Verify | Identify official release and checkpoint. |
| S08-ST-26 | NeuralGCM | Hybrid numerical/ML model | Verify | Verify formulation and code release; test physical diagnostics. |
| S08-ST-27 | NowcastNet | Precipitation nowcasting model | Verify | Identify model version and forecast evaluation. |
| S08-ST-28 | DGMR | Generative precipitation nowcasting | Verify | Verify model/checkpoint and probabilistic metrics. |
| S08-ST-29 | MetNet | Precipitation nowcasting model | Verify | Identify version and input/output protocol. |
| S08-ST-30 | Fourier Neural Operator (FNO) | Neural operator | Verify | Verify spectral convolution and boundary handling. |
| S08-ST-31 | DeepONet | Neural operator | Verify | Verify branch/trunk formulation and operator learning. |
| S08-ST-32 | Physics-informed neural networks (PINNs) | Physics-informed learning | Open | Define PDE residual, boundary/initial conditions and loss scaling. |
| S08-ST-33 | CorrDiff | Generative downscaling model | Verify | Identify exact release and conditioning; evaluate extremes. |
| S08-ST-34 | Earth-system world models/emulators | Model family | Open | Identify concrete systems and target solvers; test physical consistency. |
| S08-ST-35 | Spherical CNNs | Spherical architecture family | Open | Define sphere sampling and equivariance; test rotations. |
| S08-ST-36 | DeepSphere | Spherical CNN model | Verify | Verify exact implementation and HEALPix graph. |
| S08-ST-37 | Icosahedral convolutions | Spherical architecture | Open | Define mesh and convolution; test rotation/equivariance. |
| S08-ST-38 | HEALPix convolutions | Spherical architecture | Open | Define pixel neighbourhood and resolution; test seam/pole behaviour. |
| S08-ST-39 | Equivariant message passing | Geometric graph learning | Open | Define group action and feature types; test equivariance numerically. |
| S08-ST-40 | 3D Gaussian splatting | 3D representation/rendering | Verify | Verify optimisation, projection and depth ordering; assess geospatial coordinate integration. |

### Spatial machine learning and hybrid statistics — page 17

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S08-ML-01 | Geographically weighted random forest | Spatial ML method | Open | Define local training/kernel and bandwidth; spatially blocked validation. |
| S08-ML-02 | RFsp | Spatial random forest method | Verify | Verify exact RFsp formulation and feature construction. |
| S08-ML-03 | Spatial stacking | Ensemble method | Open | Define spatial folds and meta-learner; prevent leakage. |
| S08-ML-04 | Kriging plus ML residuals | Hybrid geostatistical model | Open | Define residual variogram and cross-fitting; compare with universal kriging. |
| S08-ML-05 | Spatial kNN | Spatial prediction method | Open | Define distance/feature metric and spatial support; test extrapolation. |
| S08-ML-06 | GNNWR | Geographically weighted neural regression | Verify | Resolve exact paper/model and local parameterisation. |
| S08-ML-07 | GWNN | Geographically weighted neural network | Verify | Resolve exact acronym and architecture. |
| S08-ML-08 | Deep kriging | Hybrid spatial prediction | Open | Identify concrete formulation and covariance; calibrate uncertainty. |
| S08-ML-09 | Deep Gaussian processes | Probabilistic model family | Open | Define layers/inducing points and posterior; test calibration. |
| S08-ML-10 | Neural Gaussian processes | Probabilistic model family | Open | Resolve exact model and likelihood; compare with GP. |
| S08-ML-11 | Spatial Lag Neural Networks | Spatial neural model | Verify | Resolve exact paper and spatial lag mechanism. |
| S08-ML-12 | TabPFN on spatial features | Foundation tabular model adaptation | Verify | Identify version and adaptation; compare spatially blocked baseline. |
| S08-ML-13 | Buffer-statistic feature engineering | Feature construction | Partial | Existing object-based features do not cover generic buffers; define geometry and aggregation. |
| S08-ML-14 | Distance-to-feature features | Feature construction | Open | Define geodesic/network distance and missing-feature handling. |
| S08-ML-15 | Spatial lag features | Feature construction | Partial | Existing spatial econometric lag package tested; define weights and leakage controls. |
| S08-ML-16 | Positive-unlabelled learning | Weak supervision | Verify | Identify exact PU risk estimator and class-prior assumptions. |
| S08-ML-17 | One-class SVM | Anomaly/novelty detection | Verify | Verify kernel and nu parameter; test spatial generalisation. |
| S08-ML-18 | Noisy-label learning | Learning method family | Open | Split noise transition, robust loss and sample selection methods. |
| S08-ML-19 | FixMatch | Semi-supervised learning | Verify | Verify consistency/threshold protocol; document geospatial augmentation. |
| S08-ML-20 | Active learning | Learning strategy family | Partial | Existing sampling primitives are bounded; define query, annotation and retraining loop. |
| S08-ML-21 | LSTM plus process model (hydrology) | Hybrid process-ML model | Open | Identify exact process model and coupling; test mass balance. |
| S08-ML-22 | LSTM plus process model (crop modelling) | Hybrid process-ML model | Open | Define crop state/process and learned residual; validate seasonally. |

### Losses, augmentation, evaluation and validity — pages 17–18

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S08-LS-01 | Dice loss | Segmentation loss | Verify | Define smoothing/empty-class convention; test gradients. |
| S08-LS-02 | Tversky loss | Segmentation loss | Verify | Define alpha/beta and class imbalance; test limiting cases. |
| S08-LS-03 | Focal loss | Classification loss | Verify | Define gamma/alpha and logits convention; test gradients. |
| S08-LS-04 | Lovász-softmax | IoU surrogate loss | Verify | Verify sorted-error construction and class averaging. |
| S08-LS-05 | Class-balanced cross-entropy | Classification loss | Open | Define effective-number weighting and class prior. |
| S08-LS-06 | Boundary loss | Segmentation loss | Open | Define distance transform and sign; test boundary gradient. |
| S08-LS-07 | Distance-transform loss | Segmentation loss | Open | Define target distance and truncation; test empty masks. |
| S08-LS-08 | clDice | Topology-aware segmentation metric/loss | Verify | Verify skeleton precision/sensitivity formulation; test thin structures. |
| S08-LS-09 | Huber loss | Robust regression loss | Verify | Define delta and scaling; test transition to L2/L1. |
| S08-LS-10 | Quantile loss | Probabilistic regression loss | Verify | Define pinball convention and quantile crossing. |
| S08-LS-11 | Pinball loss | Quantile regression loss | Verify | Confirm equivalence/convention with quantile loss and residual sign. |
| S08-AU-01 | Rotation augmentation | Data augmentation | Not applicable | Define allowed rotations by sensor/target; document invariance assumptions. |
| S08-AU-02 | Flip augmentation | Data augmentation | Not applicable | Define axis and orientation semantics; avoid invalid directional flips. |
| S08-AU-03 | Scale jitter | Data augmentation | Not applicable | Define GSD/resampling and label transformation. |
| S08-AU-04 | CutMix | Data augmentation | Verify | Verify mask/bbox mixing and label weighting. |
| S08-AU-05 | Mosaic augmentation | Data augmentation | Verify | Define tile composition and coordinate metadata; test object clipping. |
| S08-AU-06 | Copy-paste augmentation | Data augmentation | Open | Define instance mask blending and context; assess synthetic artefacts. |
| S08-AU-07 | Spectral jitter | EO augmentation | Open | Define band-specific perturbations and physical limits. |
| S08-AU-08 | Band dropout | EO augmentation | Open | Define missing-band simulation and model input mask. |
| S08-AU-09 | Cloud simulation | EO augmentation | Open | Define cloud optical properties and sensor response; validate realism. |
| S08-AU-10 | Shadow simulation | EO augmentation | Open | Define solar geometry and cloud/terrain shadows; validate. |
| S08-AU-11 | Test-time augmentation | Inference ensemble | Not applicable | Define transform aggregation and inverse mapping; test calibration. |
| S08-ME-01 | Overall accuracy | Classification metric | Partial | Existing accuracy package includes OA; define sample weighting and uncertainty. |
| S08-ME-02 | F1 score | Classification metric | Partial | Existing package includes per-class/macro F1; define averaging. |
| S08-ME-03 | IoU / mean IoU | Segmentation metric | Partial | Existing package includes per-class/mIoU; define empty class convention. |
| S08-ME-04 | Dice score | Segmentation metric | Partial | Existing package includes Dice; distinguish macro/micro. |
| S08-ME-05 | Cohen's kappa | Classification agreement metric | Partial | Existing package includes kappa; document prevalence limitations. |
| S08-ME-06 | Rotated IoU | Oriented geometry metric | Open | Define polygon/rotated-box intersection and angle convention. |
| S08-ME-07 | Mean average precision (mAP) | Detection metric | Open | Define IoU thresholds, class averaging and confidence interpolation. |
| S08-ME-08 | Boundary F-score | Segmentation boundary metric | Partial | Existing tolerance-aware binary boundary F1 is bounded; define tolerance/geometry. |
| S08-ME-09 | Panoptic Quality | Panoptic segmentation metric | Open | Verify matching threshold and SQ/RQ decomposition. |
| S08-ME-10 | RMSE | Regression metric | Partial | Tested finite paired-observation implementation with optional non-negative sample weights and analytic tests: [accuracy-assessment package](../implementations/python/accuracy-assessment/README.md). Forecast aggregation and spatial support remain open. |
| S08-ME-11 | MAE | Regression metric | Partial | Tested weighted/unweighted mean absolute error with input validation: [accuracy-assessment package](../implementations/python/accuracy-assessment/README.md). Design-based aggregation and missing-data policies remain study-specific. |
| S08-ME-12 | R-squared | Regression metric | Partial | Tested weighted coefficient of determination with explicit finite constant-target convention: [accuracy-assessment package](../implementations/python/accuracy-assessment/README.md). Out-of-sample spatial evaluation protocol remains open. |
| S08-ME-13 | Nash–Sutcliffe efficiency (NSE) | Hydrology metric | Partial | Tested weighted NSE with observed-mean denominator and explicit constant-observation convention: [accuracy-assessment package](../implementations/python/accuracy-assessment/README.md). Missing-data and hydrological event aggregation remain application-specific. |
| S08-ME-14 | Kling–Gupta efficiency (KGE) | Hydrology metric | Partial | Tested KGE 2009 with correlation, variability and bias components; undefined zero-variance/zero-mean cases return None: [accuracy-assessment package](../implementations/python/accuracy-assessment/README.md). Modified KGE variants remain open. |
| S08-ME-15 | CRPS | Probabilistic forecast metric | Partial | Tested empirical ensemble CRPS with variable ensemble size and optional case weights: [accuracy-assessment package](../implementations/python/accuracy-assessment/README.md). Parametric/continuous-distribution estimators and forecast calibration remain open. |
| S08-ME-16 | Expected Calibration Error (ECE) | Calibration metric | Partial | Tested top-label ECE with equal-width confidence bins and optional sample weights: [accuracy-assessment package](../implementations/python/accuracy-assessment/README.md). Adaptive/classwise estimators and bin/sample-size bias analysis remain open. |
| S08-EV-01 | Linear probing | Representation evaluation | Partial | Define frozen encoder and geographic split. |
| S08-EV-02 | kNN probing | Representation evaluation | Partial | Define embedding normalisation and k; compare with linear probe. |
| S08-EV-03 | Recall@k retrieval | Retrieval metric | Partial | Tested macro query-level recall@k with deterministic duplicate handling and explicit empty-relevance policy: [accuracy-assessment package](../implementations/python/accuracy-assessment/README.md). Benchmark relevance definitions and geographic strata remain open. |
| S08-EV-04 | Normalised Mutual Information (NMI) | Clustering metric | Partial | Tested arithmetic-normalised mutual information with permutation-invariant cluster labels and constant-partition handling: [accuracy-assessment package](../implementations/python/accuracy-assessment/README.md). Benchmark-specific clustering protocols remain open. |
| S08-EV-05 | Spatial block cross-validation | Spatial validation design | Partial | Existing block splitter is bounded; select block scale scientifically. |
| S08-EV-06 | Leave-location-out validation | Spatial validation design | Partial | Define location grouping and buffer; test transfer. |
| S08-EV-07 | Autocorrelation-aware sampling/loss | Validation/training method | Open | Define dependence model and sampling design; test calibration. |
| S08-EV-08 | Domain-Adversarial Neural Network (DANN) | Domain adaptation | Verify | Verify adversarial objective and domain labels; test negative transfer. |
| S08-EV-09 | CORAL | Domain adaptation | Verify | Verify covariance alignment and variants; test feature shift. |
| S08-EV-10 | Test-time adaptation | Domain adaptation family | Open | Split entropy/minimisation/statistics methods; assess online instability. |
| S08-EV-11 | Covariate shift correction | Statistical adaptation | Open | Define density ratio and positivity; test weighted calibration. |
| S08-EV-12 | Importance weighting | Statistical adaptation | Open | Define ratio estimation/clipping; evaluate variance. |
| S08-EV-13 | Out-of-distribution detection | Robustness method family | Open | Split score types and calibration; test geographic novelty. |
| S08-EV-14 | Area of applicability | Applicability diagnostic | Partial | Existing nearest-neighbour feature-space envelope is bounded; verify reference method and thresholds. |
| S08-UN-01 | Monte Carlo dropout | Uncertainty method | Open | Define stochastic layers and sample count; test calibration. |
| S08-UN-02 | Deep ensembles | Uncertainty method | Open | Define ensemble diversity and compute; test coverage. |
| S08-UN-03 | Conformal prediction | Uncertainty method family | Partial | Existing spatial block conformal is bounded; document exchangeability assumptions. |
| S08-UN-04 | Evidential deep learning | Uncertainty method | Open | Identify likelihood/evidence formulation; test overconfidence. |
| S08-UN-05 | Bayesian neural networks | Bayesian model family | Open | Define posterior approximation and calibration. |
| S08-UN-06 | SWAG | Bayesian weight approximation | Verify | Verify covariance approximation and sampling. |
| S08-UN-07 | Laplace approximation | Bayesian approximation | Partial | Existing approximate inference baseline bounded; verify Hessian/curvature and prior. |
| S08-UN-08 | Temperature scaling | Calibration method | Open | Define validation set and scalar optimisation; test class-wise calibration. |
| S08-XAI-01 | SHAP | Feature attribution family | Verify | Identify exact explainer and background distribution; test consistency. |
| S08-XAI-02 | GeoShapley | Spatial attribution method | Verify | Verify exact paper and spatial dependence assumptions. |
| S08-XAI-03 | LIME | Local surrogate explanation | Verify | Define perturbation and locality kernel; test stability. |
| S08-XAI-04 | Grad-CAM | Visual attribution | Verify | Verify target layer and gradient weighting; test localisation. |
| S08-XAI-05 | Integrated gradients | Attribution method | Verify | Define baseline and integration steps; test completeness. |
| S08-XAI-06 | Attention rollout | Transformer attribution | Verify | Verify attention aggregation and residual handling; do not equate with causal explanation. |
| S08-XAI-07 | TCAV | Concept-based explanation | Verify | Verify concept examples and statistical test. |
| S08-XAI-08 | Probing | Representation analysis | Not applicable | Define probe capacity and controls; distinguish diagnostic from explanation. |
| S08-XAI-09 | Spatial partial dependence | Model interpretation | Open | Define spatial dependence caveats and conditional alternatives. |
| S08-XAI-10 | Accumulated Local Effects (ALE) | Model interpretation | Verify | Verify binning/centering and correlated-feature assumptions. |
| S08-XAI-11 | Counterfactual explanations | Explanation method family | Open | Define feasible geographic changes and causal plausibility. |
| S08-FA-01 | Geographic generalisation-gap audit | Fairness/evaluation | Open | Define geographic groups, support and confidence intervals. |
| S08-FA-02 | Spatial fairness metrics | Fairness evaluation | Open | Define group, outcome and normative criterion. |
| S08-FA-03 | Training-data coverage audit | Data representativeness | Partial | Existing group coverage metrics are not a full geographic audit; add label/sensor/time coverage. |
| S08-FA-04 | Federated learning on spatial data | Distributed learning | Open | Define client geography, non-IID shift and privacy threat. |
| S08-FA-05 | Privacy-preserving spatial training | Privacy-preserving ML | Open | Define threat model, privacy budget and utility. |
| S08-FA-06 | EO foundation-model scaling laws | Empirical scaling analysis | Open | Define compute/data/model axes and benchmark; fit uncertainty-aware scaling. |

## Completion gates

1. Verify every named model against primary paper, official repository, model card and exact checkpoint; record hashes and licences.
2. Verify dataset provenance, sensor coverage, annotation terms, train/test splits and benchmark protocol.
3. For architecture/objective families, specify exact tensor shapes, loss, augmentations, optimisation and inference.
4. Evaluate geographic, temporal, sensor, resolution and spectral transfer with leakage-safe splits.
5. Compare foundation models to transparent task-specific and classical baselines; report compute and label budgets.
6. For generative models, test observation consistency, uncertainty, hallucination and physical plausibility.
7. For agentic workflows, enforce tool permissions, sandboxing, schema validation and reproducible execution.
8. Reconcile model catalogue, canonical lessons, implementation packages, tests, notebooks, provenance and rights after evidence changes.

**Current conclusion:** Section 8 is decomposed into atomic review items. It remains open; the register is not a verified model catalogue or endorsement of any checkpoint.
