# Progressive morphological point-cloud ground filter

A rasterised progressive morphological filtering baseline for projected XYZ
point clouds. It builds a minimum-elevation grid from candidate ground points,
nearest-fills empty cells, applies grayscale morphological openings at
increasing odd window sizes, and removes points above a progressive threshold.

## Threshold

For window width w, horizontal cell size c, initial tolerance d0 and slope
factor s, the allowed vertical difference is

    d(w) = min(d_max, d0 + s * c * (w - 1)).

The output is a Boolean mask aligned with the input point order.

## Run

Install with python -m pip install -r requirements.txt, then run
python -m pytest -q.

## Limits

This is a transparent teaching baseline, not a reproduction of every
published progressive morphological filter variant. Raster cell size, window
schedule and threshold parameters materially affect results. Nearest filling
of empty cells is a simplifying assumption; large gaps, steep terrain,
bridges, buildings connected to terrain and dense vegetation can cause
errors. Coordinates must use a consistent projected linear unit. Validate
against reference ground labels and report completeness/correctness by
terrain type before operational use.
