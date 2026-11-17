# Section 5 atomic completion register

**Source:** *Spatial Analysis Algorithms: Complete Compendium*, Section 5, pages 7–10.  
**Intake:** [preserved pages 6–10 transcription](../source-inventory/pages-06-10.md).  
**Section index:** [Section 5 catalogue record](../catalog/sections/05-remote-sensing.md).

This register decomposes the source's grouped EO, SAR, LiDAR and photogrammetry methods. Use the [verification protocol](../catalog/verification-protocol.md) and [completion standard](compendium-completion-standard.md). Sensor-specific workflows require explicit calibration, version, data provenance and independent validation.

| Status | Meaning |
|---|---|
| Open | No item-specific independent evidence recorded. |
| Partial | A bounded related implementation exists; variants or validation remain open. |
| Verify | Exact algorithm, sensor product, software or model identity must be resolved. |
| Not applicable | A data product or broad workflow requires a different record type. |

## Atomic source register

### Preprocessing and correction — pages 7–8

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S05-PR-01 | Dark Object Subtraction (DOS) | Atmospheric correction | Partial | Define DOS variant and haze assumption; test reflectance bias and water/bright surfaces. |
| S05-PR-02 | 6S | Radiative transfer atmospheric correction | Verify | Pin 6S version and atmosphere/aerosol inputs; validate against reference reflectance. |
| S05-PR-03 | MODTRAN | Radiative transfer software | Verify | Pin version, spectral settings and licence; document atmospheric profiles and sensor response. |
| S05-PR-04 | FLAASH | Atmospheric correction workflow | Verify | Identify implementation/version and MODTRAN dependency; document parameter assumptions. |
| S05-PR-05 | Sen2Cor | Sentinel-2 atmospheric correction processor | Verify | Pin version and processing baseline; document aerosol/water vapour and scene-classification outputs. |
| S05-PR-06 | Ocean-colour atmospheric correction | Atmospheric correction family | Open | Split sensor-specific algorithms; define aerosol, glint and adjacency corrections. |
| S05-PR-07 | C-correction | Topographic correction | Partial | Define illumination and regression coefficients; test slope/aspect effects. |
| S05-PR-08 | SCS+C | Topographic correction | Verify | Verify exact formula and forest-canopy assumptions; test overcorrection. |
| S05-PR-09 | Minnaert correction | Topographic correction | Verify | Verify exponent estimation and band dependence; test terrain illumination. |
| S05-PR-10 | Ross–Li BRDF model | BRDF kernel model | Partial | Existing `ross-li-brdf` package implements isotropic, Ross-Thick volumetric and Li-Sparse-Reciprocal geometric kernels, per-band rank-checked least-squares coefficient fitting and reference-geometry normalization. Synthetic tests recover known coefficients and check geometry-dependent kernels and normalized reflectance. This is not the MODIS MCD43 processing chain; angular sampling, atmospheric correction, quality flags, uncertainty and sensor-specific calibration remain open. |
| S05-PR-11 | BRDF normalisation | Reflectance normalisation workflow | Partial | Define target geometry and kernel model; test cross-date consistency. |
| S05-PR-12 | IR-MAD | Relative radiometric normalisation | Partial | Existing `ir-mad` package implements global iteratively reweighted MAD: weighted covariance whitening, canonical correlation/SVD, MAD variates, chi-square scores and no-change probability weights with mask/ridge/convergence controls. Tests cover identical imagery, affine band response, changed patches, masks and differing band counts. Co-registration, representative no-change population, sensor-specific operational processing and source-specific variants remain open. |
| S05-PR-13 | Pseudo-invariant feature normalisation | Relative calibration workflow | Partial | Define PIF selection and regression; test land-cover change contamination. |
| S05-PR-14 | Histogram matching | Radiometric normalisation | Partial | Define reference histogram and transfer; test scene content bias. |
| S05-PR-15 | Empirical line calibration | Radiometric calibration | Partial | Define targets, regression and uncertainty; test extrapolation. |
| S05-PR-16 | Fmask | Cloud/shadow masking algorithm | Verify | Pin Fmask version/sensor implementation; evaluate cloud, shadow and snow confusion. |
| S05-PR-17 | s2cloudless | Sentinel-2 cloud probability model | Verify | Pin package/model version and thresholds; validate by biome/season. |
| S05-PR-18 | CloudSEN12-style models | Learned cloud mask family | Verify | Identify exact dataset/model release; record labels, weights and domain transfer. |
| S05-PR-19 | Harmonized Landsat Sentinel (HLS) | Harmonised EO product/workflow | Verify | Pin HLS version and harmonisation corrections; document QA and licence. |
| S05-PR-20 | Mosaicking | Image compositing workflow | Partial | Define overlap and priority rules; test seam and metadata preservation. |
| S05-PR-21 | Voronoi seamline detection | Mosaic seamline algorithm | Verify | Define source image sites and seam constraints; test visual/semantic seams. |
| S05-PR-22 | Graph-cut seamline detection | Mosaic optimisation | Verify | Verify graph construction and energy terms; test discontinuities and occlusion. |
| S05-PR-23 | Color balancing | Image mosaic adjustment | Open | Define radiometric model and reference; test colour drift and edge effects. |
| S05-PR-24 | Orthorectification | Geometric correction workflow | Partial | Define sensor model, DEM and resampling; validate against independent control. |
| S05-PR-25 | Co-registration | Image alignment workflow | Partial | Define transform model, tie points and residuals; test cross-sensor alignment. |
| S05-PR-26 | Brovey pan-sharpening | Image fusion method | Partial | Verify formula and spectral distortion; test band scaling. |
| S05-PR-27 | IHS pan-sharpening | Image fusion method | Partial | Define RGB/IHS transform and intensity replacement; test spectral fidelity. |
| S05-PR-28 | Gram–Schmidt pan-sharpening | Image fusion method | Verify | Verify simulated low-resolution pan and transform; test spectral response. |
| S05-PR-29 | PCA pan-sharpening | Image fusion method | Partial | Define component replacement and inverse transform; test spectral distortion. |
| S05-PR-30 | Wavelet pan-sharpening | Image fusion family | Open | Specify wavelet/decomposition and injection rule; test spatial/spectral metrics. |
| S05-PR-31 | CNN pan-sharpening | Learned image fusion | Open | Identify architecture/data and sensor response; test generalisation and spectral consistency. |
| S05-PR-32 | Spatiotemporal image fusion | Fusion family | Partial | Split STARFM/ESTARFM/FSDAF and learned variants; test temporal transfer. |
| S05-PR-33 | Bayesian image fusion | Probabilistic fusion family | Open | Define likelihood/prior and sensor support; quantify posterior uncertainty. |
| S05-PR-34 | Kalman image fusion | Sequential fusion | Partial | Define state/observation models and covariance; test temporal consistency. |
| S05-PR-35 | Sub-pixel mapping | Super-resolution classification | Open | Split spatial allocation and unmixing methods; define fraction constraints. |
| S05-PR-36 | Super-resolution mapping | Image enhancement/reconstruction family | Open | Define target resolution and sensor model; assess hallucination and spectral fidelity. |

