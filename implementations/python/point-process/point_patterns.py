"""Planar point-pattern summaries for rectangular observation windows."""
from __future__ import annotations
from math import cos, exp, hypot, isfinite, pi, sin
from numbers import Integral
import random
import numpy as np

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


def _validate_marked(points, marks, window=None):
    if window is None:
        pts = [(float(p[0]), float(p[1])) for p in points]
        if len(pts) < 2 or any(not isfinite(x) or not isfinite(y) for x, y in pts):
            raise ValueError("at least two finite points are required")
        if len(set(pts)) != len(pts):
            raise ValueError("duplicate point coordinates are not supported")
        bounds = None
    else:
        pts, bounds = _validate(points, window)
    if len(marks) != len(pts):
        raise ValueError("one mark is required for each point")
    labels = list(marks)
    if any(label is None for label in labels):
        raise ValueError("marks must not contain None")
    return pts, labels, bounds


def cross_nearest_neighbor_cdf(points, marks, from_mark, to_mark, radii):
    """Empirical G_ij: nearest type-j distance from each type-i event."""
    pts, labels, _ = _validate_marked(points, marks)
    if from_mark == to_mark:
        raise ValueError("cross-type summaries require two distinct mark values")
    source = [p for p, m in zip(pts, labels) if m == from_mark]
    target = [p for p, m in zip(pts, labels) if m == to_mark]
    if not source or not target:
        raise ValueError("both requested mark types must be present")
    rs = [float(r) for r in radii]
    if not rs or any(not isfinite(r) or r < 0 for r in rs):
        raise ValueError("radii must be a non-empty sequence of finite non-negative values")
    distances = [min(hypot(x-a, y-b) for a, b in target) for x, y in source]
    return [sum(d <= r for d in distances) / len(distances) for r in rs]


def cross_ripley_k_translation(points, marks, window, from_mark, to_mark, radii):
    """Cross-type K_ij with rectangular translation edge correction.

    K_ij(r) estimates the expected number of type-j events within r of a
    typical type-i event, divided by the type-j intensity. Under independence
    of the two stationary component processes, K_ij(r)=pi*r**2.
    """
    pts, labels, (xmin, ymin, xmax, ymax) = _validate_marked(points, marks, window)
    if from_mark == to_mark:
        raise ValueError("cross-type summaries require two distinct mark values")
    source = [p for p, m in zip(pts, labels) if m == from_mark]
    target = [p for p, m in zip(pts, labels) if m == to_mark]
    if not source or not target:
        raise ValueError("both requested mark types must be present")
    rs = [float(r) for r in radii]
    if not rs or any(not isfinite(r) or r < 0 for r in rs):
        raise ValueError("radii must be a non-empty sequence of finite non-negative values")
    width, height = xmax - xmin, ymax - ymin
    area = width * height
    pairs = []
    for x, y in source:
        for a, b in target:
            dx, dy = abs(x-a), abs(y-b)
            overlap = (width-dx) * (height-dy)
            if overlap <= 0:
                continue
            pairs.append((hypot(dx, dy), area / overlap))
    scale = area / (len(source) * len(target))
    return [scale * sum(weight for distance, weight in pairs if distance <= r)
            for r in rs]


def cross_pair_correlation_from_k(radii, k_values):
    """Finite-difference cross pair correlation g_ij=K'_ij(r)/(2*pi*r)."""
    return pair_correlation_from_k(radii, k_values)


def cross_j_function(points, marks, window, from_mark, to_mark, radii, *,
                     n_samples=10000, seed=0):
    """Estimate cross-type J_ij=(1-G_ij)/(1-F_j) using uniform window probes."""
    pts, labels, (xmin, ymin, xmax, ymax) = _validate_marked(points, marks, window)
    if from_mark == to_mark:
        raise ValueError("cross-type summaries require two distinct mark values")
    target = [p for p, m in zip(pts, labels) if m == to_mark]
    if not target or not any(m == from_mark for m in labels):
        raise ValueError("both requested mark types must be present")
    rs = [float(r) for r in radii]
    if not rs or any(not isfinite(r) or r < 0 for r in rs):
        raise ValueError("radii must be a non-empty sequence of finite non-negative values")
    if isinstance(n_samples, bool) or not isinstance(n_samples, Integral) or n_samples <= 0:
        raise ValueError("n_samples must be a positive integer")
    if isinstance(seed, bool) or not isinstance(seed, Integral):
        raise ValueError("seed must be an integer")
    rng = random.Random(int(seed))
    empty_distances = []
    for _ in range(int(n_samples)):
        x, y = rng.uniform(xmin, xmax), rng.uniform(ymin, ymax)
        empty_distances.append(min(hypot(x-a, y-b) for a, b in target))
    f_values = [sum(d <= r for d in empty_distances) / len(empty_distances) for r in rs]
    g_values = cross_nearest_neighbor_cdf(points, labels, from_mark, to_mark, rs)
    j_values = [(1-g)/(1-f) if f < 1 else float("nan")
                for g, f in zip(g_values, f_values)]
    return g_values, f_values, j_values


