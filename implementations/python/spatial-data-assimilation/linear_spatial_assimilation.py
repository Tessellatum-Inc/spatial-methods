"""Spatial advection-diffusion and linear data-assimilation teaching models."""
from __future__ import annotations
from numbers import Integral
import numpy as np


def _array(value, name, ndim):
    a = np.asarray(value, dtype=float)
    if a.ndim != ndim or not np.isfinite(a).all():
        raise ValueError(f"{name} must be a finite {ndim}-dimensional array")
    return a


def _covariance(value, name, n, positive_definite=False):
    a = _array(value, name, 2)
    if a.shape != (n, n) or not np.allclose(a, a.T, rtol=1e-10, atol=1e-12):
        raise ValueError(f"{name} must be symmetric with shape ({n}, {n})")
    eig = np.linalg.eigvalsh((a + a.T) / 2)
    tol = 1e-10 * max(1.0, float(np.max(np.abs(eig))))
    invalid = eig.min() <= tol if positive_definite else eig.min() < -tol
    if invalid:
        qualifier = "positive definite" if positive_definite else "positive semidefinite"
        raise ValueError(f"{name} must be {qualifier}")
    return a


def periodic_advection_diffusion_operator(n_cells, cell_width, time_step, velocity, diffusivity):
    """One explicit upwind-advection/centred-diffusion step on a uniform periodic grid."""
    if isinstance(n_cells, bool) or not isinstance(n_cells, Integral) or n_cells < 3:
        raise ValueError("n_cells must be an integer of at least 3")
    dx, dt, u, kappa = map(float, (cell_width, time_step, velocity, diffusivity))
    if not all(np.isfinite(v) for v in (dx, dt, u, kappa)) or dx <= 0 or dt <= 0 or kappa < 0:
        raise ValueError("grid spacing/time step must be positive; parameters finite and diffusivity non-negative")
    c, r = abs(u) * dt / dx, kappa * dt / dx**2
    if c + 2*r > 1 + 1e-12:
        raise ValueError("time step violates explicit advection-diffusion stability bound")
    F = np.zeros((n_cells, n_cells))
    for i in range(n_cells):
        left, right = (i-1) % n_cells, (i+1) % n_cells
        F[i, i] = 1 - c - 2*r
        F[i, left] += r
        F[i, right] += r
        F[i, left if u >= 0 else right] += c
    return F


def periodic_point_observation_operator(n_cells, cell_width, sensor_positions):
    """Periodic linear interpolation from uniform cell-centred states to point sensors."""
    if isinstance(n_cells, bool) or not isinstance(n_cells, Integral) or n_cells < 3:
        raise ValueError("n_cells must be an integer of at least 3")
    dx = float(cell_width)
    pos = _array(sensor_positions, "sensor_positions", 1)
    if not np.isfinite(dx) or dx <= 0 or pos.size == 0:
        raise ValueError("cell_width must be positive and sensor_positions non-empty")
    q = np.mod(pos, n_cells*dx) / dx
    left = np.floor(q).astype(int)
    frac = q-left
    H = np.zeros((pos.size, n_cells))
    rows = np.arange(pos.size)
    H[rows, left] = 1-frac
    H[rows, (left+1) % n_cells] += frac
    return H


