# Irregular eligibility masks: spatial uncertainty coverage diagnostic

**Status:** exploratory; estimator unit tests and the irregular-mask CI simulation passed. Moving-window bootstrap and product-kernel HAC both execute on sparse masks, but neither demonstrates nominal coverage under strong dependence. Spatial subsampling explicitly refuses irregular masks.  
**Script:** `simulate_spatial_uncertainty_irregular_masks.py`  
**Validation run:** [GitHub Actions run 45663516998](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45663516998)  
**Artifact:** `spatial-uncertainty-irregular-masks`  
**Design:** 30 × 30 mean-zero separable Gaussian AR(1) fields; 100 realizations per correlation/mask; the same field and mask passed to both supported methods; seed 20261202. Masks are generated independently of field values.

## Selected paired results

Coverage for width 8 and width 12. Wilson intervals are 95% intervals for the Monte Carlo coverage proportion.

| Mask | ρ | Moving 8 | HAC 8 | Moving 12 | HAC 12 |
|---|---:|---:|---:|---:|---:|
| Random 20% holes | 0.3 | 0.880 (0.802–0.930) | 0.910 (0.838–0.952) | 0.880 (0.802–0.930) | 0.890 (0.814–0.937) |
| Random 20% holes | 0.6 | 0.870 (0.790–0.922) | 0.860 (0.779–0.915) | 0.860 (0.779–0.915) | 0.850 (0.767–0.907) |
| Random 20% holes | 0.8 | 0.610 (0.512–0.700) | 0.630 (0.532–0.718) | 0.690 (0.594–0.772) | 0.700 (0.604–0.781) |
| Single clustered hole | 0.3 | 0.900 (0.826–0.945) | 0.880 (0.802–0.930) | 0.890 (0.814–0.937) | 0.870 (0.790–0.922) |
| Single clustered hole | 0.6 | 0.870 (0.790–0.922) | 0.880 (0.802–0.930) | 0.910 (0.838–0.952) | 0.900 (0.826–0.945) |
| Single clustered hole | 0.8 | 0.700 (0.604–0.781) | 0.680 (0.583–0.763) | 0.720 (0.625–0.799) | 0.710 (0.615–0.790) |
| Edge truncation + holes | 0.3 | 0.880 (0.802–0.930) | 0.910 (0.838–0.952) | 0.870 (0.790–0.922) | 0.890 (0.814–0.937) |
| Edge truncation + holes | 0.6 | 0.870 (0.790–0.922) | 0.860 (0.779–0.915) | 0.860 (0.779–0.915) | 0.870 (0.790–0.922) |
| Edge truncation + holes | 0.8 | 0.660 (0.563–0.745) | 0.680 (0.583–0.763) | 0.690 (0.594–0.772) | 0.720 (0.625–0.799) |
| Multiple clustered holes | 0.3 | 0.860 (0.779–0.915) | 0.850 (0.767–0.907) | 0.880 (0.802–0.930) | 0.880 (0.802–0.930) |
| Multiple clustered holes | 0.6 | 0.800 (0.711–0.867) | 0.810 (0.722–0.875) | 0.820 (0.733–0.883) | 0.800 (0.711–0.867) |
| Multiple clustered holes | 0.8 | 0.710 (0.615–0.790) | 0.720 (0.625–0.799) | 0.750 (0.657–0.825) | 0.760 (0.668–0.833) |

The random-hole masks retained about 719 eligible blocks on average, the single-hole masks 836, edge-truncated masks 689–691, and multiple-hole masks 828–829. Exact counts vary slightly with the randomized mask.

## Interpretation

1. The fixed-inclusion moving-window implementation and spatial HAC both operate with random holes, clustered holes and edge truncation. The structural support is useful, but it is not a coverage guarantee.
2. Under weak dependence, coverage is often around 0.85–0.91. Under strong dependence (ρ=0.8), it falls to roughly 0.61–0.76 across these mask scenarios.
3. Neither method is consistently superior. Differences at a given mask/width are small relative to the Monte Carlo uncertainty.
4. Spatial subsampling reports all irregular-mask cases as unsupported by design. This is preferable to applying a fixed-size scaling rule to variable-size subsamples without justification.
5. The masks are independent of the generated field. Informative missingness (where eligibility depends on the observed process), spatially varying variance and nonstationarity are not covered.

## Decision

Irregular-mask support is now demonstrated computationally for moving-window and HAC candidates, not statistically calibrated. Do not use these intervals as inferential evidence for Nairobi. Next add informative/structured missingness and nonstationary fields, then validate the matched-strata/block-contrast estimand. The spatial subsampling method needs a principled variable-size design before it can join irregular-mask comparisons.
