"""Tensor-product B-spline P-surface for scalar spatial responses."""
from __future__ import annotations
import numpy as np

def _coordinates(value,name):
    a=np.asarray(value,dtype=float)
    if a.ndim!=2 or a.shape[1]!=2 or not a.shape[0] or not np.isfinite(a).all():
        raise ValueError(f"{name} must be a nonempty finite N-by-2 array")
    return a

def _knots(n,p):
    interior=np.linspace(0.,1.,n-p+1)[1:-1]
    return np.r_[np.zeros(p+1),interior,np.ones(p+1)]

def _basis(values,knots,p):
    x=np.asarray(values,dtype=float); b=np.zeros((len(x),len(knots)-1))
    for row,v in enumerate(x):
        if v<1:
            for i in range(len(knots)-1):
                if knots[i]<=v<knots[i+1]: b[row,i]=1.; break
    for order in range(1,p+1):
        q=np.zeros((len(x),len(knots)-order-1))
        for i in range(q.shape[1]):
            a=knots[i+order]-knots[i]; z=knots[i+order+1]-knots[i+1]
            if a>0:q[:,i]+=(x-knots[i])/a*b[:,i]
            if z>0:q[:,i]+=(knots[i+order+1]-x)/z*b[:,i+1]
        b=q
    at=x==1.; b[at,:]=0.; b[at,-1]=1.
    return b

def _penalty(n,p,knots):
    g=np.array([np.mean(knots[i+1:i+p+1]) for i in range(n)])
    d=np.zeros((max(0,n-2),n))
    for i in range(n-2):
        a=g[i+1]-g[i]; z=g[i+2]-g[i+1]
        d[i,i:i+3]=(1/a,-(1/a+1/z),1/z)
    return d

class TensorProductPSpline2D:
    """Dense small-data tensor-product P-spline with x/y roughness penalties."""
    def __init__(self,n_basis=(8,8),degree=3,smoothing=1.):
        if isinstance(degree,(bool,np.bool_)) or not isinstance(degree,(int,np.integer)) or degree<1:
            raise ValueError("degree must be an integer >= 1")
        if isinstance(n_basis,(int,np.integer)) and not isinstance(n_basis,(bool,np.bool_)):
            n_basis=(int(n_basis),int(n_basis))
        if not isinstance(n_basis,(tuple,list)) or len(n_basis)!=2 or any(
            isinstance(v,(bool,np.bool_)) or not isinstance(v,(int,np.integer)) or v<degree+1 for v in n_basis):
            raise ValueError("n_basis must contain two integers >= degree + 1")
        if np.isscalar(smoothing):smoothing=(float(smoothing),float(smoothing))
        if not isinstance(smoothing,(tuple,list,np.ndarray)) or len(smoothing)!=2 or any(
            not np.isfinite(v) or v<0 for v in smoothing):
            raise ValueError("smoothing must be a nonnegative scalar or pair")
        self.n_basis=tuple(map(int,n_basis));self.degree=int(degree)
        self.smoothing=tuple(map(float,smoothing));self._coef=None

    def _design(self,xy):
        u=(xy-self._min)/self._span
        bx=_basis(u[:,0],self._kx,self.degree);by=_basis(u[:,1],self._ky,self.degree)
        return np.einsum("ni,nj->nij",bx,by).reshape(len(u),-1)

    def fit(self,coordinates,values):
        xy=_coordinates(coordinates,"coordinates");z=np.asarray(values,dtype=float)
        if z.ndim!=1 or len(z)!=len(xy) or not np.isfinite(z).all():
            raise ValueError("values must be a finite vector matching coordinates")
        if len(xy)<4 or len(np.unique(xy,axis=0))!=len(xy):
            raise ValueError("at least four unique coordinate locations are required")
        self._min=xy.min(axis=0);self._span=xy.max(axis=0)-self._min
        if np.any(self._span<=0):raise ValueError("coordinates must span both axes")
        nx,ny=self.n_basis;self._kx=_knots(nx,self.degree);self._ky=_knots(ny,self.degree)
        design=self._design(xy);dx=_penalty(nx,self.degree,self._kx);dy=_penalty(ny,self.degree,self._ky)
        penalties=[]
        if self.smoothing[0]>0 and len(dx):penalties.append(np.sqrt(self.smoothing[0])*np.kron(dx,np.eye(ny)))
        if self.smoothing[1]>0 and len(dy):penalties.append(np.sqrt(self.smoothing[1])*np.kron(np.eye(nx),dy))
        a=np.vstack([design,*penalties]) if penalties else design
        b=np.r_[z,np.zeros(sum(q.shape[0] for q in penalties))] if penalties else z
        coef,_,rank,_=np.linalg.lstsq(a,b,rcond=None)
        if rank<nx*ny:raise ValueError("spline design is rank deficient; add observations or reduce basis size")
        if not np.isfinite(coef).all():raise ValueError("non-finite spline coefficients")
        self._coef=coef;self.n_observations_=len(z);self.coefficient_shape_=self.n_basis;self.design_rank_=int(rank)
        return self

    def predict(self,coordinates):
        if self._coef is None:raise RuntimeError("fit must be called before predict")
        xy=_coordinates(coordinates,"coordinates");u=(xy-self._min)/self._span
        if np.any(u<0) or np.any(u>1):raise ValueError("prediction coordinates must lie inside training bounds")
        return self._design(xy)@self._coef

    def fit_predict(self,coordinates,values):
        return self.fit(coordinates,values).predict(coordinates)
