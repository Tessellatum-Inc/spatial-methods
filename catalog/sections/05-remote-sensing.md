# Section 5 — Remote sensing, SAR, LiDAR, photogrammetry

- **Original source section:** 5
- **Source pages:** 7–9
- **Source transcription:** [pages 6–10](../../source-inventory/pages-06-10.md)
- **Review state:** source entries extracted into this index; not every entry independently verified
- **Current canonical records: [OBIA object features](../../algorithms/remote-sensing/obia-object-features.md), [CA-CFAR detection](../../algorithms/remote-sensing/ca-cfar.md), [Lee speckle filtering](../../algorithms/remote-sensing/lee-speckle-filter.md), [DTW and time-weighted DTW](../../algorithms/remote-sensing/time-series-dtw.md),** [NDVI](../../algorithms/remote-sensing/ndvi.md), [spectral-index family](../../algorithms/remote-sensing/spectral-index-family.md), [Otsu thresholding](../../algorithms/remote-sensing/otsu-thresholding.md), [PCA transform](../../algorithms/remote-sensing/pca-transform.md), [GLCM texture](../../algorithms/remote-sensing/glcm-texture.md), [Sobel/Canny](../../algorithms/remote-sensing/edge-detection.md), [binary morphology](../../algorithms/remote-sensing/mathematical-morphology.md), and [Gabor filters](../../algorithms/remote-sensing/gabor-filters.md), [Fourier filtering](../../algorithms/remote-sensing/fourier-filtering.md), [adaptive thresholding](../../algorithms/remote-sensing/adaptive-thresholding.md), the [Hough line transform](../../algorithms/remote-sensing/hough-transform.md), [MNF](../../algorithms/remote-sensing/mnf-transform.md), [Haar wavelet](../../algorithms/remote-sensing/haar-wavelet.md), [Radon transform](../../algorithms/remote-sensing/radon-transform.md), [spectral similarity](../../algorithms/remote-sensing/spectral-similarity.md), and [global RX](../../algorithms/remote-sensing/rx-anomaly.md), [VCA](../../algorithms/remote-sensing/vca-endmembers.md), [FCLS](../../algorithms/remote-sensing/fcls-unmixing.md), and the [spectral matched filter](../../algorithms/remote-sensing/spectral-matched-filter.md), [PPI](../../algorithms/remote-sensing/pixel-purity-index.md), [temporal compositing](../../algorithms/remote-sensing/temporal-compositing.md), [empirical corrections](../../algorithms/remote-sensing/empirical-corrections.md), [IR-MAD](../../algorithms/remote-sensing/ir-mad.md) and [continuum removal](../../algorithms/remote-sensing/continuum-removal.md), plus [fractional-cover regression](../../algorithms/remote-sensing/fractional-cover-regression-tree.md). This is a partial audit; the section remains substantially incomplete.

The source spans raw imagery correction, spectral transforms, classification, hyperspectral analysis, radar, point clouds, photogrammetry and biophysical retrieval. These methods operate at different stages of a sensor-to-product workflow; do not collapse them into one generic “remote sensing algorithm” category.

## First audited index

The canonical records now cover the spectral-index family, global Otsu thresholding, covariance/correlation PCA, offset-specific GLCM texture, Sobel/Canny edges, binary morphology and Gabor filters. PCA is deliberately distinguished from MNF; GLCM covers six common features rather than the full Haralick set. Full atmospheric correction workflows, broader wavelet families, SIFT/SURF, classification, SAR, LiDAR, photogrammetry and sensor-specific retrieval remain open; MNF, Haar, Radon and several related transforms have scoped implementations described below.

