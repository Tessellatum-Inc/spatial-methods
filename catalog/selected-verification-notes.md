# Selected source-verification notes

Last updated: 14 November 2026

These notes record bounded checks against publisher or institutional bibliographic records. They do not mark an entire grouped source entry as verified. The dimensions remain separate under the [verification protocol](verification-protocol.md).

## Section 10 — Visvalingam–Whyatt line simplification

**Source entry:** “Line simplification variants: Reumann-Witkam, Lang, Opheim, Zhao-Saalfeld, Visvalingam-Whyatt with effective area” (source page 21).

- **Identity:** confirmed for the Visvalingam–Whyatt method named in the group.
- **Bibliography:** confirmed: Visvalingam, M. and Whyatt, J. D. (1993), “Line generalisation by repeated elimination of points,” *The Cartographic Journal*, 30(1), 46–51, DOI [10.1179/000870493786962263](https://doi.org/10.1179/000870493786962263).
- **Evidence:** Lancaster University's institutional research record and the Hull repository record both identify the article, journal, volume, issue, pages and DOI.
- **Technical claims:** the canonical lesson describes effective-area elimination and its distinction from Douglas–Peucker. This note verifies citation identity and metadata, not every implementation detail or every claim in the original paper.
- **Implementation:** the linked Python package is a tested open-polyline teaching baseline for Douglas–Peucker and Visvalingam–Whyatt; it does not cover Reumann–Witkam, Lang, Opheim or Zhao–Saalfeld.
- **Rights:** link to the DOI/institutional records; no paper text, figure or publisher PDF is reproduced here.
- **Remaining work:** split the grouped source row into child entries and review each named simplification variant independently.

## Section 10 — Spatial cross-validation and nearest-neighbour distance matching

**Source entry:** “Spatial cross-validation, NNDM, kNNDM, buffered leave-one-out, spatial k-fold by clustering, blockCV, spatial+temporal leave-out” (source page 21).

- **Identity:** confirmed for the NNDM and kNNDM methods discussed below; the grouped source entry still contains other designs and software names that require separate review.
- **Bibliography — NNDM:** confirmed: Milà, C., Mateu, J., Pebesma, E. and Meyer, H. (2022), “Nearest neighbour distance matching Leave-One-Out Cross-Validation for map validation,” *Methods in Ecology and Evolution*, 13(6), 1304–1316, DOI [10.1111/2041-210X.13851](https://doi.org/10.1111/2041-210X.13851). Publisher record confirms title, authors, date, journal issue and pages.
- **Bibliography — kNNDM:** confirmed: Linnenbrink, J., Milà, C., Ludwig, M. and Meyer, H. (2024), “kNNDM CV: k-fold nearest-neighbour distance matching cross-validation for map accuracy estimation,” *Geoscientific Model Development*, 17, 5897–5912, DOI [10.5194/gmd-17-5897-2024](https://doi.org/10.5194/gmd-17-5897-2024). The journal record confirms title, authors, date, volume, pages and DOI; the article is published under CC BY 4.0.
- **Technical claims checked:** the lesson's high-level distinction between prediction-oriented distance matching, spatial block CV and buffered LOO is grounded in the two primary papers. NNDM matches the distribution of nearest-neighbour distances from prediction to training locations with the corresponding test-to-training distribution. kNNDM seeks a k-fold configuration that approximates this distributional match. The papers' findings are scoped to their simulation and case-study settings; they do not establish universal superiority.
- **Important limitations:** nearest-neighbour distance matching uses geographical distances and does not by itself encode direction, anisotropy, nonstationarity or covariate-space shift. A probability-sample/design-based map-accuracy assessment remains preferable when feasible for the target population.
- **Implementation:** the existing Python package implements fixed planar grid blocks and optional buffered exclusion only. It does not implement NNDM or kNNDM. The lesson links to the maintained `blockCV` implementation as an external option; package versions and parameters must be recorded by users.
- **Rights:** link to publisher records; no article text or figures are reproduced.
- **Review date:** 14 November 2026.
- **Remaining work:** split the grouped source row into child entries and independently review spatial block CV, buffered LOO, NNDM, kNNDM, blockCV software, clustering-based folds and spatiotemporal holdouts.

## Section 22 — Nonseparable space-time covariance references

**Source entry:** “Space-time covariances: Gneiting nonseparable class, Cressie-Huang, product-sum and metric models” (source page 45).

### Cressie and Huang (1999)

- **Identity:** confirmed.
- **Bibliography:** confirmed: Cressie, N. and Huang, H.-C. (1999), “Classes of Nonseparable, Spatio-Temporal Stationary Covariance Functions,” *Journal of the American Statistical Association*, 94(448), 1330–1339, DOI [10.1080/01621459.1999.10473885](https://doi.org/10.1080/01621459.1999.10473885).
- **Evidence:** Taylor & Francis publisher record.
- **Technical claims:** not independently audited in this bibliography note.
- **Rights:** DOI link only; no article content is reproduced.

### Gneiting (2002)

- **Identity:** confirmed.
- **Bibliography:** confirmed: Gneiting, T. (2002), “Nonseparable, Stationary Covariance Functions for Space-Time Data,” *Journal of the American Statistical Association*, 97(458), 590–600, DOI [10.1198/016214502760047113](https://doi.org/10.1198/016214502760047113).
- **Evidence:** Taylor & Francis publisher record.
- **Technical claims:** the canonical lesson and package implement one Euclidean-space-by-linear-time member of a Gneiting class. The finite-matrix eigenvalue diagnostic is not a proof of positive definiteness for all samples or geometries. This note verifies citation metadata, not the complete mathematical conditions of the paper.
- **Rights:** DOI link only; no article content is reproduced.

**Scope warning:** the existing canonical record is not a comprehensive space-time covariance catalogue. Cressie–Huang, Gneiting, product-sum, metric, spherical and network covariance constructions are distinct families or settings. Only the stated Gneiting-class teaching member is implemented in the current package.

## Review metadata

- Review date: 14 November 2026.
- Review type: bibliographic identity and metadata check.
- Technical-claim status: not promoted by these notes.
- Rights status: link-only for the cited papers; no third-party content reused.


## Section 10 — Line clipping

**Source entry:** “Line clipping: Cohen-Sutherland, Liang-Barsky, Cyrus-Beck, Nicholl-Lee-Nicholl” (source page 21).

- **Identity and technical scope:** the canonical lesson treats Cohen–Sutherland as an outcode/encoding method, Liang–Barsky as parametric clipping against an axis-aligned rectangle, and Cyrus–Beck as parametric clipping against convex half-spaces. It explicitly does not claim that Cyrus–Beck handles arbitrary concave windows or that segment clipping alone produces clipped polygon output.
- **Bibliography:** Matthes, J. and Drakopoulos, V. (2022), “Line Clipping in 2D: Overview, Techniques and Algorithms,” *Journal of Imaging*, 8(10), 286, DOI [10.3390/jimaging8100286](https://doi.org/10.3390/jimaging8100286). The publisher's open-access article surveys the major line-clipping families and named algorithms.
- **Technical-claim status:** the lesson's high-level taxonomy and algorithm distinctions are checked against the review. The equations are presented as teaching derivations; they have not been validated against a new implementation in this repository.
- **Implementation:** no new clipping implementation is claimed. The lesson includes a manual test plan but no executable test suite.
- **Rights:** DOI link only; no article text or figures reproduced.
- **Remaining work:** independently inspect the exact parameter-sign convention and edge cases in a future tested implementation; verify Nicholl–Lee–Nicholl separately if it becomes a full lesson.

## Section 10 — Rasterization and grid traversal

**Source entry:** “Line and polygon rasterization: Bresenham, DDA, Wu's anti-aliased line, scanline polygon fill, supercover lines” (source page 21).

- **Identity and scope:** the lesson distinguishes thin-line rasterisation, anti-aliased display, polygon scan conversion, supercover cell visitation and fractional-area coverage. It does not treat these outputs as interchangeable.
- **Bibliography:** Levoy, M., Stanford CS 248, [Rasterization algorithms](https://www.graphics.stanford.edu/courses/cs248-08/scan/scan1.html), lecture notes covering DDA, Bresenham and polygon scan conversion; Wu, X. (1991), “An Efficient Antialiasing Technique,” *Computer Graphics*, 25(4), 143–152, DOI [10.1145/127719.122734](https://doi.org/10.1145/127719.122734); Amanatides, J. and Woo, A. (1987), “A Fast Voxel Traversal Algorithm for Ray Tracing,” *Eurographics*, DOI [10.2312/egtp.19871000](https://doi.org/10.2312/egtp.19871000).
- **Technical-claim status:** method distinctions and the need to state sample, edge, corner and cell-coverage conventions are checked against the cited teaching and research sources. The lesson's cell-coverage equations are definitions, not claims that a particular library implements exact coverage.
- **Implementation:** no new rasterization or traversal code is claimed. The lesson includes a test-design specification.
- **Rights:** links only; no third-party text or figures reproduced.
- **Remaining work:** verify each algorithm's exact variant and build independent, tested implementations with explicit row/column, affine-grid, boundary and NoData contracts.


## Section 10 — Curves, subdivision and trajectory smoothing

**Source entry:** “Curves and smoothing: Chaikin corner cutting, Catmull-Rom, B-splines, NURBS, Bezier fitting (Schneider), Kalman and RTS smoothers” (source page 21).

- **Identity and scope:** the lesson separates approximating subdivision (Chaikin), interpolating splines (Catmull–Rom), parametric design curves (Bézier, B-spline and NURBS) and state estimation/smoothing (Kalman filter and Rauch–Tung–Striebel smoother). These are not equivalent operations.
- **Bibliography and evidence:** de Boor, C. (1987), “Cutting corners always works,” *Computer Aided Geometric Design*, 4(1–2), 125–131, DOI [10.1016/0167-8396(87)90029-X](https://doi.org/10.1016/0167-8396(87)90029-X), discusses convergence of corner-cutting schemes including Chaikin's algorithm. Carnegie Mellon University course notes provide a B-spline chapter describing knot insertion and Chaikin's relationship to uniform quadratic B-splines. A 2021 Springer paper discusses Catmull–Rom as a cubic interpolating spline. Rauch, Tung and Striebel (1965), “Maximum Likelihood Estimates of Linear Dynamic Systems,” *AIAA Journal*, 3(8), 1445–1450, DOI [10.2514/3.3166](https://doi.org/10.2514/3.3166), is the classical RTS smoother reference.
- **Technical-claim status:** the lesson distinguishes interpolation from approximation, rational spline weights from statistical weights, and offline RTS smoothing from geometric spline construction. It warns that unconstrained smoothing can violate road, river or barrier constraints. The lesson is a bounded overview, not a full mathematical treatment of every basis or filter variant.
- **Implementation:** no new spline or Kalman implementation is claimed.
- **Rights:** DOI and institutional links only; no source figures or text reproduced.
- **Remaining work:** verify the Schneider fitting method as its own algorithm; expand NURBS basis and knot multiplicity treatment; build separate spline and state-space implementations with numerical and geometry-specific tests.


## Section 10 — Kernel two-sample testing and spatial distribution shift

**Source entry:** “Kernel two-sample tests and domain divergence metrics for spatial distribution shift” (source page 22).

- **Identity:** maximum mean discrepancy (MMD) is the RKHS integral-probability-metric statistic used for two-sample distribution comparison. The source row is broader than MMD and also names domain-divergence metrics; those other metrics remain separate review tasks.
- **Bibliography:** confirmed: Gretton, A., Borgwardt, K. M., Rasch, M. J., Schölkopf, B. and Smola, A. (2012), “A Kernel Two-Sample Test,” *Journal of Machine Learning Research*, 13, 723–773. The JMLR publisher record confirms the authors, title, volume and page range: https://jmlr.org/papers/v13/gretton12a.html.
- **Technical claims checked:** the cited paper defines MMD through the largest difference in expectations over the unit ball of an RKHS and develops two-sample tests. Its ordinary permutation calibration assumes exchangeability; it does not by itself justify row-wise label permutation for spatially dependent observations.
- **Implementation:** the repository provides unbiased MMD and energy-distance statistics, a row-level permutation baseline for exchangeable independent rows, and a whole-block MMD permutation baseline for equal-sized blocks. The block procedure preserves observations within each block and permutes block labels. It is valid only under a defensible independent/exchangeable-block null with comparable sampling/measurement designs. Arbitrary raster tiles are not thereby independent; cross-block dependence, confounding and non-stationarity are not corrected. The nearest-neighbour applicability envelope is a transparent teaching baseline, not an exact implementation of the Meyer–Pebesma area-of-applicability method.
- **Rights:** link to the JMLR paper only; no article text or figure is reproduced.
- **Review date:** 14 November 2026.
- **Remaining work:** separately verify energy-distance references, block/cluster randomisation designs, domain classifiers, kernel mean matching and the applicability-area method. This note does not verify every method in the grouped source entry.


## Section 4 — Exact Euclidean distance transform

**Source entry:** “Euclidean distance transform (Felzenszwalb)” (raster distance methods).

- **Identity and bibliography:** confirmed: Felzenszwalb, P. F. and Huttenlocher, D. P. (2012), “Distance Transforms of Sampled Functions,” *Theory of Computing*, 8, 415–428, DOI [10.4086/toc.2012.v008a019](https://doi.org/10.4086/toc.2012.v008a019).
- **Technical claims:** the implementation uses the one-dimensional lower envelope of parabolas and separability across raster dimensions. Its one-dimensional result is tested against brute-force minimisation and the two-dimensional result against direct nearest-target distances.
- **Implementation status:** first-principles NumPy/Python implementation with anisotropic row/column spacing; not a SciPy wrapper. Repository CI remains pending.
- **Rights:** citation and DOI link only.

## Section 4 — Multiple-flow-direction routing

**Source entry:** “Flow routing: D8, D-infinity, MFD, priority-flood depression filling and sink breaching” (raster hydrology).

- **Identity and bibliography:** confirmed for Freeman, T. G. (1991), “Calculating catchment area with divergent flow based on a regular grid,” *Computers & Geosciences*, 17(3), 413–422, DOI [10.1016/0098-3004(91)90048-I](https://doi.org/10.1016/0098-3004(91)90048-I), and Holmgren, P. (1994), “Multiple flow direction algorithms for runoff modelling in grid based elevation models: an empirical evaluation,” *Hydrological Processes*, 8(4), 327–334, DOI [10.1002/hyp.3360080405](https://doi.org/10.1002/hyp.3360080405).
- **Technical claims:** this repository implements a bounded power-law MFD variant: all strictly lower neighbours receive fractions proportional to slope raised to a convergence exponent. Flow accumulation validates a downhill DAG and uses topological processing. This is not D-infinity, Qin adaptive MFD, contour-length-corrected MFD or depression conditioning.
- **Implementation status:** implementation and tests prepared; repository CI has not yet completed.
- **Rights:** citation and DOI links only.

## Section 12 — Inhomogeneous point-pattern K

**Source entry:** “Palm distributions, nearest neighbor distance distributions, inhomogeneous K and pair correlation functions” (point-process summaries).

- **Identity and bibliography:** confirmed: Baddeley, A., Møller, J. and Waagepetersen, R. (2000), “Non- and semi-parametric estimation of interaction in inhomogeneous point patterns,” *Statistica Neerlandica*, 54, 329–350, DOI [10.1111/1467-9574.00144](https://doi.org/10.1111/1467-9574.00144).
- **Technical claims:** inverse pointwise-intensity weighting with rectangular translation correction is implemented for supplied positive intensity values. The implementation does not estimate the intensity surface; second-order intensity-reweighted stationarity remains an assumption.
- **Implementation status:** code, tests, method and lab are committed; repository CI pending.
- **Rights:** citation and DOI link only.

## Section 12 — Low-rank thin-plate regression splines

**Source entry:** “GAM and GAMM with spatial smooths (thin plate, Duchon splines, soap film smoothers), Bayesian P-splines” (spatial smoothing).

- **Identity and bibliography:** confirmed: Wood, S. N. (2003), “Thin plate regression splines,” *Journal of the Royal Statistical Society: Series B*, 65(1), 95–114, DOI [10.1111/1467-9868.00374](https://doi.org/10.1111/1467-9868.00374).
- **Technical claims:** the reduced basis is derived from the full thin-plate kernel by removing the affine null space, retaining leading eigendirections and normalising the penalty. The dense implementation matches the full-knot solver when all n−3 penalised directions are retained.
- **Limitations:** the repository implementation does not reproduce mgcv's Lanczos/subsampled large-data basis construction or automatic smoothing selection.
- **Implementation status:** code, tests and lab are committed; repository CI pending.
- **Rights:** citation and DOI link only.

## Section 12 — Forward-filtering backward-simulation particle smoothing

**Source entry:** “Kalman variants: EKF, UKF, ensemble square-root filters, RTS smoothing, particle smoothing” (state estimation).

- **Identity and bibliography:** confirmed: Godsill, S. J., Doucet, A. and West, M. (2004), “Monte Carlo smoothing for nonlinear time series,” *Journal of the American Statistical Association*, 99(465), 156–168, DOI [10.1198/016214504000000151](https://doi.org/10.1198/016214504000000151).
- **Technical claims:** FFBSi samples a terminal filtering particle, then samples earlier particles proportionally to their filtering weight times the transition density to the selected next state.
- **Limitations:** the implementation is offline and requires a transition log density consistent with the forward transition sampler. It is not FFBSm, particle Gibbs, ancestor sampling or a nonlinear RTS smoother.
- **Implementation status:** code, tests and lab are committed; local tests pass, repository CI pending.
- **Rights:** citation and DOI link only.
