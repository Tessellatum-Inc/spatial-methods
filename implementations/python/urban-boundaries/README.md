# Urban boundary and natural-city baselines

Install and test with `python -m pip install -r requirements.txt && python -m pytest -q`.

- Building-centroid DBSCAN clusters projected point coordinates using a declared metric radius.
- Building-density gridding counts centroids in caller-supplied axis-aligned cells.
- Connected urban areas labels density-thresholded cells with 4- or 8-neighbour connectivity and a minimum component size.
- The head/tail method recursively thresholds the positive density tail by its mean, stopping when the head is no longer a minority under the caller's criterion. Candidate natural-city cells are above the final threshold.

These are exploratory methods, not a validated city-clustering algorithm or official urban boundaries. Grid size, projection, density threshold, DBSCAN radius, minimum cluster size and head/tail stopping rule materially change results. No building-footprint QA, stochastic percolation, population threshold, functional commuting definition or administrative validation is supplied.