### Indices and transforms — page 8

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S05-IN-01 | NDVI | Spectral index | Partial | Define band convention and denominator handling; test sensor-specific wavelengths. |
| S05-IN-02 | EVI | Spectral index | Partial | Verify coefficients and blue-band use; test aerosol/soil effects. |
| S05-IN-03 | SAVI | Spectral index | Partial | Define soil adjustment factor and range; test bare soil. |
| S05-IN-04 | NDRE | Spectral index | Partial | Define red-edge band choice; document sensor dependence. |
| S05-IN-05 | NDMI | Spectral index | Partial | Resolve band convention (NIR/SWIR); document water/vegetation interpretation. |
| S05-IN-06 | LSWI | Spectral index | Partial | Existing `spectral-indices` package implements the common NIR/SWIR1 land-surface water index with explicit valid-mask, NoData and zero-denominator handling. Tests cover formula behaviour and invalid ratios. LSWI overlaps NDMI in common formulations; sensor-specific wavelength mapping, alternative definitions and field validation remain open. |
| S05-IN-07 | Tasseled Cap (Kauth–Thomas) | Spectral transform | Verify | Identify sensor-specific coefficients and components; test reflectance scaling. |
| S05-IN-08 | NDWI | Spectral index | Partial | Existing `spectral-indices` package explicitly labels and implements McFeeters green/NIR NDWI, distinct from Gao's NIR/SWIR vegetation-water formulation. Tests cover formula and undefined denominators. Sensor response, threshold transfer and water-reference validation remain open. |
| S05-IN-09 | MNDWI | Spectral index | Partial | Define green/SWIR bands and sensor; test built-up confusion. |
| S05-IN-10 | AWEI | Spectral index family | Partial | Existing `spectral-indices` package implements both AWEI_sh and AWEI_nsh formula variants with common validity handling. Formula tests and index-family documentation are present. Sensor band mapping, coefficient conventions, threshold calibration and dark-surface validation remain open. |
| S05-IN-11 | NBR | Spectral index | Partial | Define NIR/SWIR bands and fire context; test sensor harmonisation. |
| S05-IN-12 | dNBR | Change index | Partial | Define pre/post ordering and scaling; test phenology and severity thresholds. |
| S05-IN-13 | NDSI | Spectral index | Partial | Define green/SWIR band convention; test cloud/bright soil confusion. |
| S05-IN-14 | NDBI | Spectral index | Partial | Define SWIR/NIR bands; test urban/bare-soil confusion. |
| S05-IN-15 | Principal Component Analysis (PCA) | Linear transform | Partial | Define centring/scaling and covariance; test reconstruction and sign ambiguity. |
| S05-IN-16 | Minimum Noise Fraction (MNF) | Noise-adjusted transform | Verify | Verify noise covariance whitening and component ordering; test SNR separation. |
| S05-IN-17 | Fourier transform | Signal transform | Partial | Define discrete transform, windowing and spatial frequency units; test inverse. |
| S05-IN-18 | Wavelet transform | Multiscale transform family | Open | Specify wavelet, boundary extension and decomposition; test reconstruction. |
| S05-IN-19 | Hough transform | Feature detection transform | Partial | Define parameterisation and accumulator; test line/circle detection and quantisation. |
| S05-IN-20 | Radon transform | Projection transform | Partial | Define angles/offsets and discretisation; test inverse/limited-angle behaviour. |
| S05-IN-21 | GLCM texture | Texture statistic family | Partial | Define quantisation, offsets and symmetry; test window and direction aggregation. |
| S05-IN-22 | Gabor filters | Texture filter bank | Partial | Define frequency/orientation and scale; test edge/boundary handling. |
| S05-IN-23 | Sobel operator | Edge detector | Partial | Define kernel/spacing and gradient magnitude; test orientation response. |
| S05-IN-24 | Canny edge detector | Edge detection algorithm | Partial | Verify smoothing, nonmaximum suppression and hysteresis; test noisy edges. |
| S05-IN-25 | Mathematical morphology | Image processing family | Partial | Split structuring elements and binary/grayscale operations; test connectivity. |
| S05-IN-26 | SIFT | Local image feature | Partial | Verify scale-space and descriptor; see Section 15/registration record for variants. |
| S05-IN-27 | SURF | Local image feature | Verify | Verify integral-image Hessian and descriptor; review patent/history and current availability. |
| S05-IN-28 | Otsu thresholding | Threshold algorithm | Partial | Verify between-class variance and multi-level variants; test bimodal/imbalanced histograms. |
| S05-IN-29 | Adaptive thresholding | Local threshold family | Partial | Define local mean/Gaussian and block size; test illumination gradients. |
| S05-IN-30 | Stumpf satellite bathymetry | Empirical bathymetric retrieval | Verify | Verify log-ratio formulation and calibration; test water clarity/bottom type. |
| S05-IN-31 | OC4 chlorophyll algorithm | Ocean-colour retrieval | Verify | Verify sensor-specific coefficients and band ratios; document valid range. |
| S05-IN-32 | Best-pixel compositing | Compositing workflow | Partial | Define quality score and tie-break; test seasonal sampling bias. |
| S05-IN-33 | Medoid compositing | Robust composite method | Partial | Define spectral distance and valid observations; test outliers/missing data. |
| S05-IN-34 | Maximum-NDVI compositing | Compositing rule | Partial | Define temporal window and tie handling; test phenological bias. |

