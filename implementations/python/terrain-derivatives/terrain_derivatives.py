"""Horn 3x3 finite-difference terrain slope and downslope aspect."""
from __future__ import annotations
from typing import Sequence
import numpy as np

def horn_slope_aspect(elevation: Sequence[Sequence[float]] | np.ndarray, *, cell_size_x: float = 1.0, cell_size_y: float = 1.0, z_factor: float = 1.0) -> dict[str, np.ndarray]:
    """Return slope degrees, slope percent and downslope aspect clockwise from north.

    Borders and any 3x3 window containing non-finite elevation return NaN.
    Flat cells have NaN aspect.
    """
    dem = np.asarray(elevation, dtype=float)
    if dem.ndim != 2 or dem.size == 0:
        raise ValueError("elevation must be a non-empty 2D array")
    if not np.isfinite([cell_size_x, cell_size_y, z_factor]).all():
        raise ValueError("cell sizes and z_factor must be finite")
    if cell_size_x <= 0 or cell_size_y <= 0 or z_factor <= 0:
        raise ValueError("cell sizes and z_factor must be positive")
    rows, cols = dem.shape
    slope_deg = np.full(dem.shape, np.nan)
    slope_pct = np.full(dem.shape, np.nan)
    aspect_deg = np.full(dem.shape, np.nan)
    if rows < 3 or cols < 3:
        return {"slope_degrees": slope_deg, "slope_percent": slope_pct, "aspect_degrees": aspect_deg}
    a,b,c = dem[:-2,:-2],dem[:-2,1:-1],dem[:-2,2:]
    d,e,f = dem[1:-1,:-2],dem[1:-1,1:-1],dem[1:-1,2:]
    g,h,i = dem[2:,:-2],dem[2:,1:-1],dem[2:,2:]
    valid = np.isfinite(a)&np.isfinite(b)&np.isfinite(c)&np.isfinite(d)&np.isfinite(e)&np.isfinite(f)&np.isfinite(g)&np.isfinite(h)&np.isfinite(i)
    dz_dx = ((c+2*f+i)-(a+2*d+g))/(8*cell_size_x)*z_factor
    # Array rows increase southward; this derivative is north-positive.
    dz_dy = ((a+2*b+c)-(g+2*h+i))/(8*cell_size_y)*z_factor
    gradient = np.hypot(dz_dx,dz_dy)
    slope = np.degrees(np.arctan(gradient))
    percent = gradient*100.0
    aspect = np.degrees(np.arctan2(-dz_dx,-dz_dy))%360.0
    aspect = np.where(gradient==0,np.nan,aspect)
    target=(slice(1,-1),slice(1,-1))
    slope_deg[target]=np.where(valid,slope,np.nan)
    slope_pct[target]=np.where(valid,percent,np.nan)
    aspect_deg[target]=np.where(valid,aspect,np.nan)
    return {"slope_degrees":slope_deg,"slope_percent":slope_pct,"aspect_degrees":aspect_deg}


def zevenbergen_thorne_slope_aspect(elevation: Sequence[Sequence[float]] | np.ndarray, *, cell_size_x: float = 1.0, cell_size_y: float = 1.0, z_factor: float = 1.0) -> dict[str, np.ndarray]:
    """Return slope degrees, percent rise and downslope aspect using central differences.

    This is the Zevenbergen–Thorne first-derivative stencil: only the four
    cardinal neighbours contribute to the gradient. Borders and any 3x3
    window containing non-finite elevation return NaN; flat aspect is NaN.
    """
    dem = np.asarray(elevation, dtype=float)
    if dem.ndim != 2 or dem.size == 0:
        raise ValueError("elevation must be a non-empty 2D array")
    if not np.isfinite([cell_size_x, cell_size_y, z_factor]).all():
        raise ValueError("cell sizes and z_factor must be finite")
    if cell_size_x <= 0 or cell_size_y <= 0 or z_factor <= 0:
        raise ValueError("cell sizes and z_factor must be positive")
    rows, cols = dem.shape
    slope_deg = np.full(dem.shape, np.nan)
    slope_pct = np.full(dem.shape, np.nan)
    aspect_deg = np.full(dem.shape, np.nan)
    if rows < 3 or cols < 3:
        return {"slope_degrees": slope_deg, "slope_percent": slope_pct, "aspect_degrees": aspect_deg}
    a, b, c = dem[:-2, :-2], dem[:-2, 1:-1], dem[:-2, 2:]
    d, e, f = dem[1:-1, :-2], dem[1:-1, 1:-1], dem[1:-1, 2:]
    g, h, i = dem[2:, :-2], dem[2:, 1:-1], dem[2:, 2:]
    valid = np.isfinite(a)&np.isfinite(b)&np.isfinite(c)&np.isfinite(d)&np.isfinite(e)&np.isfinite(f)&np.isfinite(g)&np.isfinite(h)&np.isfinite(i)
    dz_dx = (f - d) / (2.0 * cell_size_x) * z_factor
    # Rows increase southward, so the north-positive derivative is b-h.
    dz_dy = (b - h) / (2.0 * cell_size_y) * z_factor
    gradient = np.hypot(dz_dx, dz_dy)
    slope = np.degrees(np.arctan(gradient))
    aspect = np.degrees(np.arctan2(-dz_dx, -dz_dy)) % 360.0
    aspect = np.where(gradient == 0, np.nan, aspect)
    target = (slice(1, -1), slice(1, -1))
    slope_deg[target] = np.where(valid, slope, np.nan)
    slope_pct[target] = np.where(valid, gradient * 100.0, np.nan)
    aspect_deg[target] = np.where(valid, aspect, np.nan)
    return {"slope_degrees": slope_deg, "slope_percent": slope_pct, "aspect_degrees": aspect_deg}


