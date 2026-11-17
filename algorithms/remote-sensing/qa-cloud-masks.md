# QA-based cloud and shadow masking

Quality-layer masks convert sensor-provided flags into boolean clear-pixel
masks. The reference package supports Landsat Collection 2 QA_PIXEL bit
fields, Sentinel-2 Scene Classification Layer (SCL) classes, and thresholding
of an existing cloud-probability layer.

This is not Fmask or s2cloudless: it does not infer clouds from reflectance,
project cloud shadows, or train a classifier. It only interprets supplied
quality layers and requires product-specific QA semantics to be confirmed.