def _poisson_count(mean, rng):
    """Exact Poisson draw by exponential inter-arrival times."""
    if mean <= 0:
        return 0
    total = 0.0
    count = 0
    while True:
        total += rng.expovariate(1.0)
        if total > mean:
            return count
        count += 1


def simulate_homogeneous_poisson(window, intensity, *, seed=0):
    """Simulate a homogeneous planar Poisson process in a rectangle.

    intensity is expected events per squared coordinate unit. Conditional on
    N, event locations are independent uniform draws in the window.
    """
    if len(window) != 4:
        raise ValueError("window must be (xmin, ymin, xmax, ymax)")
    xmin, ymin, xmax, ymax = map(float, window)
    if not all(isfinite(v) for v in (xmin, ymin, xmax, ymax)) or xmax <= xmin or ymax <= ymin:
        raise ValueError("window bounds must be finite and have positive width and height")
    lam = float(intensity)
    if not isfinite(lam) or lam < 0:
        raise ValueError("intensity must be finite and non-negative")
    if isinstance(seed, bool) or not isinstance(seed, Integral):
        raise ValueError("seed must be an integer")
    rng = random.Random(int(seed))
    count = _poisson_count(lam * (xmax-xmin) * (ymax-ymin), rng)
    return [(rng.uniform(xmin, xmax), rng.uniform(ymin, ymax)) for _ in range(count)]


def simulate_thomas_process(window, parent_intensity, mean_offspring, sigma, *,
                            seed=0, buffer_sigma=4.0):
    """Simulate a stationary Thomas (Gaussian Neyman-Scott) cluster process.

    Parents form a homogeneous Poisson process. Each parent generates a
    Poisson(mean_offspring) number of offspring with independent isotropic
    Gaussian coordinate offsets of standard deviation sigma. Parents are
    simulated in a buffer-expanded rectangle and only offspring inside the
    target window are retained. The finite buffer truncates Gaussian tails.
    """
    if len(window) != 4:
        raise ValueError("window must be (xmin, ymin, xmax, ymax)")
    xmin, ymin, xmax, ymax = map(float, window)
    if not all(isfinite(v) for v in (xmin, ymin, xmax, ymax)) or xmax <= xmin or ymax <= ymin:
        raise ValueError("window bounds must be finite and have positive width and height")
    kappa, mu, spread, buffer = map(float, (parent_intensity, mean_offspring, sigma, buffer_sigma))
    if not all(isfinite(v) for v in (kappa, mu, spread, buffer)) or kappa < 0 or mu < 0 or spread <= 0 or buffer <= 0:
        raise ValueError("parent intensity and mean offspring must be non-negative; sigma and buffer_sigma must be positive")
    if isinstance(seed, bool) or not isinstance(seed, Integral):
        raise ValueError("seed must be an integer")
    rng = random.Random(int(seed))
    margin = buffer * spread
    expanded = (xmin-margin, ymin-margin, xmax+margin, ymax+margin)
    parents = simulate_homogeneous_poisson(expanded, kappa, seed=rng.randrange(0, 2**63))
    offspring = []
    for px, py in parents:
        count = _poisson_count(mu, rng)
        for _ in range(count):
            x = rng.gauss(px, spread)
            y = rng.gauss(py, spread)
            if xmin <= x <= xmax and ymin <= y <= ymax:
                offspring.append((x, y))
    return offspring


