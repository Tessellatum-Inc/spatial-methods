"""Huff gravity model for probabilistic competitive facility choice."""
from __future__ import annotations
import math
import numpy as np


def huff_probabilities(attractiveness, travel_cost, *, alpha=1.0, beta=2.0,
                       minimum_cost=1e-6):
    """Return origin-by-facility Huff choice probabilities.

    Weight_ij = attractiveness_j**alpha / max(cost_ij, minimum_cost)**beta.
    Each origin row is normalized to sum to one. Costs must be comparable
    nonnegative generalized impedance values; minimum_cost regularizes
    zero-cost origin-facility pairs.
    """
    a=np.asarray(attractiveness,dtype=float)
    c=np.asarray(travel_cost,dtype=float)
    if a.ndim!=1 or a.size==0 or not np.isfinite(a).all() or np.any(a<=0):
        raise ValueError("attractiveness must be a non-empty finite positive vector")
    if c.ndim!=2 or c.shape[1]!=a.size or c.shape[0]==0 or not np.isfinite(c).all() or np.any(c<0):
        raise ValueError("travel_cost must be a finite nonnegative origin-by-facility matrix")
    if not np.isfinite(alpha) or alpha<0 or not np.isfinite(beta) or beta<0:
        raise ValueError("alpha and beta must be finite and non-negative")
    if not np.isfinite(minimum_cost) or minimum_cost<=0:
        raise ValueError("minimum_cost must be finite and positive")
    log_weight=alpha*np.log(a)[None,:]-beta*np.log(np.maximum(c,minimum_cost))
    log_weight-=log_weight.max(axis=1,keepdims=True)
    weights=np.exp(log_weight)
    return weights/weights.sum(axis=1,keepdims=True)


def huff_market_shares(probabilities, origin_demand):
    """Aggregate origin demand into expected facility visits."""
    p=np.asarray(probabilities,dtype=float)
    d=np.asarray(origin_demand,dtype=float)
    if p.ndim!=2 or d.shape!=(p.shape[0],) or p.shape[1]==0:
        raise ValueError("probabilities and demand dimensions do not match")
    if not np.isfinite(p).all() or np.any(p<0) or not np.allclose(p.sum(axis=1),1,atol=1e-10):
        raise ValueError("each probability row must be finite, nonnegative and sum to one")
    if not np.isfinite(d).all() or np.any(d<0):
        raise ValueError("origin_demand must be finite and nonnegative")
    return d@p


def huff_expected_visits(attractiveness,travel_cost,origin_demand,*,alpha=1.0,beta=2.0,minimum_cost=1e-6):
    p=huff_probabilities(attractiveness,travel_cost,alpha=alpha,beta=beta,minimum_cost=minimum_cost)
    return huff_market_shares(p,origin_demand)