## Preprocessing and correction

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Atmospheric: dark object subtraction, 6S, MODTRAN, FLAASH, Sen2Cor, ocean color atmospheric correction | Atmospheric correction methods / models / software | 7 | Partial — a tested percentile-based dark-object subtraction baseline is implemented; 6S/MODTRAN/FLAASH/Sen2Cor and ocean-colour atmospheric correction remain distinct physical or sensor-specific workflows |
| Topographic and BRDF: C-correction, SCS+C, Minnaert, Ross-Li, BRDF normalization | Topographic correction / reflectance modelling | 7 | Partial — tested C-correction, SCS+C and caller-exponent Minnaert terrain corrections plus fitted RossThick-LiSparseR multi-angle BRDF normalization are implemented; operational sensor-specific BRDF products and atmospheric/terrain preprocessing remain open |
| Relative normalization: [pseudo-invariant features and histogram matching](../../algorithms/remote-sensing/empirical-corrections.md), IR-MAD, empirical line calibration | Radiometric normalisation / calibration methods | 7 | Partial — tested empirical-quantile histogram matching, robustly selected PIF affine normalization, empirical-line DN-to-reflectance calibration and iteratively reweighted canonical-variate IR-MAD are implemented; sensor-specific radiometric calibration and independent field validation remain open |
| Cloud and shadow masking: Fmask, s2cloudless, CloudSEN12-style models; sensor harmonization (HLS) | Masking algorithms / model families / harmonisation products | 8 | Partial — tested Landsat Collection 2 QA_PIXEL bit interpretation, Sentinel-2 SCL clear-class masks and thresholding of supplied cloud-probability layers; Fmask/s2cloudless detection models and HLS harmonisation remain open |
| Mosaicking, seamline detection (Voronoi, graph cut), color balancing, orthorectification, co-registration | Image assembly / seamline algorithms / geometric correction | 8 | Partially implemented: phase-correlation translation and RANSAC affine estimation from matched points have tested baselines; feature detection/matching, local deformation, orthorectification, mosaicking and seamline optimization remain open |
| Fusion: pan-sharpening (Brovey, IHS, Gram-Schmidt, PCA, wavelet, CNN), spatiotemporal fusion, Bayesian and Kalman fusion, sub-pixel and super-resolution mapping | Image fusion methods / statistical methods / neural approaches | 8 | Partially implemented: tested N-band Brovey and three-band RGB IHS component-substitution baselines preserve input band ratios or HSI hue/saturation while replacing intensity and explicitly masking invalid inputs; Gram-Schmidt, wavelet, Bayesian/Kalman, spatiotemporal and learned fusion remain open |

## Indices and transforms

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Vegetation and soil: [NDVI](../../algorithms/remote-sensing/ndvi.md), EVI, SAVI, NDRE, NDMI, LSWI, [Tasseled Cap](../../algorithms/remote-sensing/tasseled-cap.md) (Kauth–Thomas) | Spectral indices / transforms | 8 | Partial — a tested NumPy index package covers NDVI, EVI, SAVI, NDRE, NDMI/LSWI and an extended [spectral-index family](../../algorithms/remote-sensing/spectral-index-family.md); a sensor-coefficient-driven Tasseled Cap projection is now implemented; source-entry review and sensor-specific coefficient sets remain open |
| Water, burn, snow, urban: NDWI, MNDWI, AWEI, NBR, dNBR, NDSI, NDBI | Spectral indices | 8 | Partial — tested NDWI, MNDWI, AWEI, NBR/dNBR, NDSI and NDBI implementations are covered in the [spectral-index family note](../../algorithms/remote-sensing/spectral-index-family.md); threshold calibration and source-entry review remain open |
| Transforms: [PCA](../../algorithms/remote-sensing/pca-transform.md), [minimum noise fraction (MNF)](../../algorithms/remote-sensing/mnf-transform.md), [Fourier](../../algorithms/remote-sensing/fourier-filtering.md), [Haar wavelet](../../algorithms/remote-sensing/haar-wavelet.md), [Hough](../../algorithms/remote-sensing/hough-transform.md), [Radon](../../algorithms/remote-sensing/radon-transform.md) | Statistical and signal transforms | 8 | Partial — PCA, MNF, Fourier, Haar wavelet, Hough and Radon have scoped reference implementations; broader wavelet families and inverse Radon reconstruction remain open |
| Texture and edges: [GLCM](../../algorithms/remote-sensing/glcm-texture.md), Gabor, Sobel, Canny, mathematical morphology, SIFT, SURF | Texture measures / filters / feature detectors and descriptors | 8 | Partial — offset-specific GLCM and six common features implemented; SIFT and SURF remain open; Sobel/Canny, binary morphology and Gabor now have reference implementations |
| Thresholding: [Otsu](../../algorithms/remote-sensing/otsu-thresholding.md), [adaptive thresholding](../../algorithms/remote-sensing/adaptive-thresholding.md); Stumpf bathymetry; OC4 chlorophyll | Thresholding methods / retrieval algorithms | 8 | Partially implemented: global Otsu and local mean/Gaussian adaptive thresholding have tested baselines; Stumpf log-band-ratio bathymetry now has local linear calibration/application and SeaWiFS OC4v4 chlorophyll has its published maximum-blue-ratio polynomial; sensor variants, atmospheric correction and in-situ validation remain open |
| Compositing: best-pixel, medoid, maximum NDVI | Image compositing rules | 8 | Partially implemented: tested quality-score best-pixel selection, observed-spectrum medoid and maximum-NDVI compositing; cloud masking, harmonisation and sensor-specific quality scoring remain upstream requirements |

