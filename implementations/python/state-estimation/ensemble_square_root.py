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