### Classification and segmentation — page 8

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S05-CL-01 | Maximum-likelihood classification | Statistical classifier | Partial | Define class covariance and priors; test singular covariance and calibration. |
| S05-CL-02 | Support Vector Machine (SVM) | Classifier family | Partial | Specify kernel, scaling and multiclass strategy; test spatial transfer. |
| S05-CL-03 | Random forest | Ensemble classifier | Partial | Define sampling, trees and class weights; test spatial leakage and calibration. |
| S05-CL-04 | XGBoost | Gradient boosting software/algorithm | Verify | Pin version/objective and regularisation; document model integration and licence. |
| S05-CL-05 | LightGBM | Gradient boosting software/algorithm | Verify | Pin version, histogram/leaf-wise behaviour and licence; benchmark spatially. |
| S05-CL-06 | Stacked generalisation | Ensemble learning method | Verify | Define out-of-fold meta-features and spatial folds; prevent leakage. |
| S05-CL-07 | k-means classification | Unsupervised classifier | Partial | Define feature scaling and initialization; validate cluster-to-class mapping. |
| S05-CL-08 | ISODATA | Iterative self-organising classification | Verify | Verify split/merge rules and convergence; identify implementation variant. |
| S05-CL-09 | Watershed segmentation | Image segmentation algorithm | Partial | Define gradient/topography and marker control; test oversegmentation. |
| S05-CL-10 | SLIC superpixels | Superpixel algorithm | Partial | Verify compactness and connectivity enforcement; test scale/colour space. |
| S05-CL-11 | Mean-shift segmentation | Mode-seeking segmentation | Partial | Define spatial/range bandwidth and convergence; test high-dimensional imagery. |
| S05-CL-12 | Region growing | Segmentation family | Partial | Define seed, homogeneity and merge rules; test order dependence. |
| S05-CL-13 | Multiresolution segmentation | OBIA segmentation family | Verify | Identify exact software algorithm and scale/shape/compactness parameters. |
| S05-CL-14 | Graph-cut segmentation | Energy minimisation | Partial | Define unary/pairwise terms and solver; test submodularity and label constraints. |
| S05-CL-15 | Markov Random Field (MRF) segmentation | Probabilistic segmentation | Partial | Define graph, potentials and inference; test boundary preservation. |
| S05-CL-16 | Conditional Random Field (CRF) segmentation | Probabilistic segmentation | Partial | Define unary/pairwise terms and inference; distinguish dense CRF from grid models. |
| S05-CL-17 | Active contours | Deformable boundary model | Verify | Split parametric/geometric snakes and energies; test initialization sensitivity. |
| S05-CL-18 | Level sets | Implicit contour evolution | Partial | Define PDE/regularisation and reinitialisation; test topology changes. |
| S05-CL-19 | Object-Based Image Analysis (OBIA) | Analysis workflow | Not applicable | Document segmentation, object features and classifier pipeline; not one algorithm. |
| S05-CL-20 | TempCNN | Time-series classification architecture | Verify | Verify exact model/version and temporal sampling; test chronological splits. |
| S05-CL-21 | Transformer time-series classification | Model family | Open | Split attention/positional encoding variants; define temporal resolution and leakage safeguards. |
| S05-CL-22 | InceptionTime | Time-series architecture | Verify | Verify architecture and ensemble; document input length and receptive field. |
| S05-CL-23 | TimeMatch | Time-series method | Verify | Resolve exact paper/model and task; do not infer from name alone. |
| S05-CL-24 | Dynamic Time Warping (DTW) | Sequence similarity algorithm | Partial | Define local cost, constraints and normalisation; test unequal lengths. |
| S05-CL-25 | Time-Weighted DTW (TWDTW) | Time-series distance | Verify | Verify temporal penalty and parameters; test phenological alignment. |
| S05-CL-26 | Image differencing | Change detection method | Partial | Define radiometric normalisation and threshold; test noise/phenology. |
| S05-CL-27 | Change Vector Analysis (CVA) | Multivariate change detection | Partial | Define feature space and magnitude/direction; test sensor harmonisation. |
| S05-CL-28 | Post-classification comparison | Change detection workflow | Partial | Define independent classifiers and transition matrix; quantify compounded errors. |
| S05-CL-29 | IR-MAD change detection | Multivariate change detection | Partial | Cross-linked to the tested `ir-mad` package: global iteratively reweighted canonical variates, chi-square change scores and no-change weights, with synthetic unchanged/affine-response/changed-patch tests. This is not a calibrated change probability or a spatially regularised detector; threshold selection, independent reference validation and source-specific stopping conventions remain open. |
| S05-CL-30 | Siamese change detection networks | Learned change detection | Open | Split architecture/loss and temporal ordering; test geographic/seasonal transfer. |
| S05-CL-31 | ChangeFormer | Transformer change detection model | Verify | Verify exact model/checkpoint and benchmark; document input registration. |
| S05-CL-32 | Spectral mixture analysis | Sub-pixel unmixing family | Partial | Define linear/nonlinear mixing and endmember assumptions; test abundance constraints. |
| S05-CL-33 | Regression-tree fractional cover | Fractional cover estimation | Partial | Define training labels and output constraints; test independent field plots. |
| S05-CL-34 | Vegetation Continuous Fields (VCF) | Fractional cover product/model | Verify | Identify product version and model; document definitions, calibration and licence. |

