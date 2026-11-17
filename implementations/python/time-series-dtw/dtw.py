"""DTW and time-weighted DTW for multivariate sequences."""
import numpy as np


def _series(value, name):
    arr = np.asarray(value, dtype=float)
    if arr.ndim == 1:
        arr = arr[:, None]
    if arr.ndim != 2 or not arr.shape[0] or not arr.shape[1]:
        raise ValueError(f"{name} must be a non-empty 1D or 2D sequence")
    if not np.isfinite(arr).all():
        raise ValueError(f"{name} must contain only finite values")
    return arr


def _window(n, m, window):
    if window is None:
        return max(n, m)
    if isinstance(window, bool) or not isinstance(window, (int, np.integer)) or window < abs(n-m):
        raise ValueError("window must be an integer >= abs(len(a)-len(b))")
    return int(window)


def _align(x, y, local_cost, window, return_path):
    n, m = len(x), len(y)
    w = _window(n, m, window)
    costs = np.full((n+1, m+1), np.inf)
    costs[0, 0] = 0.0
    parent = np.full((n+1, m+1), -1, dtype=np.int8)
    for i in range(1, n+1):
        for j in range(max(1, i-w), min(m, i+w)+1):
            prev = (costs[i-1,j-1], costs[i-1,j], costs[i,j-1])
            move = int(np.argmin(prev))
            costs[i,j] = local_cost(i-1,j-1) + prev[move]
            parent[i,j] = move
    score = float(costs[n,m])
    if not return_path:
        return score
    if not np.isfinite(score):
        return score, []
    path, i, j = [], n, m
    while i and j:
        path.append((i-1,j-1))
        move = int(parent[i,j])
        if move == 0:
            i, j = i-1, j-1
        elif move == 1:
            i -= 1
        elif move == 2:
            j -= 1
        else:
            raise RuntimeError("invalid DTW predecessor")
    path.reverse()
    return score, path


def dtw(a, b, window=None, return_path=False):
    """Accumulated Euclidean DTW cost; optional Sakoe-Chiba index window."""
    x, y = _series(a, "a"), _series(b, "b")
    if x.shape[1] != y.shape[1]:
        raise ValueError("sequences must have the same feature count")
    return _align(x, y, lambda i,j: float(np.linalg.norm(x[i]-y[j])), window, return_path)


def time_weighted_dtw(a, b, times_a, times_b, alpha=0.1, beta=1.0,
                      window=None, return_path=False):
    """DTW with additive logistic penalty on temporal separation.

    Penalty: 1 / (1 + exp(-alpha * (abs(t-u) - beta))).
    Timestamps must share a numeric unit and be non-decreasing.
    """
    x, y = _series(a, "a"), _series(b, "b")
    if x.shape[1] != y.shape[1]:
        raise ValueError("sequences must have the same feature count")
    tx, ty = np.asarray(times_a, dtype=float), np.asarray(times_b, dtype=float)
    if tx.shape != (len(x),) or ty.shape != (len(y),):
        raise ValueError("timestamp arrays must match sequence lengths")
    if not np.isfinite(tx).all() or not np.isfinite(ty).all():
        raise ValueError("timestamps must be finite")
    if np.any(np.diff(tx)<0) or np.any(np.diff(ty)<0):
        raise ValueError("timestamps must be non-decreasing")
    if not np.isfinite(alpha) or alpha <= 0 or not np.isfinite(beta):
        raise ValueError("alpha must be positive and beta finite")

    def local(i, j):
        z = np.clip(alpha * (abs(tx[i]-ty[j])-beta), -700.0, 700.0)
        penalty = 1.0 / (1.0 + np.exp(-z))
        return float(np.linalg.norm(x[i]-y[j])) + penalty

    return _align(x, y, local, window, return_path)
