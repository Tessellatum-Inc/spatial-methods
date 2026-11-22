"""Piecewise navigation-trajectory interpolation for hydrographic observations."""
import math
from time_aligned_sensor_chain import _so3_log, _so3_exp, _mm, _mv, _transpose
from sensor_chain_geometry import _r, _v

def interpolate_navigation_trajectory(navigation_times, gnss_positions,
                                      imu_to_navigation_rotations, query_times,
                                      rotation_tolerance=1e-8):
    """Interpolate a strictly time-ordered navigation trajectory at query epochs.

    Positions use piecewise-linear interpolation. Attitudes use shortest-path
    geodesic interpolation on SO(3). Queries outside the trajectory support
    are rejected; no extrapolation or silent endpoint clamping is performed.

    Returns one pose record per query with position, rotation, segment index,
    interpolation fraction, constant-segment velocity and body angular rate.
    """
    try:
        tol=float(rotation_tolerance)
        times=[float(t) for t in navigation_times]
        queries=[float(t) for t in query_times]
    except (TypeError,ValueError):
        raise ValueError("times and rotation_tolerance must be numeric") from None
    if not math.isfinite(tol) or tol<=0:
        raise ValueError("rotation_tolerance must be finite and positive")
    if len(times)<2 or len(gnss_positions)!=len(times) or len(imu_to_navigation_rotations)!=len(times):
        raise ValueError("at least two aligned navigation times, positions and rotations are required")
    if not all(math.isfinite(t) for t in times+queries):
        raise ValueError("all times must be finite")
    if any(times[i+1]<=times[i] for i in range(len(times)-1)):
        raise ValueError("navigation_times must be strictly increasing")
    positions=[_v(p,f"gnss_positions[{i}]") for i,p in enumerate(gnss_positions)]
    rotations=[_r(r,f"imu_to_navigation_rotations[{i}]",tol)
               for i,r in enumerate(imu_to_navigation_rotations)]
    output=[]
    for qi,t in enumerate(queries):
        if t<times[0] or t>times[-1]:
            raise ValueError(f"query_times[{qi}] is outside trajectory support")
        # At an interior knot, select the segment beginning at that knot;
        # at the final knot, use the final segment with alpha=1.
        lo=0
        hi=len(times)-1
        while lo+1<hi:
            mid=(lo+hi)//2
            if t<times[mid]: hi=mid
            else: lo=mid
        i=lo
        dt=times[i+1]-times[i]
        alpha=(t-times[i])/dt
        phi=_so3_log(_mm(_transpose(rotations[i]),rotations[i+1]))
        rotation=_mm(rotations[i],_so3_exp([alpha*x for x in phi]))
        velocity=[(positions[i+1][k]-positions[i][k])/dt for k in range(3)]
        omega=[x/dt for x in phi]
        position=[(1-alpha)*positions[i][k]+alpha*positions[i+1][k] for k in range(3)]
        output.append({"time":t,"position_navigation":position,
                       "imu_to_navigation_rotation":rotation,
                       "segment_index":i,"interpolation_fraction":alpha,
                       "velocity_navigation":velocity,
                       "angular_rate_body":omega})
    return output
