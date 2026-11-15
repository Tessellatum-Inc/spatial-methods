# Source verification — multiple-testing corrections

## Identity and bibliography
The procedures are established in Holm (1979), Hochberg (1988), Benjamini and Hochberg (1995), Benjamini and Yekutieli (2001), and Šidák (1967). Maintained R stats p.adjust documentation lists the Holm, Hochberg, BH and BY references and their adjusted-p-value outputs.

## Technical claims
Bonferroni and Holm control FWER under arbitrary dependence. Šidák is exact under independence. Hochberg requires independence or suitable positive dependence. BH controls FDR under independence and common positive-dependence conditions; BY applies the harmonic factor for arbitrary dependence.

## Implementation and reproduction
Implemented: Bonferroni, Šidák, Holm, Hochberg, BH and BY adjusted p-values, plus alpha-based rejection decisions. Tests cover reference values, order restoration, permutation invariance, ties, boundaries, monotonicity, single-test families and invalid inputs.

Not implemented: weighted/hierarchical/online FDR, Westfall-Young resampling, max-T/min-P, selective inference or spatial dependence estimation. The user must define the family. Repository CI is required to establish committed tests pass in its target environment.

## Rights
Algorithms are independently implemented from published definitions; no external source code or figures are reproduced.
