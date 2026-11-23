"""Deterministic ensemble-transform Kalman analysis for linear observations."""
from __future__ import annotations
import numpy as np


def etkf_analysis(ensemble, observations, observation_operator, observation_covariance):
    """Apply a batch ETKF analysis in ensemble space.

    Ensemble is (n_state, n_members), observations are (n_obs,), H is
    (n_obs, n_state), and R is the positive-definite observation-error
    covariance. The ensemble anomalies use the sample covariance convention
    A A.T/(N-1). A symmetric square-root transform updates all members
    deterministically without perturbing observations.
    """
    E=np.asarray(ensemble,dtype=float); y=np.asarray(observations,dtype=float)
    H=np.asarray(observation_operator,dtype=float); R=np.asarray(observation_covariance,dtype=float)
    if E.ndim!=2 or E.shape[0]<1 or E.shape[1]<3 or not np.all(np.isfinite(E)):
        raise ValueError("ensemble must be a finite (n_state, n_members) matrix with at least 3 members")
    n,N=E.shape
    if y.ndim!=1 or H.ndim!=2 or H.shape!=(y.size,n) or y.size<1:
        raise ValueError("observations and observation operator dimensions do not match ensemble")
    m=y.size
    if not np.all(np.isfinite(y)) or not np.all(np.isfinite(H)):
        raise ValueError("observations and observation operator must be finite")
    if R.shape!=(m,m) or not np.all(np.isfinite(R)) or not np.allclose(R,R.T,atol=1e-10):
        raise ValueError("observation covariance must be finite, symmetric and m by m")
    try: np.linalg.cholesky(R)
    except np.linalg.LinAlgError as exc: raise ValueError("observation covariance must be positive definite") from exc
    mean=E.mean(axis=1); A=E-mean[:,None]
    Y=H@A; innovation=y-H@mean
    RinvY=np.linalg.solve(R,Y); RinvInnovation=np.linalg.solve(R,innovation)
    C=(N-1)*np.eye(N)+Y.T@RinvY
    C=(C+C.T)/2
    eigvals,eigvecs=np.linalg.eigh(C)
    if np.any(eigvals<=0): raise ValueError("ensemble-space analysis matrix is not positive definite")
    weights=eigvecs@((eigvecs.T@(Y.T@RinvInnovation))/eigvals)
    analysis_mean=mean+A@weights
    transform=(eigvecs*(np.sqrt((N-1)/eigvals)))@eigvecs.T
    analysis_anomalies=A@transform
    analysis=analysis_mean[:,None]+analysis_anomalies
    analysis_cov=analysis_anomalies@analysis_anomalies.T/(N-1)
    return {"analysis_ensemble":analysis,"analysis_mean":analysis_mean,
            "analysis_covariance":analysis_cov,"analysis_anomalies":analysis_anomalies,
            "forecast_mean":mean,"forecast_covariance":A@A.T/(N-1),
            "innovation":innovation,"ensemble_weights":weights,
            "ensemble_transform":transform}



def enkf_analysis(ensemble, observations, observation_operator, observation_covariance, *, seed=0):
    """Stochastic EnKF analysis with independently perturbed observations."""
    from numbers import Integral
    E=np.asarray(ensemble,dtype=float)
    y=np.asarray(observations,dtype=float)
    H=np.asarray(observation_operator,dtype=float)
    R=np.asarray(observation_covariance,dtype=float)
    if E.ndim!=2 or E.shape[0]<1 or E.shape[1]<2 or not np.isfinite(E).all():
        raise ValueError("ensemble must be a finite (n_state, n_members) matrix with at least 2 members")
    n,N=E.shape
    if y.ndim!=1 or y.size<1 or H.shape!=(y.size,n):
        raise ValueError("observations and observation operator dimensions do not match ensemble")
    m=y.size
    if not np.isfinite(y).all() or not np.isfinite(H).all():
        raise ValueError("observations and observation operator must be finite")
    if R.shape!=(m,m) or not np.isfinite(R).all() or not np.allclose(R,R.T,atol=1e-10):
        raise ValueError("observation covariance must be finite, symmetric and m by m")
    try:
        chol=np.linalg.cholesky(R)
    except np.linalg.LinAlgError as exc:
        raise ValueError("observation covariance must be positive definite") from exc
    if isinstance(seed,bool) or (seed is not None and not isinstance(seed,Integral)):
        raise ValueError("seed must be an integer or None")
    mean=E.mean(axis=1)
    anomalies=E-mean[:,None]
    predicted=H@E
    predicted_mean=predicted.mean(axis=1)
    predicted_anomalies=predicted-predicted_mean[:,None]
    denominator=N-1
    cross_covariance=anomalies@predicted_anomalies.T/denominator
    observation_sample_covariance=predicted_anomalies@predicted_anomalies.T/denominator
    innovation_covariance=observation_sample_covariance+R
    try:
        gain=np.linalg.solve(innovation_covariance,cross_covariance.T).T
    except np.linalg.LinAlgError as exc:
        raise ValueError("innovation covariance is singular") from exc
    rng=np.random.default_rng(None if seed is None else int(seed))
    perturbations=chol@rng.standard_normal((m,N))
    analysis=E+gain@(y[:,None]+perturbations-predicted)
    analysis_mean=analysis.mean(axis=1)
    analysis_anomalies=analysis-analysis_mean[:,None]
    analysis_covariance=analysis_anomalies@analysis_anomalies.T/denominator
    return {
        "analysis_ensemble":analysis,"analysis_mean":analysis_mean,
        "analysis_covariance":analysis_covariance,"forecast_mean":mean,
        "forecast_covariance":anomalies@anomalies.T/denominator,
        "predicted_observation_mean":predicted_mean,"innovation":y-predicted_mean,
        "innovation_covariance":innovation_covariance,"gain":gain,
        "observation_perturbations":perturbations,
    }