def run_linear_spatial_assimilation(initial_mean, initial_covariance, transition_matrix,
                                    process_covariance, observations, *, forecast_steps=0):
    """Run sequential forecast-analysis updates; each item is None or (y,H,R)."""
    mean = _array(initial_mean, "initial_mean", 1).copy()
    n = mean.size
    if n == 0:
        raise ValueError("initial_mean must not be empty")
    P = _covariance(initial_covariance, "initial_covariance", n).copy()
    F = _array(transition_matrix, "transition_matrix", 2)
    if F.shape != (n,n):
        raise ValueError("transition_matrix must match state dimension")
    Q = _covariance(process_covariance, "process_covariance", n)
    if isinstance(forecast_steps, bool) or not isinstance(forecast_steps, Integral) or forecast_steps < 0:
        raise ValueError("forecast_steps must be a non-negative integer")
    fm, fp, am, ap, innovations, innovation_covariances = [], [], [], [], [], []
    for k, item in enumerate(observations):
        mean = F @ mean
        P = F @ P @ F.T + Q
        P = (P + P.T)/2
        fm.append(mean.copy()); fp.append(P.copy())
        if item is None:
            innovations.append(np.empty(0)); innovation_covariances.append(np.empty((0,0)))
        else:
            if not isinstance(item, (tuple,list)) or len(item) != 3:
                raise ValueError(f"observation {k} must be None or (y,H,R)")
            y = _array(item[0], f"observations[{k}].y", 1)
            H = _array(item[1], f"observations[{k}].H", 2)
            if y.size == 0 or H.shape != (y.size,n):
                raise ValueError(f"observation {k} dimensions do not match state")
            R = _covariance(item[2], f"observations[{k}].R", y.size, True)
            d = y-H@mean
            S = H@P@H.T+R
            S = (S+S.T)/2
            try:
                K = np.linalg.solve(S, H@P).T
            except np.linalg.LinAlgError as exc:
                raise ValueError(f"observation {k} innovation covariance is singular") from exc
            mean = mean+K@d
            A = np.eye(n)-K@H
            P = A@P@A.T+K@R@K.T
            P = (P+P.T)/2
            innovations.append(d.copy()); innovation_covariances.append(S.copy())
        am.append(mean.copy()); ap.append(P.copy())
    ffm, ffp = [], []
    for _ in range(int(forecast_steps)):
        mean = F@mean
        P = F@P@F.T+Q
        P = (P+P.T)/2
        ffm.append(mean.copy()); ffp.append(P.copy())
    stack = lambda rows, shape: np.stack(rows) if rows else np.empty(shape)
    return {
        "forecast_means": stack(fm,(0,n)), "forecast_covariances": stack(fp,(0,n,n)),
        "analysis_means": stack(am,(0,n)), "analysis_covariances": stack(ap,(0,n,n)),
        "innovations": innovations, "innovation_covariances": innovation_covariances,
        "free_forecast_means": stack(ffm,(0,n)),
        "free_forecast_covariances": stack(ffp,(0,n,n)),
    }


def periodic_nonuniform_advection_diffusion_operator(cell_widths, time_step,
                                                       face_velocities, face_diffusivities):
    """Conservative explicit finite-volume step on a periodic nonuniform 1-D grid.

    State entries are cell-centred concentrations. Face i is the right face
    between cells i and (i+1) modulo n. Advection uses upwind face values;
    diffusion uses the centre-to-centre gradient. Face velocity and diffusivity
    may vary spatially. The step is accepted only if its transition matrix is
    non-negative (within round-off tolerance).
    """
    widths = _array(cell_widths, "cell_widths", 1)
    n = widths.size
    if n < 3 or np.any(widths <= 0):
        raise ValueError("cell_widths must contain at least three positive values")
    dt = float(time_step)
    if not np.isfinite(dt) or dt <= 0:
        raise ValueError("time_step must be positive and finite")
    velocity = _array(face_velocities, "face_velocities", 1)
    diffusivity = _array(face_diffusivities, "face_diffusivities", 1)
    if velocity.shape != (n,) or diffusivity.shape != (n,) or np.any(diffusivity < 0):
        raise ValueError("face velocity and diffusivity must have one value per face; diffusivity non-negative")
    distances = 0.5 * (widths + np.roll(widths, -1))
    L = np.zeros((n,n))
    for i in range(n):
        j = (i+1) % n
        u, k, distance = velocity[i], diffusivity[i], distances[i]
        a = max(u, 0.0) + k/distance
        b = min(u, 0.0) - k/distance
        L[i,i] -= a/widths[i]
        L[i,j] -= b/widths[i]
        L[j,i] += a/widths[j]
        L[j,j] += b/widths[j]
    F = np.eye(n) + dt*L
    if np.min(F) < -1e-12:
        raise ValueError("time step violates finite-volume positivity/stability bound")
    F[F < 0] = 0.0
    return F



