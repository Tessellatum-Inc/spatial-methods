"""Univariate exponential Hawkes process simulation and likelihood."""
from __future__ import annotations
import numpy as np


def _parameters(baseline, excitation, decay):
    mu,alpha,beta=map(float,(baseline,excitation,decay))
    if not np.isfinite([mu,alpha,beta]).all() or mu<=0 or alpha<0 or beta<=0 or alpha>=beta:
        raise ValueError("require finite baseline > 0, excitation >= 0 and decay > excitation")
    return mu,alpha,beta


def simulate_exponential_hawkes(baseline,excitation,decay,horizon,*,seed=None,max_events=1000000):
    """Simulate a stationary subcritical Hawkes process by Ogata thinning."""
    mu,alpha,beta=_parameters(baseline,excitation,decay)
    end=float(horizon)
    if not np.isfinite(end) or end<=0: raise ValueError("horizon must be finite and positive")
    if isinstance(max_events,(bool,np.bool_)) or not isinstance(max_events,(int,np.integer)) or max_events<1:
        raise ValueError("max_events must be a positive integer")
    rng=np.random.default_rng(seed); events=[]; current=0.0
    while current<end:
        if events:
            ages=current-np.asarray(events)
            upper=mu+alpha*float(np.sum(np.exp(-beta*ages)))
        else:
            upper=mu
        candidate=current-rng.exponential()/upper
        if candidate>=end: break
        if events:
            intensity=mu+alpha*float(np.sum(np.exp(-beta*(candidate-np.asarray(events)))))
        else:
            intensity=mu
        if rng.random()*upper<=intensity:
            events.append(float(candidate))
            if len(events)>max_events: raise RuntimeError("max_events exceeded; check horizon and process parameters")
        current=candidate
    return np.asarray(events,dtype=float)


def exponential_hawkes_log_likelihood(event_times,baseline,excitation,decay,horizon):
    """Conditional log-likelihood for ordered events on [0, horizon]."""
    mu,alpha,beta=_parameters(baseline,excitation,decay)
    t=np.asarray(event_times,dtype=float); end=float(horizon)
    if t.ndim!=1 or not np.isfinite(t).all() or np.any(np.diff(t)<0):
        raise ValueError("event_times must be a finite nondecreasing vector")
    if not np.isfinite(end) or end<=0 or np.any((t<0)|(t>end)):
        raise ValueError("horizon must be positive and contain all event times")
    history=0.0; log_sum=0.0; previous=0.0
    for ti in t:
        history*=np.exp(-beta*(ti-previous))
        intensity=mu+alpha*history
        log_sum+=np.log(intensity)
        history+=1.0
        previous=ti
    compensator=mu*end+(alpha/beta)*float(np.sum(1.0-np.exp(-beta*(end-t))))
    return float(log_sum-compensator)
