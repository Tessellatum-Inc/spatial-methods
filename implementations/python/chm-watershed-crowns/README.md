# Canopy-height local maxima and watershed crowns

A marker-controlled watershed baseline for tree-crown segmentation from a
canopy height model (CHM). It finds local maxima, merges connected peak
plateaus into one deterministic seed each, then floods the negative CHM
inside a canopy-height mask.

## Inputs and outputs

- CHM: 2-D height-above-ground array in a consistent vertical unit.
- canopy_threshold: minimum height included in the segmentation mask.
- min_peak_height: minimum treetop seed height.
- window_size: odd local-maximum neighbourhood width.
- compactness: scikit-image watershed compactness parameter.
- Output: integer crown labels (zero outside canopy) and row/column seed cells.

## Run

Install with python -m pip install -r requirements.txt, then run
python -m pytest -q.

## Limits

This is a CHM-based local-maxima/watershed baseline. It is not the Dalponte
algorithm, does not use point-cloud returns directly, and does not perform
individual tree species classification, crown allometry or field validation.
Window size and height thresholds strongly affect over/under-segmentation.
Evaluate against delineated reference crowns across canopy density, terrain,
sensor resolution and forest type.
