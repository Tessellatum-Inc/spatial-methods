# Verification dossier: grayscale area morphology

## Implemented
- Grayscale area opening by threshold-level connected components.
- Dual area closing.
- Four- and eight-neighbour connectivity.

## Independent tests
Tests cover removal of a small bright island, preservation and idempotence of a larger component, filling of a small dark hole, connectivity-dependent diagonal components, invalid area/connectivity parameters and non-finite raster rejection.

## Exclusions
Canonical max-tree/min-tree construction, alpha-tree, shape attributes, other connected attribute filters and large-raster optimisation remain open. The grouped source entry remains Partial.
