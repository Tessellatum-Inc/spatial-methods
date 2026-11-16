"""Scattered point gridding: nearest neighbour and Delaunay linear interpolation."""
from __future__ import annotations
import numpy as np
from scipy.spatial import cKDTree,Delaunay,QhullError

def _samples(points,values):
    p=np.asarray(points,dtype=float);v=np.asarray(values,dtype=float)
    if p.ndim!=2 or p.shape[1]!=2 or len(p)<1:raise ValueError("points must have shape (n,2)")
    if v.ndim!=1 or len(v)!=len(p):raise ValueError("values must have one scalar per point")
    if not np.all(np.isfinite(p)) or not np.all(np.isfinite(v)):raise ValueError("sample coordinates and values must be finite")
    if len(np.unique(p,axis=0))!=len(p):raise ValueError("duplicate sample coordinates are not supported")
    return p,v

def _grid(x_coordinates,y_coordinates):
    x=np.asarray(x_coordinates,dtype=float);y=np.asarray(y_coordinates,dtype=float)
    if x.ndim!=1 or y.ndim!=1 or len(x)<1 or len(y)<1:raise ValueError("grid coordinates must be non-empty 1D arrays")
    if not np.all(np.isfinite(x)) or not np.all(np.isfinite(y)):raise ValueError("grid coordinates must be finite")
    xx,yy=np.meshgrid(x,y)
    return np.column_stack((xx.ravel(),yy.ravel())),xx.shape

def nearest_neighbor_grid(points,values,x_coordinates,y_coordinates,max_distance=None):
    """Assign each grid node the value at its nearest sample point."""
    p,v=_samples(points,values);q,shape=_grid(x_coordinates,y_coordinates)
    if max_distance is not None and (not np.isfinite(max_distance) or max_distance<0):raise ValueError("max_distance must be finite and non-negative")
    distance,index=cKDTree(p).query(q,k=1)
    out=v[index].astype(float)
    if max_distance is not None:out[distance>max_distance]=np.nan
    return out.reshape(shape)

def triangulation_grid(points,values,x_coordinates,y_coordinates,fill_value=np.nan):
    """Piecewise-linear interpolation over a Delaunay triangulation.

    Grid nodes outside the convex hull receive fill_value. Interpolation is
    barycentric within each simplex and exactly reproduces affine planes.
    """
    p,v=_samples(points,values)
    if len(p)<3:raise ValueError("triangulation needs at least three non-collinear samples")
    q,shape=_grid(x_coordinates,y_coordinates)
    try:tri=Delaunay(p)
    except QhullError as exc:raise ValueError("sample points must span a non-degenerate 2D triangulation") from exc
    simplex=tri.find_simplex(q);out=np.full(len(q),float(fill_value),dtype=float)
    inside=simplex>=0
    if np.any(inside):
        s=simplex[inside];delta=q[inside]-tri.transform[s,2]
        first=np.einsum("nij,nj->ni",tri.transform[s,:2],delta)
        weights=np.column_stack((first,1-first.sum(axis=1)))
        out[inside]=np.einsum("ni,ni->n",v[tri.simplices[s]],weights)
    return out.reshape(shape)


def thin_plate_spline_grid(points, values, x_coordinates, y_coordinates, smoothing=0.0):
    """Grid scattered data with a 2D thin-plate-spline radial basis function.

    The kernel r**2 * log(r) with an affine polynomial tail gives the
    minimum-bending-energy thin-plate spline interpolant when smoothing=0.
    Positive smoothing trades exact sample fit for a smoother least-squares
    surface. This is a thin-plate-spline minimum-curvature-style method; it
    should not be confused with the classic Briggs iterative gridding scheme.
    """
    from scipy.interpolate import RBFInterpolator

    p, v = _samples(points, values)
    if len(p) < 3:
        raise ValueError("thin-plate spline needs at least three non-collinear samples")
    design = np.column_stack((np.ones(len(p)), p))
    if np.linalg.matrix_rank(design) < 3:
        raise ValueError("thin-plate spline samples must span a non-degenerate 2D domain")
    smoothing = float(smoothing)
    if not np.isfinite(smoothing) or smoothing < 0:
        raise ValueError("smoothing must be finite and non-negative")
    q, shape = _grid(x_coordinates, y_coordinates)
    try:
        interpolator = RBFInterpolator(
            p, v, kernel="thin_plate_spline", degree=1, smoothing=smoothing
        )
        result = interpolator(q)
    except (ValueError, np.linalg.LinAlgError) as exc:
        raise ValueError("thin-plate spline system could not be solved for these samples") from exc
    return np.asarray(result, dtype=float).reshape(shape)


