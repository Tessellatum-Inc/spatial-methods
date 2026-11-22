"""Time-aligned GNSS/IMU pose interpolation for sounding geometry."""
import math
from sensor_chain_geometry import sensor_chain_sounding_point_and_jacobian, _r, _v, _mv, _mm, _sk

def _transpose(a):
    return [[a[j][i] for j in range(3)] for i in range(3)]

def _so3_log(r):
    c=max(-1.0,min(1.0,(r[0][0]+r[1][1]+r[2][2]-1.0)/2.0))
    theta=math.acos(c)
    vee=[r[2][1]-r[1][2],r[0][2]-r[2][0],r[1][0]-r[0][1]]
    if theta<1e-8:return [0.5*x for x in vee]
    if math.pi-theta<1e-6:
        d=[max(0.0,(r[i][i]+1.0)/2.0) for i in range(3)]
        k=max(range(3),key=lambda i:d[i]);axis=[0.0,0.0,0.0]
        axis[k]=math.sqrt(d[k])
        if axis[k]<1e-8:raise ValueError("relative rotation is ambiguous near pi")
        for j in range(3):
            if j!=k:axis[j]=(r[k][j]+r[j][k])/(4.0*axis[k])
        norm=math.sqrt(sum(x*x for x in axis));axis=[x/norm for x in axis]
        for x in axis:
            if abs(x)>1e-12:
                if x<0:axis=[-y for y in axis]
                break
        return [theta*x for x in axis]
    scale=theta/(2.0*math.sin(theta))
    return [scale*x for x in vee]

def _so3_exp(phi):
    theta=math.sqrt(sum(x*x for x in phi));k=_sk(phi);k2=_mm(k,k)
    if theta<1e-8:
        return [[(1.0 if i==j else 0.0)+k[i][j]+0.5*k2[i][j] for j in range(3)] for i in range(3)]
    a=math.sin(theta)/theta;b=(1.0-math.cos(theta))/(theta*theta)
    return [[(1.0 if i==j else 0.0)+a*k[i][j]+b*k2[i][j] for j in range(3)] for i in range(3)]

def time_aligned_sensor_chain_sounding_point_and_jacobian(
    ping_time,time_offset_s,navigation_time_0,navigation_time_1,
    gnss_position_0_navigation,gnss_position_1_navigation,
    imu_to_navigation_rotation_0,imu_to_navigation_rotation_1,
    imu_to_gnss_lever_arm_imu,imu_to_transducer_lever_arm_imu,
    imu_to_transducer_rotation,acoustic_vector_transducer,rotation_tolerance=1e-8):
    """Return point and 3x19 J; last column differentiates time offset in seconds.

    Evaluation epoch is ping_time + time_offset_s. Positive offset evaluates
    navigation later than ping timestamp. Position is linearly interpolated;
    attitude follows the shortest SO(3) geodesic. Extrapolation is rejected.
    Input covariance order is the static 18-parameter sensor-chain order,
    followed by time_offset_s.
    """
    try:tol=float(rotation_tolerance)
    except (TypeError,ValueError):raise ValueError("rotation_tolerance must be finite and positive") from None
    if not math.isfinite(tol) or tol<=0:raise ValueError("rotation_tolerance must be finite and positive")
    try:tping,toff,t0,t1=[float(x) for x in (ping_time,time_offset_s,navigation_time_0,navigation_time_1)]
    except (TypeError,ValueError):raise ValueError("times must be finite numbers") from None
    if not all(math.isfinite(x) for x in (tping,toff,t0,t1)) or t1<=t0:
        raise ValueError("times must be finite and navigation_time_1 > navigation_time_0")
    te=tping+toff
    if te<t0 or te>t1:raise ValueError("evaluation epoch is outside the navigation bracket; extrapolation is not allowed")
    p0=_v(gnss_position_0_navigation,"gnss_position_0_navigation");p1=_v(gnss_position_1_navigation,"gnss_position_1_navigation")
    R0=_r(imu_to_navigation_rotation_0,"imu_to_navigation_rotation_0",tol)
    R1=_r(imu_to_navigation_rotation_1,"imu_to_navigation_rotation_1",tol)
    dt=t1-t0;alpha=(te-t0)/dt;delta=_so3_log(_mm(_transpose(R0),R1))
    R=_mm(R0,_so3_exp([alpha*x for x in delta]))
    pos=[p0[k]+alpha*(p1[k]-p0[k]) for k in range(3)]
    out=sensor_chain_sounding_point_and_jacobian(pos,R,imu_to_gnss_lever_arm_imu,
        imu_to_transducer_lever_arm_imu,imu_to_transducer_rotation,
        acoustic_vector_transducer,tol)
    a=_v(imu_to_gnss_lever_arm_imu,"imu_to_gnss_lever_arm_imu")
    b=_v(imu_to_transducer_lever_arm_imu,"imu_to_transducer_lever_arm_imu")
    Q=_r(imu_to_transducer_rotation,"imu_to_transducer_rotation",tol)
    s=_v(acoustic_vector_transducer,"acoustic_vector_transducer")
    q=_mv(Q,s);vi=[-a[k]+b[k]+q[k] for k in range(3)]
    omega=[x/dt for x in delta]
    rotational=_mv(R,_mv(_sk(omega),vi))
    jt=[(p1[k]-p0[k])/dt+rotational[k] for k in range(3)]
    out["jacobian"]=[out["jacobian"][i]+[jt[i]] for i in range(3)]
    out["time_offset_sensitivity"]=jt;out["evaluation_time"]=te
    out["interpolation_fraction"]=alpha
    return out
