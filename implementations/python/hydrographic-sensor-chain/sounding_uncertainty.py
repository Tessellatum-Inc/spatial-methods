"""Propagate navigation and sensor-chain uncertainty into sounding coordinates."""
from multiping_covariance import _matrix, _multiply, _transpose
from sensor_chain_geometry import sensor_chain_sounding_point_and_jacobian

def propagate_sounding_uncertainty(
    gnss_position_navigation, imu_to_navigation_rotation,
    imu_to_gnss_lever_arm_imu, imu_to_transducer_lever_arm_imu,
    imu_to_transducer_rotation, acoustic_vector_transducer,
    joint_input_covariance, rotation_tolerance=1e-8):
    """Return sounding point and covariance from the complete 18-state input.

    Input covariance order is exactly the sensor-chain Jacobian order:
    [GNSS position (3), navigation-frame left attitude error (3),
     IMU-to-GNSS lever arm (3), IMU-to-transducer lever arm (3),
     IMU-frame left mounting error (3), acoustic vector (3)].

    The full covariance may contain correlations among navigation, lever-arm,
    mounting and acoustic terms. It must be supplied as one joint matrix;
    this function does not assume those groups are independent.
    """
    result=sensor_chain_sounding_point_and_jacobian(
        gnss_position_navigation,imu_to_navigation_rotation,
        imu_to_gnss_lever_arm_imu,imu_to_transducer_lever_arm_imu,
        imu_to_transducer_rotation,acoustic_vector_transducer,
        rotation_tolerance)
    covariance=_matrix(joint_input_covariance,"joint_input_covariance",rows=18,columns=18)
    scale=max(1.0,max(abs(x) for row in covariance for x in row))
    if any(abs(covariance[i][j]-covariance[j][i])>1e-10*scale
           for i in range(18) for j in range(i)):
        raise ValueError("joint_input_covariance must be symmetric")
    j=result["jacobian"]
    output=_multiply(_multiply(j,covariance),_transpose(j))
    return {"point_navigation":result["point_navigation"],
            "jacobian":j,
            "covariance":output,
            "standard_uncertainties":[max(0.0,output[i][i])**0.5 for i in range(3)],
            "covariance_input_order":"[GNSS position, navigation attitude, GNSS lever arm, transducer lever arm, mounting attitude, acoustic vector]",
            "covariance_output_order":"[sounding position in navigation coordinates]"}
