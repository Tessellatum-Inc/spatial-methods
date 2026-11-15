"""Planar point-pattern summaries for rectangular observation windows."""
from __future__ import annotations
from math import hypot, isfinite, pi
from numbers import Integral
import random

def _validate(points, window):
    pts=[(float(p[0]),float(p[1])) for p in points]
    if len(pts)<2 or any(not isfinite(x) or not isfinite(y) for x,y in pts):
        raise ValueError("at least two finite points are required")
    if len(window)!=4:
        raise ValueError("window must be (xmin, ymin, xmax, ymax)")
    xmin,ymin,xmax,ymax=map(float,window)
    if not all(map(isfinite,(xmin,ymin,xmax,ymax))) or xmax<=xmin or ymax<=ymin:
        raise ValueError("window bounds must be finite and have positive width and height")
    if any(x<xmin or x>xmax or y<ymin or y>ymax for x,y in pts):
        raise ValueError("all points must lie within the observation window")
    if len(set(pts))!=len(pts):
        raise ValueError("duplicate point coordinates are not supported")
    return pts,(xmin,ymin,xmax,ymax)

def nearest_neighbor_distances(points):
    """Distance from each point to its closest other point."""
    if len(points)<2:
        raise ValueError("at least two points are required")
    pts=[(float(p[0]),float(p[1])) for p in points]
    if any(not isfinite(x) or not isfinite(y) for x,y in pts):
        raise ValueError("coordinates must be finite")
    if len(set(pts))!=len(pts):
        raise ValueError("duplicate point coordinates are not supported")
    return [min(hypot(x-a,y-b) for j,(a,b) in enumerate(pts) if j!=i)
            for i,(x,y) in enumerate(pts)]

def nearest_neighbor_cdf(points, radii):
    """Empirical nearest-neighbor distance CDF evaluated at requested radii."""
    distances=nearest_neighbor_distances(points)
    rs=[float(r) for r in radii]
    if any(not isfinite(r) or r<0 for r in rs):
        raise ValueError("radii must be finite and non-negative")
    return [sum(d<=r for d in distances)/len(distances) for r in rs]

def ripley_k_translation(points, window, radii):
    """Homogeneous Ripley K with rectangular translation edge correction.

    The translation weight is the inverse fraction of window overlap after
    shifting by each ordered pair displacement. Assumes stationarity and
    isotropy; output units are squared coordinate units.
    """
    pts,(xmin,ymin,xmax,ymax)=_validate(points,window)
    rs=[float(r) for r in radii]
    if not rs or any(not isfinite(r) or r<0 for r in rs):
        raise ValueError("radii must be a non-empty sequence of finite non-negative values")
    width,height=xmax-xmin,ymax-ymin
    area=width*height;n=len(pts)
    pairs=[]
    for i,(x,y) in enumerate(pts):
        for j,(a,b) in enumerate(pts):
            if i==j: continue
            dx,dy=abs(x-a),abs(y-b)
            overlap=((width-dx)/width)*((height-dy)/height)
            if overlap>0:
                pairs.append((hypot(dx,dy),1.0/overlap))
    result=[]
    for radius in rs:
        total=sum(weight for distance,weight in pairs if distance<=radius)
        result.append(area*total/(n*(n-1)))
    return result

def pair_correlation_from_k(radii, k_values):
    """Finite-difference g(r)=K'(r)/(2*pi*r) on strictly increasing radii."""
    rs=[float(r) for r in radii]; ks=[float(k) for k in k_values]
    if len(rs)!=len(ks) or len(rs)<3:
        raise ValueError("at least three matching radii and K values are required")
    if any(not isfinite(r) or r<=0 for r in rs) or any(rs[i]>=rs[i+1] for i in range(len(rs)-1)):
        raise ValueError("radii must be finite, positive and strictly increasing")
    if any(not isfinite(k) for k in ks):
        raise ValueError("K values must be finite")
    out=[]
    for i,r in enumerate(rs):
        lo=max(0,i-1);hi=min(len(rs)-1,i+1)
        derivative=(ks[hi]-ks[lo])/(rs[hi]-rs[lo])
        out.append(derivative/(2*pi*r))
    return out


def ripley_k_inhomogeneous_translation(points, window, radii, intensities):
    """Inhomogeneous K with supplied pointwise intensities and translation correction.

    Estimates K_inhom(r) = sum_{i != j, d_ij <= r}
        1 / (lambda_i * lambda_j * |W intersect (W + x_j - x_i)|).

    Intensities are assumed known or externally estimated at each observed
    point, in events per squared coordinate unit. No intensity model is fitted.
    The estimator assumes the inhomogeneous K target is translation invariant
    (second-order intensity-reweighted stationarity). Window must be a rectangle.
    """
    pts, (xmin, ymin, xmax, ymax) = _validate(points, window)
    lam = [float(v) for v in intensities]
    if len(lam) != len(pts):
        raise ValueError("one intensity value is required for each point")
    if any(not isfinite(v) or v <= 0 for v in lam):
        raise ValueError("intensities must be finite and strictly positive")
    rs = [float(r) for r in radii]
    if not rs or any(not isfinite(r) or r < 0 for r in rs):
        raise ValueError("radii must be a non-empty sequence of finite non-negative values")
    width, height = xmax - xmin, ymax - ymin
    pairs = []
    for i, (x, y) in enumerate(pts):
        for j, (a, b) in enumerate(pts):
            if i == j:
                continue
            dx, dy = abs(x - a), abs(y - b)
            overlap_area = (width - dx) * (height - dy)
            if overlap_area <= 0:
                continue
            distance = hypot(dx, dy)
            weight = 1.0 / (lam[i] * lam[j] * overlap_area)
            pairs.append((distance, weight))
    return [sum(weight for distance, weight in pairs if distance <= radius)
            for radius in rs]


