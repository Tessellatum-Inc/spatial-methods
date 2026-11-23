"""Third-order tensor SVD (t-SVD) using FFT along mode three."""
from __future__ import annotations
import numpy as np

def t_svd(tensor, tubal_rank=None):
    """Return frequency-domain t-SVD factors (U_hat, S_hat, Vh_hat).

    The FFT is applied along mode 3; each frontal slice is factorized by a
    matrix SVD. Factors remain in the Fourier domain to avoid hiding complex
    conjugate structure. Reconstruct with t_svd_reconstruct().
    """
    x=np.asarray(tensor)
    if x.ndim!=3 or min(x.shape)<1 or not np.all(np.isfinite(x)):
        raise ValueError("tensor must be a finite, nonempty third-order array")
    limit=min(x.shape[0],x.shape[1])
    if tubal_rank is None: k=limit
    else:
        if isinstance(tubal_rank,bool) or int(tubal_rank)!=tubal_rank or not 1<=tubal_rank<=limit:
            raise ValueError("tubal_rank must be an integer in [1, min(n1,n2)]")
        k=int(tubal_rank)
    xf=np.fft.fft(x,axis=2); n3=x.shape[2]
    u=np.empty((x.shape[0],k,n3),dtype=complex)
    s=np.zeros((k,k,n3),dtype=complex)
    vh=np.empty((k,x.shape[1],n3),dtype=complex)
    spectra=[]
    for j in range(n3):
        uj,sj,vhj=np.linalg.svd(xf[:,:,j],full_matrices=False)
        u[:,:,j]=uj[:,:k]; s[:,:,j]=np.diag(sj[:k]); vh[:,:,j]=vhj[:k,:]
        spectra.append(sj)
    return u,s,vh

def t_svd_reconstruct(u_hat,s_hat,vh_hat):
    """Reconstruct a real or complex tensor from frequency-domain t-SVD factors."""
    u=np.asarray(u_hat); s=np.asarray(s_hat); vh=np.asarray(vh_hat)
    if u.ndim!=3 or s.ndim!=3 or vh.ndim!=3 or u.shape[1]!=s.shape[0] or s.shape[0]!=s.shape[1] or s.shape[2]!=u.shape[2] or vh.shape[0]!=s.shape[1] or vh.shape[2]!=u.shape[2]:
        raise ValueError("incompatible frequency-domain factor shapes")
    product=np.empty((u.shape[0],vh.shape[1],u.shape[2]),dtype=complex)
    for j in range(u.shape[2]): product[:,:,j]=u[:,:,j]@s[:,:,j]@vh[:,:,j]
    out=np.fft.ifft(product,axis=2)
    return np.real_if_close(out,tol=1000)

def t_svd_truncate(tensor,tubal_rank):
    """Compute a tubal-rank-k approximation and return it with its factors."""
    factors=t_svd(tensor,tubal_rank=tubal_rank)
    return t_svd_reconstruct(*factors),factors