def nonperiodic_nonuniform_advection_diffusion_operator(
        cell_widths, time_step, interior_face_velocities, interior_face_diffusivities):
    """Explicit conservative transport step with zero total flux at both boundaries.

    Cell-centred concentrations occupy a nonperiodic 1-D grid. The n-1
    supplied face velocities and diffusivities describe only interior faces;
    both boundary fluxes are exactly zero. This applies to the combined
    advective-diffusive flux, not merely the diffusive gradient.
    """
    widths = _array(cell_widths, "cell_widths", 1)
    n = widths.size
    if n < 2 or np.any(widths <= 0):
        raise ValueError("cell_widths must contain at least two positive values")
    dt = float(time_step)
    if not np.isfinite(dt) or dt <= 0:
        raise ValueError("time_step must be positive and finite")
    velocity = _array(interior_face_velocities, "interior_face_velocities", 1)
    diffusivity = _array(interior_face_diffusivities, "interior_face_diffusivities", 1)
    if velocity.shape != (n-1,) or diffusivity.shape != (n-1,) or np.any(diffusivity < 0):
        raise ValueError("interior face fields must have n-1 values; diffusivity must be non-negative")
    distances = 0.5 * (widths[:-1] + widths[1:])
    L = np.zeros((n,n))
    for i, (u, k, distance) in enumerate(zip(velocity, diffusivity, distances)):
        a = max(u, 0.0) + k/distance
        b = min(u, 0.0) - k/distance
        L[i,i] -= a/widths[i]
        L[i,i+1] -= b/widths[i]
        L[i+1,i] += a/widths[i+1]
        L[i+1,i+1] += b/widths[i+1]
    F = np.eye(n) + dt*L
    if np.min(F) < -1e-12:
        raise ValueError("time step violates finite-volume positivity/stability bound")
    F[F < 0] = 0.0
    return F


def nonperiodic_nonuniform_advection_diffusion_step(
        cell_widths, time_step, interior_face_velocities,
        interior_face_diffusivities, concentrations, *,
        source_rates=None, boundary_fluxes=(0.0, 0.0)):
    """Advance concentrations with prescribed sources and boundary fluxes.

    Boundary fluxes are oriented in the positive x direction at both ends:
    positive left flux enters the domain, while positive right flux exits it.
    They are prescribed total (advective plus diffusive) fluxes, not fluxes
    inferred from ghost cells or boundary states. Source rates have units of
    concentration per time. The returned mass budget is checked against the
    actual state change. Negative concentrations are rejected, never clipped.
    """
    widths = _array(cell_widths, "cell_widths", 1)
    state = _array(concentrations, "concentrations", 1)
    n = widths.size
    if n < 2 or state.shape != (n,) or np.any(widths <= 0):
        raise ValueError("cell_widths and concentrations must have matching dimensions and positive widths")
    dt = float(time_step)
    if not np.isfinite(dt) or dt <= 0:
        raise ValueError("time_step must be positive and finite")
    if source_rates is None:
        sources = np.zeros(n)
    else:
        sources = _array(source_rates, "source_rates", 1)
        if sources.shape != (n,):
            raise ValueError("source_rates must contain one rate per cell")
    boundaries = _array(boundary_fluxes, "boundary_fluxes", 1)
    if boundaries.shape != (2,):
        raise ValueError("boundary_fluxes must contain (left, right) fluxes")
    transition = nonperiodic_nonuniform_advection_diffusion_operator(
        widths, dt, interior_face_velocities, interior_face_diffusivities)
    updated = transition @ state + dt * sources
    updated[0] += dt * boundaries[0] / widths[0]
    updated[-1] -= dt * boundaries[1] / widths[-1]
    tolerance = 1e-12 * max(1.0, float(np.max(np.abs(state))))
    if np.min(updated) < -tolerance:
        raise ValueError("explicit forced step would produce negative concentrations; reduce time_step or forcing")
    initial_mass = float(widths @ state)
    final_mass = float(widths @ updated)
    source_change = float(dt * (widths @ sources))
    boundary_change = float(dt * (boundaries[0] - boundaries[1]))
    expected_change = source_change + boundary_change
    actual_change = final_mass - initial_mass
    residual = actual_change - expected_change
    budget_tolerance = 1e-10 * max(1.0, abs(initial_mass), abs(expected_change))
    if abs(residual) > budget_tolerance:
        raise ArithmeticError("finite-volume source/boundary mass budget failed")
    return {
        "concentrations": updated,
        "initial_mass": initial_mass,
        "final_mass": final_mass,
        "source_mass_change": source_change,
        "boundary_mass_change": boundary_change,
        "expected_mass_change": expected_change,
        "mass_budget_residual": residual,
    }



