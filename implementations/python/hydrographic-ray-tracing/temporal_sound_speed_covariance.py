"""Temporally correlated uncertainty for layered sound-speed profiles."""
from __future__ import annotations

import math
from collections.abc import Sequence


def _symmetric_psd_matrix(value, name):
    try:
        matrix = [[float(item) for item in row] for row in value]
    except (TypeError, ValueError):
        raise ValueError(f"{name} must be a finite numeric square matrix") from None
    if not matrix or any(len(row) != len(matrix) for row in matrix):
        raise ValueError(f"{name} must be a non-empty square matrix")
    if any(not math.isfinite(item) for row in matrix for item in row):
        raise ValueError(f"{name} must contain only finite values")
    scale = max(1.0, max(abs(item) for row in matrix for item in row))
    if any(
        abs(matrix[i][j] - matrix[j][i]) > 1e-10 * scale
        for i in range(len(matrix)) for j in range(i)
    ):
        raise ValueError(f"{name} must be symmetric")
    matrix = [
        [0.5 * (matrix[i][j] + matrix[j][i]) for j in range(len(matrix))]
        for i in range(len(matrix))
    ]
    if min(_jacobi_eigenvalues(matrix)) < -1e-10 * scale:
        raise ValueError(f"{name} must be positive semidefinite")
    return matrix


def _jacobi_eigenvalues(matrix):
    """Eigenvalues of a real symmetric matrix using Jacobi rotations."""
    a = [row[:] for row in matrix]
    n = len(a)
    for _ in range(max(1, 50 * n * n)):
        p, q, largest = 0, 0, 0.0
        for i in range(n):
            for j in range(i + 1, n):
                if abs(a[i][j]) > largest:
                    p, q, largest = i, j, abs(a[i][j])
        if largest <= 1e-12 * max(1.0, max(abs(a[i][i]) for i in range(n))):
            break
        tau = (a[q][q] - a[p][p]) / (2.0 * a[p][q])
        t = math.copysign(1.0, tau) / (
            abs(tau) + math.sqrt(1.0 + tau * tau)
        )
        c = 1.0 / math.sqrt(1.0 + t * t)
        s = t * c
        app, aqq, apq = a[p][p], a[q][q], a[p][q]
        a[p][p] = app - t * apq
        a[q][q] = aqq + t * apq
        a[p][q] = a[q][p] = 0.0
        for k in range(n):
            if k in (p, q):
                continue
            akp, akq = a[k][p], a[k][q]
            a[k][p] = a[p][k] = c * akp - s * akq
            a[k][q] = a[q][k] = s * akp + c * akq
    return [a[i][i] for i in range(n)]


def build_temporally_correlated_sound_speed_covariance(
    profile_epochs_s: Sequence[float],
    single_epoch_profile_covariance: Sequence[Sequence[float]],
    correlation_time_s: float,
) -> dict[str, object]:
    """Build a joint covariance for profile errors at multiple survey epochs.

    The single-epoch covariance describes the vertical cross-layer covariance
    at any one epoch. Temporal correlation follows a stationary exponential
    (Ornstein-Uhlenbeck) kernel exp(-|t_i-t_j| / tau). The full covariance is
    separable: C[(i,k),(j,l)] = R[i,j] * C_profile[k,l].

    State order is epoch-major: all layer sound-speed errors at epoch 1,
    followed by all layers at epoch 2, and so on. Epoch order is preserved,
    including repeated epochs. The model represents correlated profile
    anomalies, not a time-evolving mean profile or a physical ocean forecast.
    """
    try:
        epochs = [float(value) for value in profile_epochs_s]
        correlation_time = float(correlation_time_s)
    except (TypeError, ValueError):
        raise ValueError("epochs and correlation time must be numeric") from None
    if not epochs or not all(math.isfinite(value) for value in epochs):
        raise ValueError("profile_epochs_s must contain finite epochs")
    if not math.isfinite(correlation_time) or correlation_time <= 0.0:
        raise ValueError("correlation_time_s must be finite and positive")

    profile_covariance = _symmetric_psd_matrix(
        single_epoch_profile_covariance, "single_epoch_profile_covariance"
    )
    epoch_count = len(epochs)
    layer_count = len(profile_covariance)
    temporal_correlation = [
        [
            math.exp(-abs(epochs[i] - epochs[j]) / correlation_time)
            for j in range(epoch_count)
        ]
        for i in range(epoch_count)
    ]
    joint = [
        [
            temporal_correlation[i][j] * profile_covariance[k][ell]
            for j in range(epoch_count)
            for ell in range(layer_count)
        ]
        for i in range(epoch_count)
        for k in range(layer_count)
    ]
    return {
        "joint_profile_covariance": joint,
        "temporal_correlation": temporal_correlation,
        "profile_epochs_s": epochs,
        "correlation_time_s": correlation_time,
        "layer_count": layer_count,
        "state_order": "epoch-major: [layer sound-speed errors at each supplied epoch]",
        "temporal_model": "stationary exponential / Ornstein-Uhlenbeck correlation",
        "covariance_model": "C[(i,k),(j,l)] = exp(-abs(t_i-t_j)/tau) * C_profile[k,l]",
    }
