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



def interpolate_temporal_sound_speed_profiles(
    profile_epochs_s: Sequence[float],
    observed_profiles_mps: Sequence[Sequence[float]],
    query_epochs_s: Sequence[float],
    joint_profile_covariance: Sequence[Sequence[float]],
) -> dict[str, object]:
    """Linearly interpolate observed profiles and propagate their full covariance.

    Profile and covariance state order is epoch-major, then layer-major.
    Interpolation is restricted to the closed observation-time interval:
    extrapolation is rejected. The returned operator H maps the flattened
    observed profile vector to the flattened query profile vector, and the
    propagated covariance is exactly H C_observed H.T.

    This deterministic interpolation does not add a stochastic model for
    unresolved variability between observations.
    """
    try:
        epochs = [float(value) for value in profile_epochs_s]
        queries = [float(value) for value in query_epochs_s]
        profiles = [[float(value) for value in row] for row in observed_profiles_mps]
    except (TypeError, ValueError):
        raise ValueError("epochs, query epochs and profiles must be numeric") from None
    if not epochs or not all(math.isfinite(value) for value in epochs):
        raise ValueError("profile_epochs_s must contain finite epochs")
    if any(epochs[i + 1] <= epochs[i] for i in range(len(epochs) - 1)):
        raise ValueError("profile_epochs_s must be strictly increasing")
    if not queries or not all(math.isfinite(value) for value in queries):
        raise ValueError("query_epochs_s must contain finite epochs")
    if any(value < epochs[0] or value > epochs[-1] for value in queries):
        raise ValueError("query epochs must lie within the observed epoch range")
    if len(profiles) != len(epochs) or any(not row for row in profiles):
        raise ValueError("one non-empty observed profile is required per epoch")
    layer_count = len(profiles[0])
    if any(len(row) != layer_count for row in profiles):
        raise ValueError("all observed profiles must have the same layer count")
    if any(not math.isfinite(value) for row in profiles for value in row):
        raise ValueError("observed profiles must contain only finite values")

    observed_covariance = _symmetric_psd_matrix(
        joint_profile_covariance, "joint_profile_covariance"
    )
    state_width = len(epochs) * layer_count
    if len(observed_covariance) != state_width:
        raise ValueError(
            "joint_profile_covariance dimension must equal epoch_count * layer_count"
        )

    operator = []
    interpolated = []
    for query in queries:
        upper = next((i for i, epoch in enumerate(epochs) if epoch >= query), None)
        if upper is None:
            raise ValueError("query epochs must lie within the observed epoch range")
        if epochs[upper] == query:
            lower = upper
            fraction = 0.0
        else:
            lower = upper - 1
            fraction = (query - epochs[lower]) / (epochs[upper] - epochs[lower])
        weights = [0.0] * len(epochs)
        weights[lower] = 1.0 - fraction
        weights[upper] += fraction
        # Sum the epoch contributions for each layer.
        profile = [
            sum(weights[epoch] * profiles[epoch][layer]
                for epoch in range(len(epochs)))
            for layer in range(layer_count)
        ]
        interpolated.append(profile)
        for layer in range(layer_count):
            row = [0.0] * state_width
            for epoch in range(len(epochs)):
                row[epoch * layer_count + layer] = weights[epoch]
            operator.append(row)

    def multiply(left, right):
        return [
            [sum(left[i][k] * right[k][j] for k in range(len(right)))
             for j in range(len(right[0]))]
            for i in range(len(left))
        ]

    def transpose(matrix):
        return [list(column) for column in zip(*matrix)]

    propagated = multiply(
        multiply(operator, observed_covariance), transpose(operator)
    )
    return {
        "query_epochs_s": queries,
        "interpolated_profiles_mps": interpolated,
        "interpolation_operator": operator,
        "joint_profile_covariance": propagated,
        "source_joint_profile_covariance": observed_covariance,
        "source_profile_epochs_s": epochs,
        "layer_count": layer_count,
        "state_order": "query-epoch-major: [layer sound speeds at each query epoch]",
        "source_state_order": "observation-epoch-major: [layer sound speeds at each observation epoch]",
        "covariance_propagation": "C_query = H C_observed H^T",
        "interpolation_model": "piecewise-linear in time; no extrapolation",
        "limitation": (
            "Deterministic interpolation propagates supplied observation covariance "
            "but does not model unresolved variability between observation epochs."
        ),
    }
