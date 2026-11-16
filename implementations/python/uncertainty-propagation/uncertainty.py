"""Monte Carlo uncertainty propagation and Saltelli Sobol sensitivity."""
from __future__ import annotations
import numpy as np

def _bounds(bounds):
    b=np.asarray(bounds,dtype=float)
    if b.ndim!=2 or b.shape[1]!=2 or b.shape[0]==0 or not np.isfinite(b).all() or np.any(b[:,1]<=b[:,0]):
        raise ValueError("bounds must be a finite (n_inputs, 2) array with upper > lower")
    return b

def _evaluate(model,samples):
    y=np.asarray(model(samples),dtype=float)
    if y.ndim==0: y=np.full(len(samples),float(y))
    if y.shape[0]!=len(samples) or not np.isfinite(y).all():
        raise ValueError("model must return finite outputs with sample count as first dimension")
    return y

def monte_carlo_propagation(model,bounds,*,n_samples=10000,quantiles=(.025,.5,.975),seed=None,return_samples=False):
    """Propagate independent uniform inputs through a vectorized model."""
    b=_bounds(bounds)
    if isinstance(n_samples,(bool,np.bool_)) or not isinstance(n_samples,(int,np.integer)) or n_samples<2:
        raise ValueError("n_samples must be an integer >= 2")
    q=np.asarray(quantiles,dtype=float)
    if q.ndim!=1 or not len(q) or not np.isfinite(q).all() or np.any((q<0)|(q>1)) or np.any(np.diff(q)<0):
        raise ValueError("quantiles must be ordered values in [0, 1]")
    rng=np.random.default_rng(seed); u=rng.random((int(n_samples),len(b)))
    x=b[:,0]+u*(b[:,1]-b[:,0]); y=_evaluate(model,x)
    out={"mean":np.mean(y,axis=0),"standard_deviation":np.std(y,axis=0,ddof=1),
         "quantiles":np.quantile(y,q,axis=0),"quantile_levels":q,
         "n_samples":int(n_samples),"input_bounds":b}
    if return_samples: out.update(input_samples=x,output_samples=y)
    return out

def sobol_sensitivity(model,bounds,*,n_samples=16384,seed=None):
    """Estimate first- and total-order Sobol indices by Saltelli pick-freeze."""
    b=_bounds(bounds)
    if isinstance(n_samples,(bool,np.bool_)) or not isinstance(n_samples,(int,np.integer)) or n_samples<2:
        raise ValueError("n_samples must be an integer >= 2")
    rng=np.random.default_rng(seed); n=int(n_samples); d=len(b)
    a=rng.random((n,d)); bb=rng.random((n,d)); scale=b[:,1]-b[:,0]
    a=b[:,0]+a*scale; bb=b[:,0]+bb*scale
    ya=_evaluate(model,a); yb=_evaluate(model,bb)
    if ya.ndim!=1 or yb.ndim!=1: raise ValueError("Sobol sensitivity requires scalar model output")
    variance=float(np.var(np.concatenate([ya,yb]),ddof=1))
    if not np.isfinite(variance) or variance<=np.finfo(float).eps:
        raise ValueError("model output variance must be positive")
    first=np.empty(d); total=np.empty(d)
    for i in range(d):
        ab=a.copy(); ab[:,i]=bb[:,i]; yab=_evaluate(model,ab)
        if yab.ndim!=1: raise ValueError("Sobol sensitivity requires scalar model output")
        first[i]=np.mean(yb*(yab-ya))/variance
        total[i]=.5*np.mean((ya-yab)**2)/variance
    return {"first_order":first,"total_order":total,"n_samples":n,
            "output_variance":variance,"input_bounds":b,"estimator":"Saltelli pick-freeze"}
