# QA-based cloud and shadow masks

This package provides deterministic mask interpretation for three common
inputs: Landsat Collection 2 QA_PIXEL bit fields, Sentinel-2 Scene
Classification Layer (SCL) codes, and an already-computed 0–100 cloud
probability layer.

## Install and test

    python -m pip install -r requirements.txt
    python -m pytest -q

## Scope

These helpers interpret existing quality layers; they do not detect clouds
from raw reflectance. The Landsat function uses fill, cloud, shadow, cirrus,
snow and dilated-cloud flags. The Sentinel-2 function uses SCL classes and
conservative clear classes by default. The probability helper only applies
a threshold to a supplied probability raster.

This is not an implementation of Fmask, s2cloudless, CloudSEN12 or HLS
harmonisation. Those algorithms/models and their sensor-specific validation
remain separate work. QA bit layouts and SCL semantics must be checked
against the exact sensor/product collection before operational use.
