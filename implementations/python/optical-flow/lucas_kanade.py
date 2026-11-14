"""Dense local Lucas–Kanade optical flow for small inter-frame motion."""
from __future__ import annotations
from math import isfinite

def _image(values):
    image = [list(map(float, row)) for row in values]
    if not image or not image[0] or any(len(row) != len(image[0]) for row in image):
        raise ValueError("images must be non-empty rectangular 2D sequences")
    if any(not isfinite(v) for row in image for v in row):
        raise ValueError("image values must be finite")
    return image

def _derivative(image, axis):
    rows, cols = len(image), len(image[0])
    out = [[0.0] * cols for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            if axis == 0:
                a, b = max(0, i-1), min(rows-1, i+1)
                out[i][j] = (image[b][j] - image[a][j]) / max(1, b-a)
            else:
                a, b = max(0, j-1), min(cols-1, j+1)
                out[i][j] = (image[i][b] - image[i][a]) / max(1, b-a)
    return out

def lucas_kanade_dense(first, second, window_radius=2, min_eigenvalue=1e-6):
    """Estimate per-pixel (u, v) flow using local normal equations.

    u is column displacement and v is row displacement, in pixels per frame.
    Gradients are averaged across the two frames; temporal difference is
    second-first. Windows are clipped at image edges. Ill-conditioned windows
    are marked invalid and receive zero flow. Assumes brightness constancy,
    small motion and locally constant flow; no pyramid or warping is applied.
    """
    a, b = _image(first), _image(second)
    if len(a) != len(b) or len(a[0]) != len(b[0]):
        raise ValueError("images must have identical dimensions")
    if isinstance(window_radius, bool) or not isinstance(window_radius, int) or window_radius < 1:
        raise ValueError("window_radius must be a positive integer")
    if not isfinite(float(min_eigenvalue)) or min_eigenvalue <= 0:
        raise ValueError("min_eigenvalue must be finite and positive")
    rows, cols = len(a), len(a[0])
    ax, ay, bx, by = _derivative(a, 1), _derivative(a, 0), _derivative(b, 1), _derivative(b, 0)
    ix = [[(ax[i][j]+bx[i][j])/2 for j in range(cols)] for i in range(rows)]
    iy = [[(ay[i][j]+by[i][j])/2 for j in range(cols)] for i in range(rows)]
    it = [[b[i][j]-a[i][j] for j in range(cols)] for i in range(rows)]
    u = [[0.0]*cols for _ in range(rows)]
    v = [[0.0]*cols for _ in range(rows)]
    valid = [[False]*cols for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            sxx=sxy=syy=sxt=syt=0.0
            for r in range(max(0,i-window_radius), min(rows,i+window_radius+1)):
                for c in range(max(0,j-window_radius), min(cols,j+window_radius+1)):
                    gx, gy, gt = ix[r][c], iy[r][c], it[r][c]
                    sxx += gx*gx; sxy += gx*gy; syy += gy*gy
                    sxt += gx*gt; syt += gy*gt
            trace = sxx + syy
            disc = max(0.0, (sxx-syy)**2 + 4*sxy*sxy)**0.5
            smallest = (trace-disc)/2
            det = sxx*syy-sxy*sxy
            if smallest < min_eigenvalue or det <= 1e-15:
                continue
            u[i][j] = (-syy*sxt+sxy*syt)/det
            v[i][j] = (sxy*sxt-sxx*syt)/det
            valid[i][j] = True
    return {"u": u, "v": v, "valid": valid}
