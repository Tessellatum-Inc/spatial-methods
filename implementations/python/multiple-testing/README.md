# Multiple-testing corrections

Dependency-free p-value adjustment methods for family-wise error-rate (FWER) and false-discovery-rate (FDR) control.

## Quick start

~~~python
from multiple_testing import adjust_pvalues
pvalues = [0.001, 0.006, 0.02, 0.03, 0.08, 0.12]
for method in ("bonferroni", "sidak", "holm", "hochberg", "bh", "by"):
    print(method, adjust_pvalues(pvalues, method=method, alpha=0.05))
~~~

## Methods and assumptions

- **Bonferroni:** single-step FWER control under arbitrary dependence.
- **Šidák:** single-step FWER adjustment exact under independent tests.
- **Holm:** step-down FWER procedure valid under arbitrary dependence.
- **Hochberg:** step-up FWER procedure under independence or suitable positive dependence.
- **Benjamini-Hochberg (BH):** step-up FDR control under independence and common positive-dependence conditions.
- **Benjamini-Yekutieli (BY):** harmonic-factor step-up FDR control under arbitrary dependence.

Adjusted p-values are returned in original input order. The supplied p-values define the complete family; the package does not infer family membership.

## Limits

No weighted/structured/online FDR, hierarchical testing, permutation max-T/min-P resampling, Westfall-Young step-down resampling, selective inference or dependence estimation. The user must define the hypothesis family and choose the error criterion.
