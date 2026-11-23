"""Propagate navigation, sensor-chain and acoustic ray uncertainty into soundings."""
import math

from multiping_covariance import _matrix, _multiply, _transpose
from sensor_chain_geometry import sensor_chain_sounding_point_and_jacobian


def propagate_sounding_uncertainty(
    gnss_position_navigation, imu_to_navigation_rotation,
    imu_to_gnss_lever_arm_imu, imu_to_transducer_lever_arm_imu,
    imu_to_transducer_rotation, acoustic_vector_transducer,
    joint_input_covariance, rotation_tolerance=1e-8):
    """Return sounding point and covariance from the complete 18-state input.

    Input covariance order:
    [GNSS position (3), navigation-frame left attitude error (3),
     IMU-to-GNSS lever arm (3), IMU-to-transducer lever arm (3),
     IMU-frame left mounting error (3), acoustic vector (3)].
    """
    result = sensor_chain_sounding_point_and_jacobian(
        gnss_position_navigation, imu_to_navigation_rotation,
        imu_to_gnss_lever_arm_imu, imu_to_transducer_lever_arm_imu,
        imu_to_transducer_rotation, acoustic_vector_transducer,
        rotation_tolerance)
    covariance = _matrix(joint_input_covariance, "joint_input_covariance", rows=18, columns=18)
    scale = max(1.0, max(abs(x) for row in covariance for x in row))
    if any(abs(covariance[i][j] - covariance[j][i]) > 1e-10 * scale
           for i in range(18) for j in range(i)):
        raise ValueError("joint_input_covariance must be symmetric")
    jacobian = result["jacobian"]
    output = _multiply(_multiply(jacobian, covariance), _transpose(jacobian))
    return {
        "point_navigation": result["point_navigation"],
        "jacobian": jacobian,
        "covariance": output,
        "standard_uncertainties": [max(0.0, output[i][i]) ** 0.5 for i in range(3)],
        "covariance_input_order": "[GNSS position, navigation attitude, GNSS lever arm, transducer lever arm, mounting attitude, acoustic vector]",
        "covariance_output_order": "[sounding position in navigation coordinates]",
    }


def propagate_ray_traced_sounding_uncertainty(
    gnss_position_navigation, imu_to_navigation_rotation,
    imu_to_gnss_lever_arm_imu, imu_to_transducer_lever_arm_imu,
    imu_to_transducer_rotation, ray_endpoint_xz_m, beam_azimuth_deg,
    joint_input_covariance, rotation_tolerance=1e-8):
    """Propagate ray endpoint [horizontal offset, depth] uncertainty to a sounding.

    The 17-state covariance order is the first 15 sensor-chain inputs
    [GNSS position, navigation attitude, GNSS lever arm, transducer lever
    arm, mounting attitude], followed by [ray horizontal offset, ray depth].
    The beam azimuth is measured in the transducer x-y plane from +x toward
    +y. The ray endpoint maps to the transducer-frame acoustic vector
    [x*cos(azimuth), x*sin(azimuth), depth].

    The full covariance may include ray-to-navigation and ray-to-calibration
    cross-correlations. This composes the acoustic ray endpoint Jacobian with
    the sensor-chain Jacobian without inserting a separate independent
    acoustic-vector covariance or counting the same ray uncertainty twice.
    """
    try:
        endpoint = [float(value) for value in ray_endpoint_xz_m]
        azimuth = float(beam_azimuth_deg)
    except (TypeError, ValueError):
        raise ValueError("ray endpoint and beam azimuth must be numeric") from None
    if len(endpoint) != 2 or not all(math.isfinite(value) for value in endpoint):
        raise ValueError("ray_endpoint_xz_m must contain two finite values")
    if not math.isfinite(azimuth):
        raise ValueError("beam_azimuth_deg must be finite")

    angle = math.radians(azimuth)
    cosine, sine = math.cos(angle), math.sin(angle)
    acoustic_vector = [endpoint[0] * cosine, endpoint[0] * sine, endpoint[1]]
    result = sensor_chain_sounding_point_and_jacobian(
        gnss_position_navigation, imu_to_navigation_rotation,
        imu_to_gnss_lever_arm_imu, imu_to_transducer_lever_arm_imu,
        imu_to_transducer_rotation, acoustic_vector, rotation_tolerance)

    covariance = _matrix(joint_input_covariance, "joint_input_covariance", rows=17, columns=17)
    scale = max(1.0, max(abs(x) for row in covariance for x in row))
    if any(abs(covariance[i][j] - covariance[j][i]) > 1e-10 * scale
           for i in range(17) for j in range(i)):
        raise ValueError("joint_input_covariance must be symmetric")

    # d[acoustic vector]/d[ray x, ray z], in transducer coordinates.
    beam_map = [[cosine, 0.0], [sine, 0.0], [0.0, 1.0]]
    chain_jacobian = result["jacobian"]
    jacobian = [chain_jacobian[row][:15] + [
        sum(chain_jacobian[row][15 + k] * beam_map[k][column] for k in range(3))
        for column in range(2)
    ] for row in range(3)]
    output = _multiply(_multiply(jacobian, covariance), _transpose(jacobian))
    return {
        "point_navigation": result["point_navigation"],
        "acoustic_vector_transducer": acoustic_vector,
        "jacobian": jacobian,
        "covariance": output,
        "standard_uncertainties": [max(0.0, output[i][i]) ** 0.5 for i in range(3)],
        "covariance_input_order": "[GNSS position, navigation attitude, GNSS lever arm, transducer lever arm, mounting attitude, ray horizontal offset, ray depth]",
        "covariance_output_order": "[sounding position in navigation coordinates]",
        "beam_azimuth_deg": azimuth,
    }
