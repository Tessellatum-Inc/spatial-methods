# Knox space-time interaction test

The Knox test counts pairs of events that are close in both space and time.
It compares the observed count with a Monte Carlo null distribution formed by
permuting event times over fixed locations. The implemented one-sided
alternative is an excess of close-in-space/close-in-time pairs.

## Inputs and output

Coordinates are an N by D numeric array; times are a matching numeric vector.
Spatial and temporal thresholds use caller-defined consistent units. The
result reports the observed pair count, null counts, null mean/standard
deviation, z-score and plus-one Monte Carlo p-value.

## Run

Install with python -m pip install -r requirements.txt, then run
python -m pytest -q.

## Limits

This is an O(N^2) pair-enumeration baseline. It does not implement the
space-time K function, scan statistics, multiple testing correction, edge
correction or a full event-process model. The permutation scheme assumes
exchangeability of event times under the null; trends, seasonality, varying
observation windows and spatially varying sampling intensity require a
different null model. Report the window and thresholds with every result.
