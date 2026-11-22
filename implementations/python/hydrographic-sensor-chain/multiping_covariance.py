"""Joint covariance for multi-ping hydrographic sounding coordinates."""
import math

def _matrix(value, name, rows=None, columns=None):
    try: a=[[float(x) for x in row] for row in value]
    except (TypeError,ValueError): raise ValueError(f"{name} must be a finite rectangular matrix") from None
    if not a or not a[0] or any(len(r)!=len(a[0]) for r in a): raise ValueError(f"{name} must be non-empty and rectangular")
    if rows is not None and len(a)!=rows: raise ValueError(f"{name} must have {rows} rows")
    if columns is not None and len(a[0])!=columns: raise ValueError(f"{name} must have {columns} columns")
    if not all(math.isfinite(x) for r in a for x in r): raise ValueError(f"{name} must be finite")
    return a

def _transpose(a): return [list(c) for c in zip(*a)]
def _multiply(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]

def assemble_multiping_jacobian(local_jacobians, shared_jacobians):
    """Assemble output order [p1,...,pN], input order [x1,...,xN,c]."""
    if not isinstance(local_jacobians,(list,tuple)) or not local_jacobians: raise ValueError("at least one local Jacobian is required")
    if not isinstance(shared_jacobians,(list,tuple)) or len(shared_jacobians)!=len(local_jacobians): raise ValueError("one shared Jacobian is required per ping")
    local=[_matrix(j,f"local_jacobians[{i}]",rows=3) for i,j in enumerate(local_jacobians)]
    shared=[_matrix(j,f"shared_jacobians[{i}]",rows=3) for i,j in enumerate(shared_jacobians)]
    l=len(local[0][0]); s=len(shared[0][0]); n=len(local)
    if any(len(j[0])!=l for j in local): raise ValueError("local Jacobians must have equal column counts")
    if any(len(j[0])!=s for j in shared): raise ValueError("shared Jacobians must have equal column counts")
    out=[[0.0]*(n*l+s) for _ in range(3*n)]
    for i in range(n):
        for k in range(3):
            out[3*i+k][i*l:(i+1)*l]=local[i][k]
            out[3*i+k][n*l:]=shared[i][k]
    return out

def clock_offset_and_drift_sensitivities(time_sensitivities,ping_times,reference_time):
    """Return per-ping columns for common offset and drift parameters."""
    if not isinstance(time_sensitivities,(list,tuple)) or not time_sensitivities: raise ValueError("at least one time sensitivity is required")
    if not isinstance(ping_times,(list,tuple)) or len(ping_times)!=len(time_sensitivities): raise ValueError("one ping time is required per sensitivity")
    try: tref=float(reference_time); times=[float(t) for t in ping_times]
    except (TypeError,ValueError): raise ValueError("times must be finite numbers") from None
    if not math.isfinite(tref) or not all(math.isfinite(t) for t in times): raise ValueError("times must be finite numbers")
    out=[]
    for i,v in enumerate(time_sensitivities):
        try: v=[float(x) for x in v]
        except (TypeError,ValueError): raise ValueError(f"time_sensitivities[{i}] must be a finite 3-vector") from None
        if len(v)!=3 or not all(math.isfinite(x) for x in v): raise ValueError(f"time_sensitivities[{i}] must be a finite 3-vector")
        d=times[i]-tref; out.append([[x,d*x] for x in v])
    return out

def propagate_multiping_covariance(local_jacobians,shared_jacobians,joint_input_covariance):
    """Propagate full joint covariance; covariance input follows assembled column order."""
    j=assemble_multiping_jacobian(local_jacobians,shared_jacobians); n=len(j[0])
    c=_matrix(joint_input_covariance,"joint_input_covariance",rows=n,columns=n)
    scale=max(1.0,max(abs(x) for r in c for x in r))
    if any(abs(c[i][k]-c[k][i])>1e-10*scale for i in range(n) for k in range(i)): raise ValueError("joint_input_covariance must be symmetric")
    return {"jacobian":j,"covariance":_multiply(_multiply(j,c),_transpose(j))}


def assemble_time_aligned_multiping_jacobian(
    local_jacobians, shared_jacobians, time_sensitivities,
    ping_times, reference_time):
    """Append common clock-offset and clock-drift columns to shared inputs.

    Input order is [ping-local blocks..., shared calibration block,
    common clock offset (s), common clock drift (s/s)]. The per-ping
    time_sensitivities are derivatives of sounding coordinates with respect
    to that ping's evaluation-time shift, in navigation-coordinate units/s.
    """
    if not isinstance(local_jacobians, (list, tuple)) or not local_jacobians:
        raise ValueError("at least one local Jacobian is required")
    if len(time_sensitivities) != len(local_jacobians) or len(ping_times) != len(local_jacobians):
        raise ValueError("one time sensitivity and ping time are required per ping")
    clock = clock_offset_and_drift_sensitivities(
        time_sensitivities, ping_times, reference_time)
    augmented = []
    for i, shared in enumerate(shared_jacobians):
        base = _matrix(shared, f"shared_jacobians[{i}]", rows=3)
        if len(base[0]) == 0:
            raise ValueError("each shared Jacobian must contain at least one shared parameter")
        augmented.append([base[k] + clock[i][k] for k in range(3)])
    return assemble_multiping_jacobian(local_jacobians, augmented)


