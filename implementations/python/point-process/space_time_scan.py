"""Discrete space-time cylindrical Poisson scan with conditional Monte Carlo."""
from __future__ import annotations
from math import isfinite, log
from numbers import Integral
import numpy as np


def _inputs(coordinates,cases,population,max_exposure_fraction,min_cases,
            min_time_bins,max_time_bins):
    xy=np.asarray(coordinates,dtype=float)
    c=np.asarray(cases,dtype=float)
    e=np.asarray(population,dtype=float)
    if xy.ndim!=2 or xy.shape[1]!=2 or xy.shape[0]<2 or not np.isfinite(xy).all():
        raise ValueError("coordinates must be a finite N-by-2 array with N>=2")
    if c.ndim!=2 or c.shape[1]!=len(xy) or c.shape[0]<1 or not np.isfinite(c).all():
        raise ValueError("cases must be a finite T-by-N array")
    if np.any(c<0) or np.any(c!=np.floor(c)):
        raise ValueError("cases must be nonnegative integer counts")
    if e.shape!=c.shape or not np.isfinite(e).all() or np.any(e<0):
        raise ValueError("population exposure must be a matching nonnegative finite T-by-N array")
    if not np.isfinite(c.sum()) or c.sum()<=0:
        raise ValueError("total cases must be positive and finite")
    if not np.isfinite(e.sum()) or e.sum()<=0:
        raise ValueError("total population exposure must be positive and finite")
    fraction=float(max_exposure_fraction)
    if not isfinite(fraction) or not 0<fraction<=1:
        raise ValueError("max_exposure_fraction must be in (0,1]")
    if isinstance(min_cases,bool) or not isinstance(min_cases,Integral) or min_cases<1:
        raise ValueError("min_cases must be a positive integer")
    T=c.shape[0]
    if isinstance(min_time_bins,bool) or not isinstance(min_time_bins,Integral) or not 1<=min_time_bins<=T:
        raise ValueError("min_time_bins must be between 1 and T")
    if max_time_bins is None:max_time_bins=T
    if isinstance(max_time_bins,bool) or not isinstance(max_time_bins,Integral) or not min_time_bins<=max_time_bins<=T:
        raise ValueError("max_time_bins must be between min_time_bins and T")
    return xy,c.astype(int),e,fraction,int(min_cases),int(min_time_bins),int(max_time_bins)


def _zones(xy):
    zones={}
    for centre in range(len(xy)):
        delta=xy-xy[centre]
        distances=np.hypot(delta[:,0],delta[:,1])
        if not np.isfinite(distances).all():raise ValueError("coordinate range caused distance overflow")
        order=np.argsort(distances,kind="stable")
        start=0
        while start<len(order):
            radius=float(distances[order[start]])
            tol=1e-12*max(1.,abs(radius))
            end=start+1
            while end<len(order) and abs(float(distances[order[end]])-radius)<=tol:end+=1
            members=tuple(sorted(int(v) for v in order[:end]))
            zones[members]=(centre,radius)
            start=end
    return [(members,*meta) for members,meta in zones.items()]


def _llr(inside,total,expected):
    outside=total-inside
    expected_out=total-expected
    if inside<=expected:return 0.0
    def term(obs,exp):
        if obs==0:return 0.0
        if exp<=0:return float("inf")
        return obs*log(obs/exp)
    return max(0.0,term(inside,expected)+term(outside,expected_out))


def space_time_poisson_scan(coordinates,cases,population,*,max_exposure_fraction=.5,
                            min_cases=2,min_time_bins=1,max_time_bins=None):
    """Maximize an elevated-rate Poisson LLR over spatial circles × time intervals.

    cases and population are T-by-N arrays over ordered discrete time bins.
    Returned time_end is exclusive. Candidate circles are centroid-centred
    and include all equal-distance ties. Population is exposure per area-bin.
    """
    xy,c,e,fraction,min_cases,min_t,max_t=_inputs(
        coordinates,cases,population,max_exposure_fraction,min_cases,min_time_bins,max_time_bins)
    total_cases=int(c.sum());total_exposure=float(e.sum());T,N=c.shape
    best={"log_likelihood_ratio":0.0,"relative_risk":float("nan"),
          "center_index":None,"radius":None,"member_indices":(),
          "time_start":None,"time_end":None,"cases_inside":0,
          "exposure_inside":0.0,"expected_cases_inside":0.0,
          "total_cases":total_cases,"total_exposure":total_exposure}
    zones=_zones(xy)
    for members,centre,radius in zones:
        zone_cases=c[:,members].sum(axis=1)
        zone_exposure=e[:,members].sum(axis=1)
        cp=np.r_[0,np.cumsum(zone_cases)]
        ep=np.r_[0,np.cumsum(zone_exposure)]
        for start in range(T):
            for length in range(min_t,min(max_t,T-start)+1):
                end=start+length
                inside=int(cp[end]-cp[start])
                exposure=float(ep[end]-ep[start])
                share=exposure/total_exposure
                if exposure<=0 or share>fraction+1e-12 or share>=1.0-1e-12 or inside<min_cases:
                    continue
                expected=total_cases*share
                llr=_llr(inside,total_cases,expected)
                if llr>best["log_likelihood_ratio"]+1e-14:
                    outside_cases=total_cases-inside
                    outside_exposure=total_exposure-exposure
                    risk_in=inside/exposure
                    risk_out=outside_cases/outside_exposure
                    rr=risk_in/risk_out if risk_out>0 else float("inf")
                    best={"log_likelihood_ratio":llr,"relative_risk":rr,
                          "center_index":centre,"radius":radius,
                          "member_indices":members,"time_start":start,"time_end":end,
                          "cases_inside":inside,"exposure_inside":exposure,
                          "expected_cases_inside":expected,"total_cases":total_cases,
                          "total_exposure":total_exposure}
    return best


def monte_carlo_space_time_scan(coordinates,cases,population,*,n_simulations=999,
                                max_exposure_fraction=.5,min_cases=2,
                                min_time_bins=1,max_time_bins=None,rng=None):
    """Conditional multinomial calibration of the maximum cylinder LLR."""
    xy,c,e,fraction,min_cases,min_t,max_t=_inputs(
        coordinates,cases,population,max_exposure_fraction,min_cases,min_time_bins,max_time_bins)
    if isinstance(n_simulations,bool) or not isinstance(n_simulations,Integral) or n_simulations<1:
        raise ValueError("n_simulations must be a positive integer")
    if isinstance(rng,bool):raise ValueError("rng must be an integer, Generator or None")
    observed=space_time_poisson_scan(xy,c,e,max_exposure_fraction=fraction,
        min_cases=min_cases,min_time_bins=min_t,max_time_bins=max_t)
    generator=np.random.default_rng(rng)
    probabilities=(e/e.sum()).ravel()
    maxima=np.empty(int(n_simulations))
    for b in range(int(n_simulations)):
        simulated=generator.multinomial(int(c.sum()),probabilities).reshape(c.shape)
        maxima[b]=space_time_poisson_scan(xy,simulated,e,
            max_exposure_fraction=fraction,min_cases=min_cases,
            min_time_bins=min_t,max_time_bins=max_t)["log_likelihood_ratio"]
    exceed=int(np.count_nonzero(maxima>=observed["log_likelihood_ratio"]-1e-14))
    return {"observed":observed,"p_value":(1+exceed)/(int(n_simulations)+1),
            "n_simulations":int(n_simulations),"simulated_maxima":maxima}