def nonperiodic_rectilinear_advection_diffusion_step_2d_with_forcing(
        cell_widths_x, cell_widths_y, time_step,
        x_face_velocities, y_face_velocities,
        x_face_diffusivities, y_face_diffusivities, concentrations, *,
        source_rates=None, boundary_fluxes=None):
    """Advance a 2-D field with cell sources and prescribed total boundary fluxes.

    Boundary flux densities are ordered (left, right, bottom, top). Positive
    left/bottom flux enters the domain; positive right/top flux exits. The
    arrays have shapes (ny,), (ny,), (nx,), (nx,), respectively. Fluxes are
    total advective-diffusive flux densities; they are not inferred from
    boundary states. Source rates have concentration/time units.
    """
    dx = _array(cell_widths_x, "cell_widths_x", 1)
    dy = _array(cell_widths_y, "cell_widths_y", 1)
    state = _array(concentrations, "concentrations", 2)
    nx, ny = dx.size, dy.size
    if state.shape != (nx, ny) or np.any(state < 0):
        raise ValueError("concentrations must be non-negative with shape (nx, ny)")
    if source_rates is None:
        sources = np.zeros((nx, ny))
    else:
        sources = _array(source_rates, "source_rates", 2)
        if sources.shape != (nx, ny):
            raise ValueError("source_rates must have shape (nx, ny)")
    if boundary_fluxes is None:
        boundary_fluxes = (np.zeros(ny), np.zeros(ny), np.zeros(nx), np.zeros(nx))
    if not isinstance(boundary_fluxes, (tuple, list)) or len(boundary_fluxes) != 4:
        raise ValueError("boundary_fluxes must be (left, right, bottom, top)")
    left, right, bottom, top = (
        _array(value, name, 1) for value, name in zip(
            boundary_fluxes, ("left_boundary_flux", "right_boundary_flux",
                               "bottom_boundary_flux", "top_boundary_flux")))
    if left.shape != (ny,) or right.shape != (ny,) or bottom.shape != (nx,) or top.shape != (nx,):
        raise ValueError("boundary flux arrays must have shapes (ny,), (ny,), (nx,), (nx,)")
    dt = float(time_step)
    if not np.isfinite(dt) or dt <= 0:
        raise ValueError("time_step must be positive and finite")

    base = nonperiodic_rectilinear_advection_diffusion_step_2d(
        dx, dy, dt, x_face_velocities, y_face_velocities,
        x_face_diffusivities, y_face_diffusivities, state)
    area = dx[:, None] * dy[None, :]
    boundary_tendency = np.zeros((nx, ny))
    boundary_tendency[0, :] += left * dy / area[0, :]
    boundary_tendency[-1, :] -= right * dy / area[-1, :]
    boundary_tendency[:, 0] += bottom * dx / area[:, 0]
    boundary_tendency[:, -1] -= top * dx / area[:, -1]
    updated = base["concentrations"] + dt * (sources + boundary_tendency)
    tolerance = 1e-12 * max(1.0, float(np.max(state)))
    if np.min(updated) < -tolerance:
        raise ValueError("explicit forced 2-D step would produce negative concentrations; reduce time_step or forcing")
    initial_mass = float(np.sum(area * state))
    final_mass = float(np.sum(area * updated))
    source_change = float(dt * np.sum(area * sources))
    boundary_change = float(dt * (
        dy @ left - dy @ right + dx @ bottom - dx @ top))
    expected_change = source_change + boundary_change
    residual = final_mass - initial_mass - expected_change
    budget_tolerance = 1e-10 * max(1.0, abs(initial_mass), abs(expected_change))
    if abs(residual) > budget_tolerance:
        raise ArithmeticError("2-D finite-volume forced mass budget failed")
    return {
        "concentrations": updated,
        "initial_mass": initial_mass,
        "final_mass": final_mass,
        "source_mass_change": source_change,
        "boundary_mass_change": boundary_change,
        "expected_mass_change": expected_change,
        "mass_budget_residual": residual,
        "maximum_local_cfl": base["maximum_local_cfl"],
    }