### Hyperspectral — page 8

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S05-HS-01 | N-FINDR endmember extraction | Hyperspectral algorithm | Partial | Existing `nfindr-endmembers` package projects spectra into a leading signal subspace and iteratively replaces observed pixel candidates when the augmented simplex determinant increases. Tests use synthetic pure-pixel mixtures and verify mask exclusion. This is a computationally expensive direct reference baseline; initialization sensitivity, noise-aware variants and source-specific subspace/volume conventions remain open. |
| S05-HS-02 | Pixel Purity Index (PPI) | Endmember extraction algorithm | Partial | Existing `ppi-endmembers` package mean-centres spectra, projects them along seeded random unit directions, votes for projection extrema and ranks candidate pixels by accumulated votes. Tests cover deterministic scores/ranking, mask exclusion, ties and invalid controls. Projection count, scaling/noise sensitivity and field/spectral validation remain open. |
| S05-HS-03 | Vertex Component Analysis (VCA) | Endmember extraction algorithm | Partial | Existing `vca-endmembers` package estimates a leading signal subspace by SVD and selects observed pixel spectra using seeded random directions and orthogonalisation. Synthetic-mixture tests cover reproducibility, scene-pixel provenance, mask exclusion and the one-endmember case. It assumes a linear mixture model and sufficiently pure pixels; noise-aware variants, abundance estimation and independent spectral-library/field validation remain open. |
| S05-HS-04 | Fully Constrained Least Squares (FCLS) | Spectral unmixing algorithm | Partial | Verify nonnegativity/sum-to-one constraints; test known mixtures and solver tolerances. |
| S05-HS-05 | Sparse unmixing | Unmixing family | Open | Define dictionary and sparsity penalty; test correlated endmembers. |
| S05-HS-06 | Nonlinear unmixing | Unmixing family | Open | Split bilinear/kernel/physical models; define mixing mechanism. |
| S05-HS-07 | Deep unmixing | Learned unmixing family | Open | Identify architectures, physical constraints and training data; test synthetic abundance recovery. |
| S05-HS-08 | RX anomaly detector | Hyperspectral anomaly statistic | Partial | Define global/local covariance and masking; test Gaussian background and target injection. |
| S05-HS-09 | Kernel RX | Kernel anomaly detector | Verify | Verify kernel feature-space covariance and regularisation; test bandwidth sensitivity. |
| S05-HS-10 | Matched filter | Target detection algorithm | Partial | Define target/background covariance and constrained response; test false alarms. |
| S05-HS-11 | Constrained Energy Minimisation (CEM) | Target detection algorithm | Partial | Existing `cem-detection` package estimates or accepts an uncentred spectral second-moment matrix, applies eigenvalue regularisation and constructs the unit-target-response minimum-energy filter. Tests check the distortionless response, target-pixel ranking and rejection of an indefinite matrix. Background representativeness, regularisation sensitivity and sensor-specific false-alarm calibration remain open. |
| S05-HS-12 | Adaptive Coherence Estimator (ACE) | Target detection statistic | Partial | Existing `ace-detection` package computes the squared covariance-whitened cosine similarity between background-mean-centred pixels and a target contrast vector. Tests check [0,1] bounds, target response and degenerate-target rejection. The global covariance assumes representative background and known calibrated target spectra; threshold/false-alarm calibration and local/subspace variants remain open. |
| S05-HS-13 | Subspace target detection | Detection family | Open | Split subspace projection/residual methods; define target/background spaces. |
| S05-HS-14 | Spectral Angle Mapper (SAM) | Spectral similarity metric/classifier | Partial | Define spectral angle and zero-vector handling; test illumination scaling. |
| S05-HS-15 | Spectral Information Divergence (SID) | Spectral similarity metric | Verify | Verify probability normalisation and divergence symmetrisation; test zero bands. |
| S05-HS-16 | Hyperspectral band selection | Feature selection family | Open | Split information, redundancy and wrapper methods; evaluate transfer and stability. |
| S05-HS-17 | Continuum removal | Spectral preprocessing | Partial | Define convex hull/continuum and band interpolation; test absorption features. |
| S05-HS-18 | Absorption feature analysis | Spectral feature workflow | Open | Define band depth/width/area and continuum; validate mineral/vegetation spectra. |
| S05-HS-19 | Red-edge position | Spectral metric | Partial | Define derivative/interpolation method and bands; test sensor resolution sensitivity. |

