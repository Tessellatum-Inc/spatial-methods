"""Spatial-block bootstrap helpers for matched spatial class contrasts."""
from __future__ import annotations
import numpy as np

def block_mean_contrast(block_contrasts):
    """Return equal-block mean of finite contrasts; each block is one replicate."""
    x=np.asarray(block_contrasts,dtype=float)
    x=x[np.isfinite(x)]
    if x.size==0:return None
    return float(x.mean())

def bootstrap_interval(block_contrasts, *, replicates=2000, seed=20261125, min_blocks=20):
    """Percentile bootstrap resampling blocks, never individual pixels."""
    x=np.asarray(block_contrasts,dtype=float)
    x=x[np.isfinite(x)]
    n=int(x.size)
    if n<min_blocks:
        return {"estimate_db":block_mean_contrast(x),"lower_95_db":None,"upper_95_db":None,
                "eligible_blocks":n,"interval_status":"insufficient_blocks",
                "minimum_blocks":int(min_blocks),"replicates":0,"seed":int(seed)}
    rng=np.random.default_rng(seed)
    draws=rng.choice(x,size=(replicates,n),replace=True).mean(axis=1)
    lo,hi=np.quantile(draws,[.025,.975])
    return {"estimate_db":float(x.mean()),"lower_95_db":float(lo),"upper_95_db":float(hi),
            "eligible_blocks":n,"interval_status":"percentile_block_bootstrap",
            "minimum_blocks":int(min_blocks),"replicates":int(replicates),"seed":int(seed)}
