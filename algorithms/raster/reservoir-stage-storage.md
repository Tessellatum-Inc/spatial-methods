# Reservoir stage-storage curves from a DEM

## Purpose

A raster hypsometric stage-storage calculation estimates how much terrain lies below a sequence of water levels and integrates the depth above each cell elevation.

For stage H, cell elevation z_i, and constant horizontal cell area A_c:

A(H) = A_c sum_i 1(z_i < H), V(H) = A_c sum_i max(H-z_i, 0).

## Contract

reservoir_stage_storage(elevation, stage_levels, cell_area=1.0, valid_mask=None) returns the input stages, inundated area, storage, and valid-cell count. Stages must be finite and strictly increasing. The DEM is a regular grid whose cells have equal horizontal area. All vertical and horizontal units must be compatible for returned volume units.

This is a geometric stage-area-storage curve, not a hydraulic simulation. It does not enforce connectivity to an outlet, exclude isolated depressions, model a spillway or dam, represent bathymetry below the DEM, or account for operational rules, evaporation, seepage or uncertainty. Use a hydrologically conditioned basin mask when disconnected terrain must be excluded.

## Implementation and tests

See the terrain-indices implementation and unit tests.