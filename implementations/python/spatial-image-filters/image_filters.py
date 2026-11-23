"""Small, explicit 2-D image and raster filters using NumPy only."""
import numpy as np

def _image(image):
    a = np.asarray(image, dtype=float)
    if a.ndim != 2 or min(a.shape, default=0) < 1 or not np.all(np.isfinite(a)):
        raise ValueError("image must be a non-empty finite 2-D array")
    return a

def _positive(value, name):
    value = float(value)
    if not np.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be finite and > 0")
    return value

def _radius(value):
    if isinstance(value, bool) or int(value) != value or value < 0:
        raise ValueError("radius must be a non-negative integer")
    return int(value)

def _correlate(image, kernel):
    a = _image(image)
    k = np.asarray(kernel, dtype=float)
    if k.ndim != 2 or any(n % 2 == 0 for n in k.shape):
        raise ValueError("kernel must be 2-D with odd dimensions")
    py, px = k.shape[0] // 2, k.shape[1] // 2
    p = np.pad(a, ((py, py), (px, px)), mode="reflect")
    out = np.zeros_like(a)
    for i in range(k.shape[0]):
        for j in range(k.shape[1]):
            out += k[i, j] * p[i:i+a.shape[0], j:j+a.shape[1]]
    return out

def gaussian_filter(image, sigma, *, truncate=3.0):
    """Separable Gaussian smoothing with reflected boundaries and unit-sum kernel."""
    a = _image(image)
    sigma = _positive(sigma, "sigma")
    truncate = _positive(truncate, "truncate")
    radius = max(1, int(np.ceil(truncate * sigma)))
    x = np.arange(-radius, radius + 1, dtype=float)
    g = np.exp(-0.5 * (x / sigma) ** 2)
    g /= g.sum()
    return _correlate(_correlate(a, g[None, :]), g[:, None])

def laplacian_filter(image):
    """Return the 4-neighbour discrete Laplacian; constants map to zero."""
    return _correlate(_image(image), np.array([[0., 1., 0.], [1., -4., 1.], [0., 1., 0.]]))

def median_filter(image, radius=1):
    """Square-window median filter; reflected boundary and odd window width."""
    a = _image(image)
    radius = _radius(radius)
    if radius == 0:
        return a.copy()
    p = np.pad(a, radius, mode="reflect")
    h, w = a.shape
    windows = np.stack([p[i:i+h, j:j+w] for i in range(2*radius+1)
                        for j in range(2*radius+1)], axis=0)
    return np.median(windows, axis=0)

def bilateral_filter(image, sigma_spatial, sigma_range, *, radius=None):
    """Edge-preserving bilateral filter with circular spatial neighbourhood.

    Intensities are in input units. This direct implementation is intended for
    small rasters; runtime is O(pixels * neighbourhood area).
    """
    a = _image(image)
    ss = _positive(sigma_spatial, "sigma_spatial")
    sr = _positive(sigma_range, "sigma_range")
    r = max(1, int(np.ceil(3 * ss))) if radius is None else _radius(radius)
    offsets = [(dy, dx, np.exp(-(dx*dx+dy*dy)/(2*ss*ss)))
               for dy in range(-r, r+1) for dx in range(-r, r+1)
               if dx*dx + dy*dy <= r*r]
    p = np.pad(a, r, mode="reflect")
    out = np.empty_like(a)
    h, w = a.shape
    for y in range(h):
        for x in range(w):
            centre = a[y, x]
            total = weight_sum = 0.0
            for dy, dx, sw in offsets:
                value = p[y+r+dy, x+r+dx]
                weight = sw * np.exp(-0.5*((value-centre)/sr)**2)
                total += weight * value
                weight_sum += weight
            out[y, x] = total / weight_sum
    return out

def anisotropic_diffusion(image, *, iterations=10, conductance=20.0,
                          step=0.2, option="exponential"):
    """Perona-Malik explicit 4-neighbour diffusion; conservative step <= 0.25."""
    a = _image(image).copy()
    if isinstance(iterations, bool) or int(iterations) != iterations or iterations < 0:
        raise ValueError("iterations must be a non-negative integer")
    k = _positive(conductance, "conductance")
    step = float(step)
    if not np.isfinite(step) or not 0 < step <= 0.25:
        raise ValueError("step must satisfy 0 < step <= 0.25")
    if option not in ("exponential", "reciprocal"):
        raise ValueError("option must be 'exponential' or 'reciprocal'")
    for _ in range(int(iterations)):
        p = np.pad(a, 1, mode="edge")
        grads = (p[:-2, 1:-1]-a, p[2:, 1:-1]-a,
                 p[1:-1, :-2]-a, p[1:-1, 2:]-a)
        if option == "exponential":
            conduct = [np.exp(-(g/k)**2) for g in grads]
        else:
            conduct = [1.0/(1.0+(g/k)**2) for g in grads]
        a = a + step * sum(c*g for c, g in zip(conduct, grads))
    return a
