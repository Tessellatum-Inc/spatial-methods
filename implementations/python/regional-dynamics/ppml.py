"""Poisson pseudo-maximum-likelihood regression for nonnegative outcomes."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np

@dataclass
class PPMLResult:
    coefficients: np.ndarray
    covariance: np.ndarray
    standard_errors: np.ndarray
    fitted_mean: np.ndarray
    converged: bool
    iterations: int
    log_pseudolikelihood: float

def _loglike(y, eta):
    if np.max(eta) > 700: return -np.inf
    return float(np.sum(y * eta - np.exp(eta)))

def ppml(y, x, *, offset=None, max_iter=200, tol=1e-9):
    """Fit E[y|x]=exp(offset+x@beta) using Newton/IRLS scoring and HC0 covariance.

    x must include an intercept if desired. Zero outcomes are allowed. This
    cross-sectional baseline does not absorb fixed effects or cluster errors.
    """
    y, x = np.asarray(y, float), np.asarray(x, float)
    if y.ndim != 1 or x.ndim != 2 or x.shape[0] != y.size or y.size == 0 or x.shape[1] == 0:
        raise ValueError("y must be (n,) and x must be (n,p) with matching n")
    if not np.all(np.isfinite(y)) or not np.all(np.isfinite(x)) or np.any(y < 0):
        raise ValueError("y and x must be finite and y nonnegative")
    if np.linalg.matrix_rank(x) < x.shape[1]: raise ValueError("x must have full column rank")
    if not isinstance(max_iter, int) or max_iter < 1 or tol <= 0: raise ValueError("invalid iteration controls")
    off = np.zeros_like(y) if offset is None else np.asarray(offset, float)
    if off.shape != y.shape or not np.all(np.isfinite(off)): raise ValueError("invalid offset")
    beta = np.zeros(x.shape[1]); eta = off + x @ beta; ll = _loglike(y, eta); converged = False
    for iteration in range(1, max_iter + 1):
        mu = np.exp(np.clip(eta, -700, 700))
        h = x.T @ (mu[:, None] * x); score = x.T @ (y - mu)
        try: step = np.linalg.solve(h, score)
        except np.linalg.LinAlgError as exc: raise ValueError("singular information matrix") from exc
        scale = 1.0; accepted = False
        while scale >= 2.0**-30:
            candidate = beta + scale * step; candidate_eta = off + x @ candidate
            candidate_ll = _loglike(y, candidate_eta)
            if candidate_ll >= ll - 1e-12: accepted = True; break
            scale *= 0.5
        if not accepted:
            if np.linalg.norm(score, np.inf) <= tol * (1 + np.sum(y)): converged = True; break
            raise ValueError("step halving failed; possible separation or poor scaling")
        delta = candidate - beta; beta, eta, ll = candidate, candidate_eta, candidate_ll
        if np.linalg.norm(delta, np.inf) <= tol * (1 + np.linalg.norm(beta, np.inf)): converged = True; break
    mu = np.exp(np.clip(eta, -700, 700))
    bread = np.linalg.inv(x.T @ (mu[:, None] * x)); residual = y - mu
    meat = x.T @ ((residual**2)[:, None] * x)
    cov = bread @ meat @ bread; cov = (cov + cov.T) / 2
    se = np.sqrt(np.maximum(np.diag(cov), 0))
    return PPMLResult(beta, cov, se, mu, converged, iteration, ll)