def periodic_nonuniform_point_observation_operator(cell_widths, sensor_positions):
    """Linear interpolation from nonuniform periodic cell centres to point sensors."""
    widths = _array(cell_widths, "cell_widths", 1)
    n = widths.size
    pos = _array(sensor_positions, "sensor_positions", 1)
    if n < 3 or np.any(widths <= 0) or pos.size == 0:
        raise ValueError("need at least three positive cell widths and one sensor")
    length = float(widths.sum())
    centres = np.cumsum(widths) - 0.5*widths
    q = np.mod(pos, length)
    H = np.zeros((pos.size,n))
    for row, point in enumerate(q):
        right = int(np.searchsorted(centres, point, side="right"))
        if right == 0:
            li, ri = n-1, 0
            lx, rx = centres[-1]-length, centres[0]
        elif right == n:
            li, ri = n-1, 0
            lx, rx = centres[-1], centres[0]+length
        else:
            li, ri = right-1, right
            lx, rx = centres[li], centres[ri]
        fraction = (point-lx)/(rx-lx)
        H[row,li] = 1.0-fraction
        H[row,ri] += fraction
    return H


def verify_spatial_forecasts(forecast_means, heldout_observations):
    """Score free forecasts against separate held-out (y,H) observations by lead."""
    forecasts = _array(forecast_means, "forecast_means", 2)
    if forecasts.shape[0] != len(heldout_observations) or forecasts.shape[1] == 0:
        raise ValueError("forecast_means and heldout_observations must have matching non-empty leads")
    scores = []
    for lead, item in enumerate(heldout_observations):
        if item is None:
            scores.append({"lead": lead+1, "count": 0, "bias": np.nan, "mae": np.nan, "rmse": np.nan})
            continue
        if not isinstance(item, (tuple,list)) or len(item) != 2:
            raise ValueError(f"heldout observation {lead} must be None or (y,H)")
        y = _array(item[0], f"heldout_observations[{lead}].y", 1)
        H = _array(item[1], f"heldout_observations[{lead}].H", 2)
        if y.size == 0 or H.shape != (y.size,forecasts.shape[1]):
            raise ValueError(f"heldout observation {lead} dimensions do not match forecast state")
        error = H@forecasts[lead]-y
        scores.append({
            "lead": lead+1, "count": int(error.size),
            "bias": float(np.mean(error)), "mae": float(np.mean(np.abs(error))),
            "rmse": float(np.sqrt(np.mean(error**2))),
        })
    return scores