def quadrat_count_test(points, window, nx=4, ny=4, *, n_simulations=999, seed=None):
    """Conditional Monte Carlo Pearson quadrat test for homogeneous CSR.

    The rectangular window is split into nx columns and ny rows of equal area.
    Conditional on the observed number of points, CSR implies multinomial
    quadrat counts with equal cell probabilities. The upper-tail Monte Carlo
    p-value uses the plus-one correction.
    """
    if isinstance(nx, bool) or not isinstance(nx, Integral) or nx < 1:
        raise ValueError("nx must be a positive integer")
    if isinstance(ny, bool) or not isinstance(ny, Integral) or ny < 1:
        raise ValueError("ny must be a positive integer")
    nx, ny = int(nx), int(ny)
    k = nx * ny
    if k < 2:
        raise ValueError("at least two quadrats are required")
    if isinstance(n_simulations, bool) or not isinstance(n_simulations, Integral) or n_simulations < 1:
        raise ValueError("n_simulations must be a positive integer")
    if seed is not None and (isinstance(seed, bool) or not isinstance(seed, Integral)):
        raise ValueError("seed must be an integer or None")
    if len(window) != 4:
        raise ValueError("window must be (xmin, ymin, xmax, ymax)")
    xmin, ymin, xmax, ymax = map(float, window)
    if not all(map(isfinite, (xmin, ymin, xmax, ymax))) or xmax <= xmin or ymax <= ymin:
        raise ValueError("window bounds must be finite and have positive width and height")
    pts = []
    for point in points:
        if len(point) != 2:
            raise ValueError("each point must have two coordinates")
        x, y = map(float, point)
        if not isfinite(x) or not isfinite(y):
            raise ValueError("point coordinates must be finite")
        if x < xmin or x > xmax or y < ymin or y > ymax:
            raise ValueError("all points must lie within the observation window")
        pts.append((x, y))
    if not pts:
        raise ValueError("at least one point is required")
    if len(set(pts)) != len(pts):
        raise ValueError("duplicate point coordinates are not supported")

    observed = [0] * k
    width, height = xmax - xmin, ymax - ymin
    for x, y in pts:
        col = min(int((x - xmin) / width * nx), nx - 1)
        row = min(int((y - ymin) / height * ny), ny - 1)
        observed[row * nx + col] += 1

    n = len(pts)
    expected = n / k
    statistic = sum((count - expected) ** 2 / expected for count in observed)
    rng = random.Random(int(seed) if seed is not None else None)
    exceedances = 0
    for _ in range(int(n_simulations)):
        simulated = [0] * k
        for _ in range(n):
            simulated[rng.randrange(k)] += 1
        simulated_stat = sum((count - expected) ** 2 / expected for count in simulated)
        if simulated_stat >= statistic - 1e-12:
            exceedances += 1
    pvalue = (exceedances + 1) / (int(n_simulations) + 1)
    counts_grid = [observed[r * nx:(r + 1) * nx] for r in range(ny)]
    return {
        "counts": counts_grid, "expected_per_quadrat": expected,
        "pearson_statistic": statistic, "degrees_of_freedom": k - 1,
        "pvalue": pvalue, "simulations": int(n_simulations),
        "exceedances": exceedances, "n_points": n, "nx": nx, "ny": ny,
    }


def empty_space_cdf(points, window, radii, *, n_samples=10000, seed=0):
    """Estimate the empty-space F function by uniform Monte Carlo sampling.

    Each random location is sampled uniformly in the rectangular window and
    its distance to the nearest observed event is measured. This is an
    uncorrected rectangular-window teaching estimator; boundary effects and
    Monte Carlo error should be considered when interpreting F(r).
    """
    pts, (xmin, ymin, xmax, ymax) = _validate(points, window)
    rs = [float(r) for r in radii]
    if not rs or any(not isfinite(r) or r < 0 for r in rs):
        raise ValueError("radii must be a non-empty sequence of finite non-negative values")
    if isinstance(n_samples, bool) or not isinstance(n_samples, Integral) or n_samples <= 0:
        raise ValueError("n_samples must be a positive integer")
    if isinstance(seed, bool) or not isinstance(seed, Integral):
        raise ValueError("seed must be an integer")
    rng = random.Random(int(seed))
    distances = []
    for _ in range(int(n_samples)):
        x = rng.uniform(xmin, xmax)
        y = rng.uniform(ymin, ymax)
        distances.append(min(hypot(x - px, y - py) for px, py in pts))
    return [sum(distance <= radius for distance in distances) / len(distances)
            for radius in rs]


def j_function(points, window, radii, *, n_samples=10000, seed=0):
    """Return (G, F, J) estimates, where J(r)=(1-G(r))/(1-F(r)).

    G is the empirical nearest-neighbour CDF; F is the Monte Carlo empty-space
    CDF. J is undefined when F(r)=1 and is returned as NaN at those radii.
    """
    g_values = nearest_neighbor_cdf(points, radii)
    f_values = empty_space_cdf(points, window, radii, n_samples=n_samples, seed=seed)
    j_values = [((1.0 - g) / (1.0 - f)) if f < 1.0 else float("nan")
                for g, f in zip(g_values, f_values)]
    return g_values, f_values, j_values
