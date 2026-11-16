"""Dense local Lucas–Kanade optical flow for two regular image frames."""
from __future__ import annotations
import numpy as np
from scipy.ndimage import uniform_filter

def lucas_kanade(first,second,window_size=9,min_determinant=1e-6):
    """Estimate dense local flow (u=column/x, v=row/y) between two frames.

    Spatial gradients are averaged across frames; temporal gradient is
    second-first. Local normal equations are averaged over a square window.
    Pixels with insufficient two-direction texture are marked invalid and
    receive NaN flow. This is a single-scale small-motion teaching baseline.
    """
    a=np.asarray(first,dtype=float);b=np.asarray(second,dtype=float)
    if a.ndim!=2 or a.shape!=b.shape or min(a.shape)<2:raise ValueError("frames must be equally shaped 2D arrays")
    if not np.all(np.isfinite(a)) or not np.all(np.isfinite(b)):raise ValueError("frames must be finite")
    if not isinstance(window_size,int) or isinstance(window_size,bool) or window_size<1 or window_size%2==0:raise ValueError("window_size must be a positive odd integer")
    if not np.isfinite(min_determinant) or min_determinant<0:raise ValueError("min_determinant must be finite and non-negative")
    gy,gx=np.gradient((a+b)/2.0);gt=b-a
    avg=lambda z:uniform_filter(z,size=window_size,mode="reflect")
    xx=avg(gx*gx);xy=avg(gx*gy);yy=avg(gy*gy)
    xt=avg(gx*gt);yt=avg(gy*gt)
    det=xx*yy-xy*xy
    valid=det>min_determinant
    u=np.full(a.shape,np.nan);v=np.full(a.shape,np.nan)
    u[valid]=(-yy[valid]*xt[valid]+xy[valid]*yt[valid])/det[valid]
    v[valid]=(xy[valid]*xt[valid]-xx[valid]*yt[valid])/det[valid]
    return {"u":u,"v":v,"valid":valid,"determinant":det}


def _reference_image(values):
    """Validate and copy a small image into nested Python lists."""
    from math import isfinite

    image = [list(map(float, row)) for row in values]
    if not image or not image[0] or any(len(row) != len(image[0]) for row in image):
        raise ValueError("images must be non-empty rectangular 2D sequences")
    if any(not isfinite(value) for row in image for value in row):
        raise ValueError("image values must be finite")
    return image


def _reference_derivative(image, axis):
    rows, columns = len(image), len(image[0])
    output = [[0.0] * columns for _ in range(rows)]
    for row in range(rows):
        for column in range(columns):
            if axis == 0:
                first, last = max(0, row - 1), min(rows - 1, row + 1)
                output[row][column] = (
                    image[last][column] - image[first][column]
                ) / max(1, last - first)
            else:
                first, last = max(0, column - 1), min(columns - 1, column + 1)
                output[row][column] = (
                    image[row][last] - image[row][first]
                ) / max(1, last - first)
    return output


def lucas_kanade_dense_reference(
    first, second, window_radius=2, min_eigenvalue=1e-6
):
    """Pure-Python local Lucas–Kanade reference for small image fixtures.

    This intentionally transparent O(H*W*r^2) implementation complements
    the vectorised SciPy-backed version. Windows are clipped at image edges;
    poorly conditioned windows are invalid and receive zero flow. It assumes
    brightness constancy, small motion and locally constant flow.
    """
    from math import isfinite

    a, b = _reference_image(first), _reference_image(second)
    if len(a) != len(b) or len(a[0]) != len(b[0]):
        raise ValueError("images must have identical dimensions")
    if isinstance(window_radius, bool) or not isinstance(window_radius, int) or window_radius < 1:
        raise ValueError("window_radius must be a positive integer")
    if not isfinite(float(min_eigenvalue)) or min_eigenvalue <= 0:
        raise ValueError("min_eigenvalue must be finite and positive")

    rows, columns = len(a), len(a[0])
    ax, ay = _reference_derivative(a, 1), _reference_derivative(a, 0)
    bx, by = _reference_derivative(b, 1), _reference_derivative(b, 0)
    ix = [[(ax[i][j] + bx[i][j]) / 2 for j in range(columns)] for i in range(rows)]
    iy = [[(ay[i][j] + by[i][j]) / 2 for j in range(columns)] for i in range(rows)]
    it = [[b[i][j] - a[i][j] for j in range(columns)] for i in range(rows)]
    u = [[0.0] * columns for _ in range(rows)]
    v = [[0.0] * columns for _ in range(rows)]
    valid = [[False] * columns for _ in range(rows)]

    for i in range(rows):
        for j in range(columns):
            sxx = sxy = syy = sxt = syt = 0.0
            for row in range(max(0, i-window_radius), min(rows, i+window_radius+1)):
                for col in range(max(0, j-window_radius), min(columns, j+window_radius+1)):
                    gx, gy, gt = ix[row][col], iy[row][col], it[row][col]
                    sxx += gx*gx
                    sxy += gx*gy
                    syy += gy*gy
                    sxt += gx*gt
                    syt += gy*gt
            trace = sxx + syy
            discriminant = max(0.0, (sxx-syy)**2 + 4*sxy*sxy) ** 0.5
            smallest_eigenvalue = (trace-discriminant) / 2
            determinant = sxx*syy - sxy*sxy
            if smallest_eigenvalue < min_eigenvalue or determinant <= 1e-15:
                continue
            u[i][j] = (-syy*sxt + sxy*syt) / determinant
            v[i][j] = (sxy*sxt - sxx*syt) / determinant
            valid[i][j] = True
    return {"u": u, "v": v, "valid": valid}
