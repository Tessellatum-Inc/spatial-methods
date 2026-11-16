"""Steady-field Lagrangian particle advection and regional connectivity."""
from __future__ import annotations
import numpy as np
from scipy.interpolate import RegularGridInterpolator


def advect_particles_rk4(x_coordinates, y_coordinates, eastward_velocity,
                          northward_velocity, initial_positions, *,
                          time_step, n_steps):
    """Advect particles through a steady 2D velocity field using RK4.

    Velocity arrays have shape (len(y_coordinates), len(x_coordinates)).
    Coordinates may be non-uniform but must be strictly increasing.
    Particles leaving the interpolation domain become inactive; their
    positions are NaN from the first invalid step onward. Units must be
    consistent (for example, metres and seconds).
    """
    x = np.asarray(x_coordinates, dtype=float)
    y = np.asarray(y_coordinates, dtype=float)
    u = np.asarray(eastward_velocity, dtype=float)
    v = np.asarray(northward_velocity, dtype=float)
    positions = np.asarray(initial_positions, dtype=float)
    if x.ndim != 1 or y.ndim != 1 or len(x) < 2 or len(y) < 2:
        raise ValueError("x_coordinates and y_coordinates must be 1D with at least two values")
    if not np.all(np.isfinite(x)) or not np.all(np.diff(x) > 0):
        raise ValueError("x_coordinates must be finite and strictly increasing")
    if not np.all(np.isfinite(y)) or not np.all(np.diff(y) > 0):
        raise ValueError("y_coordinates must be finite and strictly increasing")
    if u.shape != (len(y), len(x)) or v.shape != u.shape:
        raise ValueError("velocity arrays must match (len(y), len(x))")
    if not np.all(np.isfinite(u)) or not np.all(np.isfinite(v)):
        raise ValueError("velocity arrays must contain only finite values")
    if positions.ndim != 2 or positions.shape[1] != 2 or len(positions) == 0:
        raise ValueError("initial_positions must have shape (particles, 2)")
    if not np.all(np.isfinite(positions)):
        raise ValueError("initial_positions must contain only finite coordinates")
    try:
        dt = float(time_step)
    except (TypeError, ValueError):
        raise ValueError("time_step must be finite and positive") from None
    if not np.isfinite(dt) or dt <= 0:
        raise ValueError("time_step must be finite and positive")
    if isinstance(n_steps, (bool, np.bool_)) or not isinstance(n_steps, (int, np.integer)) or n_steps < 1:
        raise ValueError("n_steps must be a positive integer")

    u_interp = RegularGridInterpolator((y, x), u, bounds_error=False, fill_value=np.nan)
    v_interp = RegularGridInterpolator((y, x), v, bounds_error=False, fill_value=np.nan)

    def velocity(points):
        query = np.column_stack((points[:, 1], points[:, 0]))
        return np.column_stack((u_interp(query), v_interp(query)))

    trajectory = np.full((int(n_steps) + 1, len(positions), 2), np.nan, dtype=float)
    trajectory[0] = positions
    active = np.ones(len(positions), dtype=bool)
    current = positions.copy()
    for step in range(1, int(n_steps) + 1):
        ids = np.flatnonzero(active)
        if ids.size == 0:
            break
        p = current[ids]
        k1 = velocity(p)
        k2 = velocity(p + 0.5 * dt * k1)
        k3 = velocity(p + 0.5 * dt * k2)
        k4 = velocity(p + dt * k3)
        valid = (np.all(np.isfinite(k1), axis=1) &
                 np.all(np.isfinite(k2), axis=1) &
                 np.all(np.isfinite(k3), axis=1) &
                 np.all(np.isfinite(k4), axis=1))
        active[ids[~valid]] = False
        if np.any(valid):
            valid_ids = ids[valid]
            updated = p[valid] + (dt / 6.0) * (
                k1[valid] + 2*k2[valid] + 2*k3[valid] + k4[valid])
            current[valid_ids] = updated
            trajectory[step, valid_ids] = updated
        # Invalid particles remain NaN in this and all later trajectory slices.
    return {"trajectory": trajectory, "active": active}


def connectivity_matrix(source_regions, destination_regions, *,
                         n_sources, n_destinations, weights=None):
    """Aggregate particle transitions into weighted regional connectivity.

    Destination ID -1 denotes an unassigned/lost particle. Probabilities are
    normalized by all released weight per source, so each row sums to at most
    one and unassigned mass is returned separately.
    """
    source = np.asarray(source_regions)
    destination = np.asarray(destination_regions)
    if source.ndim != 1 or destination.ndim != 1 or source.shape != destination.shape or source.size == 0:
        raise ValueError("source_regions and destination_regions must be matching non-empty vectors")
    if not np.issubdtype(source.dtype, np.integer) or not np.issubdtype(destination.dtype, np.integer):
        raise ValueError("region identifiers must be integers")
    if isinstance(n_sources, (bool, np.bool_)) or not isinstance(n_sources, (int, np.integer)) or n_sources < 1:
        raise ValueError("n_sources must be a positive integer")
    if isinstance(n_destinations, (bool, np.bool_)) or not isinstance(n_destinations, (int, np.integer)) or n_destinations < 1:
        raise ValueError("n_destinations must be a positive integer")
    if np.any((source < 0) | (source >= n_sources)):
        raise ValueError("source region identifier is outside declared range")
    if np.any((destination < -1) | (destination >= n_destinations)):
        raise ValueError("destination region identifier is outside declared range")
    if weights is None:
        mass = np.ones(source.size, dtype=float)
    else:
        mass = np.asarray(weights, dtype=float)
        if mass.shape != source.shape or not np.all(np.isfinite(mass)) or np.any(mass < 0):
            raise ValueError("weights must be finite, non-negative and match region vectors")
    counts = np.zeros((int(n_sources), int(n_destinations)), dtype=float)
    released = np.zeros(int(n_sources), dtype=float)
    unassigned = np.zeros(int(n_sources), dtype=float)
    np.add.at(released, source, mass)
    lost = destination == -1
    np.add.at(unassigned, source[lost], mass[lost])
    assigned = ~lost
    np.add.at(counts, (source[assigned], destination[assigned]), mass[assigned])
    probabilities = np.divide(counts, released[:, None],
                              out=np.zeros_like(counts),
                              where=released[:, None] > 0)
    unassigned_fraction = np.divide(unassigned, released,
                                    out=np.zeros_like(unassigned),
                                    where=released > 0)
    return {"counts": counts, "probabilities": probabilities,
            "released": released, "unassigned": unassigned,
            "unassigned_fraction": unassigned_fraction}
