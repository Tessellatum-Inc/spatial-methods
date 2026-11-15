"""LAMBDA reduction and MLAMBDA-style search for integer least squares."""
from __future__ import annotations
import math
import numpy as np

def _validate(float_ambiguities, covariance):
    a=np.asarray(float_ambiguities,dtype=float); q=np.asarray(covariance,dtype=float)
    if a.ndim!=1 or a.size==0 or not np.all(np.isfinite(a)): raise ValueError("float ambiguities must be a non-empty finite vector")
    n=a.size
    if q.shape!=(n,n) or not np.all(np.isfinite(q)): raise ValueError("covariance must be finite, square and match the vector")
    if not np.allclose(q,q.T,rtol=1e-10,atol=1e-12): raise ValueError("covariance must be symmetric")
    q=0.5*(q+q.T)
    try: np.linalg.cholesky(q)
    except np.linalg.LinAlgError as exc: raise ValueError("covariance must be positive definite") from exc
    return a,q

def _ld_factor(q):
    """Compute Q = L.T @ diag(D) @ L with unit lower-triangular L."""
    n=q.shape[0]; work=q.copy(); lower=np.zeros((n,n)); diagonal=np.zeros(n)
    for i in range(n-1,-1,-1):
        diagonal[i]=work[i,i]
        if not np.isfinite(diagonal[i]) or diagonal[i]<=0: raise ValueError("LD factorisation failed")
        lower[i,:i+1]=work[i,:i+1]/math.sqrt(diagonal[i])
        for j in range(i):
            for k in range(j+1): work[j,k]-=lower[i,k]*lower[i,j]
        lower[i,:i+1]/=lower[i,i]
    return lower,diagonal

def _integer_gauss(lower,transform,i,j):
    mu=int(math.floor(lower[i,j]+0.5))
    if mu:
        lower[i:,j]-=mu*lower[i:,i]
        transform[:,j]-=mu*transform[:,i]

def _permute(lower,diagonal,transform,j,delta):
    eta=diagonal[j]/delta; lam=diagonal[j+1]*lower[j+1,j]/delta
    diagonal[j]=eta*diagonal[j+1]; diagonal[j+1]=delta
    for k in range(j):
        a0,a1=lower[j,k],lower[j+1,k]
        lower[j,k]=-lower[j+1,j]*a0+a1
        lower[j+1,k]=eta*a0+lam*a1
    lower[j+1,j]=lam
    if j+2<len(diagonal): lower[j+2:,[j,j+1]]=lower[j+2:,[j+1,j]]
    transform[:,[j,j+1]]=transform[:,[j+1,j]]

def _reduce(lower,diagonal):
    n=len(diagonal); transform=np.eye(n,dtype=np.int64); j=k=n-2
    while j>=0:
        if j<=k:
            for i in range(j+1,n): _integer_gauss(lower,transform,i,j)
        delta=diagonal[j]+lower[j+1,j]**2*diagonal[j+1]
        if delta+1e-6<diagonal[j+1]:
            _permute(lower,diagonal,transform,j,delta); k=j; j=n-2
        else: j-=1
    return transform

def lambda_reduction(float_ambiguities,covariance):
    """Return the integer-unimodular LAMBDA decorrelation transform."""
    a,q=_validate(float_ambiguities,covariance); lower,diagonal=_ld_factor(q)
    transform=_reduce(lower,diagonal)
    return {"transformation":transform,"transformed_ambiguities":transform.T@a,
            "transformed_covariance":transform.T@q@transform,"L":lower,"D":diagonal}

def _search(lower,diagonal,float_values,candidate_count,max_nodes):
    n=len(diagonal); sums=np.zeros((n,n)); partial=np.zeros(n); conditional=np.zeros(n)
    integers=np.zeros(n,dtype=np.int64); steps=np.zeros(n,dtype=np.int64)
    level=n-1; conditional[level]=float_values[level]
    integers[level]=math.floor(conditional[level]+0.5); residual=conditional[level]-integers[level]
    steps[level]=-1 if residual<=0 else 1
    candidates=[]; radius=math.inf
    for visited in range(1,max_nodes+1):
        distance=partial[level]+residual*residual/diagonal[level]
        if distance<radius:
            if level!=0:
                level-=1; partial[level]=distance
                for i in range(level+1):
                    sums[level,i]=sums[level+1,i]+(integers[level+1]-conditional[level+1])*lower[level+1,i]
                conditional[level]=float_values[level]+sums[level,level]
                integers[level]=math.floor(conditional[level]+0.5)
                residual=conditional[level]-integers[level]; steps[level]=-1 if residual<=0 else 1
            else:
                candidates.append((distance,integers.copy())); candidates.sort(key=lambda item:item[0])
                if len(candidates)>candidate_count: candidates.pop()
                if len(candidates)==candidate_count: radius=candidates[-1][0]
                integers[0]+=steps[0]; residual=conditional[0]-integers[0]
                steps[0]=-steps[0]-(-1 if steps[0]<=0 else 1)
        else:
            if level==n-1: break
            level+=1; integers[level]+=steps[level]; residual=conditional[level]-integers[level]
            steps[level]=-steps[level]-(-1 if steps[level]<=0 else 1)
    else: raise RuntimeError("integer search exceeded max_nodes")
    if len(candidates)!=candidate_count: raise RuntimeError("integer search did not find enough candidates")
    return candidates,visited

def lambda_integer_least_squares(float_ambiguities,covariance,*,candidate_count=2,max_nodes=1_000_000):
    """Resolve best integer candidates using LAMBDA reduction and conditional search."""
    a,q=_validate(float_ambiguities,covariance)
    if not isinstance(candidate_count,int) or isinstance(candidate_count,bool) or candidate_count<2: raise ValueError("candidate_count must be an integer of at least two")
    if not isinstance(max_nodes,int) or isinstance(max_nodes,bool) or max_nodes<1: raise ValueError("max_nodes must be a positive integer")
    reduced=lambda_reduction(a,q); transform=reduced["transformation"]
    candidates,visited=_search(reduced["L"],reduced["D"],reduced["transformed_ambiguities"],candidate_count,max_nodes)
    transformed=np.column_stack([item[1] for item in candidates]).astype(float)
    original=np.rint(np.linalg.solve(transform.T.astype(float),transformed).T).astype(np.int64)
    chol=np.linalg.cholesky(q); scored=[]
    for vector in original:
        whitened=np.linalg.solve(chol,a-vector); scored.append((float(whitened@whitened),vector.copy()))
    scored.sort(key=lambda item:item[0]); best_score,best=scored[0]; second_score,second=scored[1]
    return {"best":best,"best_objective":best_score,"second_best":second,
            "second_best_objective":second_score,"ratio":second_score/max(best_score,1e-15),
            "transformation":transform,"transformed_float_ambiguities":reduced["transformed_ambiguities"],
            "visited_nodes":visited}
