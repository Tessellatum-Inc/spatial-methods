"""Simple and partial Mantel tests for aligned distance matrices."""
from __future__ import annotations
import math, random
from typing import Sequence

def _matrix(values: Sequence[Sequence[float]], name: str) -> list[list[float]]:
    try: a = [[float(v) for v in row] for row in values]
    except (TypeError, ValueError) as exc: raise ValueError(f"{name} must be numeric") from exc
    n = len(a)
    if n < 3 or any(len(row) != n for row in a): raise ValueError(f"{name} must be square with at least three observations")
    if any(not math.isfinite(v) for row in a for v in row): raise ValueError(f"{name} must be finite")
    scale = max(1.0, max(abs(v) for row in a for v in row)); tol = 1e-10 * scale
    for i in range(n):
        if abs(a[i][i]) > tol: raise ValueError(f"{name} diagonal must be zero")
        for j in range(i + 1, n):
            if a[i][j] < 0 or a[j][i] < 0: raise ValueError(f"{name} distances must be non-negative")
            if abs(a[i][j] - a[j][i]) > tol: raise ValueError(f"{name} must be symmetric")
    if any(v < 0 for row in a for v in row): raise ValueError(f"{name} distances must be non-negative")
    return a

def _upper(a): return [a[i][j] for i in range(len(a)) for j in range(i + 1, len(a))]

def _correlation(x, y):
    mx, my = sum(x)/len(x), sum(y)/len(y)
    dx, dy = [v-mx for v in x], [v-my for v in y]
    sx, sy = sum(v*v for v in dx), sum(v*v for v in dy)
    if sx <= 0 or sy <= 0: raise ValueError("distance vectors must have non-zero variance")
    return sum(a*b for a,b in zip(dx,dy))/math.sqrt(sx*sy)

def _partial(x, y, z):
    mx,my,mz = (sum(v)/len(v) for v in (x,y,z)); dz=[v-mz for v in z]
    zz=sum(v*v for v in dz)
    if zz <= 0: raise ValueError("control distance vector must have non-zero variance")
    bx=sum((a-mx)*d for a,d in zip(x,dz))/zz
    by=sum((b-my)*d for b,d in zip(y,dz))/zz
    return _correlation([a-mx-bx*d for a,d in zip(x,dz)],
                        [b-my-by*d for b,d in zip(y,dz)])

def _options(permutations, alternative):
    if isinstance(permutations,bool) or not isinstance(permutations,int) or permutations < 1:
        raise ValueError("permutations must be a positive integer")
    if alternative not in {"two-sided","greater","less"}:
        raise ValueError("invalid alternative")

def _extreme(v, obs, alternative):
    if alternative=="greater": return v >= obs-1e-15
    if alternative=="less": return v <= obs+1e-15
    return abs(v) >= abs(obs)-1e-15

def mantel_test(distance_x, distance_y, *, permutations=999, seed=0, alternative="two-sided"):
    """Pearson correlation of upper-triangle distances with label permutations."""
    _options(permutations,alternative)
    x,y=_matrix(distance_x,"distance_x"),_matrix(distance_y,"distance_y")
    if len(x)!=len(y): raise ValueError("distance matrices must have the same dimensions")
    xv,yv=_upper(x),_upper(y); observed=_correlation(xv,yv)
    rng,n,hits=random.Random(seed),len(x),0
    for _ in range(permutations):
        order=list(range(n)); rng.shuffle(order)
        px=[x[order[i]][order[j]] for i in range(n) for j in range(i+1,n)]
        hits += _extreme(_correlation(px,yv),observed,alternative)
    return {"statistic":observed,"p_value":(hits+1)/(permutations+1),
            "permutations":permutations,"alternative":alternative}

def partial_mantel_test(distance_x, distance_y, distance_control, *,
                        permutations=999, seed=0, alternative="two-sided"):
    """Partial distance correlation with one control matrix; spatial caveats apply."""
    _options(permutations,alternative)
    x,y,z=(_matrix(distance_x,"distance_x"),_matrix(distance_y,"distance_y"),
           _matrix(distance_control,"distance_control"))
    if len(x)!=len(y) or len(x)!=len(z): raise ValueError("all matrices must have the same dimensions")
    xv,yv,zv=_upper(x),_upper(y),_upper(z); observed=_partial(xv,yv,zv)
    rng,n,hits=random.Random(seed),len(x),0
    for _ in range(permutations):
        order=list(range(n)); rng.shuffle(order)
        px=[x[order[i]][order[j]] for i in range(n) for j in range(i+1,n)]
        hits += _extreme(_partial(px,yv,zv),observed,alternative)
    return {"statistic":observed,"p_value":(hits+1)/(permutations+1),
            "permutations":permutations,"alternative":alternative}
