"""Regional distribution dynamics: Markov, spatial Markov and LISA transitions."""
from __future__ import annotations
import numpy as np

def _panel(values):
    x=np.asarray(values,dtype=float)
    if x.ndim!=2 or x.shape[0]<2 or x.shape[1]<2 or not np.all(np.isfinite(x)):
        raise ValueError("values must be a finite (time, regions) panel with at least 2 periods and regions")
    return x

def _weights(weights,n):
    w=np.asarray(weights,dtype=float)
    if w.shape!=(n,n) or not np.all(np.isfinite(w)) or np.any(w<0) or np.any(np.diag(w)!=0):
        raise ValueError("weights must be finite, nonnegative, square, and have zero diagonal")
    sums=w.sum(axis=1)
    if np.any(sums==0):
        raise ValueError("every region must have at least one positive-weight neighbor")
    return w/sums[:,None]

def _classes(values,n_classes):
    if not isinstance(n_classes,int) or isinstance(n_classes,bool) or n_classes<2:
        raise ValueError("n_classes must be an integer >= 2")
    edges=np.quantile(values,np.linspace(0,1,n_classes+1))
    inner=np.unique(edges[1:-1])
    return np.searchsorted(inner,values,side="right"),len(inner)+1

def _counts(states,k):
    out=np.zeros((k,k),dtype=int)
    for t in range(states.shape[0]-1):
        np.add.at(out,(states[t],states[t+1]),1)
    return out

def _probabilities(counts):
    totals=counts.sum(axis=1,keepdims=True)
    return np.divide(counts,totals,out=np.zeros(counts.shape,dtype=float),where=totals!=0)

def markov_transitions(values,n_classes=4):
    """Pooled-quantile first-order class transitions."""
    x=_panel(values); s,k=_classes(x.ravel(),n_classes); s=s.reshape(x.shape)
    c=_counts(s,k)
    return {"counts":c,"probabilities":_probabilities(c),"classes":s,"effective_classes":k}

def spatial_markov_transitions(values,weights,n_classes=4):
    """Condition class transitions on the lagged spatial-lag quantile class."""
    x=_panel(values); w=_weights(weights,x.shape[1])
    s,k=_classes(x.ravel(),n_classes); s=s.reshape(x.shape)
    lag=x@w.T
    ls,lk=_classes(lag.ravel(),n_classes); ls=ls.reshape(x.shape)
    c=np.zeros((lk,k,k),dtype=int)
    for t in range(x.shape[0]-1):
        np.add.at(c,(ls[t],s[t],s[t+1]),1)
    p=np.stack([_probabilities(v) for v in c])
    return {"counts":c,"probabilities":p,"classes":s,"spatial_lag_classes":ls,
            "effective_classes":k,"effective_spatial_lag_classes":lk}

def lisa_transition_matrix(values,weights):
    """Descriptive transitions among HH, HL, LH and LL Moran quadrants."""
    x=_panel(values); w=_weights(weights,x.shape[1])
    states=np.empty(x.shape,dtype=int)
    for t,row in enumerate(x):
        sd=row.std()
        if sd==0: raise ValueError("each period must have nonzero cross-sectional variance")
        z=(row-row.mean())/sd; lag=w@z
        states[t]=np.select([(z>0)&(lag>0),(z>0)&(lag<=0),(z<=0)&(lag>0)],[0,1,2],default=3)
    c=_counts(states,4)
    return {"labels":("HH","HL","LH","LL"),"counts":c,"probabilities":_probabilities(c),"states":states}

def sigma_convergence(values):
    """Cross-sectional population standard deviation by period."""
    return _panel(values).std(axis=1)
