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


- `landscape_patch_metrics`: per-class connected-component counts and areas, mean patch area, largest-patch index, and internal horizontal/vertical edge density. Choose 4- or 8-neighbour patch connectivity explicitly; edge counts always use shared cell sides.
- `shannon_diversity`: Shannon diversity of categorical class proportions over valid cells.

Patch edge density excludes the outer raster perimeter and NoData perimeter, and reports shared unlike-class cell boundaries only. When cell size is in metres, edge density is metres per hectare. These are transparent raster metrics, not a full FRAGSTATS implementation; contagion, interspersion/juxtaposition, core area, shape indices, class-specific aggregation and landscape connectivity metrics are not included.