def terrain_curvature(elevation: Sequence[Sequence[float]] | np.ndarray, *, cell_size_x: float = 1.0, cell_size_y: float = 1.0, z_factor: float = 1.0) -> dict[str, np.ndarray]:
    """Estimate signed profile and plan curvature from a 3x3 DEM stencil.

    Curvatures use central first and second differences in projected planar
    coordinates. The sign convention is negative for a convex-down profile
    (for example z=x**2 along an uphill profile); flat cells have undefined
    profile and plan curvature. Borders and any 3x3 NoData window are NaN.
    Returned curvature has inverse-horizontal-unit units.
    """
    dem = np.asarray(elevation, dtype=float)
    if dem.ndim != 2 or dem.size == 0:
        raise ValueError("elevation must be a non-empty 2D array")
    if not np.isfinite([cell_size_x, cell_size_y, z_factor]).all():
        raise ValueError("cell sizes and z_factor must be finite")
    if cell_size_x <= 0 or cell_size_y <= 0 or z_factor <= 0:
        raise ValueError("cell sizes and z_factor must be positive")
    shape = dem.shape
    profile = np.full(shape, np.nan)
    plan = np.full(shape, np.nan)
    if shape[0] < 3 or shape[1] < 3:
        return {"profile_curvature": profile, "plan_curvature": plan}
    a,b,c = dem[:-2,:-2],dem[:-2,1:-1],dem[:-2,2:]
    d,e,f = dem[1:-1,:-2],dem[1:-1,1:-1],dem[1:-1,2:]
    g,h,i = dem[2:,:-2],dem[2:,1:-1],dem[2:,2:]
    valid = np.isfinite(a)&np.isfinite(b)&np.isfinite(c)&np.isfinite(d)&np.isfinite(e)&np.isfinite(f)&np.isfinite(g)&np.isfinite(h)&np.isfinite(i)
    dx,dy = float(cell_size_x),float(cell_size_y)
    zx = (f-d)/(2.0*dx)*z_factor
    zy = (b-h)/(2.0*dy)*z_factor
    zxx = (f-2.0*e+d)/(dx*dx)*z_factor
    zyy = (b-2.0*e+h)/(dy*dy)*z_factor
    # Raster rows increase southward; this corner combination is north/east positive.
    zxy = (c-a-i+g)/(4.0*dx*dy)*z_factor
    p2 = zx*zx + zy*zy
    nonflat = valid & (p2 > np.finfo(float).eps)
    numerator_profile = zxx*zx*zx + 2.0*zxy*zx*zy + zyy*zy*zy
    numerator_plan = zxx*zy*zy - 2.0*zxy*zx*zy + zyy*zx*zx
    profile_inner = -numerator_profile / (p2 * np.power(1.0+p2, 1.5))
    plan_inner = -numerator_plan / (p2 * np.sqrt(1.0+p2))
    target = (slice(1,-1),slice(1,-1))
    profile[target] = np.where(nonflat, profile_inner, np.nan)
    plan[target] = np.where(nonflat, plan_inner, np.nan)
    return {"profile_curvature": profile, "plan_curvature": plan}