### SAR and InSAR — pages 8–9

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S05-SAR-01 | SAR speckle filtering | Filter family | Partial | Split Lee/Kuan/Frost/Refined Lee and nonlocal methods; test ENL and edge preservation. |
| S05-SAR-02 | H/A/alpha polarimetric decomposition | PolSAR decomposition | Verify | Verify eigenvalue/eigenvector definitions and orientation; test canonical scattering cases. |
| S05-SAR-03 | Freeman–Durden decomposition | PolSAR model decomposition | Verify | Verify volume/surface/double-bounce assumptions; test power conservation. |
| S05-SAR-04 | Yamaguchi decomposition | PolSAR model decomposition | Verify | Verify four-component extension and helix term; test orientation compensation. |
| S05-SAR-05 | CFAR detection | Radar detection algorithm family | Partial | Split CA/GO/SO/OS-CFAR; define clutter distribution and false alarm calibration. |
| S05-SAR-06 | SAR-to-optical translation | Cross-modal image translation | Open | Identify architecture and physical constraints; test geometry/radiometry hallucination. |
| S05-SAR-07 | PS-InSAR | Persistent Scatterer InSAR | Verify | Verify processing formulation and network; document atmospheric/orbit corrections. |
| S05-SAR-08 | SBAS InSAR | Small Baseline Subset method | Verify | Verify interferogram network and inversion; test temporal coherence. |
| S05-SAR-09 | SqueeSAR | InSAR method/software | Verify | Verify exact method and distributed scatterer treatment; identify release/licence. |
| S05-SAR-10 | Distributed scatterer InSAR | InSAR processing family | Open | Split statistically homogeneous pixel selection and phase estimation methods. |
| S05-SAR-11 | SNAPHU phase unwrapping | Phase unwrapping software/algorithm | Verify | Pin version and cost mode; test residues, masks and connected components. |
| S05-SAR-12 | Minimum-cost-flow phase unwrapping | Phase unwrapping algorithm | Verify | Define graph construction and cost; test residue conservation and branch cuts. |
| S05-SAR-13 | Coherence change detection | SAR change statistic | Partial | Define coherence estimator/window and temporal baseline; test decorrelation sources. |
| S05-SAR-14 | Offset tracking | SAR displacement method | Partial | Define matching window and subpixel fit; test large displacement and decorrelation. |
| S05-SAR-15 | Tomographic SAR | 3D radar imaging | Open | Define baseline geometry and inversion; assess sidelobes and ambiguity. |
| S05-SAR-16 | SAR autofocus | Phase correction method | Open | Split phase-gradient/contrast methods; define target and convergence. |

