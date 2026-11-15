# Selected source-verification notes

Last updated: 15 November 2026

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


## Section 14 — Circular Poisson spatial scan statistic

**Source entry:** “Cluster tests for case data: Cuzick-Edwards, Whittemore, spatial scan with covariates” (spatial epidemiology).

- **Identity and bibliography:** confirmed: Kulldorff, M. (1997), “A spatial scan statistic,” *Communications in Statistics—Theory and Methods*, 26(6), 1481–1496, DOI [10.1080/03610929708831995](https://doi.org/10.1080/03610929708831995).
- **Technical claims:** the implemented baseline searches centroid-centred circular zones under a Poisson model with population offset. The expected count in a zone is the total cases multiplied by its population share; the high-rate log-likelihood ratio is maximised over candidate circles.
- **Monte Carlo calibration:** conditional on total cases, simulated area counts follow a multinomial distribution with probabilities proportional to population. The plus-one p-value is used.
- **Limitations:** no covariate adjustment, Bernoulli model, time scan, elliptical/arbitrary zones or secondary cluster extraction. This is not a full SaTScan reproduction.
- **Implementation status:** implementation, tests and lab are prepared; repository CI pending.
- **Rights:** citation and DOI link only.


## Section 18 — Pareto multi-criteria shortest paths

**Source entry:** “Multi-criteria routing: Pareto label-setting (Martins), bi-objective shortest path, skyline routes, eco-routing, scenic and safe routing” (multi-objective routing).

- **Identity and bibliography:** confirmed: Martins, E. Q. V. (1984), “On a multicriteria shortest path problem,” *European Journal of Operational Research*, 16(2), 236–245, DOI [10.1016/0377-2217(84)90077-8](https://doi.org/10.1016/0377-2217(84)90077-8).
- **Technical claims:** labels accumulate nonnegative cost vectors. Componentwise dominance removes labels that cannot be Pareto-optimal; all remaining nondominated source-to-target paths are returned.
- **Limitations:** worst-case frontier size is exponential. This is not a transit-integrated route-choice model, eco-routing model, or skyline route service.
- **Implementation status:** implementation, tests and lab are prepared; repository CI pending.
- **Rights:** citation and DOI link only.


## Section 22 — Compositional data and log-ratio geometry

**Source entry:** “Compositional data: Aitchison geometry, log-ratio transforms, compositional kriging” (compositional statistics).

- **Identity and bibliography:** confirmed: Aitchison (1982), “The statistical analysis of compositional data,” *JRSS B*, 44(2), 139–160, DOI [10.1111/j.2517-6161.1982.tb01195.x](https://doi.org/10.1111/j.2517-6161.1982.tb01195.x); Egozcue et al. (2003), “Isometric logratio transformations for compositional data analysis,” *Mathematical Geology*, 35(3), 279–300, DOI [10.1023/A:1023818214614](https://doi.org/10.1023/A:1023818214614).
- **Technical claims:** CLR coordinates sum to zero; ILR projects log parts onto an orthonormal zero-sum basis and preserves Aitchison distance; ALR depends on the denominator part.
- **Limitations:** zero replacement, compositional kriging, spatial dependence and regression remain open. The implementation rejects zeros rather than inserting an arbitrary pseudocount.
- **Implementation status:** implementation, tests and lab are prepared; repository CI pending.
- **Rights:** citations and DOI links only.


## Section 2 — Marshall empirical Bayes area-rate smoothing

**Source entry:** “Empirical Bayes rate smoothing, head-banging, median polish” (source page 4).

- **Identity and bibliography:** the Marshall method is confirmed: Marshall, R. J. (1991), “Mapping Disease and Mortality Rates Using Empirical Bayes Estimators,” *Journal of the Royal Statistical Society: Series C*, 40(2), 283–294, DOI [10.2307/2347593](https://doi.org/10.2307/2347593). Publisher metadata and the article's method sections were checked; the maintained spdep EBest documentation cites Marshall for the global Poisson moment estimator.
- **Technical claims:** the article derives a global moment shrinkage estimator and a local neighbourhood variant. Global shrinkage is invariant to spatial arrangement; local shrinkage uses an explicitly defined neighbourhood and a local homogeneity assumption.
- **Implementation:** global and local moment estimators, tests and executable lab are added. The implementation does not cover head-banging, median polish, Clayton–Kaldor iterative maximum likelihood or hierarchical CAR/BYM disease mapping.
- **Rights:** mathematical equations are independently typeset and paraphrased; no article text or figures are reproduced.


## Section 2 — Quadrat count test for complete spatial randomness

**Source entry:** “Quadrat analysis, Clark-Evans, nearest neighbor index” (source page 3).

- **Identity and bibliography:** quadrat counting is a classical CSR diagnostic. The equal-area partition and Pearson statistic are documented in spatial point-process teaching references and maintained spatstat documentation.
- **Technical claims:** conditional on the observed total number of points, homogeneous CSR implies multinomial cell counts with equal probabilities. The implementation simulates this conditional multinomial null rather than relying on the asymptotic chi-square approximation; specialist spatstat documentation notes the expected-count condition for that approximation and also describes conditional Monte Carlo testing.
- **Implementation:** rectangular equal-area grid, explicit boundary assignment, Pearson statistic and plus-one Monte Carlo p-value. The grid scale/alignment is analyst-chosen; the method cannot distinguish interaction from first-order inhomogeneity.
- **Rights:** equations are paraphrased; no source text or figures are reproduced.


## Section 2 — Geographic distribution summaries

**Source entry:** “Summary geometry: mean center, median center, standard distance, standard deviational ellipse” (source page 3).

- **Identity and bibliography:** the four methods are identified in Esri's maintained ArcGIS Pro documentation for measuring geographic distributions. The median-center algorithm's classical reference is Kuhn and Kuenne (1962), “An Efficient Algorithm for the Numerical Solution of the Generalized Weber Problem in Spatial Economics,” *Journal of Regional Science*, 4(2), 21–33, DOI [10.1111/j.1467-9787.1962.tb00902.x](https://doi.org/10.1111/j.1467-9787.1962.tb00902.x).
- **Technical claims:** mean center is a weighted coordinate average; median center minimizes weighted Euclidean distance; standard distance is a weighted RMS radial distance; the ellipse uses the weighted coordinate covariance eigensystem.
- **Implementation:** weighted planar point-coordinate methods and an executable lab are added. The ellipse orientation is explicitly counterclockwise from +x; the scale parameter makes the bivariate-normal coverage adjustment visible rather than implicit.
- **Limitations:** no line/polygon centroid preprocessing, geographic distances, 3D ellipsoids, case grouping or inferential tests.
- **Rights:** equations are independently typeset and paraphrased; no proprietary code or figures are reproduced.


## Section 2 — Area-level inequality and two-group segregation measures

**Source entry:** “Spatial Gini, Theil, spatial entropy, segregation indices (dissimilarity, isolation)” (source page 4).

- **Identity and bibliography:** Duncan and Duncan (1955), “A Methodological Analysis of Segregation Indexes,” *American Sociological Review*, 20(2), 210–217, DOI 10.2307/2088328; Massey and Denton (1988), “The Dimensions of Residential Segregation,” *Social Forces*, 67(2), 281–315, DOI 10.1093/sf/67.2.281; Shannon (1948), “A Mathematical Theory of Communication,” *Bell System Technical Journal*, 27(3), 379–423, DOI 10.1002/j.1538-7305.1948.tb01338.x; Theil (1967), *Economics and Information Theory*.
- **Technical claims:** the package implements population-weighted Gini and Theil T/L for area values, Shannon entropy of population shares, two-group dissimilarity, and group-A isolation/interaction exposure.
- **Scope:** the Gini and entropy functions are area-level summaries and do not incorporate distances or adjacency. Dissimilarity measures evenness; isolation/interaction measure exposure. Distance-weighted spatial Gini, multi-group decomposition, clustering, concentration and centralization remain open.
- **Rights:** formulas are independently typeset and paraphrased; no source code or figures are reproduced.


## Section 2 — Multiple-testing corrections

**Source entry:** “Inference: permutation and Monte Carlo tests, Bonferroni, FDR and Šidák correction, Dutilleul's modified t-test, spatial and block bootstrap” (source page 3).

- **Identity and bibliography:** Holm (1979), Hochberg (1988), Benjamini and Hochberg (1995), Benjamini and Yekutieli (2001), and Šidák (1967) are confirmed by original article metadata and maintained R p.adjust documentation.
- **Technical claims:** Bonferroni and Holm control FWER under arbitrary dependence; Šidák is exact under independence; Hochberg requires independence or suitable positive dependence; BH controls FDR under independence and common positive-dependence conditions; BY uses the harmonic factor for arbitrary dependence.
- **Implementation:** six procedures return adjusted p-values in original input order and alpha-based decisions. Dutilleul's modified t-test and spatial/block bootstrap remain open.
- **Rights:** independently implemented from published definitions; no source code is copied.


## Section 2 — Weighted head-banging smoother

**Source entry:** “Empirical Bayes rate smoothing, head-banging, median polish” (source page 4).

- **Identity and bibliography:** Hansen (1991), “Head-banging: Robust smoothing in the plane,” *IEEE Transactions on Geoscience and Remote Sensing*, 29(3), 369–378; Mungiole, Pickle and Simonson (1999), “Application of a weighted head-banging algorithm to mortality data maps,” *Statistics in Medicine*, 18(23), 3201–3209, DOI 10.1002/(SICI)1097-0258(19991215)18:23%3C3201::AID-SIM310%3E3.0.CO;2-U. The public NCI Head-Bang documentation and CDC methods description were used to check the algorithm's screens, weights and parameter defaults.
- **Technical claims:** k-nearest neighbours form nearly-collinear triples; weighted medians of lower/higher endpoints define screens; a weighted median of low screen, target and high screen updates the target. The implementation fixes geometry and triple membership, then updates synchronously.
- **Implementation:** weighted head-banging, tests and lab added. Locations with no qualifying triples are unchanged; full software corner-point rules and automatic parameter selection remain unimplemented. Median polish remains open.
- **Rights:** independent implementation from published descriptions and public government documentation; no software code or figures copied.


## Section 2 — Tukey median polish

**Source entry:** “Empirical Bayes rate smoothing, head-banging, median polish” (source page 4).

- **Identity and bibliography:** Tukey (1977), *Exploratory Data Analysis*, is the foundational reference. The maintained R stats::medpolish documentation confirms the overall + row + column additive model, alternating row/column median removal, proportional reduction in absolute residual sum as the convergence rule, and optional missing-value removal.
- **Implementation:** two-way median polish with overall/row/column effects, residuals, optional missing-value handling and convergence history. The classic parachuting-deaths example is included in tests and lab.
- **Limitations:** no weights, interactions, multiway arrays or spatial neighbourhood structure. The grouped source entry remains partial because other disease-mapping variants such as Clayton–Kaldor and CAR/BYM are not implemented.
- **Rights:** independent implementation; no R source code or figures copied.


## Section 2 — Moran eigenvector spatial filtering

**Source entry:** “Spatial eigenvector filtering (Moran eigenvectors), Spatial+, restricted spatial regression” (source page 2).

- **Identity and bibliography:** Griffith (2003), *Spatial Autocorrelation and Spatial Filtering*; Griffith and Peres-Neto (2006), “Spatial modeling in ecology: the flexibility of eigenfunction spatial analyses,” *Ecology*, 87(11), 2603–2613; Tiefelsdorf and Griffith (2007), “Semiparametric Filtering of Spatial Autocorrelation: The Eigenvector Approach,” *Environment and Planning A*, 39(5), 1193–1221, DOI 10.1068/a37378.
- **Technical claims:** the intercept-centered symmetric matrix HWH yields orthogonal eigenvectors describing spatial patterns. The subset selection is central to full ESF; literature uses fit, significance or residual-autocorrelation objectives.
- **Implementation:** positive HWH eigenvectors and a fixed-size OLS filter are implemented. This baseline requires the analyst to specify the number of components and does not reproduce the semiparametric selection procedure.
- **Limitations:** general covariate projection, Spatial+, restricted spatial regression, GLM filters and inferential corrections remain open.
- **Rights:** independent implementation from published definitions; no package code or figures copied.
