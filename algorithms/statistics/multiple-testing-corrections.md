# Multiple-testing corrections

Control false positives when an analysis evaluates many hypotheses. This lesson implements Bonferroni and Šidák single-step FWER adjustments; Holm step-down and Hochberg step-up FWER procedures; and Benjamini-Hochberg and Benjamini-Yekutieli FDR procedures.

The [Python implementation](../../implementations/python/multiple-testing/README.md) returns adjusted p-values in original input order and decisions at a caller-supplied alpha.

## Spatial interpretation

Local indicators and overlapping spatial windows can be dependent. BH's dependence assumptions must be considered; BY is more conservative but controls FDR under arbitrary dependence. These corrections do not replace spatially designed resampling.

## References

Holm (1979); Hochberg (1988); Benjamini and Hochberg (1995); Benjamini and Yekutieli (2001); Šidák (1967).