def propagate_time_aligned_multiping_covariance(
    local_jacobians, shared_jacobians, time_sensitivities,
    ping_times, reference_time, joint_input_covariance):
    """Propagate multiple time-aligned soundings with shared clock errors.

    Covariance input order is the assembled Jacobian order: all ping-local
    blocks, the shared calibration block, then common clock offset and drift.
    The full matrix may contain cross-ping local-state correlations and
    calibration/clock correlations; none are discarded.
    """
    j = assemble_time_aligned_multiping_jacobian(
        local_jacobians, shared_jacobians, time_sensitivities,
        ping_times, reference_time)
    n = len(j[0])
    c = _matrix(joint_input_covariance, "joint_input_covariance", rows=n, columns=n)
    scale = max(1.0, max(abs(x) for row in c for x in row))
    if any(abs(c[i][k] - c[k][i]) > 1e-10 * scale
           for i in range(n) for k in range(i)):
        raise ValueError("joint_input_covariance must be symmetric")
    return {"jacobian": j, "covariance": _multiply(_multiply(j, c), _transpose(j)),
            "covariance_input_order": "[ping-local blocks..., shared calibration block, clock offset, clock drift]",
            "covariance_output_order": "[sounding_1, sounding_2, ..., sounding_N]"}


def assemble_stochastic_clock_multiping_jacobian(
    local_jacobians, shared_jacobians, time_sensitivities):
    """Append one correlated clock-offset state per ping to the shared block.

    The clock-offset covariance is supplied by clock_state_covariance.py.
    Input order is [ping-local blocks..., shared calibration block,
    clock_offset_at_ping_1, ..., clock_offset_at_ping_N]. Each ping's
    sounding is sensitive only to its own clock offset, while covariance
    between clock offsets creates cross-ping sounding covariance.
    """
    if not isinstance(local_jacobians, (list, tuple)) or not local_jacobians:
        raise ValueError("at least one local Jacobian is required")
    count = len(local_jacobians)
    if len(shared_jacobians) != count or len(time_sensitivities) != count:
        raise ValueError("one shared Jacobian and time sensitivity are required per ping")
    base_blocks = [_matrix(value, f"shared_jacobians[{i}]", rows=3)
                   for i, value in enumerate(shared_jacobians)]
    clock_sensitivities = []
    for i, value in enumerate(time_sensitivities):
        try:
            vector = [float(x) for x in value]
        except (TypeError, ValueError):
            raise ValueError(f"time_sensitivities[{i}] must be a finite 3-vector") from None
        if len(vector) != 3 or not all(math.isfinite(x) for x in vector):
            raise ValueError(f"time_sensitivities[{i}] must be a finite 3-vector")
        clock_sensitivities.append(vector)
    shared_count = len(base_blocks[0][0])
    if any(len(block[0]) != shared_count for block in base_blocks):
        raise ValueError("shared Jacobians must have equal column counts")
    augmented = []
    for ping in range(count):
        rows = []
        for axis in range(3):
            clock_columns = [
                clock_sensitivities[ping][axis] if clock_ping == ping else 0.0
                for clock_ping in range(count)
            ]
            rows.append(base_blocks[ping][axis] + clock_columns)
        augmented.append(rows)
    return assemble_multiping_jacobian(local_jacobians, augmented)


def propagate_stochastic_clock_multiping_covariance(
    local_jacobians, shared_jacobians, time_sensitivities,
    joint_input_covariance):
    """Propagate soundings using a full covariance including ping clock offsets.

    Supply the clock_offset_covariance from
    propagate_clock_state_covariance in the final N x N block of the joint
    input covariance. Cross-covariances with navigation/calibration may also
    be supplied in that same full matrix; this function makes no independence
    assumption and does not discard any off-diagonal terms.
    """
    jacobian = assemble_stochastic_clock_multiping_jacobian(
        local_jacobians, shared_jacobians, time_sensitivities)
    size = len(jacobian[0])
    covariance = _matrix(joint_input_covariance, "joint_input_covariance",
                         rows=size, columns=size)
    scale = max(1.0, max(abs(x) for row in covariance for x in row))
    if any(abs(covariance[i][j] - covariance[j][i]) > 1e-10 * scale
           for i in range(size) for j in range(i)):
        raise ValueError("joint_input_covariance must be symmetric")
    return {
        "jacobian": jacobian,
        "covariance": _multiply(_multiply(jacobian, covariance), _transpose(jacobian)),
        "covariance_input_order": "[ping-local blocks..., shared calibration block, clock offsets by ping]",
        "covariance_output_order": "[sounding_1, sounding_2, ..., sounding_N]",
    }