def nonperiodic_nonuniform_advection_diffusion_step_with_boundaries(
        cell_widths, time_step, interior_face_velocities,
        interior_face_diffusivities, concentrations, *,
        left_boundary_velocity=0.0, right_boundary_velocity=0.0,
        left_boundary_diffusivity=0.0, right_boundary_diffusivity=0.0,
        left_inflow_concentration=None, right_inflow_concentration=None,
        diffusive_boundary_conditions=("no_flux", "no_flux"),
        left_boundary_concentration=None, right_boundary_concentration=None,
        left_exchange_concentration=None, right_exchange_concentration=None,
        left_mass_transfer_coefficient=0.0, right_mass_transfer_coefficient=0.0,
        source_rates=None):
    """Advance a 1-D field with advective inflow/outflow and diffusive closures."""
    widths = _array(cell_widths, "cell_widths", 1)
    state = _array(concentrations, "concentrations", 1)
    n = widths.size
    if n < 2 or state.shape != (n,) or np.any(widths <= 0):
        raise ValueError("cell widths and concentrations must match; widths positive")
    if np.any(state < 0):
        raise ValueError("concentrations must be non-negative")
    dt = float(time_step)
    if not np.isfinite(dt) or dt <= 0:
        raise ValueError("time_step must be positive and finite")
    velocity = _array(interior_face_velocities, "interior_face_velocities", 1)
    diffusivity = _array(interior_face_diffusivities, "interior_face_diffusivities", 1)
    if velocity.shape != (n-1,) or diffusivity.shape != (n-1,) or np.any(diffusivity < 0):
        raise ValueError("interior face fields must have n-1 values and non-negative diffusivity")
    ul, ur, kl, kr, hl, hr = map(float, (left_boundary_velocity, right_boundary_velocity,
                                  left_boundary_diffusivity, right_boundary_diffusivity,
                                  left_mass_transfer_coefficient, right_mass_transfer_coefficient))
    if not np.isfinite([ul, ur, kl, kr, hl, hr]).all() or min(kl, kr, hl, hr) < 0:
        raise ValueError("boundary velocities must be finite; diffusivities and transfer coefficients non-negative")
    if not isinstance(diffusive_boundary_conditions, (tuple, list)) or len(diffusive_boundary_conditions) != 2:
        raise ValueError("diffusive_boundary_conditions must be (left, right)")
    modes = tuple(diffusive_boundary_conditions)
    if any(mode not in ("no_flux", "dirichlet", "robin") for mode in modes):
        raise ValueError("diffusive boundary modes must be no_flux, dirichlet or robin")
    def boundary_value(value, name, required):
        if value is None:
            if required:
                raise ValueError(f"{name} is required for the active boundary closure")
            return None
        result = float(value)
        if not np.isfinite(result) or result < 0:
            raise ValueError(f"{name} must be finite and non-negative")
        return result
    cin_l = boundary_value(left_inflow_concentration, "left_inflow_concentration", ul > 0)
    cin_r = boundary_value(right_inflow_concentration, "right_inflow_concentration", ur < 0)
    cdir_l = boundary_value(left_boundary_concentration, "left_boundary_concentration", modes[0] == "dirichlet")
    cdir_r = boundary_value(right_boundary_concentration, "right_boundary_concentration", modes[1] == "dirichlet")
    cenv_l = boundary_value(left_exchange_concentration, "left_exchange_concentration", modes[0] == "robin")
    cenv_r = boundary_value(right_exchange_concentration, "right_exchange_concentration", modes[1] == "robin")
    if source_rates is None:
        sources = np.zeros(n)
    else:
        sources = _array(source_rates, "source_rates", 1)
        if sources.shape != (n,):
            raise ValueError("source_rates must contain one rate per cell")
    distances = 0.5 * (widths[:-1] + widths[1:])
    L = np.zeros((n, n))
    for i, (u, k, distance) in enumerate(zip(velocity, diffusivity, distances)):
        a = max(u, 0.0) + k / distance
        b = min(u, 0.0) - k / distance
        L[i, i] -= a / widths[i]
        L[i, i+1] -= b / widths[i]
        L[i+1, i] += a / widths[i+1]
        L[i+1, i+1] += b / widths[i+1]
    forcing = sources.copy()
    if ul > 0:
        forcing[0] += ul * cin_l / widths[0]
    else:
        L[0, 0] += ul / widths[0]
    if modes[0] == "dirichlet":
        g = 2.0 * kl / widths[0]
        L[0, 0] -= g / widths[0]
        forcing[0] += g * cdir_l / widths[0]
    elif modes[0] == "robin":
        g = 0.0 if hl == 0 or kl == 0 else 1.0 / (1.0/hl + widths[0]/(2.0*kl))
        L[0, 0] -= g / widths[0]
        forcing[0] += g * cenv_l / widths[0]
    if ur < 0:
        forcing[-1] -= ur * cin_r / widths[-1]
    else:
        L[-1, -1] -= ur / widths[-1]
    if modes[1] == "dirichlet":
        g = 2.0 * kr / widths[-1]
        L[-1, -1] -= g / widths[-1]
        forcing[-1] += g * cdir_r / widths[-1]
    elif modes[1] == "robin":
        g = 0.0 if hr == 0 or kr == 0 else 1.0 / (1.0/hr + widths[-1]/(2.0*kr))
        L[-1, -1] -= g / widths[-1]
        forcing[-1] += g * cenv_r / widths[-1]
    transition = np.eye(n) + dt * L
    if np.min(transition) < -1e-12:
        raise ValueError("time step violates boundary-inclusive positivity/stability bound")
    transition[transition < 0] = 0.0
    updated = transition @ state + dt * forcing
    tolerance = 1e-12 * max(1.0, float(np.max(np.abs(state))))
    if np.min(updated) < -tolerance:
        raise ValueError("boundary-forced step would produce negative concentrations")
    updated[updated < 0] = 0.0
    left_adv = ul * (cin_l if ul > 0 else state[0])
    right_adv = ur * (cin_r if ur < 0 else state[-1])
    g_left = 0.0 if modes[0] != "robin" or hl == 0 or kl == 0 else 1.0/(1.0/hl+widths[0]/(2.0*kl))
    g_right = 0.0 if modes[1] != "robin" or hr == 0 or kr == 0 else 1.0/(1.0/hr+widths[-1]/(2.0*kr))
    left_diff = (2.0 * kl * (cdir_l-state[0]) / widths[0] if modes[0] == "dirichlet"
                 else -g_left * (state[0]-cenv_l) if modes[0] == "robin" else 0.0)
    right_diff = (2.0 * kr * (state[-1]-cdir_r) / widths[-1] if modes[1] == "dirichlet"
                  else g_right * (state[-1]-cenv_r) if modes[1] == "robin" else 0.0)
    left_flux, right_flux = float(left_adv+left_diff), float(right_adv+right_diff)
    initial_mass, final_mass = float(widths@state), float(widths@updated)
    source_change = float(dt*(widths@sources))
    boundary_change = float(dt*(left_flux-right_flux))
    expected_change = source_change+boundary_change
    residual = final_mass-initial_mass-expected_change
    budget_tolerance = 1e-10*max(1.0,abs(initial_mass),abs(expected_change))
    if abs(residual)>budget_tolerance:
        raise ArithmeticError("boundary-closed finite-volume mass budget failed")
    return {"concentrations":updated,"initial_mass":initial_mass,"final_mass":final_mass,
            "left_boundary_flux":left_flux,"right_boundary_flux":right_flux,
            "source_mass_change":source_change,"boundary_mass_change":boundary_change,
            "expected_mass_change":expected_change,"mass_budget_residual":float(residual),
            "transition_matrix":transition}


