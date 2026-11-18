# Catalogue crosswalk — Batch 4: bundled methods and unresolved scope

**Date:** 18 November 2026  
**Reviewed head:** `fed4dd557f5b13ae67d8a23df66720d76c0468b8`  
**Scope:** Resolve the Batch 3 name-mapping uncertainty for five GNSS entries and four non-GNSS entries. This is a mapping and bibliographic review; it does not promote source-entry review labels or claim reproduction of source papers.

## GNSS package mappings resolved

Batch 3 listed the following verification slugs as unresolved package-path questions. The current tree contains a single bundled package, `implementations/python/gnss-ambiguity/`, which includes geometry-free cycle-slip screening, Melbourne–Wübbena screening, dual-frequency combinations, Cholesky integer least squares, and LAMBDA-reduced integer search. It is a bounded educational implementation set, not a raw-observation GNSS processor.

| Source/verification record | Package mapping | Status / limit |
|---|---|---|
| `gnss-geometry-free-cycle-slip-screening` | `gnss-ambiguity` | Sequential quadratic prediction residual screen; flags candidates only, no integer slip estimation or repair |
| `gnss-melbourne-wubbena-cycle-slip-screening` | `gnss-ambiguity` | Running mean/noise-threshold screen; code noise, multipath, bias, and paired-slip blind spots remain |
| `gnss-integer-ambiguity-resolution` | `gnss-ambiguity` | Integer least-squares baselines; supplied float vector/covariance, not float ambiguity estimation |
| `gnss-lambda-integer-ambiguity-resolution` | `gnss-ambiguity` | Integer Gauss transforms, permutations, and conditional search; implementation/tests are checked separately from paper claims |
| `gnss-residual-raim-fde` | `gnss-raim` | Snapshot residual chi-square and single-measurement leave-one-out FDE; not aviation-certified RAIM/ARAIM, no protection levels or integrity risk bounds |

Package READMEs reviewed directly at the reviewed head: `implementations/python/gnss-ambiguity/README.md` and `implementations/python/gnss-raim/README.md`.

### Technical identity notes

- **Geometry-free cycle-slip screening** and **Melbourne–Wübbena screening** are complementary observables, not interchangeable detectors. GF phase combinations suppress geometry but are sensitive to ionosphere and combination noise; MW wide-lane combines phase and code and can be strongly affected by code noise and multipath.
- **LAMBDA** is a covariance-aware integer least-squares method with ambiguity decorrelation and conditional search. The package is not an end-to-end PPP/RTK estimator. A fixed ambiguity candidate or ratio statistic alone is not an integrity guarantee.
- **Residual RAIM/FDE** here is a small linear-model exercise: residual test, single-observation deletion candidates and ambiguity reporting. A unique deletion is not proof of fault identity; safety-critical integrity needs fault hypotheses, missed-detection/false-alarm risk, protection levels, availability/continuity analysis and model-specific monitoring.

## Remaining four canonical records: mapping stays open

| Record | Evidence / implementation observation | Current classification |
|---|---|---|
| Hansen–Hurwitz estimator | The with-replacement estimator weights each draw by inverse draw probability and averages draw-level total estimates. It differs from Horvitz–Thompson under without-replacement designs. No dedicated package is present in the current implementation tree. | Canonical identity supported; implementation mapping not found |
| Hausdorff and discrete Fréchet distance | Canonical record covers finite point-set Hausdorff and ordered vertex-sequence discrete Fréchet. Continuous Hausdorff of geometric sets and continuous Fréchet are different scopes; no dedicated package README was found. | Canonical identity supported; implementation mapping not found |
| Harris market potential | Canonical record describes destination market mass weighted by inverse-power distance decay, with configurable exponent and self-potential treatment. No dedicated package README was found. | Canonical identity supported; implementation mapping not found |
| Inhomogeneous Ripley K | Canonical record describes the ordered-pair intensity-reweighted estimator with optional rectangular translation correction. The existing `ripley-k` package README documents homogeneous K/L and a CSR envelope, not the inhomogeneous estimator. | Canonical record exists; package implementation not confirmed in tree |

## Bibliographic anchors for follow-up verification

- **Geometry-free and MW cycle-slip methods:** Blewitt (1990), “An automatic editing algorithm for GPS data,” *Geophysical Research Letters*, 17(3), 199–202, DOI https://doi.org/10.1029/GL017i003p00199. Complementary GF/HMW cycle-slip processing is also described in the recent multi-GNSS literature; do not treat any one combination as universally sufficient.
- **LAMBDA:** Teunissen, de Jonge & Tiberius (1995), “The LAMBDA-method for fast GPS surveying,” proceedings paper; and Teunissen (1995), “The least-squares ambiguity decorrelation adjustment: a method for fast GPS integer ambiguity estimation,” *Journal of Geodesy*, 70, 65–82, DOI https://doi.org/10.1007/BF00863419. Teunissen et al. (1997), *Navigation*, 44(3), 373–383, DOI https://doi.org/10.1002/j.2161-4296.1997.tb02355.x provides a performance discussion.
- **Hansen–Hurwitz:** Hansen & Hurwitz (1943), “On the theory of sampling from finite populations,” *Annals of Mathematical Statistics*, 14(4), 333–362, DOI https://doi.org/10.1214/aoms/1177731356. Scope is independent with-replacement draws with known draw probabilities.
- **Discrete Fréchet:** Eiter & Mannila (1994), *Computing Discrete Fréchet Distance*, Technical Report CD-TR 94/64, Vienna University of Technology. The continuous polygonal-curve Fréchet method is separately treated by Alt & Godau (1995), “Computing the Fréchet distance between two polygonal curves,” *International Journal of Computational Geometry & Applications*, 5(1–2), 75–91.
- **Harris market potential:** Harris (1954), “The Market as a Factor in the Localization of Industry in the United States,” *Annals of the Association of American Geographers*, DOI https://doi.org/10.1080/00045605409352140.
- **Inhomogeneous Ripley K:** The inhomogeneous estimator requires intensity reweighting of pairs, generally under an estimated or specified spatial intensity surface; it is not equivalent to homogeneous K with only an edge correction. The current record's supplied intensity contract is a narrow baseline and does not implement intensity estimation or global inference.

## Next action

Do not mark these rows Fully verified. Continue package mapping by examining likely related implementations and tests, then independently audit the source identity, exact estimator/variant, bibliography, numerical contract, and rights. A name match or README match is not a complete source review.
