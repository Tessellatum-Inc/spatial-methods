# QA cloud-mask walkthrough

1. **Landsat QA_PIXEL.** Interpret the Collection 2 bit field. Fill, cloud
   and cloud-shadow flags always invalidate a pixel; dilated cloud, cirrus
   and snow are configurable. The clear bit is required by default. Water
   remains valid unless another bit invalidates it.
2. **Sentinel-2 SCL.** Retain vegetation, bare/non-vegetated and water
   classes. Unclassified and snow/ice can be explicitly included; shadow,
   cloud, cirrus, saturated and no-data classes are excluded.
3. **Probability raster.** Apply a user-selected threshold to an existing
   0–100 cloud-probability surface. The threshold is not estimated by this
   helper.

The output is a boolean clear-pixel mask with the input shape. These
functions do not perform cloud detection, shadow projection, morphological
buffering or multi-sensor harmonisation.
