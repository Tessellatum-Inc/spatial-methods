"""Transparent Theil–Sen robust linear trend estimator."""
from __future__ import annotations
from math import isfinite
from statistics import median
from typing import Iterable

def theil_sen(times: Iterable[float], values: Iterable[float]) -> dict[str, float | int]:
    """Return median pairwise slope and median residual intercept.

    Only pairs with distinct times contribute slopes. Inputs must be finite
    numeric values; time units determine the slope units. This is a point
    estimator, not an autocorrelation-adjusted significance test.
    """
    x=[float(v) for v in times]
    y=[float(v) for v in values]
    if len(x)!=len(y) or len(x)<2:
        raise ValueError("times and values must have equal length of at least two")
    if any(not isfinite(v) for v in x+y):
        raise ValueError("times and values must be finite")
    slopes=[(y[j]-y[i])/(x[j]-x[i])
            for i in range(len(x)) for j in range(i+1,len(x))
            if x[j]!=x[i]]
    if not slopes:
        raise ValueError("at least one pair must have distinct times")
    slope=float(median(slopes))
    intercept=float(median([yi-slope*xi for xi,yi in zip(x,y)]))
    return {"slope":slope,"intercept":intercept,"pair_count":len(slopes)}

def mann_kendall_test(values, *, seasonal_period=None):
    """Two-sided Mann-Kendall monotonic trend test with tie correction.

    For seasonal_period=m, comparisons are restricted to observations in
    the same position of each consecutive m-observation cycle. The normal
    approximation is used; serial correlation is not corrected.
    """
    from math import erfc, sqrt
    y=[float(v) for v in values]
    if len(y)<3 or any(not isfinite(v) for v in y):
        raise ValueError("values must contain at least three finite observations")
    if seasonal_period is None:
        groups=[y]
    else:
        if isinstance(seasonal_period,bool) or not isinstance(seasonal_period,int) or seasonal_period<1 or seasonal_period>=len(y):
            raise ValueError("seasonal_period must be an integer between 1 and n-1")
        groups=[y[k::seasonal_period] for k in range(seasonal_period)]
    score=0; variance=0.0; pair_count=0
    for group in groups:
        n=len(group)
        if n<2: continue
        for i in range(n-1):
            for j in range(i+1,n):
                score+=(group[j]>group[i])-(group[j]<group[i])
        pair_count+=n*(n-1)//2
        counts={}
        for value in group: counts[value]=counts.get(value,0)+1
        tie_sum=sum(t*(t-1)*(2*t+5) for t in counts.values() if t>1)
        variance+=(n*(n-1)*(2*n+5)-tie_sum)/18.0
    if pair_count==0: raise ValueError("seasonal grouping leaves no comparable pairs")
    if variance<=0:
        z=0.0; p=1.0
    elif score>0:
        z=(score-1)/sqrt(variance); p=erfc(abs(z)/sqrt(2))
    elif score<0:
        z=(score+1)/sqrt(variance); p=erfc(abs(z)/sqrt(2))
    else:
        z=0.0; p=1.0
    return {"score":int(score),"variance":float(variance),"z":float(z),
            "p_value":float(p),"kendall_tau":float(score/pair_count),
            "pair_count":int(pair_count),"seasonal_period":seasonal_period,
            "test":"seasonal Mann-Kendall" if seasonal_period else "Mann-Kendall"}
