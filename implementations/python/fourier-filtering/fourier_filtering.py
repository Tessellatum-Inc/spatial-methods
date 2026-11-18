"""2-D Fourier transforms and radial frequency-domain filters."""
from __future__ import annotations
import numpy as np

def fft2_image(image):
    a=np.asarray(image,dtype=float)
    if a.ndim != 2 or not np.all(np.isfinite(a)):
        raise ValueError("image must be a finite 2-D array")
    return np.fft.fftshift(np.fft.fft2(a))

def ifft2_image(spectrum, real=True):
    z=np.asarray(spectrum)
    if z.ndim != 2 or not np.all(np.isfinite(z)):
        raise ValueError("spectrum must be a finite 2-D array")
    out=np.fft.ifft2(np.fft.ifftshift(z))
    return out.real if real else out

def radial_filter(shape, cutoff, kind="gaussian", order=2, highpass=False, band=None):
    """Return a centered transfer function; frequencies are cycles/pixel."""
    if len(shape)!=2 or min(shape)<1: raise ValueError("shape must be positive 2-D")
    if cutoff<=0 or cutoff>np.sqrt(0.5): raise ValueError("cutoff must be in (0, sqrt(0.5)]")
    if order<1: raise ValueError("order must be >= 1")
    fy=np.fft.fftshift(np.fft.fftfreq(shape[0]))
    fx=np.fft.fftshift(np.fft.fftfreq(shape[1]))
    radius=np.hypot(fy[:,None],fx[None,:])
    if kind=="ideal": low=(radius<=cutoff).astype(float)
    elif kind=="gaussian": low=np.exp(-(radius**2)/(2*cutoff**2))
    elif kind=="butterworth": low=1/(1+(radius/cutoff)**(2*order))
    else: raise ValueError("kind must be ideal, gaussian or butterworth")
    if band is not None:
        lo,hi=band
        if not (0<lo<hi<=np.sqrt(0.5)): raise ValueError("band must satisfy 0 < low < high <= sqrt(0.5)")
        if kind=="ideal": result=((radius>=lo)&(radius<=hi)).astype(float)
        else:
            outer=1/(1+(radius/hi)**(2*order)) if kind=="butterworth" else np.exp(-radius**2/(2*hi**2))
            inner=1/(1+(radius/lo)**(2*order)) if kind=="butterworth" else np.exp(-radius**2/(2*lo**2))
            result=np.clip(outer-inner,0,1)
        return result
    return 1-low if highpass else low

def filter_frequency(image, transfer):
    a=np.asarray(image,dtype=float); h=np.asarray(transfer,dtype=float)
    if a.ndim!=2 or h.shape!=a.shape: raise ValueError("image and transfer must be same-shaped 2-D arrays")
    if not np.all(np.isfinite(a)) or not np.all(np.isfinite(h)): raise ValueError("inputs must be finite")
    return ifft2_image(fft2_image(a)*h)


def notch_reject_filter(shape, centers, radius, kind="gaussian"):
    """Build a conjugate-symmetric 2-D notch-reject transfer function.

    `centers` are (fy, fx) frequency coordinates in cycles/pixel, in the
    centered interval [-0.5, 0.5). Each requested center is paired with its
    conjugate-frequency location (-fy, -fx), modulo the sampling lattice.
    The radius is in cycles/pixel. This is a user-guided notch filter: it does
    not discover stripe frequencies automatically.
    """
    if len(shape) != 2 or min(shape) < 1:
        raise ValueError("shape must be positive 2-D")
    if not np.isfinite(radius) or radius <= 0:
        raise ValueError("radius must be finite and positive")
    if kind not in ("gaussian", "ideal"):
        raise ValueError("kind must be gaussian or ideal")
    points = list(centers)
    if not points:
        raise ValueError("at least one notch center is required")
    fy = np.fft.fftshift(np.fft.fftfreq(shape[0]))
    fx = np.fft.fftshift(np.fft.fftfreq(shape[1]))
    yy, xx = fy[:, None], fx[None, :]
    transfer = np.ones(shape, dtype=float)
    for center in points:
        if len(center) != 2:
            raise ValueError("each center must be (fy, fx)")
        cy, cx = float(center[0]), float(center[1])
        if not np.isfinite(cy) or not np.isfinite(cx) or not (-0.5 <= cy < 0.5) or not (-0.5 <= cx < 0.5):
            raise ValueError("notch centers must be finite and in [-0.5, 0.5)")
        for py, px in ((cy, cx), (-cy, -cx)):
            dy = (yy - py + 0.5) % 1.0 - 0.5
            dx = (xx - px + 0.5) % 1.0 - 0.5
            distance = np.hypot(dy, dx)
            if kind == "ideal":
                transfer *= (distance > radius)
            else:
                transfer *= 1.0 - np.exp(-(distance ** 2) / (2.0 * radius ** 2))
    return transfer


def destripe_periodic(image, centers, radius, kind="gaussian"):
    """Attenuate known periodic stripe frequencies using conjugate notches.

    Frequencies must be identified by the caller, for example from a log
    magnitude spectrum. The DFT's periodic boundary model applies; tapering
    can reduce edge leakage but also changes image values near the border.
    """
    a = np.asarray(image, dtype=float)
    if a.ndim != 2 or not np.all(np.isfinite(a)):
        raise ValueError("image must be a finite 2-D array")
    transfer = notch_reject_filter(a.shape, centers, radius, kind=kind)
    return filter_frequency(a, transfer)
