"""Directional empirical variograms and bounded theoretical model fitting."""
from __future__ import annotations
from math import atan2, comb, cos, degrees, isfinite, radians, sin
import numpy as np
from scipy.optimize import least_squares, minimize
from scipy.special import gamma as gamma_function, kv

_MODELS={"spherical","exponential","gaussian","matern"}

def _correlation(ratio, model, nu):
    if model == "spherical":
        return 1.0 - np.where(ratio < 1.0, 1.5 * ratio - 0.5 * ratio**3, 1.0)
    if model == "exponential":
        return np.exp(-3.0 * ratio)
    if model == "gaussian":
        return np.exp(-3.0 * ratio**2)
    argument = np.sqrt(2.0 * nu) * ratio
    result = np.ones_like(argument)
    positive = argument > 0
    a_pos = argument[positive]
    result[positive] = (2.0**(1.0 - nu) / gamma_function(nu)) * a_pos**nu * kv(nu, a_pos)
    return result


def variogram_model(lags,*,model="spherical",nugget=0.0,partial_sill=1.0,range_=1.0,nu=1.5):
    """Evaluate spherical, exponential, Gaussian or Matérn semivariogram models."""
    h=np.asarray(lags,dtype=float); n=float(nugget); s=float(partial_sill); a=float(range_)
    if model not in _MODELS: raise ValueError("model must be spherical, exponential, gaussian or matern")
    if not np.isfinite(h).all() or np.any(h<0): raise ValueError("lags must be finite and non-negative")
    if not np.isfinite((n,s,a)).all() or n<0 or s<0 or a<=0:
        raise ValueError("nugget and partial_sill must be non-negative; range_ must be positive")
    nu=float(nu)
    if not np.isfinite(nu) or nu<=0:
        raise ValueError("nu must be finite and positive")
    ratio=h/a
    shape=1.0-_correlation(ratio,model,nu)
    result=n+s*shape
    return np.where(h==0.0,0.0,result)

