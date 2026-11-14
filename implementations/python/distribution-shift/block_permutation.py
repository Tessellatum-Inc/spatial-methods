"""Block-level MMD two-sample test with spatial-block label permutations."""
from __future__ import annotations
import numpy as np

def _rbf_kernel(a,b,bandwidth):
    sq=np.sum(a*a,axis=1)[:,None]+np.sum(b*b,axis=1)[None,:]-2*a@b.T
    return np.exp(-np.maximum(sq,0)/(2*bandwidth**2))

def _mmd2_unbiased(K,labels):
    a=np.flatnonzero(labels==0); b=np.flatnonzero(labels==1)
    if len(a)<2 or len(b)<2: raise ValueError("each group needs at least two exchangeable blocks")
    kaa=K[np.ix_(a,a)]; kbb=K[np.ix_(b,b)]; kab=K[np.ix_(a,b)]
    return float((kaa.sum()-np.trace(kaa))/(len(a)*(len(a)-1))+(kbb.sum()-np.trace(kbb))/(len(b)*(len(b)-1))-2*kab.mean())

def spatial_block_mmd_test(features,group_labels,block_ids,*,bandwidth=None,permutations=999,alpha=0.05,seed=0):
    """Block-level MMD with whole-block label permutations.

    Each block must belong to exactly one of two groups. The block kernel is
    the mean RBF similarity over all pairs of observations in two blocks.
    Validity requires block labels to be exchangeable under the null; spatial
    tiles are not automatically independent or exchangeable.
    """
    X=np.asarray(features,dtype=float); y=np.asarray(group_labels); blocks=np.asarray(block_ids)
    if X.ndim!=2 or X.shape[0]<4 or X.shape[1]<1 or not np.all(np.isfinite(X)):
        raise ValueError("features must be a finite n by d matrix with n >= 4")
    n=X.shape[0]
    if y.ndim!=1 or blocks.ndim!=1 or y.size!=n or blocks.size!=n:
        raise ValueError("group_labels and block_ids must have length n")
    if not np.all(np.isin(y,[0,1])) or set(np.unique(y).tolist())!={0,1}:
        raise ValueError("group_labels must contain both binary labels 0 and 1")
    block_rows=[]; block_group=[]
    for block in np.unique(blocks):
        ix=np.flatnonzero(blocks==block); labs=np.unique(y[ix])
        if labs.size!=1: raise ValueError("each spatial block must belong to exactly one group")
        block_rows.append(ix); block_group.append(int(labs[0]))
    z=np.asarray(block_group,dtype=int)
    if np.sum(z==0)<2 or np.sum(z==1)<2: raise ValueError("each group needs at least two spatial blocks")
    if bandwidth is None:
        diff=X[:,None,:]-X[None,:,:]; distances=np.sqrt(np.sum(diff*diff,axis=2))
        positive=distances[np.triu_indices(n,1)]; positive=positive[positive>0]
        if positive.size==0: raise ValueError("automatic bandwidth is undefined for identical feature vectors")
        bw=float(np.median(positive))
    else:
        bw=float(bandwidth)
        if not np.isfinite(bw) or bw<=0: raise ValueError("bandwidth must be finite and positive")
    if isinstance(permutations,bool) or int(permutations)!=permutations or permutations<1:
        raise ValueError("permutations must be a positive integer")
    if not np.isfinite(alpha) or not 0<alpha<1: raise ValueError("alpha must lie strictly between 0 and 1")
    q=len(block_rows); K=np.empty((q,q),dtype=float)
    for i,ri in enumerate(block_rows):
        for j in range(i,q):
            rj=block_rows[j]; value=float(_rbf_kernel(X[ri],X[rj],bw).mean())
            K[i,j]=K[j,i]=value
    observed=_mmd2_unbiased(K,z); rng=np.random.default_rng(seed); null=np.empty(int(permutations))
    for b in range(int(permutations)): null[b]=_mmd2_unbiased(K,rng.permutation(z))
    pvalue=float((1+np.count_nonzero(null>=observed))/(int(permutations)+1))
    return {"mmd2_unbiased":observed,"p_value":pvalue,"reject":pvalue<=alpha,"alpha":float(alpha),
            "bandwidth":bw,"permutation_statistics":null,"n_observations":n,"n_blocks":q,
            "n_blocks_group_0":int(np.sum(z==0)),"n_blocks_group_1":int(np.sum(z==1)),
            "permutations":int(permutations),"seed":seed,"permutation_unit":"whole spatial block",
            "validity_assumption":"block labels exchangeable under the null"}