def assemble_ray_traced_multiping_jacobian(
    sensor_chain_jacobians, ray_endpoint_jacobians):
    """Compose per-ping sensor-chain and acoustic-ray Jacobians.

    Each sensor-chain Jacobian is 3x17, with columns ordered as the 15
    navigation/calibration states followed by ray endpoint [x, z].
    Each ray endpoint Jacobian is 2x(m+2), ordered as the m shared
    sound-speed layer parameters followed by that ping's launch angle
    (degrees) and two-way travel time (seconds).

    The assembled input order is
    [ping_1 local(15 sensor + angle + travel time), ...,
     ping_N local(...), shared sound-speed profile(m)].
    Thus sound-speed errors are represented once, in a shared block,
    and induce the physically required cross-ping covariance.
    """
    if not isinstance(sensor_chain_jacobians, (list, tuple)) or not sensor_chain_jacobians:
        raise ValueError("at least one sensor-chain Jacobian is required")
    count = len(sensor_chain_jacobians)
    if not isinstance(ray_endpoint_jacobians, (list, tuple)) or len(ray_endpoint_jacobians) != count:
        raise ValueError("one ray endpoint Jacobian is required per ping")

    sensor = [
        _matrix(value, f"sensor_chain_jacobians[{i}]", rows=3, columns=17)
        for i, value in enumerate(sensor_chain_jacobians)
    ]
    rays = [
        _matrix(value, f"ray_endpoint_jacobians[{i}]", rows=2)
        for i, value in enumerate(ray_endpoint_jacobians)
    ]
    shared_count = len(rays[0][0]) - 2
    if shared_count < 1:
        raise ValueError("ray endpoint Jacobians must include at least one shared sound-speed parameter")
    if any(len(ray[0]) != shared_count + 2 for ray in rays):
        raise ValueError("ray endpoint Jacobians must have equal input column counts")

    local_blocks = []
    shared_blocks = []
    for ping, (sensor_j, ray_j) in enumerate(zip(sensor, rays)):
        endpoint_j = [row[15:17] for row in sensor_j]
        local_ray = [[ray_j[k][shared_count + q] for q in range(2)] for k in range(2)]
        shared_ray = [[ray_j[k][q] for q in range(shared_count)] for k in range(2)]
        local_effect = _multiply(endpoint_j, local_ray)
        shared_effect = _multiply(endpoint_j, shared_ray)
        local_blocks.append([
            sensor_j[row][:15] + local_effect[row] for row in range(3)
        ])
        shared_blocks.append(shared_effect)

    return assemble_multiping_jacobian(local_blocks, shared_blocks)


def propagate_ray_traced_multiping_covariance(
    sensor_chain_jacobians, ray_endpoint_jacobians, joint_input_covariance):
    """Propagate a survey-line joint covariance through ray and sensor chains.

    Covariance input order is all per-ping blocks
    [15 sensor states, launch angle, two-way travel time], followed by
    the shared sound-speed profile parameters. The full matrix may retain
    correlations among pings, between ping-local states and the shared
    profile, and among shared profile parameters. In particular, the
    sound-speed profile is not duplicated into each ping-local covariance.

    If a clock error affects the corrected two-way travel time, include its
    contribution in the corresponding travel-time state and its cross-ping
    covariance in this same joint matrix. Do not also add that clock error
    as a separate independent term.
    """
    jacobian = assemble_ray_traced_multiping_jacobian(
        sensor_chain_jacobians, ray_endpoint_jacobians)
    size = len(jacobian[0])
    covariance = _matrix(
        joint_input_covariance, "joint_input_covariance",
        rows=size, columns=size)
    scale = max(1.0, max(abs(value) for row in covariance for value in row))
    if any(abs(covariance[i][j] - covariance[j][i]) > 1e-10 * scale
           for i in range(size) for j in range(i)):
        raise ValueError("joint_input_covariance must be symmetric")
    return {
        "jacobian": jacobian,
        "covariance": _multiply(
            _multiply(jacobian, covariance), _transpose(jacobian)),
        "covariance_input_order": (
            "[ping-local blocks: sensor states, launch angle, two-way travel time; "
            "shared sound-speed profile]"
        ),
        "covariance_output_order": "[sounding_1, sounding_2, ..., sounding_N]",
    }
