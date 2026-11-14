"""CP/PARAFAC decomposition by alternating least squares for 3-way tensors."""
from __future__ import annotations
import numpy as np

def _unfold(x,mode):
    return np.moveaxis(x,mode,0).reshape(x.shape[mode],-1)

def _khatri_rao(a,b):
    # Column-wise Kronecker product, ordered consistently with mode unfolding.
    return np.einsum("ir,jr->ijr",a,b).reshape(a.shape[0]*b.shape[0],a.shape[1])

def cp_als(tensor,rank,max_iter=200,tolerance=1e-7,seed=0):
    """Fit a rank-R CP model to a finite, fully observed 3D tensor.

    Returns factor matrices A, B, C and relative Frobenius reconstruction
    error history. This basic dense ALS implementation is intended for
    small teaching examples; it does not handle missing values or constraints.
    """
    x=np.asarray(tensor,dtype=float)
    if x.ndim!=3 or any(d<1 for d in x.shape) or not np.all(np.isfinite(x)):
        raise ValueError("tensor must be a finite, nonempty 3D array")
    if not isinstance(rank,int) or isinstance(rank,bool) or rank<1:
        raise ValueError("rank must be a positive integer")
    if not isinstance(max_iter,int) or isinstance(max_iter,bool) or max_iter<1:
        raise ValueError("max_iter must be a positive integer")
    if not np.isfinite(tolerance) or tolerance<0:
        raise ValueError("tolerance must be finite and nonnegative")
    rng=np.random.default_rng(seed)
    factors=[rng.normal(size=(d,rank)) for d in x.shape]
    norm_x=np.linalg.norm(x)
    if norm_x==0:
        factors=[np.eye(d,rank) for d in x.shape]
        return {"factors":factors,"weights":np.zeros(rank),"error_history":[0.0],"iterations":0}
    errors=[]
    for iteration in range(max_iter):
        for mode in range(3):
            others=[i for i in range(3) if i!=mode]
            a,b=factors[others[0]],factors[others[1]]
            kr=_khatri_rao(a,b)
            gram=(a.T@a)*(b.T@b)
            rhs=_unfold(x,mode)@kr
            factors[mode]=rhs@np.linalg.pinv(gram,hermitian=True)
        norms=[np.linalg.norm(f,axis=0) for f in factors]
        for f,n in zip(factors,norms):
            f/=np.where(n>0,n,1.0)[None,:]
        weights=norms[0]*norms[1]*norms[2]
        # Compute reconstruction error without materializing each rank-one term.
        approx=np.einsum("r,ir,jr,kr->ijk",weights,*factors,optimize=True)
        error=float(np.linalg.norm(x-approx)/norm_x)
        errors.append(error)
        if len(errors)>1 and abs(errors[-2]-errors[-1])<=tolerance*max(1.0,errors[-2]):
            break
    return {"factors":factors,"weights":weights,"error_history":errors,"iterations":iteration+1}
