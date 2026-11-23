# Verification record: Otsu thresholding

## Source identity
- Compendium: *Spatial Analysis Algorithms: Complete Compendium*
- Original location: Section 5, page 8
- Source entry: thresholding — Otsu, adaptive

## Implemented scope
- Exact observed-level, two-class global Otsu threshold for finite scalar arrays.
- Optional boolean inclusion mask; non-finite pixels are excluded.
- Binary output with explicit strict-greater-than foreground convention.

## Verification design
- Bimodal fixture.
- 100 seeded random arrays checked against an independent exhaustive
  split-and-score oracle.
- Masking, non-finite values, constant arrays and invalid inputs.
- Translation and positive-scale invariance.

## Limitations
Only global two-class Otsu is implemented. Adaptive/local and multi-level
variants are not included. Tests are authored but execution is pending.