### LiDAR and point clouds — pages 9–10

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S05-LI-01 | Cloth Simulation Filter (CSF) | LiDAR ground filtering | Verify | Verify cloth parameters and slope handling; test terrain/vegetation classes. |
| S05-LI-02 | Progressive morphological filter | LiDAR ground filtering | Partial | Define window schedule and height threshold; test urban/steep terrain. |
| S05-LI-03 | ICP point-cloud registration | Registration algorithm family | Partial | Split point-to-point/plane/GICP/robust variants; test known transformations. |
| S05-LI-04 | RANSAC shape fitting | Robust geometric estimation | Partial | Split planes/cylinders/spheres; define inlier threshold and degeneracy. |
| S05-LI-05 | Local-maxima tree segmentation | Tree detection/segmentation | Partial | Define CHM smoothing and variable window; validate tree detection by canopy density. |
| S05-LI-06 | Watershed tree segmentation | Tree segmentation | Partial | Define marker generation and CHM; test crown merging/splitting. |
| S05-LI-07 | Dalponte tree segmentation | Tree segmentation algorithm | Verify | Verify exact algorithm and parameters; reproduce reference benchmark. |
| S05-LI-08 | Canopy Height Model (CHM) | Raster derivative/workflow | Partial | Define DSM-DTM alignment and interpolation; test negative heights and gaps. |
| S05-LI-09 | Crown delineation | Tree geometry extraction | Open | Define crown boundary method and overlap handling; validate field polygons. |
| S05-LI-10 | Point-cloud classification | Classification family | Open | Split rule-based/ML/deep methods; define class schema and spatial split. |
| S05-LI-11 | Point-cloud voxelization | Data representation | Partial | Define voxel origin/size and aggregation; test quantisation error. |
| S05-LI-12 | LiDAR strip adjustment | Survey calibration workflow | Verify | Verify strip matching/bundle adjustment and boresight parameters; test control data. |
| S05-LI-13 | GEDI waveform processing | Full-waveform LiDAR processing | Verify | Pin product/version and waveform decomposition; document geolocation/quality flags. |
| S05-LI-14 | ICESat-2 ground photon classification | Photon classification workflow | Verify | Pin ATL product/algorithm version; document confidence and terrain dependence. |
| S05-LI-15 | PointNet | Point-cloud neural architecture | Verify | Verify original architecture and task; document sampling and checkpoint licence. |
| S05-LI-16 | PointNet++ | Hierarchical point-cloud architecture | Verify | Verify set abstraction and feature propagation; test density robustness. |
| S05-LI-17 | KPConv | Point-cloud convolution | Verify | Verify kernel point placement/deformable variants; document computational cost. |
| S05-LI-18 | Point Transformer | Point-cloud transformer family | Verify | Identify exact version/paper; separate Point Transformer variants. |
| S05-LI-19 | RandLA-Net | Large-scale point-cloud architecture | Verify | Verify random sampling and local feature aggregation; document density limits. |
| S05-LI-20 | MinkowskiNet | Sparse voxel convolution architecture | Verify | Verify sparse tensor backend/version and voxel resolution; document licence. |

