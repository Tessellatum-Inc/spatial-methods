# Source verification — Hausdorff and discrete Fréchet distances

## Identity

The Hausdorff metric originates in Hausdorff's *Grundzüge der Mengenlehre* (1914). The discrete Fréchet dynamic program is described by Eiter and Mannila (1994), *Computing Discrete Fréchet Distance*, Technical Report CD-TR 94/64, Vienna University of Technology.

## Implemented scope

The Python baseline computes directed and symmetric Hausdorff distance between finite point sets and discrete Fréchet distance between ordered vertex sequences. The latter uses the standard max-min dynamic-programming recurrence with a rolling row.

## Limitations

Hausdorff is applied to sampled vertices, not continuous segments. Discrete Fréchet is not continuous Fréchet. Both are planar Euclidean computations and require consistent coordinate units. The direct Hausdorff implementation is quadratic in the two point-set sizes; the Fréchet implementation is O(mn) time and O(n) memory.

## Rights

Definitions and algorithm recurrences are paraphrased; no source code or figures are reproduced.
