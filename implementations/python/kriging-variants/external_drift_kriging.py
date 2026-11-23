"""External-drift kriging with caller-supplied covariates."""
from __future__ import annotations
import numpy as np
from kriging_variants import _MODELS, _covariance, _points


def external_drift_kriging_predict(points, values, targets, training_covariates,
                                   target_covariates, *, model="exponential",
                                   nugget=0.0, partial_sill=1.0, range_=1.0,
                                   observation_noise=0.0):
    """Universal-kriging block solve with an intercept and external covariates."""
    xy=_points(points,"points",minimum=1); target=_points(targets,"targets",minimum=1)
    z=np.asarray(values,dtype=float)
    if z.shape!=(len(xy),) or not np.isfinite(z).all():
        raise ValueError("values must be finite and match points")
    ext=np.asarray(training_covariates,dtype=float)
    ext_target=np.asarray(target_covariates,dtype=float)
    if ext.ndim!=2 or ext.shape[0]!=len(xy) or ext.shape[1]<1:
        raise ValueError("training_covariates must be an n-by-p matrix")
    if ext_target.shape!=(len(target),ext.shape[1]):
        raise ValueError("target_covariates shape must be (m, p)")
    if not np.isfinite(ext).all() or not np.isfinite(ext_target).all():
        raise ValueError("external covariates must be finite")
    if model not in _MODELS: raise ValueError("unsupported covariance model")
    try: nugget,sill,range_,noise=map(float,(nugget,partial_sill,range_,observation_noise))
    except (TypeError,ValueError) as exc: raise ValueError("covariance parameters must be scalar numbers") from exc
    if not np.isfinite([nugget,sill,range_,noise]).all() or nugget<0 or noise<0 or sill<=0 or range_<=0:
        raise ValueError("nugget/noise must be nonnegative and sill/range positive finite")
    design=np.column_stack((np.ones(len(xy)),ext))
    target_design=np.column_stack((np.ones(len(target)),ext_target))
    if np.linalg.matrix_rank(design)<design.shape[1]:
        raise ValueError("external drift design is rank deficient")
    dd=xy[:,None,:]-xy[None,:,:]
    td=xy[:,None,:]-target[None,:,:]
    data_dist=np.hypot(dd[:,:,0],dd[:,:,1])
    target_dist=np.hypot(td[:,:,0],td[:,:,1])
    covariance=_covariance(data_dist,model=model,partial_sill=sill,range_=range_)
    covariance.flat[::len(xy)+1]+=nugget+noise
    cross=_covariance(target_dist,model=model,partial_sill=sill,range_=range_)
    p=design.shape[1]
    system=np.block([[covariance,design],[design.T,np.zeros((p,p))]])
    rhs=np.vstack((cross,target_design.T))
    try: solution=np.linalg.solve(system,rhs)
    except np.linalg.LinAlgError as exc: raise ValueError("external-drift kriging system is singular") from exc
    weights=solution[:len(xy)]; multipliers=solution[len(xy):]
    prediction=weights.T@z
    variance=sill-np.sum(weights*cross,axis=0)-np.sum(multipliers*target_design.T,axis=0)
    tol=1e-9*max(1.,sill)
    if not np.isfinite(prediction).all() or not np.isfinite(variance).all():
        raise ValueError("external-drift solution is non-finite")
    if np.any(variance < -tol): raise ValueError("external-drift kriging variance is materially negative")
    return {"prediction":prediction,"variance":np.maximum(variance,0.),
            "weights":weights.T,"drift":"external","model":model,
            "observations":len(xy),"targets":len(target)}