## Classification and segmentation

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Pixel-based: [Gaussian maximum likelihood, k-means and ISODATA](../../algorithms/remote-sensing/classical-classification.md), SVM, random forest, XGBoost, LightGBM, stacked generalization, ISODATA | Classification models / ensemble methods / clustering | 8 | Partial — tested Gaussian maximum-likelihood, k-means++, ISODATA, linear/RBF/polynomial/sigmoid SVM and random-forest baselines; XGBoost, LightGBM, stacked generalization, spatial regularization, model selection and accuracy assessment remain open |
| Segmentation: watershed, SLIC superpixels, mean shift, region growing, multiresolution segmentation, graph cuts, MRF and CRF, active contours, level sets | Segmentation algorithms / optimisation and probabilistic models | 8 | Partially implemented: SLIC-style feature/spatial superpixel clustering with local assignment and deterministic centre updates has a tested baseline; connectedness enforcement, watershed, mean shift, region growing, graph cuts, MRF/CRF, active contours and level sets remain open |
| Object-based image analysis (OBIA) | Analysis workflow / method family | 8 | Partial — tested object geometry, per-band summaries and region adjacency from supplied segmentation labels; segmentation, multiscale hierarchies, texture and object classification remain open |
| Time-series classification: TempCNN, Transformer, InceptionTime, TimeMatch, DTW, TWDTW | Time-series models / matching methods | 8 | Partial — tested multivariate DTW with an optional Sakoe–Chiba window and an explicit logistic time-weighted DTW distance baseline; TempCNN, Transformer, InceptionTime, TimeMatch, training, classification and benchmark reproduction remain open |
| Change detection: [differencing and CVA](../../algorithms/remote-sensing/change-vector-analysis.md), post-classification, IR-MAD, Siamese networks, ChangeFormer | Change-detection methods / model families | 8 | Partial — tested bitemporal spectral differencing/CVA (Euclidean and covariance-standardized magnitudes) and ordered post-classification transition matrices and iteratively reweighted MAD change scores are implemented; learned Siamese/ChangeFormer methods, threshold calibration and accuracy-adjusted change estimation remain open |
| Fractional cover: spectral mixture analysis, regression trees, vegetation continuous fields | Spectral unmixing / regression / derived products | 8 | Partial — FCLS linear unmixing and a tested CART fractional-cover regression baseline now exist; vegetation continuous fields products, spatial validation, uncertainty calibration and source-entry review remain open |