### Photogrammetry and 3D — page 9

| ID | Atomic item | Kind | Status | Required completion work |
|---|---|---|---|---|
| S05-PH-01 | Structure from Motion (SfM) | Reconstruction workflow | Partial | Define feature matching, incremental/global reconstruction and scale; test known camera scene. |
| S05-PH-02 | COLMAP | Photogrammetry software | Verify | Pin version and reconstruction modes; document dependencies/licence. |
| S05-PH-03 | Bundle adjustment | Nonlinear optimisation | Partial | Define reprojection objective, gauge fixing and robust loss; test synthetic camera poses. |
| S05-PH-04 | Aerial triangulation | Photogrammetric adjustment | Verify | Define block geometry, tie/GCP observations and adjustment; report residuals. |
| S05-PH-05 | GCP-aided adjustment | Georeferencing workflow | Partial | Define control weighting and datum; test independent checkpoints. |
| S05-PH-06 | IMU-aided adjustment | Integrated sensor adjustment | Verify | Define boresight/time lever arms and stochastic model; test trajectory consistency. |
| S05-PH-07 | Direct georeferencing | Sensor georeferencing workflow | Partial | Define GNSS/IMU frame transformations and timing; validate independent controls. |
| S05-PH-08 | Semi-Global Matching (SGM) | Dense stereo matching | Verify | Verify path aggregation and penalty parameters; test disparity accuracy. |
| S05-PH-09 | PatchMatch stereo | Dense stereo matching | Verify | Verify random propagation/search and view aggregation; test textureless regions. |
| S05-PH-10 | Multi-view stereo | Reconstruction family | Open | Split patch-based/voxel/depth-map methods; define visibility and fusion. |
| S05-PH-11 | Rational Polynomial Coefficient (RPC) sensor model | Sensor geometry model | Partial | Define forward/inverse normalisation and height; test ground-image residuals. |
| S05-PH-12 | Satellite stereo DSM | Surface reconstruction workflow | Partial | Define stereo pair, RPC bias correction and matching; validate against lidar. |
| S05-PH-13 | DSM derivation | Surface modelling workflow | Partial | Define interpolation, filtering and datum; test completeness and vertical accuracy. |
| S05-PH-14 | DTM derivation | Terrain modelling workflow | Partial | Define ground classification and interpolation; validate terrain breaks. |
| S05-PH-15 | nDSM derivation | Normalised surface metric | Partial | Define DSM-DTM alignment and height sign; test vegetation/building artifacts. |
| S05-PH-16 | Brown–Conrady lens calibration | Camera calibration model | Partial | Existing `brown-conrady` package implements forward radial (k1–k3) and tangential (p1,p2) distortion in normalised camera-plane coordinates and Newton inversion with analytic Jacobian. Tests cover zero-coefficient identity, radial/tangential round trips, shape preservation and invalid controls. It does not estimate intrinsics or coefficients and is not a calibration optimiser; pixel/intrinsic conventions and independent reprojection validation remain open. |
| S05-PH-17 | Boresight calibration | Sensor calibration workflow | Verify | Define angular/lever-arm alignment and estimation; validate independent trajectories. |
| S05-PH-18 | Orthomosaic generation | Photogrammetric workflow | Partial | Define seamlines, blending and radiometric balance; test geometric seams. |
| S05-PH-19 | Mesh texturing | 3D reconstruction workflow | Open | Define visibility/UV assignment and blending; assess occlusion and colour seams. |
| S05-PH-20 | Poisson surface reconstruction | Surface reconstruction algorithm | Verify | Verify screened/unscreened formulation and octree depth; test watertightness and shrinkage. |
| S05-PH-21 | Marching cubes | Isosurface extraction algorithm | Partial | Cross-link Section 4; test ambiguous cases and manifoldness. |
| S05-PH-22 | Mesh simplification | Mesh processing family | Partial | Split quadric and other methods; define geometric/topological error. |
| S05-PH-23 | 3D alpha shapes | Shape reconstruction | Verify | Verify alpha complex and 3D boundary extraction; test degenerate tetrahedra. |
| S05-PH-24 | NeRF | Neural radiance field model family | Verify | Identify exact NeRF variant and scene assumptions; test scale/georeferencing and licence. |
| S05-PH-25 | 3D Gaussian Splatting | Neural scene representation/rendering | Verify | Verify official paper/release and optimisation; document geospatial alignment and licence. |

## Completion gates

1. Pin sensor/product/software versions, band definitions, radiometric units, CRS, acquisition geometry and calibration parameters.
2. Use independent reference data and sensor-aware validation; avoid random tile splits that leak adjacent scenes.
3. For indices and retrievals, document exact equations and band wavelengths; aliases must not conceal different definitions.
4. For segmentation/detection, report class-wise metrics, area-adjusted estimates where appropriate, boundary/topology quality and uncertainty.
5. For SAR/InSAR, document orbit, phase, coherence, speckle, atmosphere, reference frame and unwrapping assumptions.
6. For LiDAR/photogrammetry, test geometric accuracy, completeness, point density, calibration and independent checkpoints.
7. Check licences separately for software, model weights, training data, EO products and derived artefacts.
8. Reconcile canonical lessons, implementation contracts, tests, notebooks, verification records and catalogue only after evidence is recorded.

**Current conclusion:** Section 5 is atomised into auditable child records. It remains open; no product, algorithm family or operational EO workflow is declared fully verified by this register.
