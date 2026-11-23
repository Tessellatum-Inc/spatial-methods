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


def _transpose(matrix):
    return [list(column) for column in zip(*matrix)]


def _multiply(left, right):
    if not left or not right or len(left[0]) != len(right):
        raise ValueError("matrix dimensions are incompatible")
    return [
        [
            sum(left[i][k] * right[k][j] for k in range(len(right)))
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def _cholesky_solve(matrix, right_hand_side):
    """Solve A X = B for symmetric positive-definite A without inversion."""
    n = len(matrix)
    if n == 0 or len(right_hand_side) != n:
        raise ValueError("linear-system dimensions are incompatible")
    width = len(right_hand_side[0])
    if width == 0 or any(len(row) != width for row in right_hand_side):
        raise ValueError("right-hand side must be a non-empty rectangular matrix")
    lower = [[0.0] * n for _ in range(n)]
    scale = max(1.0, max(abs(value) for row in matrix for value in row))
    for i in range(n):
        for j in range(i + 1):
            residual = matrix[i][j] - sum(
                lower[i][k] * lower[j][k] for k in range(j)
            )
            if i == j:
                if residual <= 1e-14 * scale:
                    raise ValueError(
                        "observation temporal covariance is not numerically positive definite"
                    )
                lower[i][j] = math.sqrt(residual)
            else:
                lower[i][j] = residual / lower[j][j]

    forward = [[0.0] * width for _ in range(n)]
    for i in range(n):
        for col in range(width):
            forward[i][col] = (
                right_hand_side[i][col]
                - sum(lower[i][k] * forward[k][col] for k in range(i))
            ) / lower[i][i]

    solution = [[0.0] * width for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for col in range(width):
            solution[i][col] = (
                forward[i][col]
                - sum(lower[k][i] * solution[k][col] for k in range(i + 1, n))
            ) / lower[i][i]
    return solution


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

    The returned operator H maps the flattened observation profile vector to
    query profiles; the propagated covariance is H C_observed H.T. This
    deterministic interpolation does not model unresolved variability.
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
        raise ValueError("joint_profile_covariance dimension must equal epoch_count * layer_count")

    operator = []
    interpolated = []
    for query in queries:
        upper = next((i for i, epoch in enumerate(epochs) if epoch >= query), None)
        if upper is None:
            raise ValueError("query epochs must lie within the observed epoch range")
        if epochs[upper] == query:
            lower, fraction = upper, 0.0
        else:
            lower = upper - 1
            fraction = (query - epochs[lower]) / (epochs[upper] - epochs[lower])
        weights = [0.0] * len(epochs)
        weights[lower] = 1.0 - fraction
        weights[upper] += fraction
        interpolated.append([
            sum(weights[e] * profiles[e][layer] for e in range(len(epochs)))
            for layer in range(layer_count)
        ])
        for layer in range(layer_count):
            row = [0.0] * state_width
            for epoch in range(len(epochs)):
                row[epoch * layer_count + layer] = weights[epoch]
            operator.append(row)

    propagated = _multiply(
        _multiply(operator, observed_covariance), _transpose(operator)
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
        "limitation": "Does not model unresolved variability between observation epochs.",
    }


def condition_temporal_sound_speed_profiles_ou(
    profile_epochs_s: Sequence[float],
    observed_profiles_mps: Sequence[Sequence[float]],
    query_epochs_s: Sequence[float],
    single_epoch_profile_covariance: Sequence[Sequence[float]],
    correlation_time_s: float,
    reference_profile_mps: Sequence[float],
) -> dict[str, object]:
    """Condition a separable OU profile process on noiseless observed profiles.

    The reference profile is the assumed temporal mean/trend. Profile
    anomalies have covariance R(t_i,t_j) * C_profile, where R is the
    stationary exponential kernel. Observation epochs must be distinct and
    strictly increasing. Query epochs may repeat and need not lie inside the
    observation interval; extrapolation is a model prediction, not linear
    interpolation.

    Observations are treated as exact process values. Measurement noise must
    not be folded into C_profile; a future noisy-observation model would add
    an explicit observation-noise covariance to R_oo tensor C_profile.
    """
    try:
        epochs = [float(value) for value in profile_epochs_s]
        queries = [float(value) for value in query_epochs_s]
        profiles = [[float(value) for value in row] for row in observed_profiles_mps]
        reference = [float(value) for value in reference_profile_mps]
        tau = float(correlation_time_s)
    except (TypeError, ValueError):
        raise ValueError("epochs, profiles, reference profile and correlation time must be numeric") from None
    if not epochs or not all(math.isfinite(value) for value in epochs):
        raise ValueError("profile_epochs_s must contain finite epochs")
    if any(epochs[i + 1] <= epochs[i] for i in range(len(epochs) - 1)):
        raise ValueError("profile_epochs_s must be strictly increasing")
    if not queries or not all(math.isfinite(value) for value in queries):
        raise ValueError("query_epochs_s must contain finite epochs")
    if not math.isfinite(tau) or tau <= 0.0:
        raise ValueError("correlation_time_s must be finite and positive")
    if len(profiles) != len(epochs) or any(not row for row in profiles):
        raise ValueError("one non-empty observed profile is required per epoch")
    layer_count = len(profiles[0])
    if len(reference) != layer_count or any(len(row) != layer_count for row in profiles):
        raise ValueError("observed and reference profiles must have the same layer count")
    if any(not math.isfinite(value) for row in profiles for value in row) or not all(
        math.isfinite(value) for value in reference
    ):
        raise ValueError("observed and reference profile values must be finite")
    profile_covariance = _symmetric_psd_matrix(
        single_epoch_profile_covariance, "single_epoch_profile_covariance"
    )
    if len(profile_covariance) != layer_count:
        raise ValueError("single_epoch_profile_covariance dimension must equal layer_count")

    temporal_oo = [
        [math.exp(-abs(a - b) / tau) for b in epochs] for a in epochs
    ]
    temporal_qo = [
        [math.exp(-abs(query - epoch) / tau) for epoch in epochs]
        for query in queries
    ]
    temporal_qq = [
        [math.exp(-abs(a - b) / tau) for b in queries] for a in queries
    ]
    # Solve R_oo X = R_oq; transpose X to obtain W = R_qo R_oo^-1.
    solved = _cholesky_solve(temporal_oo, _transpose(temporal_qo))
    weights = _transpose(solved)
    residual_temporal = [
        [
            temporal_qq[i][j] - sum(
                weights[i][k] * temporal_qo[j][k] for k in range(len(epochs))
            )
            for j in range(len(queries))
        ]
        for i in range(len(queries))
    ]
    residual_temporal = [
        [
            0.5 * (residual_temporal[i][j] + residual_temporal[j][i])
            for j in range(len(queries))
        ]
        for i in range(len(queries))
    ]
    temporal_scale = max(1.0, max(abs(v) for row in temporal_qq for v in row))
    for i in range(len(queries)):
        for j in range(len(queries)):
            if abs(residual_temporal[i][j]) <= 1e-12 * temporal_scale:
                residual_temporal[i][j] = 0.0
    if min(_jacobi_eigenvalues(residual_temporal)) < -1e-9 * temporal_scale:
        raise ArithmeticError("conditional temporal covariance lost positive semidefiniteness")

    conditional_profiles = []
    for query_index in range(len(queries)):
        conditional_profiles.append([
            reference[layer] + sum(
                weights[query_index][epoch] *
                (profiles[epoch][layer] - reference[layer])
                for epoch in range(len(epochs))
            )
            for layer in range(layer_count)
        ])

    profile_operator = []
    for query_index in range(len(queries)):
        for layer in range(layer_count):
            row = [0.0] * (len(epochs) * layer_count)
            for epoch in range(len(epochs)):
                row[epoch * layer_count + layer] = weights[query_index][epoch]
            profile_operator.append(row)

    conditional_covariance = [
        [
            residual_temporal[i][j] * profile_covariance[k][ell]
            for j in range(len(queries))
            for ell in range(layer_count)
        ]
        for i in range(len(queries))
        for k in range(layer_count)
    ]
    return {
        "query_epochs_s": queries,
        "conditional_profiles_mps": conditional_profiles,
        "temporal_conditioning_weights": weights,
        "profile_conditioning_operator": profile_operator,
        "conditional_temporal_covariance": residual_temporal,
        "conditional_joint_profile_covariance": conditional_covariance,
        "source_profile_epochs_s": epochs,
        "reference_profile_mps": reference,
        "single_epoch_profile_covariance": profile_covariance,
        "correlation_time_s": tau,
        "layer_count": layer_count,
        "state_order": "query-epoch-major: [layer sound-speed anomalies at each query epoch]",
        "source_state_order": "observation-epoch-major: [layer sound-speed anomalies at each observation epoch]",
        "mean_model": "c_query = c_reference + (W tensor I_layer) (c_observed - c_reference)",
        "covariance_model": "C_query|observed = (R_qq - W R_oq) tensor C_profile",
        "temporal_model": "stationary exponential / Ornstein-Uhlenbeck covariance",
        "observation_model": "noiseless observations of the latent profile process",
        "limitation": (
            "A stationary separable temporal model with one correlation time and a supplied "
            "reference mean profile; it does not model advection, horizontal variability, "
            "currents, evolving mean structure, or measurement noise."
        ),
    }
