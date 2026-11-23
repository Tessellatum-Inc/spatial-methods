"""First-order covariance interpolation for navigation trajectory poses."""
import math
from navigation_trajectory import interpolate_navigation_trajectory
from time_aligned_sensor_chain import _so3_exp, _so3_log, _mm, _transpose as _rotation_transpose
from multiping_covariance import _matrix, _multiply

def _pose_at(times, positions, rotations, query, tolerance):
    pose=interpolate_navigation_trajectory(times,positions,rotations,[query],tolerance)[0]
    return pose["position_navigation"],pose["imu_to_navigation_rotation"]

def _matrix_transpose(matrix):
    return [list(column) for column in zip(*matrix)]

def _perturb_rotation(rotation, delta):
    return _mm(_so3_exp(delta),rotation)

def interpolate_navigation_pose_with_covariance(
    navigation_times, gnss_positions, imu_to_navigation_rotations,
    query_time, endpoint_joint_covariance, rotation_tolerance=1e-8,
    difference_step=1e-6):
    """Interpolate one pose and propagate its two endpoint pose covariance.

    Endpoint input order is [position_0(3), attitude_0(3),
    position_1(3), attitude_1(3)]. Positions are additive in navigation
    coordinates. Attitude errors are left-multiplicative navigation-frame
    perturbations: R_perturbed = Exp(delta_theta) R.

    Output covariance order is [interpolated_position(3),
    interpolated_attitude_left_error(3)]. The attitude Jacobian is evaluated
    by central finite differences on SO(3), avoiding a small-relative-angle
    approximation. All endpoint cross-covariances are retained.
    """
    try:
        step=float(difference_step);tol=float(rotation_tolerance);t=float(query_time)
    except (TypeError,ValueError):
        raise ValueError("query time, tolerances and difference step must be numeric") from None
    if not math.isfinite(step) or step<=0 or not math.isfinite(tol) or tol<=0 or not math.isfinite(t):
        raise ValueError("query time and tolerances must be finite; steps must be positive")
    if len(navigation_times)!=2 or len(gnss_positions)!=2 or len(imu_to_navigation_rotations)!=2:
        raise ValueError("exactly two bracketing navigation states are required")
    times=[float(x) for x in navigation_times]
    if not all(math.isfinite(x) for x in times) or times[1]<=times[0]:
        raise ValueError("navigation times must be finite and strictly increasing")
    if t<times[0] or t>times[1]:
        raise ValueError("query time is outside endpoint support")
    p0=[float(x) for x in gnss_positions[0]];p1=[float(x) for x in gnss_positions[1]]
    if len(p0)!=3 or len(p1)!=3 or not all(math.isfinite(x) for x in p0+p1):
        raise ValueError("endpoint positions must be finite 3-vectors")
    nominal_position,nominal_rotation=_pose_at(times,[p0,p1],imu_to_navigation_rotations,t,tol)
    covariance=_matrix(endpoint_joint_covariance,"endpoint_joint_covariance",rows=12,columns=12)
    scale=max(1.0,max(abs(x) for row in covariance for x in row))
    if any(abs(covariance[i][j]-covariance[j][i])>1e-10*scale
           for i in range(12) for j in range(i)):
        raise ValueError("endpoint_joint_covariance must be symmetric")
    jacobian=[[0.0]*12 for _ in range(6)]
    for col in range(12):
        plus_p=[p0[:],p1[:]];minus_p=[p0[:],p1[:]]
        plus_r=[ [row[:] for row in imu_to_navigation_rotations[k]] for k in range(2)]
        minus_r=[ [row[:] for row in imu_to_navigation_rotations[k]] for k in range(2)]
        endpoint=0 if col<6 else 1
        component=col%6
        if component<3:
            plus_p[endpoint][component]+=step
            minus_p[endpoint][component]-=step
        else:
            axis=[0.0,0.0,0.0];axis[component-3]=step
            plus_r[endpoint]=_perturb_rotation(plus_r[endpoint],axis)
            axis[component-3]=-step
            minus_r[endpoint]=_perturb_rotation(minus_r[endpoint],axis)
        pp,pr=_pose_at(times,plus_p,plus_r,t,tol)
        mp,mr=_pose_at(times,minus_p,minus_r,t,tol)
        for k in range(3):
            jacobian[k][col]=(pp[k]-mp[k])/(2*step)
        # Express output attitude perturbation as a left error in navigation axes.
        dp=_so3_log(_mm(pr,_rotation_transpose(nominal_rotation)))
        dm=_so3_log(_mm(mr,_rotation_transpose(nominal_rotation)))
        for k in range(3):
            jacobian[3+k][col]=(dp[k]-dm[k])/(2*step)
    output_covariance=_multiply(_multiply(jacobian,covariance),_matrix_transpose(jacobian))
    return {"position_navigation":nominal_position,
            "imu_to_navigation_rotation":nominal_rotation,
            "jacobian":jacobian,
            "covariance":output_covariance,
            "interpolation_fraction":(t-times[0])/(times[1]-times[0]),
            "covariance_input_order":"[position_0, attitude_0, position_1, attitude_1]",
            "covariance_output_order":"[position, left attitude error]" }