def ordinary_kriging_grid(
    points, values, x_coordinates, y_coordinates, range_, sill, nugget=0.0
):
    """Ordinary kriging with a fixed exponential covariance model.

    Returns prediction and kriging variance grids. The covariance is
    C(h)=sill*exp(-h/range_) and nugget is added only to the observation
    covariance diagonal. Variogram/covariance parameters are supplied, not
    fitted. This is a small-data reference implementation (dense O(n^3)
    factorisation); it is not a scalable production kriging engine.
    """
    p, v = _samples(points, values)
    if len(p) < 2:
        raise ValueError("ordinary kriging needs at least two sample points")
    range_ = float(range_)
    sill = float(sill)
    nugget = float(nugget)
    if not np.isfinite(range_) or range_ <= 0:
        raise ValueError("range_ must be finite and positive")
    if not np.isfinite(sill) or sill <= 0:
        raise ValueError("sill must be finite and positive")
    if not np.isfinite(nugget) or nugget < 0:
        raise ValueError("nugget must be finite and non-negative")

    from scipy.spatial.distance import cdist

    q, shape = _grid(x_coordinates, y_coordinates)
    distances = cdist(p, p)
    covariance = sill * np.exp(-distances / range_)
    covariance.flat[:: len(p) + 1] += nugget
    system = np.empty((len(p) + 1, len(p) + 1), dtype=float)
    system[:-1, :-1] = covariance
    system[:-1, -1] = 1.0
    system[-1, :-1] = 1.0
    system[-1, -1] = 0.0
    prediction = np.empty(len(q), dtype=float)
    variance = np.empty(len(q), dtype=float)
    for start in range(0, len(q), 256):
        stop = min(start + 256, len(q))
        cross = sill * np.exp(-cdist(p, q[start:stop]) / range_)
        rhs = np.vstack((cross, np.ones((1, stop - start))))
        try:
            solution = np.linalg.solve(system, rhs)
        except np.linalg.LinAlgError as exc:
            raise ValueError("kriging system is singular; inspect sample geometry and covariance parameters") from exc
        weights = solution[:-1]
        lagrange = solution[-1]
        prediction[start:stop] = weights.T @ v
        raw_variance = sill - np.sum(weights * cross, axis=0) - lagrange
        if np.any(raw_variance < -1e-8 * sill):
            raise ValueError("computed kriging variance is materially negative; inspect model conditioning")
        variance[start:stop] = np.maximum(raw_variance, 0.0)
    return {
        "prediction": prediction.reshape(shape),
        "variance": variance.reshape(shape),
    }


def _analysis_grid(points, values, x_coordinates, y_coordinates, radii, background):
    """Validate a rectilinear analysis grid and prepare a first-guess field."""
    p, v = _samples(points, values)
    x = np.asarray(x_coordinates, dtype=float)
    y = np.asarray(y_coordinates, dtype=float)
    if x.ndim != 1 or y.ndim != 1 or len(x) < 2 or len(y) < 2:
        raise ValueError("objective analysis needs at least two coordinates on each axis")
    if not np.all(np.isfinite(x)) or not np.all(np.isfinite(y)):
        raise ValueError("grid coordinates must be finite")
    if np.any(np.diff(x) <= 0) or np.any(np.diff(y) <= 0):
        raise ValueError("grid coordinates must be strictly increasing")
    if np.any(p[:, 0] < x[0]) or np.any(p[:, 0] > x[-1]) or np.any(p[:, 1] < y[0]) or np.any(p[:, 1] > y[-1]):
        raise ValueError("all observations must lie inside the analysis grid")
    r = np.asarray(radii, dtype=float)
    if r.ndim != 1 or len(r) < 1 or not np.all(np.isfinite(r)) or np.any(r <= 0):
        raise ValueError("radii must be a non-empty sequence of finite positive values")
    if len(r) > 1 and np.any(np.diff(r) >= 0):
        raise ValueError("radii must be strictly decreasing from coarse to fine")
    xx, yy = np.meshgrid(x, y)
    if background is None:
        field = np.zeros_like(xx, dtype=float)
    else:
        b = np.asarray(background, dtype=float)
        if b.ndim == 0:
            field = np.full(xx.shape, float(b), dtype=float)
        elif b.shape == xx.shape:
            field = b.copy()
        else:
            raise ValueError("background must be a scalar or have shape (len(y), len(x))")
        if not np.all(np.isfinite(field)):
            raise ValueError("background must be finite")
    return p, v, x, y, xx, yy, r, field


