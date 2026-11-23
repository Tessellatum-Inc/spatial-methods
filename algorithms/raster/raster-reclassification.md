# Raster range reclassification

Range reclassification maps each input cell through an explicit set of non-overlapping half-open intervals [lower, upper). The lower bound is included and the upper bound excluded. Rules are sorted by lower bound; overlap is rejected rather than resolved by order. Values outside all intervals receive the configured default. NaN values remain NaN, and an explicit NoData sentinel can be preserved.

This operation is distinct from classification-break estimation: the caller supplies the intervals and replacement values. It is also distinct from categorical lookup-table reclassification, resampling and CRS-aware warping. Output is floating-point to support NaN defaults.