def nonperiodic_rectilinear_advection_diffusion_step_2d(
        cell_widths_x, cell_widths_y, time_step,
        x_face_velocities, y_face_velocities,
        x_face_diffusivities, y_face_diffusivities, concentrations):
    """Advance a 2-D cell-centred field on a nonuniform rectangular grid.

    Interior x-face arrays have shape (nx-1, ny); y-face arrays have
    shape (nx, ny-1). Face fluxes are positive in +x or +y respectively.
    All four outer boundaries have zero *total* flux. The explicit
    finite-volume step is rejected unless its local outgoing-CFL condition
    guarantees a non-negative update. Work and storage are O(nx*ny).
    """
    dx = _array(cell_widths_x, "cell_widths_x", 1)
    dy = _array(cell_widths_y, "cell_widths_y", 1)
    state = _array(concentrations, "concentrations", 2)
    nx, ny = dx.size, dy.size
    if nx < 2 or ny < 2 or np.any(dx <= 0) or np.any(dy <= 0):
        raise ValueError("each grid axis must contain at least two positive cell widths")
    if state.shape != (nx, ny) or np.any(state < 0):
        raise ValueError("concentrations must be non-negative with shape (nx, ny)")
    dt = float(time_step)
    if not np.isfinite(dt) or dt <= 0:
        raise ValueError("time_step must be positive and finite")
    ux = _array(x_face_velocities, "x_face_velocities", 2)
    uy = _array(y_face_velocities, "y_face_velocities", 2)
    kx = _array(x_face_diffusivities, "x_face_diffusivities", 2)
    ky = _array(y_face_diffusivities, "y_face_diffusivities", 2)
    if ux.shape != (nx-1, ny) or kx.shape != (nx-1, ny):
        raise ValueError("x-face velocity and diffusivity must have shape (nx-1, ny)")
    if uy.shape != (nx, ny-1) or ky.shape != (nx, ny-1):
        raise ValueError("y-face velocity and diffusivity must have shape (nx, ny-1)")
    if np.any(kx < 0) or np.any(ky < 0):
        raise ValueError("face diffusivities must be non-negative")

    area = dx[:, None] * dy[None, :]
    outgoing = np.zeros((nx, ny))
    mass_tendency = np.zeros((nx, ny))

    # x-normal faces: face length is the local y-cell width.
    distance_x = 0.5 * (dx[:-1] + dx[1:])
    ax = np.maximum(ux, 0.0) + kx / distance_x[:, None]
    bx = np.minimum(ux, 0.0) - kx / distance_x[:, None]
    flux_x = dy[None, :] * (ax * state[:-1, :] + bx * state[1:, :])
    mass_tendency[:-1, :] -= flux_x
    mass_tendency[1:, :] += flux_x
    outgoing[:-1, :] += dy[None, :] * ax
    outgoing[1:, :] -= dy[None, :] * bx

    # y-normal faces: face length is the local x-cell width.
    distance_y = 0.5 * (dy[:-1] + dy[1:])
    ay = np.maximum(uy, 0.0) + ky / distance_y[None, :]
    by = np.minimum(uy, 0.0) - ky / distance_y[None, :]
    flux_y = dx[:, None] * (ay * state[:, :-1] + by * state[:, 1:])
    mass_tendency[:, :-1] -= flux_y
    mass_tendency[:, 1:] += flux_y
    outgoing[:, :-1] += dx[:, None] * ay
    outgoing[:, 1:] -= dx[:, None] * by

    local_cfl = dt * outgoing / area
    if np.max(local_cfl) > 1.0 + 1e-12:
        raise ValueError("time step violates 2-D finite-volume positivity/stability bound")
    updated = state + dt * mass_tendency / area
    tolerance = 1e-12 * max(1.0, float(np.max(state)))
    if np.min(updated) < -tolerance:
        raise ArithmeticError("positive-coefficient finite-volume update produced a negative concentration")
    initial_mass = float(np.sum(area * state))
    final_mass = float(np.sum(area * updated))
    residual = final_mass - initial_mass
    budget_tolerance = 1e-10 * max(1.0, abs(initial_mass))
    if abs(residual) > budget_tolerance:
        raise ArithmeticError("2-D finite-volume zero-boundary-flux mass budget failed")
    return {
        "concentrations": updated,
        "initial_mass": initial_mass,
        "final_mass": final_mass,
        "mass_budget_residual": residual,
        "maximum_local_cfl": float(np.max(local_cfl)),
    }


