"""Gabor kernels and convolution responses for 2-D images."""
import numpy as np

def gabor_kernel(*,frequency,theta=0.0,sigma=2.0,aspect_ratio=0.5,phase=0.0,n_stdevs=3.0):
    if not (np.isfinite(frequency) and 0<frequency<=0.5): raise ValueError("frequency must be in (0, 0.5] cycles/pixel")
    if not (np.isfinite(sigma) and sigma>0 and np.isfinite(aspect_ratio) and aspect_ratio>0):
        raise ValueError("sigma and aspect_ratio must be positive")
    if not (np.isfinite(n_stdevs) and n_stdevs>0): raise ValueError("n_stdevs must be positive")
    radius=int(np.ceil(n_stdevs*sigma))
    y,x=np.mgrid[-radius:radius+1,-radius:radius+1]
    xr=x*np.cos(theta)+y*np.sin(theta); yr=-x*np.sin(theta)+y*np.cos(theta)
    env=np.exp(-(xr*xr+(aspect_ratio*yr)**2)/(2*sigma*sigma))
    k=env*np.cos(2*np.pi*frequency*xr+phase)
    k-=k.mean()
    norm=np.sqrt((k*k).sum())
    if norm>0: k/=norm
    return k

def gabor_response(image,kernel):
    a=np.asarray(image,dtype=float); k=np.asarray(kernel,dtype=float)
    if a.ndim!=2 or k.ndim!=2 or not np.all(np.isfinite(a)) or not np.all(np.isfinite(k)):
        raise ValueError("image and kernel must be finite 2-D arrays")
    h,w=a.shape; kh,kw=k.shape; ph,pw=kh//2,kw//2
    p=np.pad(a,((ph,ph),(pw,pw)),mode="reflect")
    out=np.zeros_like(a)
    # Correlation with the kernel; use reversed kernel for mathematical convolution.
    for i in range(kh):
        for j in range(kw): out+=k[i,j]*p[i:i+h,j:j+w]
    return out

def gabor_bank(image, *, frequencies, orientations, sigma=2.0, aspect_ratio=0.5):
    """Return response magnitudes indexed by (frequency, orientation, row, col)."""
    responses=[]
    for f in frequencies:
        row=[]
        for theta in orientations:
            k=gabor_kernel(frequency=f,theta=theta,sigma=sigma,aspect_ratio=aspect_ratio)
            row.append(np.abs(gabor_response(image,k)))
        responses.append(row)
    if not responses: raise ValueError("frequencies must not be empty")
    if not orientations: raise ValueError("orientations must not be empty")
    return np.asarray(responses)
