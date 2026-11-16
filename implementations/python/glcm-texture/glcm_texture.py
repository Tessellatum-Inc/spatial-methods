"""Gray-level co-occurrence matrices and common Haralick-style features."""
from __future__ import annotations
import numpy as np

def quantize(image, *, levels=16, value_range=None, mask=None):
    a=np.asarray(image,dtype=float)
    if a.ndim!=2: raise ValueError("image must be 2-D")
    if not isinstance(levels,(int,np.integer)) or isinstance(levels,(bool,np.bool_)) or levels<2:
        raise ValueError("levels must be an integer >= 2")
    valid=np.isfinite(a)
    if mask is not None:
        m=np.asarray(mask)
        if m.shape!=a.shape or m.dtype!=np.bool_: raise ValueError("mask must be a boolean array matching image")
        valid &= m
    if value_range is None:
        if not valid.any(): raise ValueError("no valid pixels")
        lo,hi=float(a[valid].min()),float(a[valid].max())
    else:
        if len(value_range)!=2: raise ValueError("value_range must be (min, max)")
        lo,hi=map(float,value_range)
        if not np.isfinite(lo+hi) or hi<=lo: raise ValueError("value_range must be finite and increasing")
    q=np.zeros(a.shape,dtype=np.int32)
    if hi>lo:
        scaled=np.floor((np.clip(a[valid],lo,hi)-lo)/(hi-lo)*levels).astype(int)
        q[valid]=np.minimum(scaled,levels-1)
    return q,valid

def glcm(image, *, levels=16, offsets=((0,1),), symmetric=True,
         value_range=None, mask=None, normalize=True):
    """Return matrices with shape (n_offsets, levels, levels), one per offset."""
    q,valid=quantize(image,levels=levels,value_range=value_range,mask=mask)
    if not offsets: raise ValueError("at least one offset is required")
    mats=[]
    h,w=q.shape
    for dr,dc in offsets:
        if not isinstance(dr,(int,np.integer)) or not isinstance(dc,(int,np.integer)) or (dr==0 and dc==0):
            raise ValueError("offsets must be nonzero integer (row, column) pairs")
        r0,r1=max(0,-dr),min(h,h-dr); c0,c1=max(0,-dc),min(w,w-dc)
        mat=np.zeros((levels,levels),dtype=float)
        if r0<r1 and c0<c1:
            src=q[r0:r1,c0:c1]; dst=q[r0+dr:r1+dr,c0+dc:c1+dc]
            ok=valid[r0:r1,c0:c1] & valid[r0+dr:r1+dr,c0+dc:c1+dc]
            np.add.at(mat,(src[ok],dst[ok]),1)
        if symmetric: mat=mat+mat.T
        if normalize and mat.sum()>0: mat/=mat.sum()
        mats.append(mat)
    return np.stack(mats)

def glcm_features(matrix):
    """Compute contrast, dissimilarity, homogeneity, ASM, energy and correlation."""
    p=np.asarray(matrix,dtype=float)
    if p.ndim!=2 or p.shape[0]!=p.shape[1] or np.any(~np.isfinite(p)) or np.any(p<0):
        raise ValueError("matrix must be a finite, nonnegative square matrix")
    total=p.sum()
    if total<=0: raise ValueError("matrix must contain at least one pair")
    p=p/total
    i,j=np.indices(p.shape,dtype=float)
    diff=np.abs(i-j)
    mi=(p.sum(axis=1)*np.arange(len(p))).sum()
    mj=(p.sum(axis=0)*np.arange(len(p))).sum()
    si=np.sqrt((p.sum(axis=1)*(np.arange(len(p))-mi)**2).sum())
    sj=np.sqrt((p.sum(axis=0)*(np.arange(len(p))-mj)**2).sum())
    cov=(p*(i-mi)*(j-mj)).sum()
    corr=cov/(si*sj) if si>0 and sj>0 else 1.0
    return {"contrast":float((p*diff**2).sum()),
            "dissimilarity":float((p*diff).sum()),
            "homogeneity":float((p/(1+diff**2)).sum()),
            "ASM":float((p*p).sum()),
            "energy":float(np.sqrt((p*p).sum())),
            "correlation":float(corr)}
