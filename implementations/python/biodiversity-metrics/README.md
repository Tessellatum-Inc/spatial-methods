# Biodiversity range and grid metrics

NumPy/SciPy reference implementations for planar occurrence and cell-presence data.

## Install and test

    python -m pip install -r requirements.txt
    python -m pytest -q

## Methods

- `extent_of_occurrence`: convex-hull polygon and area from point occurrences.
- `area_of_occupancy`: count distinct aligned square grid cells; a 2 km grid in projected metres uses `cell_size=2000`.
- `species_richness`: number of present species per grid cell.
- `weighted_endemism`: sum of each present species' inverse occupied-cell range size.

Use suitable projected/equal-area coordinates and declare grid origin/alignment. These are descriptive metric kernels, not a complete IUCN assessment, alpha-hull implementation, range-fragmentation index, key-biodiversity-area delineation or phylogenetic-diversity workflow.
