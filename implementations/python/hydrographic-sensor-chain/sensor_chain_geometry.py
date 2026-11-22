"""Static GNSS-IMU-transducer-acoustic sounding geometry and Jacobian."""
import math

def _v(x,n):
    try: a=[float(y) for y in x]
    except (TypeError,ValueError): raise ValueError(f"{n} must be three finite numbers") from None
    if len(a)!=3 or not all(math.isfinite(y) for y in a): raise ValueError(f"{n} must be three finite numbers")
    return a

def _r(x,n,tol):
    try: a=[[float(y) for y in row] for row in x]
    except (TypeError,ValueError): raise ValueError(f"{n} must be a proper 3 by 3 rotation") from None
    if len(a)!=3 or any(len(row)!=3 for row in a) or not all(math.isfinite(y) for row in a for y in row): raise ValueError(f"{n} must be a proper 3 by 3 rotation")
    if any(abs(sum(a[k][i]*a[k][j] for k in range(3))-(1.0 if i==j else 0.0))>tol for i in range(3) for j in range(3)): raise ValueError(f"{n} must be orthonormal")
    d=a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])-a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])+a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0])
    if abs(d-1)>tol: raise ValueError(f"{n} must have determinant +1")
    return a

def _mv(a,v): return [sum(row[j]*v[j] for j in range(3)) for row in a]
def _mm(a,b): return [[sum(a[i][k]*b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
def _sk(v):
    x,y,z=v
    return [[0.,-z,y],[z,0.,-x],[-y,x,0.]]

def sensor_chain_sounding_point_and_jacobian(gnss_position_navigation,imu_to_navigation_rotation,imu_to_gnss_lever_arm_imu,imu_to_transducer_lever_arm_imu,imu_to_transducer_rotation,acoustic_vector_transducer,rotation_tolerance=1e-8):
    """Return point and 3x18 J for [r_ng,dtheta_n,l_ig,l_it,dphi_i,s_t].

    Lever arms both point outward from IMU origin in IMU axes. R_ni maps IMU
    to navigation; R_it maps transducer to IMU. GNSS position is antenna point.
    Both rotations use left-multiplicative attitude perturbations in their
    destination frame (navigation for R_ni, IMU for R_it).
    """
    try: tol=float(rotation_tolerance)
    except (TypeError,ValueError): raise ValueError("rotation_tolerance must be finite and positive") from None
    if not math.isfinite(tol) or tol<=0: raise ValueError("rotation_tolerance must be finite and positive")
    r=_v(gnss_position_navigation,"gnss_position_navigation"); a=_v(imu_to_gnss_lever_arm_imu,"imu_to_gnss_lever_arm_imu"); b=_v(imu_to_transducer_lever_arm_imu,"imu_to_transducer_lever_arm_imu"); s=_v(acoustic_vector_transducer,"acoustic_vector_transducer")
    R=_r(imu_to_navigation_rotation,"imu_to_navigation_rotation",tol); Q=_r(imu_to_transducer_rotation,"imu_to_transducer_rotation",tol)
    q=_mv(Q,s); vi=[-a[k]+b[k]+q[k] for k in range(3)]; vn=_mv(R,vi); p=[r[k]+vn[k] for k in range(3)]
    j=[[0.]*18 for _ in range(3)]; at=[[-x for x in row] for row in _sk(vn)]; mt=_mm(R,[[-x for x in row] for row in _sk(q)]); rs=_mm(R,Q)
    for i in range(3):
        j[i][i]=1.; j[i][3:6]=at[i]; j[i][6:9]=[-x for x in R[i]]; j[i][9:12]=R[i][:]; j[i][12:15]=mt[i]; j[i][15:18]=rs[i]
    return {"point_navigation":p,"jacobian":j}
