"""Binary mathematical morphology with explicit structuring elements."""
import numpy as np

def _binary(a):
    x=np.asarray(a)
    if x.ndim!=2: raise ValueError("image must be 2-D")
    return x.astype(bool)

def _structure(s):
    if s is None: return np.ones((3,3),dtype=bool)
    z=np.asarray(s)
    if z.ndim!=2 or not z.size or z.dtype!=np.bool_ or not z.any():
        raise ValueError("structure must be a nonempty 2-D boolean array")
    return z

def _shift(a,dr,dc,fill):
    h,w=a.shape; out=np.full_like(a,fill)
    r0,r1=max(0,-dr),min(h,h-dr); c0,c1=max(0,-dc),min(w,w-dc)
    if r0<r1 and c0<c1: out[r0:r1,c0:c1]=a[r0+dr:r1+dr,c0+dc:c1+dc]
    return out

def dilation(image, structure=None):
    a=_binary(image); s=_structure(structure); cr,cc=s.shape[0]//2,s.shape[1]//2
    out=np.zeros_like(a)
    for r,c in zip(*np.where(s)): out |= _shift(a,r-cr,c-cc,False)
    return out

def erosion(image, structure=None):
    a=_binary(image); s=_structure(structure); cr,cc=s.shape[0]//2,s.shape[1]//2
    out=np.ones_like(a)
    for r,c in zip(*np.where(s)): out &= _shift(a,r-cr,c-cc,False)
    return out

def opening(image, structure=None):
    return dilation(erosion(image,structure),structure)

def closing(image, structure=None):
    return erosion(dilation(image,structure),structure)

def morphological_gradient(image, structure=None):
    return dilation(image,structure) ^ erosion(image,structure)
