"""Mogi point-source surface deformation in an elastic half-space."""
from __future__ import annotations
import numpy as np


def mogi_displacement(east, north, *, source_depth, volume_change,
                      poisson_ratio=0.25, source_east=0.0, source_north=0.0):
    """Return east, north and vertical displacement at surface observations.

    Coordinates and source depth use one consistent length unit. Volume
    change uses that unit cubed, so displacement is returned in the length
    unit. Positive depth is below the observation plane; positive volume
    change is inflation. The source is an isotropic point in a homogeneous,
    isotropic, elastic half-space.
    """
    try:
        depth, volume, nu = float(source_depth), float(volume_change), float(poisson_ratio)
        x0, y0 = float(source_east), float(source_north)
    except (TypeError, ValueError):
        raise ValueError("source parameters must be numeric") from None
    if not np.all(np.isfinite([depth, volume, nu, x0, y0])):
        raise ValueError("source parameters must be finite")
    if depth <= 0:
        raise ValueError("source_depth must be positive")
    if not 0 < nu < 0.5:
        raise ValueError("poisson_ratio must be between 0 and 0.5")
    x, y = np.broadcast_arrays(np.asarray(east, dtype=float) - x0,
                               np.asarray(north, dtype=float) - y0)
    if not (np.all(np.isfinite(x)) and np.all(np.isfinite(y))):
        raise ValueError("observation coordinates must be finite")
    radius_squared = x*x + y*y + depth*depth
    scale = (1.0 - nu) * volume / np.pi / np.power(radius_squared, 1.5)
    ux, uy, uz = scale*x, scale*y, scale*depth
    magnitude = np.sqrt(ux*ux + uy*uy + uz*uz)
    if ux.ndim == 0:
        return {"east": float(ux), "north": float(uy),
                "vertical": float(uz), "magnitude": float(magnitude)}
    return {"east": ux, "north": uy, "vertical": uz, "magnitude": magnitude}
