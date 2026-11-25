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

    Uses grouped bincount aggregation rather than rescanning all pixels for every
    block/stratum. Within each block, shared strata contribute equally.
    """
    b=np.asarray(block_ids,dtype=np.int64);c=np.asarray(class_codes);s=np.asarray(stratum_ids,dtype=np.int64);r=np.asarray(residual_db,dtype=float)
    if not (b.shape==c.shape==s.shape==r.shape):raise ValueError("Inputs must have matching shapes")
    valid=np.isfinite(r)&(b>=0)&(s>=0)&((c==built_code)|(c==target_code))
    b,c,s,r=b[valid],c[valid],s[valid],r[valid]
    if b.size==0:return []
    nstrata=int(s.max())+1
    nblocks=int(b.max())+1
    # Last key dimension is class: 0=built, 1=target.
    key=((b*nstrata+s)*2)+(c==target_code).astype(np.int64)
    total=nblocks*nstrata*2
    sums=np.bincount(key,weights=np.abs(r),minlength=total).reshape(nblocks,nstrata,2)
    counts=np.bincount(key,minlength=total).reshape(nblocks,nstrata,2)
    shared=(counts[:,:,0]>0)&(counts[:,:,1]>0)
    block_rows=[]
    for block in np.flatnonzero(shared.any(axis=1)):
        strata=np.flatnonzero(shared[block]);built_n=counts[block,strata,0];target_n=counts[block,strata,1]
        built_mae=sums[block,strata,0]/built_n;target_mae=sums[block,strata,1]/target_n
        diffs=target_mae-built_mae
        details=[{"stratum_id":int(st),"built_n":int(bn),"target_n":int(tn),
                  "built_mae_db":float(bm),"target_mae_db":float(tm),"difference_db":float(df)}
                 for st,bn,tn,bm,tm,df in zip(strata,built_n,target_n,built_mae,target_mae,diffs)]
        block_rows.append({"block_id":int(block),"matched_strata":len(details),
            "built_pixels":int(built_n.sum()),"target_pixels":int(target_n.sum()),
            "contrast_db":float(diffs.mean()),"strata":details})
    return block_rows


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
