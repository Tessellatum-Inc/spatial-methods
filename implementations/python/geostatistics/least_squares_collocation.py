"""Linear least-squares collocation with an unknown fixed trend."""
from __future__ import annotations
import numpy as np


def least_squares_collocation(observations, design, signal_covariance,
                              noise_covariance, cross_covariance,
                              target_signal_covariance, target_design=None):
    """Estimate a fixed trend and predict a correlated signal at target sites.

    Observation model: y = H beta + s + e, with independent signal/noise,
    Cov(s)=C, Cov(e)=R. The supplied cross covariance is Cov(s_target,s_obs).
    The result is the universal-kriging/LSC predictor for the signal plus
    fixed trend. Covariance matrices and cross-covariance must describe one
    mutually consistent stochastic model.
    """
    y=np.asarray(observations,dtype=float)
    H=np.asarray(design,dtype=float)
    C=np.asarray(signal_covariance,dtype=float)
    R=np.asarray(noise_covariance,dtype=float)
    C0=np.asarray(cross_covariance,dtype=float)
    C00=np.asarray(target_signal_covariance,dtype=float)
    if y.ndim!=1 or H.ndim!=2 or H.shape[0]!=y.size:
        raise ValueError("observations and design dimensions do not match")
    m,p=H.shape
    if m<=p or p<1 or np.linalg.matrix_rank(H)<p:
        raise ValueError("design must have full column rank and positive residual degrees of freedom")
    if C.shape!=(m,m) or R.shape!=(m,m) or not np.all(np.isfinite(y)) or not np.all(np.isfinite(H)):
        raise ValueError("observation covariance matrices must be m by m and inputs finite")
    if not np.all(np.isfinite(C)) or not np.all(np.isfinite(R)):
        raise ValueError("covariance matrices must be finite")
    if not np.allclose(C,C.T,atol=1e-10) or not np.allclose(R,R.T,atol=1e-10):
        raise ValueError("signal and noise covariance matrices must be symmetric")
    for name, matrix in (("signal_covariance",C),("noise_covariance",R)):
        scale=max(1.0,float(np.max(np.abs(matrix))))
        if np.min(np.linalg.eigvalsh(matrix)) < -1e-10*scale:
            raise ValueError(f"{name} must be positive semidefinite")
    S=C+R
    try: np.linalg.cholesky(S)
    except np.linalg.LinAlgError as exc: raise ValueError("combined observation covariance must be positive definite") from exc
    if C0.ndim!=2 or C0.shape[1]!=m or not np.all(np.isfinite(C0)):
        raise ValueError("cross_covariance must have shape (n_targets, n_observations)")
    q=C0.shape[0]
    if C00.shape!=(q,q) or not np.all(np.isfinite(C00)) or not np.allclose(C00,C00.T,atol=1e-10):
        raise ValueError("target_signal_covariance must be finite, symmetric and n_targets by n_targets")
    if np.min(np.linalg.eigvalsh(C00)) < -1e-10*max(1.0,float(np.max(np.abs(C00)))):
        raise ValueError("target_signal_covariance must be positive semidefinite")
    H0=np.ones((q,p)) if target_design is None and p==1 else np.asarray(target_design,dtype=float) if target_design is not None else None
    if H0 is None or H0.shape!=(q,p) or not np.all(np.isfinite(H0)):
        raise ValueError("target_design is required and must have shape (n_targets, n_parameters)")
    SinvH=np.linalg.solve(S,H); Sinvy=np.linalg.solve(S,y)
    normal=H.T@SinvH
    try: Qbeta=np.linalg.inv(normal)
    except np.linalg.LinAlgError as exc: raise ValueError("generalized least-squares normal matrix is singular") from exc
    beta=Qbeta@(H.T@Sinvy)
    residual=y-H@beta
    SinvC0T=np.linalg.solve(S,C0.T)
    SinvResidual=np.linalg.solve(S,residual)
    signal_prediction=C0@SinvResidual
    prediction=H0@beta+signal_prediction
    B=H0-C0@SinvH
    prediction_covariance=C00-C0@SinvC0T+B@Qbeta@B.T
    prediction_covariance=(prediction_covariance+prediction_covariance.T)/2
    if np.min(np.linalg.eigvalsh(prediction_covariance)) < -1e-8*max(1.0,float(np.max(np.abs(C00)))):
        raise ValueError("prediction covariance is not positive semidefinite; check covariance consistency")
    return {"trend_parameters":beta,"trend_parameter_covariance":Qbeta,
            "signal_prediction":signal_prediction,"prediction":prediction,
            "prediction_covariance":prediction_covariance,
            "prediction_standard_deviation":np.sqrt(np.maximum(0,np.diag(prediction_covariance))),
            "observation_residuals":residual}
