# Mathematical morphology

Binary morphology transforms sets using a structuring element. Dilation expands foreground objects; erosion contracts them. Opening (erosion then dilation) removes small foreground features, while closing (dilation then erosion) fills small gaps and holes. The morphological gradient is the symmetric difference between dilation and erosion results.

See [the NumPy implementation](../../implementations/python/morphology/README.md).

The implementation is binary-only, uses explicit boolean footprints and treats out-of-bounds cells as background. Grayscale morphology, reconstruction, skeletonization and geodesic operations remain separate extensions.
