# Raster range reclassification

NumPy baseline for numeric raster reclassification using explicit, non-overlapping half-open intervals [lower, upper). Rules are sorted internally; gaps receive a caller-selected default and NoData cells can be preserved. The implementation does not infer class breaks, resample grids, transform CRS or perform categorical lookup-table reclassification.

Run `python -m pytest -q`.