# GLCM texture — verification ledger

## Scope
Offset-specific GLCM construction, optional symmetrization/normalization, quantization and six common features are implemented. Moving-window output and full Haralick feature set are not.

## Verification evidence
- Hand-computed 1-D pair-count fixture checks symmetric normalized matrix values.
- Hand-computed two-level distribution checks contrast, dissimilarity, homogeneity, ASM, energy and correlation.
- Tests cover mask/NoData pair exclusion, quantization clipping and invalid offsets/empty matrices.
- Tests are authored but have not been executed in this environment; no passing CI run is claimed.

## Limitations
Quantization must be fixed consistently for cross-scene comparisons. The default is per-image min/max. The correlation convention for a zero-variance marginal is 1.0. Texture windows and directional aggregation remain follow-up work.