def simulate_matern_cluster_process(window, parent_intensity, mean_offspring, radius, *, seed=0):
    """Simulate a stationary Matérn disc cluster (Neyman–Scott) process.

    Parents form a homogeneous Poisson process with intensity kappa. Each
    parent produces Poisson(mu) offspring, independently uniform in a disc
    of the given radius. Parents are simulated in the target rectangle
    expanded by radius, which is sufficient because the offspring kernel has
    compact support. Only offspring inside the target window are returned.
    The stationary intensity is kappa * mu.
    """
    if len(window) != 4:
        raise ValueError("window must be (xmin, ymin, xmax, ymax)")
    xmin, ymin, xmax, ymax = map(float, window)
    if not all(isfinite(v) for v in (xmin, ymin, xmax, ymax)) or xmax <= xmin or ymax <= ymin:
        raise ValueError("window bounds must be finite and have positive width and height")
    kappa, mu, scale = map(float, (parent_intensity, mean_offspring, radius))
    if not all(isfinite(v) for v in (kappa, mu, scale)) or kappa < 0 or mu < 0 or scale <= 0:
        raise ValueError("parent intensity and mean offspring must be non-negative; radius must be positive")
    if isinstance(seed, bool) or not isinstance(seed, Integral):
        raise ValueError("seed must be an integer")
    if kappa == 0 or mu == 0:
        return []
    rng = random.Random(int(seed))
    expanded = (xmin-scale, ymin-scale, xmax+scale, ymax+scale)
    parents = simulate_homogeneous_poisson(expanded, kappa, seed=rng.randrange(0, 2**63))
    offspring = []
    for px, py in parents:
        count = _poisson_count(mu, rng)
        for _ in range(count):
            distance = scale * (rng.random() ** 0.5)
            angle = rng.random() * 2 * pi
            x = px + distance * cos(angle)
            y = py + distance * sin(angle)
            if xmin <= x <= xmax and ymin <= y <= ymax:
                offspring.append((x, y))
    return offspring


def _cholesky_lower(matrix):
    """Small dense Cholesky factorisation for a symmetric positive matrix."""
    n = len(matrix)
    lower = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            value = matrix[i][j] - sum(lower[i][k] * lower[j][k] for k in range(j))
            if i == j:
                if value < -1e-10:
                    raise ValueError("covariance matrix is not positive semidefinite")
                lower[i][j] = value ** 0.5 if value > 0 else 0.0
            elif lower[j][j] > 0:
                lower[i][j] = value / lower[j][j]
    return lower


def simulate_log_gaussian_cox_process(window, mean_intensity, variance, correlation_range,
                                      *, nx=8, ny=8, seed=0):
    """Simulate a grid-discretised stationary log-Gaussian Cox process.

    A Gaussian field with exponential covariance C(h)=variance*exp(-|h|/a)
    is sampled at regular cell centres. Each cell then receives a conditionally
    Poisson count with intensity mean_intensity*exp(Z-variance/2), and points
    are uniform within that cell. The finite grid is an explicit piecewise-
    constant approximation to a continuous LGCP, not an exact continuous-
    field simulator. Dense Cholesky limits this teaching implementation to
    at most 225 cells.
    """
    if len(window) != 4:
        raise ValueError("window must be (xmin, ymin, xmax, ymax)")
    xmin, ymin, xmax, ymax = map(float, window)
    if not all(isfinite(v) for v in (xmin, ymin, xmax, ymax)) or xmax <= xmin or ymax <= ymin:
        raise ValueError("window bounds must be finite and have positive width and height")
    intensity, var, scale = map(float, (mean_intensity, variance, correlation_range))
    if not all(isfinite(v) for v in (intensity, var, scale)) or intensity < 0 or var < 0 or scale <= 0:
        raise ValueError("mean_intensity and variance must be non-negative; correlation_range must be positive")
    if any(isinstance(v, bool) or not isinstance(v, Integral) or v <= 0 for v in (nx, ny)):
        raise ValueError("nx and ny must be positive integers")
    nx, ny = int(nx), int(ny)
    n = nx * ny
    if n > 225:
        raise ValueError("nx * ny must not exceed 225 for the dense covariance solver")
    if isinstance(seed, bool) or not isinstance(seed, Integral):
        raise ValueError("seed must be an integer")
    if intensity == 0:
        return []
    width, height = (xmax-xmin)/nx, (ymax-ymin)/ny
    centres = [(xmin+(i+0.5)*width, ymin+(j+0.5)*height)
               for j in range(ny) for i in range(nx)]
    covariance = [[var * exp(-hypot(x-a, y-b)/scale)
                   for a, b in centres] for x, y in centres]
    lower = _cholesky_lower(covariance)
    rng = random.Random(int(seed))
    normal = [rng.gauss(0.0, 1.0) for _ in range(n)]
    field = [sum(lower[i][j] * normal[j] for j in range(i+1)) for i in range(n)]
    points = []
    cell_area = width * height
    for index, z in enumerate(field):
        cell_intensity = intensity * exp(z - var/2)
        count = _poisson_count(cell_intensity * cell_area, rng)
        row, col = divmod(index, nx)
        x0, y0 = xmin + col*width, ymin + row*height
        points.extend((rng.uniform(x0, x0+width), rng.uniform(y0, y0+height))
                      for _ in range(count))
    return points


