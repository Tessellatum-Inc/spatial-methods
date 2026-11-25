"""Spatial-block bootstrap helpers for matched spatial class contrasts."""
from __future__ import annotations
import numpy as np

def block_mean_contrast(block_contrasts):
    """Return equal-block mean of finite contrasts; each block is one replicate."""
    x=np.asarray(block_contrasts,dtype=float);x=x[np.isfinite(x)]
    if x.size==0:return None
    return float(x.mean())

def matched_block_contrasts(block_ids, class_codes, stratum_ids, residual_db, *, built_code=6, target_code=1):
    """Compute per-block target-minus-built MAE using only shared strata.

    A stratum is a joint slope/ANF bin. Within each block, each shared stratum
    contributes equally to the block contrast. Pixel counts are retained as support,
    not weights, preventing dense strata from dominating the contrast.
    """
    b=np.asarray(block_ids);c=np.asarray(class_codes);s=np.asarray(stratum_ids);r=np.asarray(residual_db,dtype=float)
    if not (b.shape==c.shape==s.shape==r.shape):raise ValueError("Inputs must have matching shapes")
    valid=np.isfinite(r)&(b>=0)&(c>=0)&(s>=0)
    b,c,s,r=b[valid],c[valid],s[valid],r[valid]
    rows=[]
    for block in np.unique(b):
        in_block=b==block;details=[]
        for stratum in np.unique(s[in_block]):
            m=in_block&(s==stratum);built=r[m&(c==built_code)];target=r[m&(c==target_code)]
            if built.size and target.size:
                details.append({"stratum_id":int(stratum),"built_n":int(built.size),"target_n":int(target.size),
                  "built_mae_db":float(np.abs(built).mean()),"target_mae_db":float(np.abs(target).mean()),
                  "difference_db":float(np.abs(target).mean()-np.abs(built).mean())})
        if details:
            rows.append({"block_id":int(block),"matched_strata":len(details),
              "built_pixels":sum(d["built_n"] for d in details),"target_pixels":sum(d["target_n"] for d in details),
              "contrast_db":float(np.mean([d["difference_db"] for d in details])),"strata":details})
    return rows

def bootstrap_interval(block_contrasts, *, replicates=2000, seed=20261125, min_blocks=20):
    """Percentile bootstrap resampling blocks, never individual pixels."""
    x=np.asarray(block_contrasts,dtype=float);x=x[np.isfinite(x)];n=int(x.size)
    if n<min_blocks:
        return {"estimate_db":block_mean_contrast(x),"lower_95_db":None,"upper_95_db":None,
                "eligible_blocks":n,"interval_status":"insufficient_blocks","minimum_blocks":int(min_blocks),
                "replicates":0,"seed":int(seed)}
    rng=np.random.default_rng(seed);draws=rng.choice(x,size=(replicates,n),replace=True).mean(axis=1)
    lo,hi=np.quantile(draws,[.025,.975])
    return {"estimate_db":float(x.mean()),"lower_95_db":float(lo),"upper_95_db":float(hi),
            "eligible_blocks":n,"interval_status":"percentile_block_bootstrap","minimum_blocks":int(min_blocks),
            "replicates":int(replicates),"seed":int(seed)}
