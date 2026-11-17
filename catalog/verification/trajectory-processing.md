# Verification dossier: trajectory processing

## Implemented scope

- Start-anchored stay-point detection with a distance threshold and minimum elapsed duration.
- Planar Douglas–Peucker simplification, returning retained source indices.
- Euclidean DTW with an optional Sakoe–Chiba index window.
- LCSS similarity with spatial and index tolerances.

## Independent checks

The test suite checks centroid and interval indices for a hand-constructed stay, rejection when temporal and spatial thresholds are not jointly satisfied, endpoint preservation and collinear simplification, corner retention, identity and alignment cases for DTW, LCSS matching fractions, temporal-window effects, and malformed inputs.

## Assumptions and exclusions

The coordinate plane is projected and metric-consistent; timestamps are numeric and non-decreasing. No geodesic conversion, map matching, uncertainty model, imputation, or road-network semantics are included. Stay-point grouping is anchored to the first observation, not bounded by maximum pairwise diameter.

The two source entries remain **Partial**. The implementation does not cover SQUISH, STTrace, opening-window or TD-TR compression, imputation, route recovery, TRACLUS, T-DBSCAN, continuous Fréchet methods, or indexed trajectory search. Bibliographic identity and the full grouped source wording still require independent review.
