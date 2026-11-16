"""Land-cover transition accounting and interval intensity summaries."""
from __future__ import annotations
import numpy as np

def transition_matrix(before,after,*,classes=None,mask=None):
    """Count transitions from before classes (rows) to after classes (columns)."""
    a,b=np.asarray(before),np.asarray(after)
    if a.shape!=b.shape or a.size==0: raise ValueError("before and after must have same non-empty shape")
    valid=np.ones(a.shape,dtype=bool)
    if mask is not None:
        m=np.asarray(mask)
        if m.shape!=a.shape or m.dtype!=bool: raise ValueError("mask must be boolean and match inputs")
        valid &= m
    for values in (a,b):
        if np.issubdtype(values.dtype,np.number):
            valid &= np.isfinite(values)
        else:
            valid &= np.fromiter((value is not None for value in values.flat),dtype=bool,count=values.size).reshape(values.shape)
    av,bv=a[valid],b[valid]
    labels=sorted(set(av.tolist())|set(bv.tolist()),key=lambda x:(str(type(x)),str(x))) if classes is None else list(classes)
    if not labels or len(set(labels))!=len(labels): raise ValueError("classes must be non-empty and unique")
    unknown=(set(av.tolist())|set(bv.tolist()))-set(labels)
    if unknown: raise ValueError(f"observed values missing from classes: {unknown}")
    lookup={v:i for i,v in enumerate(labels)};matrix=np.zeros((len(labels),len(labels)),dtype=np.int64)
    for x,y in zip(av.tolist(),bv.tolist()): matrix[lookup[x],lookup[y]]+=1
    return labels,matrix

def land_change_accounting(before,after,*,classes=None,mask=None):
    """Return persistence, gains/losses/net/swap and quantity/allocation disagreement."""
    labels,m=transition_matrix(before,after,classes=classes,mask=mask)
    rows=m.sum(axis=1).astype(float);cols=m.sum(axis=0).astype(float);persist=np.diag(m).astype(float)
    losses=rows-persist;gains=cols-persist;total=float(m.sum());changed=float(m.sum()-persist.sum())
    quantity=.5*float(np.abs(rows-cols).sum());disagreement=changed/total if total else 0.;q=quantity/total if total else 0.
    return {"classes":labels,"matrix":m,"from_area":rows,"to_area":cols,"persistence":persist,
      "losses":losses,"gains":gains,"net_change":gains-losses,"swap":2*np.minimum(gains,losses),
      "changed_area":changed,"total_area":total,"quantity_disagreement":q,
      "allocation_disagreement":max(0.,disagreement-q),"total_disagreement":disagreement}

def intensity_analysis(before,after,*,years,classes=None,mask=None):
    """Annualized interval intensity and per-class gain/loss intensities."""
    if not np.isfinite(years) or years<=0: raise ValueError("years must be finite and positive")
    r=land_change_accounting(before,after,classes=classes,mask=mask);total=r["total_area"]
    interval=r["changed_area"]/total/years if total else 0.;other=total-r["from_area"]
    gain=np.divide(r["gains"],other*years,out=np.zeros_like(other),where=other>0)
    loss=np.divide(r["losses"],r["from_area"]*years,out=np.zeros_like(other),where=r["from_area"]>0)
    r.update({"years":float(years),"interval_intensity":interval,"gain_intensity":gain,
      "loss_intensity":loss,"gain_vs_interval":gain-interval,"loss_vs_interval":loss-interval})
    return r