def genton_semivariance(increments):
    """Genton (1998) Q_n-based robust semivariance for one lag class."""
    values = np.asarray(increments, dtype=float)
    if values.ndim != 1 or len(values) < 2 or not np.isfinite(values).all():
        raise ValueError("increments must be a finite 1D array with at least two values")
    differences = np.abs(values[:, None] - values[None, :])
    upper = differences[np.triu_indices(len(values), k=1)]
    k = comb(len(values) // 2 + 1, 2)  # one-based order statistic
    q_n = 2.2191 * float(np.partition(upper, k - 1)[k - 1])
    result = 0.5 * q_n * q_n
    if not isfinite(result):
        raise ValueError("Genton estimate overflowed")
    return result


def dowd_semivariance(increments):
    """Dowd's median-based robust semivariance (Gaussian scale factor 1.099)."""
    values = np.asarray(increments, dtype=float)
    if values.ndim != 1 or len(values) < 1 or not np.isfinite(values).all():
        raise ValueError("increments must be a finite 1D array with at least one value")
    median = float(np.median(np.abs(values)))
    result = 1.099 * median * median
    if not isfinite(result):
        raise ValueError("Dowd estimate overflowed")
    return result


def anisotropic_distance(dx, dy, *, azimuth_deg=0.0, ratio=1.0):
    """Geometric-anisotropy distance; azimuth is clockwise from north.

    ratio is minor/major range in (0, 1]. The major axis retains unit scale.
    """
    angle = radians(float(azimuth_deg) % 180.0)
    ratio = float(ratio)
    if not isfinite(ratio) or not 0.0 < ratio <= 1.0:
        raise ValueError("anisotropy ratio must be finite and in (0, 1]")
    dx, dy = float(dx), float(dy)
    if not isfinite(dx) or not isfinite(dy):
        raise ValueError("coordinate offsets must be finite")
    along = dx * sin(angle) + dy * cos(angle)
    across = dx * cos(angle) - dy * sin(angle)
    distance = float(np.hypot(along, across / ratio))
    if not isfinite(distance):
        raise ValueError("anisotropic distance overflowed")
    return distance


def directional_semivariogram(points,values,bin_edges,*,azimuth_deg=0.0,
                               tolerance_deg=22.5,bandwidth=None,estimator="matheron",
                               anisotropy_azimuth_deg=0.0,anisotropy_ratio=1.0):
    """Compute an undirected directional semivariogram.

    Azimuth is clockwise from north; pair bearings are compared modulo 180°.
    Cross-track bandwidth, when supplied, is in coordinate units.
    """
    xy=np.asarray(points,dtype=float); z=np.asarray(values,dtype=float); edges=np.asarray(bin_edges,dtype=float)
    if xy.ndim!=2 or xy.shape[1]!=2 or len(xy)<2: raise ValueError("points must be an n-by-2 array with n>=2")
    if z.shape!=(len(xy),) or not np.isfinite(z).all(): raise ValueError("values must be finite and match points")
    if not np.isfinite(xy).all(): raise ValueError("coordinates must be finite")
    if edges.ndim!=1 or len(edges)<2 or not np.isfinite(edges).all() or edges[0]<0 or np.any(np.diff(edges)<=0):
        raise ValueError("bin_edges must be finite, non-negative and strictly increasing")
    az=float(azimuth_deg)%180; tol=float(tolerance_deg)
    if not isfinite(tol) or not 0<=tol<=90: raise ValueError("tolerance_deg must be in [0, 90]")
    if bandwidth is not None and (not isfinite(float(bandwidth)) or float(bandwidth)<0):
        raise ValueError("bandwidth must be finite and non-negative")
    if estimator not in {"matheron","cressie","genton","dowd"}: raise ValueError("estimator must be matheron, cressie, genton or dowd")
    anisotropy_ratio=float(anisotropy_ratio)
    if not isfinite(anisotropy_ratio) or not 0.0 < anisotropy_ratio <= 1.0:
        raise ValueError("anisotropy_ratio must be finite and in (0, 1]")
    sums=[[] for _ in range(len(edges)-1)]
    theta=radians(az)
    for i in range(len(xy)-1):
        for j in range(i+1,len(xy)):
            dx,dy=xy[j]-xy[i]; distance=float(np.hypot(dx,dy)); bin_distance=anisotropic_distance(dx,dy,azimuth_deg=anisotropy_azimuth_deg,ratio=anisotropy_ratio)
            if distance==0 or bin_distance<edges[0] or bin_distance>edges[-1]: continue
            bearing=degrees(atan2(dx,dy))%180
            difference=abs((bearing-az+90)%180-90)
            cross_track=abs(-cos(theta)*dx+sin(theta)*dy)
            if difference>tol or (bandwidth is not None and cross_track>float(bandwidth)): continue
            k=len(edges)-2 if bin_distance==edges[-1] else int(np.searchsorted(edges,bin_distance,side="right")-1)
            if k<0: continue
            sums[k].append(float(z[i]-z[j]) if estimator=="genton" else abs(float(z[i]-z[j])))
    output=[]
    for k,pairs in enumerate(sums):
        count=len(pairs); gamma=None
        if count:
            if estimator=="genton": gamma=genton_semivariance(pairs)
            elif estimator=="dowd": gamma=dowd_semivariance(pairs)
            elif estimator=="matheron": gamma=0.5*float(np.mean(np.square(pairs)))
            else:
                mean_root=float(np.mean(np.sqrt(pairs)))
                correction=0.457+0.494/count+0.045/(count*count)
                gamma=0.5*(mean_root**4)/correction
        output.append({"lag":float((edges[k]+edges[k+1])/2),"semivariance":gamma,"pairs":count})
    return output

def fit_variogram(lags,semivariances,*,pairs=None,model="spherical",fit_nugget=True,
                  initial=None,nu=1.5):
    """Fit nugget, partial sill and range by pair-count weighted least squares."""
    h=np.asarray(lags,dtype=float); g=np.asarray(semivariances,dtype=float)
    if model not in _MODELS: raise ValueError("unsupported variogram model")
    nu=float(nu)
    if not isfinite(nu) or nu<=0: raise ValueError("nu must be finite and positive")
    if h.ndim!=1 or g.shape!=h.shape or len(h)<3: raise ValueError("lags and semivariances need at least three aligned values")
    mask=np.isfinite(h)&np.isfinite(g)&(h>0)&(g>=0)
    h,g=h[mask],g[mask]
    if len(h)<3: raise ValueError("at least three finite positive-lag bins are required")
    if pairs is None: counts=np.ones(len(mask),dtype=float)[mask]
    else:
        p=np.asarray(pairs,dtype=float)
        if p.shape!=np.asarray(lags).shape or not np.isfinite(p).all() or np.any(p<0):
            raise ValueError("pairs must be finite non-negative counts matching lags")
        counts=p[mask]
    keep=counts>0; h,g,counts=h[keep],g[keep],counts[keep]
    if len(h)<3: raise ValueError("at least three populated lag bins are required")
    if not np.isfinite(h).all() or np.any(h<=0): raise ValueError("lags must be positive and finite")
    if initial is None:
        n0=max(0.0,float(np.min(g))*0.25); s0=max(float(np.max(g)-n0),1e-8); a0=float(np.median(h))
    else:
        n0,s0,a0=map(float,initial)
    if not np.isfinite((n0,s0,a0)).all() or n0<0 or s0<=0 or a0<=0:
        raise ValueError("initial parameters must be non-negative nugget and positive sill/range")
    weights=np.sqrt(counts/np.max(counts))
    if fit_nugget:
        x0=np.array([n0,s0,a0]); lower=[0,1e-12,max(1e-12,float(np.min(h))*1e-6)]
        upper=[np.inf,np.inf,max(float(np.max(h))*1e6,1.0)]
        def residual(x): return (variogram_model(h,model=model,nugget=x[0],partial_sill=x[1],range_=x[2],nu=nu)-g)*weights
        fit=least_squares(residual,x0,bounds=(lower,upper))
        nugget,sill,range_=map(float,fit.x)
    else:
        def residual(x): return (variogram_model(h,model=model,nugget=n0,partial_sill=x[0],range_=x[1],nu=nu)-g)*weights
        fit=least_squares(residual,[s0,a0],bounds=([1e-12,max(1e-12,float(np.min(h))*1e-6)],[np.inf,max(float(np.max(h))*1e6,1.0)]))
        nugget=n0; sill,range_=map(float,fit.x)
    return {"model":model,"nu":nu,"nugget":nugget,"partial_sill":sill,"sill":nugget+sill,
            "range":range_,"weighted_sse":float(np.sum(fit.fun**2)),
            "success":bool(fit.success),"message":str(fit.message),"bins_used":int(len(h))}



def fit_variogram_reml(points, values, *, model="exponential", initial=None, anisotropy_azimuth_deg=0.0, anisotropy_ratio=1.0, fit_anisotropy=False, nu=1.5):
    """Fit a constant-mean Gaussian covariance by dense restricted likelihood.

    With fit_anisotropy=True, jointly estimates major-axis azimuth and
    minor/major range ratio (bounded to [0.1, 1]). Otherwise uses supplied
    geometric-anisotropy parameters. This is a small-data reference method.
    """
    xy = np.asarray(points, dtype=float)
    z = np.asarray(values, dtype=float)
    if xy.ndim != 2 or xy.shape[1] != 2 or len(xy) < 4:
        raise ValueError("points must be an n-by-2 array with n>=4")
    if z.shape != (len(xy),) or not np.isfinite(z).all():
        raise ValueError("values must be finite and match points")
    if not np.isfinite(xy).all() or len(np.unique(xy, axis=0)) != len(xy):
        raise ValueError("points must be finite and unique")
    if model not in _MODELS:
        raise ValueError("model must be spherical, exponential, gaussian or matern")
    nu=float(nu)
    if not isfinite(nu) or nu<=0:
        raise ValueError("nu must be finite and positive")
    variance = float(np.var(z))
    if not isfinite(variance) or variance <= 0:
        raise ValueError("values must have positive finite variance")
    anisotropy_ratio=float(anisotropy_ratio)
    if not isfinite(anisotropy_ratio) or not 0.0 < anisotropy_ratio <= 1.0:
        raise ValueError("anisotropy_ratio must be finite and in (0, 1]")
    azimuth=float(anisotropy_azimuth_deg)
    if not isfinite(azimuth):
        raise ValueError("anisotropy_azimuth_deg must be finite")
    if not isinstance(fit_anisotropy, bool):
        raise ValueError("fit_anisotropy must be boolean")
    delta = xy[:, None, :] - xy[None, :, :]
    def transformed_distances(axis_azimuth, axis_ratio):
        angle = radians(float(axis_azimuth) % 180.0)
        along = delta[:, :, 0] * sin(angle) + delta[:, :, 1] * cos(angle)
        across = delta[:, :, 0] * cos(angle) - delta[:, :, 1] * sin(angle)
        return np.hypot(along, across / float(axis_ratio))
    distances = transformed_distances(azimuth, anisotropy_ratio)
    positive = distances[distances > 0]
    dmin, dmax = float(np.min(positive)), float(np.max(positive))
    lower_range, upper_range = dmin * 1e-3, dmax * 1e3
    lower_var, upper_var = variance * 1e-8, variance * 100.0
    if initial is None:
        start = np.array([variance * 0.1, variance * 0.9, np.median(positive)])
    else:
        try:
            if len(initial) != 3:
                raise ValueError("initial must be (nugget, partial_sill, range)")
        except TypeError as exc:
            raise ValueError("initial must be (nugget, partial_sill, range)") from exc
        start = np.asarray(initial, dtype=float)
        if not np.isfinite(start).all() or np.any(start <= 0):
            raise ValueError("initial parameters must be finite and positive")
    start = np.clip(start, [lower_var, lower_var, lower_range],
                    [upper_var, upper_var, upper_range])
    ones = np.ones(len(z))
    constant = (len(z) - 1) * np.log(2.0 * np.pi)

    def objective(parameters):
        nugget, sill, range_ = np.exp(parameters[:3])
        if fit_anisotropy and len(parameters) >= 5:
            candidate_azimuth = float(parameters[3])
            candidate_ratio = float(np.exp(parameters[4]))
            candidate_distances = transformed_distances(candidate_azimuth, candidate_ratio)
        else:
            candidate_azimuth, candidate_ratio = azimuth, anisotropy_ratio
            candidate_distances = distances
        ratio = candidate_distances / range_
        covariance = sill * _correlation(ratio, model, nu)
        covariance.flat[::len(z) + 1] += nugget + sill * 0.0
        try:
            chol = np.linalg.cholesky(covariance)
            logdet = 2.0 * np.log(np.diag(chol)).sum()
            inv_one = np.linalg.solve(chol.T, np.linalg.solve(chol, ones))
            inv_z = np.linalg.solve(chol.T, np.linalg.solve(chol, z))
            denominator = float(ones @ inv_one)
            if not isfinite(denominator) or denominator <= 0:
                return np.inf
            mean = float(ones @ inv_z) / denominator
            residual = z - mean
            inv_residual = np.linalg.solve(chol.T, np.linalg.solve(chol, residual))
            logdet_mean = np.log(denominator)
            value = 0.5 * (logdet + logdet_mean + float(residual @ inv_residual) + constant)
            return float(value) if isfinite(value) else np.inf
        except (np.linalg.LinAlgError, FloatingPointError, ValueError):
            return np.inf

    bounds = [(np.log(lower_var), np.log(upper_var)),
              (np.log(lower_var), np.log(upper_var)),
              (np.log(lower_range), np.log(upper_range))]
    fixed_result = minimize(objective, np.log(start), method="L-BFGS-B", bounds=bounds)
    result = fixed_result
    if fit_anisotropy:
        bounds.extend([(0.0, 180.0), (np.log(0.1), 0.0)])
        x0 = np.concatenate([fixed_result.x, [azimuth % 180.0, np.log(anisotropy_ratio)]])
        result = minimize(objective, x0, method="L-BFGS-B", bounds=bounds)
    nugget, sill, range_ = np.exp(result.x[:3])
    if fit_anisotropy:
        azimuth = float(result.x[3] % 180.0)
        anisotropy_ratio = float(np.exp(result.x[4]))
    distances = transformed_distances(azimuth, anisotropy_ratio)
    if not np.isfinite(result.x).all() or not isfinite(float(result.fun)):
        raise ValueError("REML optimization failed to find a finite covariance model")
    ratio = distances / range_
    covariance = sill * _correlation(ratio, model, nu)
    covariance.flat[::len(z) + 1] += nugget
    chol = np.linalg.cholesky(covariance)
    inv_one = np.linalg.solve(chol.T, np.linalg.solve(chol, ones))
    inv_z = np.linalg.solve(chol.T, np.linalg.solve(chol, z))
    fitted_mean = float(ones @ inv_z) / float(ones @ inv_one)
    return {
        "model": model, "nu": nu, "anisotropy_azimuth_deg": azimuth % 180.0, "anisotropy_ratio": anisotropy_ratio, "anisotropy_fitted": fit_anisotropy, "nugget": float(nugget),
        "partial_sill": float(sill), "sill": float(nugget + sill),
        "range": float(range_), "reml_objective": float(result.fun),
        "success": bool(result.success), "message": str(result.message),
        "observations": int(len(z)), "mean": fitted_mean
    }
