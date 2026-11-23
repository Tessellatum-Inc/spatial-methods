# Multiple-testing corrections

Spatial analysis often produces many simultaneous tests: local indicators, raster cells, scan windows, model coefficients or pairwise comparisons. Define the hypothesis family and error criterion before choosing a correction.

## Family-wise error rate

For m p-values:
- **Bonferroni:** p_i^adj = min(1, m p_i); controls FWER under arbitrary dependence.
- **Šidák:** p_i^adj = 1 - (1-p_i)^m; exact under independence.
- **Holm step-down:** sort p_(1) ≤ … ≤ p_(m), compare p_(i) with alpha/(m-i+1), stopping at the first failure. Adjusted values are cumulative maxima of (m-i+1)p_(i), capped at one; valid under arbitrary dependence.
- **Hochberg step-up:** compare from the largest p-value downward using alpha/(m-i+1). Adjusted values are reverse cumulative minima of (m-i+1)p_(i); validity requires independence or suitable positive dependence.

## False discovery rate

- **Benjamini-Hochberg (BH):** p_(i)^adj = min_{j≥i} m p_(j)/j, capped at one. Controls FDR under independence and common positive-dependence conditions.
- **Benjamini-Yekutieli (BY):** multiply BH factors by c_m = sum_{j=1}^m 1/j. Controls FDR under arbitrary dependence but is more conservative.

The implementation returns adjusted values in original order and decisions for caller-supplied alpha. The supplied p-values form the complete family.

## Spatial cautions

Local Moran tests, raster-cell tests and overlapping scan windows can be dependent. Do not automatically apply BH when its dependence conditions are not defensible; BY or a spatially designed resampling/max-statistic procedure may be more appropriate. Multiplicity correction does not fix a misspecified spatial null, edge effects or spatial confounding.

## Scope

No Westfall-Young resampling, max-T/min-P, weighted or hierarchical FDR, online FDR or selective inference.

## References

- Holm, S. (1979). “A Simple Sequentially Rejective Multiple Test Procedure.” *Scandinavian Journal of Statistics*, 6, 65–70. JSTOR [4615733](https://www.jstor.org/stable/4615733).
- Hochberg, Y. (1988). “A Sharper Bonferroni Procedure for Multiple Tests of Significance.” *Biometrika*, 75(4), 800–802. DOI [10.1093/biomet/75.4.800](https://doi.org/10.1093/biomet/75.4.800).
- Benjamini, Y. and Hochberg, Y. (1995). “Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing.” *JRSS B*, 57(1), 289–300. DOI [10.1111/j.2517-6161.1995.tb02031.x](https://doi.org/10.1111/j.2517-6161.1995.tb02031.x).
- Benjamini, Y. and Yekutieli, D. (2001). “The Control of the False Discovery Rate in Multiple Testing under Dependency.” *Annals of Statistics*, 29(4), 1165–1188. DOI [10.1214/aos/1013699998](https://doi.org/10.1214/aos/1013699998).
- Šidák, Z. (1967). “Rectangular Confidence Regions for the Means of Multivariate Normal Distributions.” *JASA*, 62(318), 626–633. DOI [10.1080/01621459.1967.10482935](https://doi.org/10.1080/01621459.1967.10482935).
