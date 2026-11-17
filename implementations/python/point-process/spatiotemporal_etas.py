"""Simplified marked ETAS branching simulator."""
from __future__ import annotations
from numbers import Integral
import numpy as np


def simulate_etas(window, horizon, baseline_intensity, branching_ratio,
                  omori_c, omori_p, magnitude_min, magnitude_beta,
                  productivity_alpha, spatial_scale, spatial_power,
                  spatial_magnitude_exponent=0.0, *, seed=None,
                  max_events=1_000_000):
    """Simulate an ETAS-style marked branching process on a spatial torus.

    Magnitude excesses are exponential. The productivity coefficient is
    calibrated so the expected number of direct offspring under that mark
    distribution equals branching_ratio. Offspring delays follow a normalized
    Omori law and spatial offsets use an isotropic power-law radial kernel.
    """
    if len(window)!=4: raise ValueError("window must be (xmin, ymin, xmax, ymax)")
    xmin,ymin,xmax,ymax=map(float,window)
    if not np.isfinite([xmin,ymin,xmax,ymax]).all() or xmax<=xmin or ymax<=ymin:
        raise ValueError("window must have finite positive width and height")
    values=np.asarray([horizon,baseline_intensity,branching_ratio,omori_c,omori_p,
        magnitude_min,magnitude_beta,productivity_alpha,spatial_scale,spatial_power,
        spatial_magnitude_exponent],dtype=float)
    if not np.isfinite(values).all(): raise ValueError("all model parameters must be finite")
    (horizon,baseline_intensity,branching_ratio,omori_c,omori_p,magnitude_min,
     magnitude_beta,productivity_alpha,spatial_scale,spatial_power,
     spatial_magnitude_exponent)=map(float,values)
    if horizon<=0 or baseline_intensity<0: raise ValueError("horizon must be positive and background intensity nonnegative")
    if not 0<=branching_ratio<1: raise ValueError("branching_ratio must lie in [0,1)")
    if omori_c<=0 or omori_p<=0: raise ValueError("Omori c and p must be positive")
    if magnitude_beta<=0 or not 0<=productivity_alpha<magnitude_beta:
        raise ValueError("magnitude_beta must exceed nonnegative productivity_alpha")
    if spatial_scale<0 or spatial_power<=1 or spatial_magnitude_exponent<0:
        raise ValueError("spatial scale must be nonnegative, spatial power > 1 and magnitude exponent nonnegative")
    if isinstance(max_events,bool) or not isinstance(max_events,Integral) or max_events<1:
        raise ValueError("max_events must be a positive integer")
    if seed is not None and (isinstance(seed,bool) or not isinstance(seed,Integral)):
        raise ValueError("seed must be an integer or None")
    rng=np.random.default_rng(None if seed is None else int(seed))
    width,height=xmax-xmin,ymax-ymin
    n0=int(rng.poisson(baseline_intensity*width*height*horizon))
    if n0>max_events: raise OverflowError("immigrant count exceeds max_events")
    kappa=branching_ratio*(magnitude_beta-productivity_alpha)/magnitude_beta
    # time, x, y, magnitude, parent, generation, immigrant
    events=[]
    for _ in range(n0):
        mag=magnitude_min+float(rng.exponential(1.0/magnitude_beta))
        events.append((float(rng.uniform(0,horizon)),float(rng.uniform(xmin,xmax)),
                       float(rng.uniform(ymin,ymax)),mag,-1,0,True))
    cursor=0
    while cursor<len(events):
        pt,px,py,pm,_,generation,_=events[cursor]
        exponent=productivity_alpha*(pm-magnitude_min)
        if exponent>700: raise OverflowError("magnitude productivity overflow")
        mean_children=kappa*float(np.exp(exponent))
        for _ in range(int(rng.poisson(mean_children))):
            u=float(rng.random())
            delay=omori_c*((1.0-u)**(-1.0/omori_p)-1.0)
            ct=pt+delay
            if not np.isfinite(ct) or ct>=horizon: continue
            angle=float(rng.uniform(0,2*np.pi))
            u=max(float(rng.random()),np.finfo(float).tiny)
            scale_exponent=spatial_magnitude_exponent*(pm-magnitude_min)
            if scale_exponent>700: raise OverflowError("magnitude-dependent spatial scale overflow")
            radius=spatial_scale*float(np.exp(scale_exponent))*float(np.sqrt(u**(-1.0/(spatial_power-1.0))-1.0))
            dx,dy=radius*np.cos(angle),radius*np.sin(angle)
            cx=xmin+((px-xmin+float(dx))%width)
            cy=ymin+((py-ymin+float(dy))%height)
            mag=magnitude_min+float(rng.exponential(1.0/magnitude_beta))
            if len(events)>=max_events: raise OverflowError("simulated event count exceeds max_events")
            events.append((ct,cx,cy,mag,cursor,generation+1,False))
        cursor+=1
    order=sorted(range(len(events)),key=lambda i:(events[i][0],i))
    remap={old:new for new,old in enumerate(order)}
    ordered=[events[i] for i in order]
    return {
        "time":np.asarray([e[0] for e in ordered]),
        "x":np.asarray([e[1] for e in ordered]),
        "y":np.asarray([e[2] for e in ordered]),
        "magnitude":np.asarray([e[3] for e in ordered]),
        "parent_index":np.asarray([-1 if e[4]<0 else remap[e[4]] for e in ordered],dtype=int),
        "generation":np.asarray([e[5] for e in ordered],dtype=int),
        "is_immigrant":np.asarray([e[6] for e in ordered],dtype=bool),
        "parameters":{"branching_ratio":branching_ratio,"productivity_coefficient":kappa,
            "omori_c":omori_c,"omori_p":omori_p,"magnitude_beta":magnitude_beta,
            "productivity_alpha":productivity_alpha,"spatial_scale":spatial_scale,
            "spatial_power":spatial_power,"spatial_magnitude_exponent":spatial_magnitude_exponent,
            "spatial_boundary":"toroidal","temporal_initialization":"no pre-window history"},
    }