def nonperiodic_rectilinear_point_observation_operator_2d(
        cell_centres_x, cell_centres_y, observation_x, observation_y):
    """Bilinearly interpolate a (nx, ny) cell-centred field to point observations.

    Coordinates are expressed in the same projected or Cartesian coordinate
    system. Each axis must contain at least two strictly increasing cell-centre
    coordinates. Observations must lie inside the rectangular convex hull of
    those centres; no extrapolation or implicit nearest-cell snapping occurs.
    State flattening is NumPy C order: flat_index = i * ny + j.
    """
    x = _array(cell_centres_x, "cell_centres_x", 1)
    y = _array(cell_centres_y, "cell_centres_y", 1)
    ox = _array(observation_x, "observation_x", 1)
    oy = _array(observation_y, "observation_y", 1)
    if x.size < 2 or y.size < 2 or np.any(np.diff(x) <= 0) or np.any(np.diff(y) <= 0):
        raise ValueError("each cell-centre coordinate axis must contain at least two strictly increasing values")
    if ox.size == 0 or oy.size != ox.size:
        raise ValueError("observation_x and observation_y must be non-empty arrays of equal length")
    if (np.any(ox < x[0]) or np.any(ox > x[-1])
            or np.any(oy < y[0]) or np.any(oy > y[-1])):
        raise ValueError("point observations must lie within the convex hull of cell centres")
    ix = np.clip(np.searchsorted(x, ox, side="right") - 1, 0, x.size - 2)
    iy = np.clip(np.searchsorted(y, oy, side="right") - 1, 0, y.size - 2)
    fx = (ox - x[ix]) / (x[ix + 1] - x[ix])
    fy = (oy - y[iy]) / (y[iy + 1] - y[iy])
    H = np.zeros((ox.size, x.size * y.size))
    rows = np.arange(ox.size)
    indices = np.stack((ix*y.size+iy, (ix+1)*y.size+iy,
                        ix*y.size+(iy+1), (ix+1)*y.size+(iy+1)), axis=1)
    weights = np.stack(((1-fx)*(1-fy), fx*(1-fy),
                        (1-fx)*fy, fx*fy), axis=1)
    H[rows[:, None], indices] = weights
    return H
