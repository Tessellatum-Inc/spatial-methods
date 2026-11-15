"""Empirical G, F and J nearest-neighbour summary functions."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class NearestNeighbourFunctionsResult:
    radii: np.ndarray
    g_values: np.ndarray
    f_values: np.ndarray
    j_values: np.ndarray
    event_nearest_distances: np.ndarray
    empty_space_distances: np.ndarray

def _coordinates(values, name, minimum):
    array=np.asarray(values,dtype=float)
    if array.ndim!=2 or array.shape[1]!=2 or array.shape[0]<minimum:
        raise ValueError(f"{name} must contain at least {minimum} 2D coordinate pairs")
    if not np.isfinite(array).all():
        raise ValueError(f"{name} coordinates must be finite")
    return array

def _nearest_distances(query, reference, *, exclude_matching_index=False):
    """Blockwise brute-force nearest distances with bounded temporary memory."""
    n_reference=len(reference)
    block_rows=max(1,min(len(query),4_000_000//max(1,n_reference)))
    result=np.empty(len(query),dtype=float)
    for start in range(0,len(query),block_rows):
        stop=min(len(query),start+block_rows)
        delta=query[start:stop,None,:]-reference[None,:,:]
        distances=np.hypot(delta[...,0],delta[...,1])
        if exclude_matching_index:
            rows=np.arange(start,stop)
            distances[np.arange(stop-start),rows]=np.inf
        result[start:stop]=np.min(distances,axis=1)
    return result

def nearest_neighbour_functions(events, test_locations, radii):
    """Estimate G, F and J for a planar point pattern.

    G(r) is the empirical CDF of each event's nearest other-event distance.
    F(r) is the empirical CDF of distances from supplied empty-space test
    locations to the nearest event. J(r)=(1-G(r))/(1-F(r)); where 1-F is
    zero, J is NaN. For an interpretable F estimate, test_locations should be
    sampled uniformly and independently in the observation window. No edge
    correction or intensity estimation is performed.

    Distances use Euclidean brute force in O(n^2 + mn) time for n events and
    m test locations, with block-bounded temporary memory. Radii are inclusive.
    """
    points=_coordinates(events,"events",2)
    tests=_coordinates(test_locations,"test_locations",1)
    r=np.asarray(radii,dtype=float)
    if r.ndim!=1 or r.size==0:
        raise ValueError("radii must be a non-empty one-dimensional sequence")
    if not np.isfinite(r).all() or (r<0).any():
        raise ValueError("radii must be finite and non-negative")
    event_distances=_nearest_distances(points,points,exclude_matching_index=True)
    empty_distances=_nearest_distances(tests,points)
    g_sorted=np.sort(event_distances); f_sorted=np.sort(empty_distances)
    g=np.searchsorted(g_sorted,r,side="right")/len(g_sorted)
    f=np.searchsorted(f_sorted,r,side="right")/len(f_sorted)
    denominator=1.0-f
    j=np.full(r.shape,np.nan,dtype=float)
    np.divide(1.0-g,denominator,out=j,where=denominator>0.0)
    return NearestNeighbourFunctionsResult(r.copy(),g,f,j,event_distances,empty_distances)
