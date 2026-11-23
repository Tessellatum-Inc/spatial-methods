"""Local rigid-body sounding-point geometry and its first-order Jacobian.

Frames: navigation-frame position and left-multiplicative small attitude
perturbation; body-frame lever arm and acoustic vector. No sonar or datum model.
"""
import math


def _vector(value, name):
    try:
        result = [float(x) for x in value]
    except (TypeError, ValueError):
        raise ValueError(f"{name} must contain three finite numbers") from None
    if len(result) != 3 or any(not math.isfinite(x) for x in result):
        raise ValueError(f"{name} must contain three finite numbers")
    return result


def _rotation(value, tolerance):
    try:
        r = [[float(x) for x in row] for row in value]
    except (TypeError, ValueError):
        raise ValueError("rotation must be a finite 3 by 3 matrix") from None
    if len(r) != 3 or any(len(row) != 3 for row in r):
        raise ValueError("rotation must be a finite 3 by 3 matrix")
    if any(not math.isfinite(x) for row in r for x in row):
        raise ValueError("rotation must be a finite 3 by 3 matrix")
    for i in range(3):
        for j in range(3):
            dot = sum(r[k][i] * r[k][j] for k in range(3))
            if abs(dot - (1.0 if i == j else 0.0)) > tolerance:
                raise ValueError("rotation matrix must be orthonormal")
    det = (
        r[0][0]*(r[1][1]*r[2][2]-r[1][2]*r[2][1])
        - r[0][1]*(r[1][0]*r[2][2]-r[1][2]*r[2][0])
        + r[0][2]*(r[1][0]*r[2][1]-r[1][1]*r[2][0])
    )
    if abs(det - 1.0) > tolerance:
        raise ValueError("rotation matrix must be proper (determinant +1)")
    return r


def _matvec(matrix, vector):
    return [sum(row[j] * vector[j] for j in range(3)) for row in matrix]


def sounding_point_and_jacobian(
    navigation_position,
    body_to_navigation_rotation,
    lever_arm_body,
    acoustic_vector_body,
    rotation_tolerance=1e-8,
):
    """Return sounding point and Jacobian for [r_n, dtheta_n, lever_b, s_b].

    p_n = r_n + R_n<-b (lever_b + acoustic_vector_b).

    dtheta_n is a left-multiplicative, infinitesimal attitude perturbation
    expressed in navigation axes: R' = Exp([dtheta_n]x) R. The Jacobian
    columns are ordered as three navigation-position, three attitude,
    three body lever-arm, then three body acoustic-vector components.

    This local derivative excludes timing, sensor-chain transforms, ray
    tracing, vertical-datum reduction and calibration-parameter estimation.
    """
    try:
        tolerance = float(rotation_tolerance)
    except (TypeError, ValueError):
        raise ValueError("rotation_tolerance must be finite and positive") from None
    if not math.isfinite(tolerance) or tolerance <= 0:
        raise ValueError("rotation_tolerance must be finite and positive")
    r_n = _vector(navigation_position, "navigation_position")
    lever = _vector(lever_arm_body, "lever_arm_body")
    acoustic = _vector(acoustic_vector_body, "acoustic_vector_body")
    rotation = _rotation(body_to_navigation_rotation, tolerance)
    body_vector = [lever[i] + acoustic[i] for i in range(3)]
    rotated = _matvec(rotation, body_vector)
    point = [r_n[i] + rotated[i] for i in range(3)]

    x, y, z = rotated
    skew = [[0.0, -z, y], [z, 0.0, -x], [-y, x, 0.0]]
    attitude_jacobian = [[-skew[i][j] for j in range(3)] for i in range(3)]
    jacobian = []
    for i in range(3):
        row = [0.0] * 12
        row[i] = 1.0
        row[3:6] = attitude_jacobian[i]
        row[6:9] = rotation[i][:]
        row[9:12] = rotation[i][:]
        jacobian.append(row)
    return {"point_navigation": point, "jacobian": jacobian}
