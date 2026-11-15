# Multiple-testing corrections — implementation walkthrough

## 1. Define the family
All supplied p-values form one family. Family definition is a scientific design decision, not inferred from variable names or spatial adjacency.

## 2. Family-wise error rate
Bonferroni and Šidák are single-step adjustments. Holm is step-down and valid under arbitrary dependence. Hochberg is step-up and requires independence or suitable positive dependence.

## 3. False discovery rate
Benjamini-Hochberg controls FDR under independence and common positive-dependence conditions. Benjamini-Yekutieli adds the harmonic factor for arbitrary dependence, at a power cost.

## 4. Output order
The implementation sorts internally and restores adjusted p-values to original input order. Rejections are derived from adjusted values and caller alpha.