def _objective_analysis(points, values, x_coordinates, y_coordinates, radii,
                        background, kernel, kappa=1.0, gamma=1.0):
    from scipy.interpolate import RegularGridInterpolator

    p, v, x, y, xx, yy, radii, field = _analysis_grid(
        points, values, x_coordinates, y_coordinates, radii, background
    )
    gammas = np.asarray(gamma, dtype=float)
    if gammas.ndim == 0:
        gammas = np.full(len(radii), float(gammas))
    if gammas.shape != radii.shape or not np.all(np.isfinite(gammas)) or np.any(gammas <= 0) or np.any(gammas > 1):
        raise ValueError("gamma must be in (0, 1] or provide one value per radius")
    kappa = float(kappa)
    if kernel == "barnes" and (not np.isfinite(kappa) or kappa <= 0):
        raise ValueError("kappa must be finite and positive")

    # Distances are computed in the same planar coordinate units as x/y.
    d2 = (xx[..., None] - p[None, None, :, 0]) ** 2 + (yy[..., None] - p[None, None, :, 1]) ** 2
    sample_locations = np.column_stack((p[:, 1], p[:, 0]))
    for radius, relaxation in zip(radii, gammas):
        interpolator = RegularGridInterpolator((y, x), field, bounds_error=True)
        residual = v - interpolator(sample_locations)
        if kernel == "cressman":
            radius2 = radius * radius
            weights = np.where(d2 < radius2, (radius2 - d2) / (radius2 + d2), 0.0)
        else:
            weights = np.exp(-d2 / (kappa * radius * radius))
        denominator = weights.sum(axis=2)
        correction = np.divide(
            np.sum(weights * residual[None, None, :], axis=2),
            denominator,
            out=np.zeros_like(field),
            where=denominator > 0,
        )
        field += relaxation * correction
    return field


def cressman_grid(points, values, x_coordinates, y_coordinates, radii,
                  background=None):
    """Iterative Cressman objective analysis on a regular rectilinear grid.

    At each pass, observation residuals are formed against bilinear
    interpolation of the current grid. Grid-node corrections use
    w=(R²-d²)/(R²+d²) for d<R and zero otherwise. Radii are supplied in
    strictly decreasing coarse-to-fine order. Coordinates must be planar
    and share units. The default first guess is zero.
    """
    return _objective_analysis(
        points, values, x_coordinates, y_coordinates, radii, background,
        kernel="cressman",
    )


def barnes_grid(points, values, x_coordinates, y_coordinates, radii,
                background=None, kappa=1.0, gamma=1.0):
    """Iterative Barnes objective analysis using Gaussian correction weights.

    Each pass weights residuals by exp(-d²/(kappa*R²)); gamma in (0,1]
    relaxes each correction. Supply strictly decreasing radii. A scalar
    gamma is reused for every pass or a sequence supplies one value per
    radius. This is a transparent educational Barnes-style successive
    correction scheme; parameter conventions differ among operational
    implementations, so kappa, gamma and radii must be reported.
    """
    return _objective_analysis(
        points, values, x_coordinates, y_coordinates, radii, background,
        kernel="barnes", kappa=kappa, gamma=gamma,
    )
