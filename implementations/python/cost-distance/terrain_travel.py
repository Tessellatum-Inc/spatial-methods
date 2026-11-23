"""Directional terrain travel-time functions and raster Dijkstra accumulation."""
from __future__ import annotations
from heapq import heappop, heappush
import math
import numpy as np

def tobler_speed_kmh(slope_grade):
    """Tobler (1993) walking speed for signed rise/run slope grade."""
    slope=np.asarray(slope_grade,dtype=float)
    if not np.isfinite(slope).all(): raise ValueError("slope_grade must be finite")
    speed=6.0*np.exp(-3.5*np.abs(slope+0.05))
    return float(speed) if speed.ndim==0 else speed

def tobler_edge_time_seconds(horizontal_distance_m,elevation_change_m):
    """Travel time over one directed edge using Tobler's hiking function."""
    if not np.isfinite(horizontal_distance_m) or horizontal_distance_m<0: raise ValueError("horizontal_distance_m must be finite and non-negative")
    if not np.isfinite(elevation_change_m): raise ValueError("elevation_change_m must be finite")
    if horizontal_distance_m==0: return 0.0
    speed=tobler_speed_kmh(elevation_change_m/horizontal_distance_m)
    return math.inf if speed==0 else horizontal_distance_m*3.6/speed

def naismith_time_seconds(horizontal_distance_m,ascent_m):
    """Naismith rule: 5 km/h horizontal pace plus 600 m ascent per hour."""
    if not np.isfinite(horizontal_distance_m) or horizontal_distance_m<0: raise ValueError("horizontal_distance_m must be finite and non-negative")
    if not np.isfinite(ascent_m) or ascent_m<0: raise ValueError("ascent_m must be finite and non-negative")
    return horizontal_distance_m/5000.0*3600.0+ascent_m/600.0*3600.0

def langmuir_time_seconds(horizontal_distance_m,ascent_m,descent_m,descent_angle_deg):
    """Naismith plus Langmuir descent correction for one segment.

    Subtract 10 min per 300 m descent for 5-12 degree descents; add the same
    amount for descents steeper than 12 degrees; no correction below 5 degrees.
    """
    if not np.isfinite(descent_m) or descent_m<0: raise ValueError("descent_m must be finite and non-negative")
    if not np.isfinite(descent_angle_deg) or not 0<=descent_angle_deg<=90: raise ValueError("descent_angle_deg must be between 0 and 90")
    base=naismith_time_seconds(horizontal_distance_m,ascent_m)
    correction=0.0 if descent_angle_deg<5 else (-2.0*descent_m if descent_angle_deg<=12 else 2.0*descent_m)
    return max(0.0,base+correction)

def _validate_grid(elevation,sources,cell_size_x,cell_size_y,connectivity):
    grid=np.asarray(elevation,dtype=float)
    if grid.ndim!=2 or grid.size==0: raise ValueError("elevation must be a non-empty 2D array")
    if not np.isfinite([cell_size_x,cell_size_y]).all() or cell_size_x<=0 or cell_size_y<=0: raise ValueError("cell sizes must be finite and positive")
    if connectivity not in (4,8): raise ValueError("connectivity must be 4 or 8")
    valid=np.isfinite(grid); rows,cols=grid.shape; source_cells=list(sources)
    if not source_cells: raise ValueError("at least one source cell is required")
    normalized=[]
    for source in source_cells:
        if len(source)!=2 or any(not isinstance(v,(int,np.integer)) for v in source): raise ValueError("each source must be a (row, column) integer pair")
        row,col=map(int,source)
        if not(0<=row<rows and 0<=col<cols): raise ValueError("source is outside the elevation raster")
        if not valid[row,col]: raise ValueError("source must be on a finite elevation cell")
        normalized.append((row,col))
    return grid,valid,sorted(set(normalized))

def least_cost_time(elevation,sources,*,model="tobler",cell_size_x=1.0,cell_size_y=1.0,connectivity=8,prevent_corner_cutting=True):
    """Accumulate directional travel time in seconds from source raster cells.

    Model is tobler, naismith or langmuir. Edge costs depend on directed
    elevation change, so uphill and downhill costs may differ. Non-finite
    elevations are barriers; unreachable finite cells remain infinity.
    """
    if model not in ("tobler","naismith","langmuir"): raise ValueError("model must be tobler, naismith or langmuir")
    grid,valid,source_cells=_validate_grid(elevation,sources,cell_size_x,cell_size_y,connectivity)
    rows,cols=grid.shape
    steps=[(-1,0,cell_size_y),(1,0,cell_size_y),(0,-1,cell_size_x),(0,1,cell_size_x)]
    if connectivity==8:
        diagonal=math.hypot(cell_size_x,cell_size_y)
        steps.extend([(-1,-1,diagonal),(-1,1,diagonal),(1,-1,diagonal),(1,1,diagonal)])
    times=np.full(grid.shape,np.inf,dtype=float); queue=[]
    for row,col in source_cells:
        times[row,col]=0.0; heappush(queue,(0.0,row,col))
    while queue:
        current,row,col=heappop(queue)
        if current!=times[row,col]: continue
        for dr,dc,length in steps:
            nr,nc=row+dr,col+dc
            if not(0<=nr<rows and 0<=nc<cols) or not valid[nr,nc]: continue
            if dr and dc and prevent_corner_cutting and (not valid[row+dr,col] or not valid[row,col+dc]): continue
            change=grid[nr,nc]-grid[row,col]; ascent=max(change,0.0); descent=max(-change,0.0)
            if model=="tobler": edge=tobler_edge_time_seconds(length,change)
            elif model=="naismith": edge=naismith_time_seconds(length,ascent)
            else:
                angle=math.degrees(math.atan2(descent,length))
                edge=langmuir_time_seconds(length,ascent,descent,angle)
            candidate=current+edge
            if candidate<times[nr,nc]:
                times[nr,nc]=candidate;heappush(queue,(candidate,nr,nc))
    times[~valid]=np.nan
    return times
