"""Systematic-scan Gibbs sampler for a proper Gaussian CAR latent field."""
from __future__ import annotations
import numpy as np


def car_gibbs(adjacency, observations, observation_variance, *, rho=0.0,
              precision=1.0, mean=0.0, n_samples=1000, burn_in=1000,
              thin=1, initial=None, seed=None):
    """Sample a proper CAR latent field with independent Gaussian observations.

    Prior precision is Q = precision * (D - rho W), where W is symmetric
    nonnegative adjacency and D contains row sums. Observations follow
    y_i | x_i ~ Normal(x_i, observation_variance_i); NaN observations are
    treated as missing. Hyperparameters are fixed, not estimated.
    """
    w=np.asarray(adjacency,dtype=float)
    y=np.asarray(observations,dtype=float)
    var=np.asarray(observation_variance,dtype=float)
    if w.ndim!=2 or w.shape[0]!=w.shape[1] or w.shape[0]==0: raise ValueError("adjacency must be a non-empty square matrix")
    n=w.shape[0]
    if y.shape!=(n,) or var.shape!=(n,): raise ValueError("observations and variances must match adjacency")
    if not np.isfinite(w).all() or np.any(w<0) or np.any(np.diag(w)!=0): raise ValueError("adjacency must be finite, nonnegative and have zero diagonal")
    if not np.allclose(w,w.T,rtol=0,atol=1e-12): raise ValueError("adjacency must be symmetric")
    degree=w.sum(axis=1)
    if np.any(degree<=0): raise ValueError("every node must have positive degree")
    if not np.isfinite(rho) or not np.isfinite(precision) or precision<=0 or not np.isfinite(mean):
        raise ValueError("rho and mean must be finite and precision finite positive")
    q=precision*(np.diag(degree)-rho*w)
    try: np.linalg.cholesky(q)
    except np.linalg.LinAlgError as exc: raise ValueError("CAR prior precision is not positive definite for this rho") from exc
    observed=np.isfinite(y)
    if np.any(observed & (~np.isfinite(var) | (var<=0))): raise ValueError("observed cells need finite positive observation variances")
    obs_precision=np.zeros(n);obs_precision[observed]=1.0/var[observed]
    if not isinstance(n_samples,int) or n_samples<1 or not isinstance(burn_in,int) or burn_in<0 or not isinstance(thin,int) or thin<1:
        raise ValueError("n_samples and thin must be positive integers; burn_in must be nonnegative")
    state=np.full(n,float(mean)) if initial is None else np.asarray(initial,dtype=float).copy()
    if state.shape!=(n,) or not np.isfinite(state).all(): raise ValueError("initial state must be a finite vector matching nodes")
    rng=np.random.default_rng(seed)
    out=np.empty((n_samples,n),dtype=float)
    total=burn_in+n_samples*thin
    for sweep in range(total):
        for i in range(n):
            conditional_precision=precision*degree[i]+obs_precision[i]
            neighbor_term=float(w[i]@(state-mean))
            numerator=precision*degree[i]*mean+precision*rho*neighbor_term
            if observed[i]: numerator+=obs_precision[i]*y[i]
            conditional_mean=numerator/conditional_precision
            state[i]=rng.normal(conditional_mean,1.0/np.sqrt(conditional_precision))
        if sweep>=burn_in and (sweep-burn_in+1)%thin==0:
            out[(sweep-burn_in)//thin]=state
    return out