## Hyperspectral

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Endmember extraction: [N-FINDR](../../algorithms/remote-sensing/nfindr-endmembers.md), [ATGP](../../algorithms/remote-sensing/atgp-endmembers.md), [VCA](../../algorithms/remote-sensing/vca-endmembers.md), [Pixel Purity Index (PPI)](../../algorithms/remote-sensing/pixel-purity-index.md); unmixing: [FCLS](../../algorithms/remote-sensing/fcls-unmixing.md), sparse, nonlinear, deep | Endmember extraction / spectral unmixing methods | 8 | Partial — N-FINDR, ATGP, VCA and FCLS have scoped reference implementations; PPI now has a seeded NumPy candidate-ranking baseline; sparse, nonlinear and deep unmixing remain open |
| Anomaly and target detection: [global RX](../../algorithms/remote-sensing/rx-anomaly.md), Kernel RX, [global spectral matched filter](../../algorithms/remote-sensing/spectral-matched-filter.md), [CEM](../../algorithms/remote-sensing/cem-detection.md), [ACE](../../algorithms/remote-sensing/ace-detection.md), subspace methods | Detection algorithms / statistical methods | 8 | Partial — global RX, matched filter, CEM and ACE implemented; Kernel RX and subspace methods remain open |
| [Spectral angle mapper and spectral information divergence](../../algorithms/remote-sensing/spectral-similarity.md), band selection, continuum removal, absorption feature analysis, red-edge position | Spectral similarity measures / feature selection / spectral analysis | 8 | Partial — SAM and SID implemented; band selection and feature-specific diagnostic fitting remain open; a tested upper-convex-hull continuum-removal and absorption-depth/area baseline is now implemented |

## SAR and InSAR

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Speckle filtering, polarimetric decomposition (H/A/alpha, Freeman-Durden, Yamaguchi), CFAR detection, SAR-to-optical translation | Filtering / decomposition methods / detection / translation models | 8 | Partial — tested adaptive Lee intensity filtering and square-window CA-CFAR for exponential intensity backgrounds; a tested square-window OS-CFAR order-statistics baseline now covers bright-interferer resistance under the independent exponential model; refined/polarimetric filters, H/A/alpha and Freeman-Durden/Yamaguchi decompositions, GO/SO-CFAR and SAR-to-optical translation remain open |
| InSAR: PS-InSAR, SBAS, SqueeSAR, distributed scatterers, phase unwrapping (SNAPHU, minimum cost flow), coherence change detection, offset tracking, tomographic SAR, autofocus | Interferometric processing workflows / algorithms / software | 9 | Not checked — intake only |

## LiDAR and point clouds

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Ground filtering: CSF, progressive morphological; ICP registration; RANSAC shape fitting | Point-cloud filtering / registration / model fitting | 9 | Not checked — intake only |
| Tree segmentation (local maxima, watershed, Dalponte), canopy height models, crown delineation | Segmentation methods / derived surface models | 9 | Not checked — intake only |
| Classification, voxelization, strip adjustment, GEDI waveform processing, ICESat-2 ground photon classification | Point-cloud processing / sensor-specific workflows | 9 | Not checked — intake only |
| Deep point networks: PointNet, PointNet++, KPConv, Point Transformer, RandLA-Net, MinkowskiNet | Neural network architectures for point clouds | 9 | Not checked — intake only |

## Photogrammetry and 3D

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Structure from Motion (COLMAP), bundle adjustment, aerial triangulation, GCP and IMU-aided adjustment, direct georeferencing | Photogrammetric workflows / optimisation / software | 9 | Not checked — intake only |
| Dense matching: SGM, PatchMatch, multi-view stereo; RPC sensor models; satellite stereo DSM; DSM, DTM and nDSM derivation | Stereo matching algorithms / sensor models / surface products | 9 | Not checked — intake only |
| Lens calibration (Brown-Conrady), boresight calibration, orthomosaic generation, mesh texturing | Calibration methods / production workflows | 9 | Partial — tested Brown-Conrady radial/tangential forward distortion and Newton inverse are implemented in normalized camera coordinates; calibration estimation, boresight, orthomosaic generation and mesh texturing remain open |
| Surface reconstruction: Poisson, marching cubes, mesh simplification, 3D alpha shapes, NeRF, 3D Gaussian splatting | Surface reconstruction / mesh algorithms / neural representations | 9 | Not checked — intake only |

## Biophysical and geophysical retrieval

| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|--- |
| Evapotranspiration and energy balance: SEBAL, METRIC, SEBS, ALEXI, Penman-Monteith, Hargreaves; [land surface temperature](../../algorithms/remote-sensing/thermal-land-surface-temperature.md) (split-window, single-channel, temperature-emissivity separation) | Energy-balance models / evapotranspiration and temperature retrieval | 9 | Partial — tested Planck brightness-temperature conversion, single-channel radiative-transfer inversion and caller-calibrated generalized split-window correction are implemented; emissivity/atmospheric retrieval, sensor-specific coefficient sets and full energy-balance models remain open |
| Productivity and structure: light-use efficiency GPP, biomass allometry, LAI and fAPAR retrieval, soil moisture retrieval, albedo | Biophysical retrieval methods / allometric models / products | 9 | Not checked — intake only |
| Water and atmosphere: Case 2 water quality inversion, aerosol retrieval (dark target, MAIAC), DOAS trace gases, cloud property retrieval | Inversion and retrieval methods | 9 | Not checked — intake only |
| Cryosphere and ocean: sea ice concentration (NASA Team, Bootstrap), ice motion, glacier velocity, DEM differencing, eddy detection (Okubo-Weiss), SST fronts, altimetry processing | Retrieval / motion estimation / ocean analysis methods | 9 | Not checked — intake only |
| Thermal and fire: thermal anomaly and volcanic hotspot detection, active fire detection, burned area (MCD64A1) | Detection algorithms / products | 9 | Not checked — intake only |

## Decisions for the next pass

1. Keep sensor correction, feature extraction, classification, change detection and retrieval as distinct stages.
2. Record sensor, band configuration, spatial and temporal resolution, atmospheric assumptions and preprocessing.
3. Distinguish an algorithm from a named software package, product, dataset or model architecture.
4. Verify recent neural architectures and product names against original papers and maintainer sources.
5. Include conventional baselines and independent validation when evaluating learned methods.

## Bibliographic checks on selected spectral-index foundations

- Rouse, J. W., Jr., Haas, R. H., Schell, J. A., Deering, D. W. and Harlan, J. C. (1974, November), *Monitoring the vernal advancement and retrogradation (green wave effect) of natural vegetation*. Type III final report for September 1972–November 1974, Texas A&M University Remote Sensing Center, prepared for NASA Goddard Space Flight Center; NASA-CR-144661 (RSC-1978-4). [NASA NTRS record](https://ntrs.nasa.gov/citations/19750020419).
- Huete (1988), “A soil-adjusted vegetation index (SAVI),” *Remote Sensing of Environment*, 25(3), 295–309, [10.1016/0034-4257(88)90106-X](https://doi.org/10.1016/0034-4257(88)90106-X).
- Huete, Didan, Miura, Rodriguez, Gao and Ferreira (2002), “Overview of the radiometric and biophysical performance of the MODIS vegetation indices,” *Remote Sensing of Environment*, 83(1–2), 195–213, [10.1016/S0034-4257(02)00096-2](https://doi.org/10.1016/S0034-4257(02)00096-2).
- McFeeters (1996), “The use of the Normalized Difference Water Index (NDWI) in the delineation of open water features,” *International Journal of Remote Sensing*, 17(7), 1425–1432, [10.1080/01431169608948714](https://doi.org/10.1080/01431169608948714).
- Xu (2006), “Modification of normalised difference water index (NDWI) to enhance open water features in remotely sensed imagery,” *International Journal of Remote Sensing*, 27(14), 3025–3033, [10.1080/01431160600589179](https://doi.org/10.1080/01431160600589179).
- Huete, Liu, Batchily and van Leeuwen (1997), “A comparison of vegetation indices over a global set of TM images for EOS-MODIS,” *Remote Sensing of Environment*, 59(3), 440–451, [10.1016/S0034-4257(96)00112-5](https://doi.org/10.1016/S0034-4257(96)00112-5).

The NDVI report identity, author list and report number were checked against the NASA record and report title page. The journal metadata for SAVI, EVI, NDWI and MNDWI was checked against publisher records. This is a selected bibliography pass, not a technical audit of all Section 5 indices, preprocessing workflows or remote-sensing source entries.


The co-registration source entry now includes a tested FFT phase-correlation translation estimator and a RANSAC affine estimator for supplied point correspondences. Feature detection/matching, local deformation, orthorectification, mosaicking, color balancing and seamline optimization remain separate outstanding workflows.


The change-detection source entry now has a NumPy CVA baseline (after-minus-before vectors, Euclidean magnitude and ridge-stabilized Mahalanobis magnitude) plus post-classification transition matrices and change masks. These require aligned, radiometrically comparable dates and do not implement IR-MAD or learned change-detection architectures.
