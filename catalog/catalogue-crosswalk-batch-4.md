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

## Four-record implementation mapping reconciliation

| Record | Evidence / implementation observation | Current classification |
|---|---|---|
| Hansen–Hurwitz estimator | Dedicated package `implementations/python/hansen-hurwitz/` includes estimator, unit tests, README, requirements and isolated CI registration. | Mapping confirmed; CI pending at current head |
| Hausdorff and discrete Fréchet distance | `implementations/python/geometry-metrics/` directly covers sampled-point Hausdorff, discrete Fréchet, and continuous Fréchet decision/approximation, with scopes distinguished in its README. | Mapping confirmed; variant-specific source review remains open |
| Harris market potential | Existing `implementations/python/regional-dynamics/market_potential.py` provides inverse-power impedance with configurable exponent and self-potential policy; `test_market_potential.py` and the registered lab notebook cover it. No separate package is required. | Mapping confirmed; CI pending at current head |
| Inhomogeneous Ripley K | Existing `implementations/python/ripley-k/ripley_k.py` includes `inhomogeneous_ripley_k`, supplied event-specific intensity weighting, and optional rectangular translation correction; `test_ripley_k.py` covers constant-intensity equivalence, event weights and validation. | Mapping confirmed; CI pending at current head |

## Bibliographic anchors for follow-up verification

- **Geometry-free and MW cycle-slip methods:** Blewitt (1990), “An automatic editing algorithm for GPS data,” *Geophysical Research Letters*, 17(3), 199–202, DOI https://doi.org/10.1029/GL017i003p00199. Complementary GF/HMW cycle-slip processing is also described in the recent multi-GNSS literature; do not treat any one combination as universally sufficient.
- **LAMBDA:** Teunissen, de Jonge & Tiberius (1995), “The LAMBDA-method for fast GPS surveying,” proceedings paper; and Teunissen (1995), “The least-squares ambiguity decorrelation adjustment: a method for fast GPS integer ambiguity estimation,” *Journal of Geodesy*, 70, 65–82, DOI https://doi.org/10.1007/BF00863419. Teunissen et al. (1997), *Navigation*, 44(3), 373–383, DOI https://doi.org/10.1002/j.2161-4296.1997.tb02355.x provides a performance discussion.
- **Hansen–Hurwitz:** Hansen & Hurwitz (1943), “On the theory of sampling from finite populations,” *Annals of Mathematical Statistics*, 14(4), 333–362, DOI https://doi.org/10.1214/aoms/1177731356. Scope is independent with-replacement draws with known draw probabilities.
- **Discrete Fréchet:** Eiter & Mannila (1994), *Computing Discrete Fréchet Distance*, Technical Report CD-TR 94/64, Vienna University of Technology. The continuous polygonal-curve Fréchet method is separately treated by Alt & Godau (1995), “Computing the Fréchet distance between two polygonal curves,” *International Journal of Computational Geometry & Applications*, 5(1–2), 75–91.
- **Harris market potential:** Harris (1954), “The Market as a Factor in the Localization of Industry in the United States,” *Annals of the Association of American Geographers*, DOI https://doi.org/10.1080/00045605409352140.
- **Inhomogeneous Ripley K:** The inhomogeneous estimator requires intensity reweighting of pairs, generally under an estimated or specified spatial intensity surface; it is not equivalent to homogeneous K with only an edge correction. The current record's supplied intensity contract is a narrow baseline and does not implement intensity estimation or global inference.

## Next action

Do not mark these rows Fully verified. Mapping is now confirmed for all four records; continue the independent source identity, exact estimator/variant, bibliography, numerical contract, and rights review. A name match, README match or passing unit test is not a complete source review.


## Implementation follow-up — Hansen–Hurwitz (18 November 2026)

- Added a dedicated NumPy package at `implementations/python/hansen-hurwitz/` with estimator, tests, README and isolated CI registration.
- The implementation keeps repeated draws in the ordered sample, estimates the total as the mean of (y_i/p_i), estimates variance as the sample variance of draw-level estimates divided by (n), and optionally scales to mean/mean variance for a supplied population size.
- Updated `catalog/verification/hansen-hurwitz.md` to link the implementation and distinguish CI pending from tests authored.
- Package CI registration adds one isolated Python test shard. Current CI must validate the new files before this implementation is marked tested.


## Follow-up mapping corrections — 18 November 2026

The previous four-record table is superseded by these current tree findings:

- **Hansen–Hurwitz:** dedicated package `implementations/python/hansen-hurwitz/` now exists, with estimator, tests, README, requirements and isolated Python CI manifest registration. Validation awaits current-head CI.
- **Hausdorff and Fréchet:** the previously missed direct mapping is `implementations/python/geometry-metrics/`. README describes point-set directed/symmetric Hausdorff, discrete Fréchet, and a separate continuous Fréchet decision/approximation implementation. The canonical verification record now links this package and explicitly distinguishes sampled-point Hausdorff, discrete Fréchet and continuous Fréchet.
- **Harris market potential:** mapping is confirmed to `regional-dynamics/market_potential.py`, its dedicated test file and the existing lab notebook. `huff-model` remains a separate probabilistic competitive facility-choice model; do not conflate the two.
- **Inhomogeneous Ripley K:** mapping is confirmed to the existing `inhomogeneous_ripley_k` function in the `ripley-k` package, including tests and supplied-intensity limitations.

These are mapping-only findings; source-entry review labels remain unchanged.