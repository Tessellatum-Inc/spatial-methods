"""Sobel gradients and a compact Canny-style edge detector."""
import numpy as np

def _image(a):
    x=np.asarray(a,dtype=float)
    if x.ndim!=2 or not np.all(np.isfinite(x)): raise ValueError("image must be a finite 2-D array")
    return x

def _convolve(a,k):
    h,w=a.shape; kh,kw=k.shape; ph,pw=kh//2,kw//2
    p=np.pad(a,((ph,ph),(pw,pw)),mode="reflect")
    out=np.zeros_like(a,dtype=float)
    for i in range(kh):
        for j in range(kw): out += k[i,j]*p[i:i+h,j:j+w]
    return out

def sobel(image):
    """Return (gx, gy, magnitude, orientation radians); x is column direction."""
    a=_image(image)
    kx=np.array([[-1,0,1],[-2,0,2],[-1,0,1]],float)/8
    ky=kx.T
    gx,gy=_convolve(a,kx),_convolve(a,ky)
    return gx,gy,np.hypot(gx,gy),np.arctan2(gy,gx)

def _gaussian(a,sigma):
    if sigma<=0: return a.copy()
    radius=max(1,int(np.ceil(3*sigma)))
    z=np.arange(-radius,radius+1,dtype=float)
    g=np.exp(-(z*z)/(2*sigma*sigma)); g/=g.sum()
    return _convolve(_convolve(a,g[None,:]),g[:,None])

def canny(image, *, low_threshold, high_threshold, sigma=1.0):
    """Canny-style edges with interpolated-direction NMS and 8-connected hysteresis.

    Thresholds apply to the post-NMS gradient magnitude (absolute units).
    """
    a=_image(image)
    if not (np.isfinite(sigma) and sigma>=0): raise ValueError("sigma must be finite and >= 0")
    if not (np.isfinite(low_threshold) and np.isfinite(high_threshold) and 0<=low_threshold<=high_threshold):
        raise ValueError("thresholds must satisfy 0 <= low <= high")
    gx,gy,mag,ang=sobel(_gaussian(a,float(sigma)))
    h,w=a.shape; yy,xx=np.indices((h,w),dtype=float)
    dx,dy=np.cos(ang),np.sin(ang)
    # Bilinear samples one pixel forward/backward along the local gradient.
    def sample(x,y):
        x=np.clip(x,0,w-1); y=np.clip(y,0,h-1)
        x0=np.floor(x).astype(int); y0=np.floor(y).astype(int)
        x1=np.minimum(x0+1,w-1); y1=np.minimum(y0+1,h-1)
        wx=x-x0; wy=y-y0
        return ((1-wx)*(1-wy)*mag[y0,x0]+wx*(1-wy)*mag[y0,x1]+
                (1-wx)*wy*mag[y1,x0]+wx*wy*mag[y1,x1])
    keep=(mag>=sample(xx+dx,yy+dy)) & (mag>=sample(xx-dx,yy-dy))
    thin=np.where(keep,mag,0.0)
    strong=thin>=high_threshold
    weak=thin>=low_threshold
    edges=strong.copy()
    # Flood weak pixels reachable from strong pixels under 8-connectivity.
    while True:
        p=np.pad(edges,1)
        grown=(p[:-2,:-2]|p[:-2,1:-1]|p[:-2,2:]|p[1:-1,:-2]|
               p[1:-1,2:]|p[2:,:-2]|p[2:,1:-1]|p[2:,2:])
        nxt=weak & grown
        if np.array_equal(nxt,edges): break
        edges=nxt
    return edges
