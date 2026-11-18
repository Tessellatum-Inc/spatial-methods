# Catalogue crosswalk — Batch 2: direct name matches inspected

**Snapshot:** 18 November 2026  
**Inspected tree:** `e264b26d9eef53ac08f0667b3c9b8ec76b9bba5d`  
**Current branch:** `completion/section-22-atomic-audit`

This batch inspected 20 Python package README files for the exact matching verification record/package slug. The mappings below are direct-slug relationships with scope notes retained in package documentation; this is a file inspection, not a full algorithm validation.

## Inspected matches

- [`accuracy-assessment`](verification/accuracy-assessment.md)
- [`ace-detection`](verification/ace-detection.md)
- [`adaptive-sampling`](verification/adaptive-sampling.md)
- [`adaptive-thresholding`](verification/adaptive-thresholding.md)
- [`alpha-shapes`](verification/alpha-shapes.md)
- [`atgp-endmembers`](verification/atgp-endmembers.md)
- [`cem-detection`](verification/cem-detection.md)
- [`change-point-detection`](verification/change-point-detection.md)
- [`classification-breaks`](verification/classification-breaks.md)
- [`closest-pair`](verification/closest-pair.md)
- [`collision-broadphase`](verification/collision-broadphase.md)
- [`constrained-delaunay`](verification/constrained-delaunay.md)
- [`contraction-hierarchies`](verification/contraction-hierarchies.md)
- [`drainage-basin-morphometry`](verification/drainage-basin-morphometry.md)
- [`drought-indices`](verification/drought-indices.md)
- [`edge-detection`](verification/edge-detection.md)
- [`factor-analysis`](verification/factor-analysis.md)
- [`fay-herriot`](verification/fay-herriot.md)
- [`fcls-unmixing`](verification/fcls-unmixing.md)
- [`fft-grid-kde`](verification/fft-grid-kde.md)

## Scope cautions identified during this inspection

- **ACE, CEM, ATGP and FCLS:** separate hyperspectral methods with distinct assumptions; avoid conflating detector outputs or endmember selection with classification.
- **Adaptive sampling:** combines a network adaptive cluster sampling method and a finite-candidate GP-UCB example; this package is intentionally broader than a single named technique.
- **Alpha shapes:** parameter `alpha` is explicitly documented as a radius in coordinate units (some libraries use a reciprocal convention).
- **Classification breaks:** includes six distinct break methods, not a universal “best” classifier.
- **Contraction hierarchies:** directed graph weights and contraction order are explicit; the default degree order is pedagogical, not a production road-network ordering heuristic.
- **Fay–Herriot:** area-level model assumptions, sampling variances and approximate prediction-MSE boundary are documented.
- **FFT grid KDE:** binned/grid-convolution approximation is distinguished from exact KDE; extent, bandwidth and grid resolution affect error.
- **Edge detection:** thresholds are absolute gradient magnitudes, not auto-normalised across images.
- **Drought indices:** VCI/TCI/VHI/SPI/GDD have calibration/seasonality assumptions; they are indicators rather than forecasts.

## Current-tree reconciliation

A subsequent tree-level check at branch head `d6130f6bb7631068ae0404947429808c9320d2f4` confirmed that all 20 canonical verification files named in this crosswalk still exist. This check was performed against the canonical `catalog/verification/` directory; the earlier README inspection of package paths remains the evidence for implementation-file presence.


## Limitations

This pass did not inspect source indexes, package code, test execution, notebooks or primary literature. Matching slugs and file presence are evidence of structural alignment only. Verification status remains unchanged until the algorithm record's technical claims, source identity, bibliography and rights are independently reviewed.
