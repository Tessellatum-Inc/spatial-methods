# Mogi point-source deformation

This package implements the analytical Mogi solution for surface displacement caused by an isotropic point source in a homogeneous, isotropic, elastic half-space.

## Install and test

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## Contract

`mogi_displacement` accepts broadcastable east/north observation coordinates, source depth, volume change, Poisson ratio and optional source horizontal coordinates. Coordinate and depth units must match; volume change uses the corresponding cubed unit. Positive volume change represents inflation. Outputs are east, north and vertical displacement plus magnitude.

## Scope

This is a point-source approximation. It does not model finite rectangular dislocations (Okada), finite-fault slip inversion, layered or heterogeneous elastic structure, topography, viscoelastic relaxation, time-varying source geometry, or uncertainty. The approximation is most defensible when source dimensions are small relative to source depth and the half-space assumptions are reasonable.

See `algorithms/geodesy/mogi-point-source.md`.
