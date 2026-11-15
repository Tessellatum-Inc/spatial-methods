"""FWER and FDR p-value adjustment procedures."""
from __future__ import annotations
from math import expm1, fsum, isfinite, log1p

_METHODS={"bonferroni","sidak","holm","hochberg","bh","by"}

def _validate(pvalues,alpha):
    try: p=[float(v) for v in pvalues]
    except (TypeError,ValueError) as exc: raise ValueError("pvalues must be numeric") from exc
    if not p or any(not isfinite(v) or v<0 or v>1 for v in p):
        raise ValueError("pvalues must be non-empty, finite and in [0,1]")
    if isinstance(alpha,bool): raise ValueError("alpha must be finite and in [0,1]")
    try: alpha=float(alpha)
    except (TypeError,ValueError) as exc: raise ValueError("alpha must be finite and in [0,1]") from exc
    if not isfinite(alpha) or not 0<=alpha<=1: raise ValueError("alpha must be finite and in [0,1]")
    return p,alpha

def adjust_pvalues(pvalues,method="holm",alpha=0.05):
    """Return adjusted p-values and alpha decisions in original input order."""
    p,alpha=_validate(pvalues,alpha)
    method=str(method).lower()
    if method not in _METHODS: raise ValueError(f"method must be one of {sorted(_METHODS)}")
    m=len(p)
    if method=="bonferroni":
        adjusted=[min(1.0,m*v) for v in p]
    elif method=="sidak":
        adjusted=[1.0 if v>=1.0 else -expm1(m*log1p(-v)) for v in p]
    else:
        order=sorted(range(m),key=lambda i:(p[i],i))
        sp=[p[i] for i in order]
        sa=[0.0]*m
        if method=="holm":
            running=0.0
            for rank,value in enumerate(sp):
                running=max(running,min(1.0,(m-rank)*value))
                sa[rank]=running
        else:
            factor=fsum(1.0/i for i in range(1,m+1)) if method=="by" else 1.0
            running=1.0
            for rank in range(m-1,-1,-1):
                if method=="hochberg": candidate=(m-rank)*sp[rank]
                else: candidate=(m*factor/(rank+1))*sp[rank]
                running=min(running,candidate,1.0)
                sa[rank]=running
        adjusted=[0.0]*m
        for rank,original in enumerate(order): adjusted[original]=sa[rank]
    return {"method":method,"alpha":alpha,"adjusted_pvalues":adjusted,
            "reject":[v<=alpha for v in adjusted],"family_size":m}
