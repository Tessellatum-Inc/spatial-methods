"""State-space covariance for a clock with white frequency-rate noise.

The clock state is [time offset (s), fractional frequency/drift (s/s)].
The continuous-time model is d(offset)/dt = drift and
d(drift) = sqrt(q) dW, where q is the white frequency-rate noise
spectral density. The exact discrete-time process covariance is used.
"""
import math


def _finite_number(value, name):
    try:
        result = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{name} must be a finite number") from None
    if not math.isfinite(result):
        raise ValueError(f"{name} must be a finite number")
    return result


def _matrix_2x2(value, name):
    try:
        matrix = [[float(x) for x in row] for row in value]
    except (TypeError, ValueError):
        raise ValueError(f"{name} must be a finite 2x2 matrix") from None
    if len(matrix) != 2 or any(len(row) != 2 for row in matrix):
        raise ValueError(f"{name} must be a finite 2x2 matrix")
    if not all(math.isfinite(x) for row in matrix for x in row):
        raise ValueError(f"{name} must be a finite 2x2 matrix")
    scale = max(1.0, max(abs(x) for row in matrix for x in row))
    if abs(matrix[0][1] - matrix[1][0]) > 1e-12 * scale:
        raise ValueError(f"{name} must be symmetric")
    if matrix[0][0] < -1e-12 * scale or matrix[1][1] < -1e-12 * scale:
        raise ValueError(f"{name} must be positive semidefinite")
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] ** 2
    if determinant < -1e-12 * scale * scale:
        raise ValueError(f"{name} must be positive semidefinite")
    return matrix


def _transpose(matrix):
    return [list(column) for column in zip(*matrix)]


def _multiply(a, b):
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b)))
         for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def clock_state_transition(interval_s):
    """Exact transition for offset and constant drift over interval_s."""
    dt = _finite_number(interval_s, "interval_s")
    if dt < 0.0:
        raise ValueError("interval_s must be non-negative")
    return [[1.0, dt], [0.0, 1.0]]


def clock_process_noise_covariance(interval_s, spectral_density):
    """Exact Q for d(offset)=drift dt, d(drift)=sqrt(q) dW.

    q has units s^-1 when offset is measured in seconds and drift in s/s.
    """
    dt = _finite_number(interval_s, "interval_s")
    q = _finite_number(spectral_density, "spectral_density")
    if dt < 0.0 or q < 0.0:
        raise ValueError("interval_s and spectral_density must be non-negative")
    return [
        [q * dt ** 3 / 3.0, q * dt ** 2 / 2.0],
        [q * dt ** 2 / 2.0, q * dt],
    ]


def propagate_clock_state_covariance(epochs_s, initial_covariance,
                                     process_noise_spectral_density=0.0):
    """Return marginal, joint-state and clock-offset covariance at epochs.

    The initial state is defined at epochs_s[0]. For i <= j, the cross-time
    block is Cov(x_i,x_j) = P_i Phi(t_j-t_i)^T. This follows from the
    Markov model and independent process noise after epoch i.

    Result matrices use state order [clock offset, clock drift]. The
    offset_covariance is the N x N covariance of the offset component.
    """
    if not isinstance(epochs_s, (list, tuple)) or not epochs_s:
        raise ValueError("epochs_s must contain at least one epoch")
    epochs = [_finite_number(t, f"epochs_s[{i}]")
              for i, t in enumerate(epochs_s)]
    if any(epochs[i + 1] <= epochs[i] for i in range(len(epochs) - 1)):
        raise ValueError("epochs_s must be strictly increasing")
    p0 = _matrix_2x2(initial_covariance, "initial_covariance")
    q = _finite_number(process_noise_spectral_density,
                       "process_noise_spectral_density")
    if q < 0.0:
        raise ValueError("process_noise_spectral_density must be non-negative")

    marginals = [p0]
    for i in range(1, len(epochs)):
        dt = epochs[i] - epochs[i - 1]
        phi = clock_state_transition(dt)
        noise = clock_process_noise_covariance(dt, q)
        propagated = _multiply(_multiply(phi, marginals[-1]), _transpose(phi))
        marginals.append([
            [propagated[r][c] + noise[r][c] for c in range(2)]
            for r in range(2)
        ])

    count = len(epochs)
    joint = [[0.0] * (2 * count) for _ in range(2 * count)]
    for i in range(count):
        for j in range(i, count):
            phi = clock_state_transition(epochs[j] - epochs[i])
            block = _multiply(marginals[i], _transpose(phi))
            for r in range(2):
                for c in range(2):
                    joint[2 * i + r][2 * j + c] = block[r][c]
                    joint[2 * j + c][2 * i + r] = block[r][c]
    offset_covariance = [
        [joint[2 * i][2 * j] for j in range(count)]
        for i in range(count)
    ]
    return {
        "epochs_s": epochs,
        "state_covariances": marginals,
        "joint_state_covariance": joint,
        "offset_covariance": offset_covariance,
        "process_noise_spectral_density": q,
        "state_order": "[clock_offset_s, clock_drift_s_per_s]",
        "process_model": "d(offset)/dt=drift; d(drift)=sqrt(q) dW",
    }