def simulate_strauss_process(window, beta, gamma, interaction_radius, *,
                             burn_in=5000, n_steps=5000, seed=0):
    """Simulate a Strauss repulsive process using birth-death Metropolis-Hastings.

    The density relative to a unit-rate Poisson process is proportional to
    beta**n * gamma**s, where s counts unordered pairs closer than the
    interaction radius. beta is an intensity-like activity parameter and
    0 <= gamma <= 1 controls repulsion (gamma=1 is Poisson; gamma=0 is
    hard-core). This finite-run MCMC output is approximate, not exact.
    """
    if len(window) != 4:
        raise ValueError("window must be (xmin, ymin, xmax, ymax)")
    xmin, ymin, xmax, ymax = map(float, window)
    if not all(isfinite(v) for v in (xmin, ymin, xmax, ymax)) or xmax <= xmin or ymax <= ymin:
        raise ValueError("window bounds must be finite and have positive width and height")
    activity, interaction, radius = map(float, (beta, gamma, interaction_radius))
    if (not all(isfinite(v) for v in (activity, interaction, radius))
            or activity < 0 or not 0 <= interaction <= 1 or radius <= 0):
        raise ValueError("beta must be non-negative, gamma must be in [0, 1], and interaction_radius positive")
    if any(isinstance(v, bool) or not isinstance(v, Integral) or v < 0 for v in (burn_in, n_steps)):
        raise ValueError("burn_in and n_steps must be non-negative integers")
    if n_steps == 0:
        raise ValueError("n_steps must be positive")
    if isinstance(seed, bool) or not isinstance(seed, Integral):
        raise ValueError("seed must be an integer")
    if activity == 0:
        return []
    rng = random.Random(int(seed))
    area = (xmax - xmin) * (ymax - ymin)
    points = []
    for _ in range(int(burn_in) + int(n_steps)):
        if rng.random() < 0.5:
            candidate = (rng.uniform(xmin, xmax), rng.uniform(ymin, ymax))
            neighbours = sum(hypot(candidate[0]-x, candidate[1]-y) < radius
                             for x, y in points)
            ratio = activity * area * (interaction ** neighbours) / (len(points) + 1)
            if rng.random() < min(1.0, ratio):
                points.append(candidate)
        elif points:
            index = rng.randrange(len(points))
            x, y = points[index]
            neighbours = sum(hypot(x-other_x, y-other_y) < radius
                             for j, (other_x, other_y) in enumerate(points) if j != index)
            factor = activity * area * (interaction ** neighbours)
            ratio = float("inf") if factor == 0 else len(points) / factor
            if rng.random() < min(1.0, ratio):
                points.pop(index)
    return points



def simulate_inhomogeneous_poisson(intensity_grid, window, *, seed=None):
    """Simulate a piecewise-constant inhomogeneous planar Poisson process.

    intensity_grid is a finite non-negative (rows, columns) array in events
    per squared coordinate unit. Each cell has constant intensity and events
    are uniform within that cell. The grid partitions the rectangular window
    into equal-sized cells; rows run from ymin upward.
    """
    intensity = np.asarray(intensity_grid, dtype=float)
    if intensity.ndim != 2 or intensity.size == 0:
        raise ValueError("intensity_grid must be a non-empty 2D array")
    if not np.isfinite(intensity).all() or np.any(intensity < 0):
        raise ValueError("intensity_grid must be finite and non-negative")
    if len(window) != 4:
        raise ValueError("window must be (xmin, ymin, xmax, ymax)")
    xmin, ymin, xmax, ymax = map(float, window)
    if not all(map(isfinite, (xmin, ymin, xmax, ymax))) or xmax <= xmin or ymax <= ymin:
        raise ValueError("window bounds must be finite and have positive width and height")
    if seed is not None and (isinstance(seed, bool) or not isinstance(seed, Integral)):
        raise ValueError("seed must be an integer or None")
    rng = np.random.default_rng(None if seed is None else int(seed))
    rows, columns = intensity.shape
    cell_width = (xmax - xmin) / columns
    cell_height = (ymax - ymin) / rows
    cell_area = cell_width * cell_height
    points = []
    try:
        for row in range(rows):
            for column in range(columns):
                count = int(rng.poisson(float(intensity[row, column]) * cell_area))
                if count == 0:
                    continue
                x0 = xmin + column * cell_width
                y0 = ymin + row * cell_height
                xs = rng.uniform(x0, x0 + cell_width, size=count)
                ys = rng.uniform(y0, y0 + cell_height, size=count)
                points.extend((float(x), float(y)) for x, y in zip(xs, ys))
    except (ValueError, OverflowError) as exc:
        raise ValueError("intensity scale is too large to simulate safely") from exc
    return points
