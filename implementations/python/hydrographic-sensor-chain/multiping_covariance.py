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


def assemble_time_aligned_ray_traced_multiping_jacobian(
    sensor_chain_jacobians, ray_endpoint_jacobians,
    navigation_time_sensitivities):
    """Add one navigation-epoch clock-offset column per ray-traced ping.

    Base input order is [ping-local 17-state blocks, shared sound-speed
    profile]. The returned order appends N navigation epoch clock offsets,
    one per ping. Each time sensitivity is d(sounding)/d(epoch shift), in
    navigation-coordinate units per second.

    Acoustic two-way travel-time uncertainty remains in each ping-local ray
    input block. If the same physical clock drives both epoch tagging and
    acoustic timing, represent their correlation in the full covariance.
    """
    if not isinstance(sensor_chain_jacobians, (list, tuple)) or not sensor_chain_jacobians:
        raise ValueError("at least one sensor-chain Jacobian is required")
    count = len(sensor_chain_jacobians)
    if not isinstance(navigation_time_sensitivities, (list, tuple)) or len(navigation_time_sensitivities) != count:
        raise ValueError("one navigation time sensitivity is required per ping")
    base = assemble_ray_traced_multiping_jacobian(
        sensor_chain_jacobians, ray_endpoint_jacobians)
    vectors = []
    for i, value in enumerate(navigation_time_sensitivities):
        try:
            vector = [float(x) for x in value]
        except (TypeError, ValueError):
            raise ValueError(f"navigation_time_sensitivities[{i}] must be a finite 3-vector") from None
        if len(vector) != 3 or not all(math.isfinite(x) for x in vector):
            raise ValueError(f"navigation_time_sensitivities[{i}] must be a finite 3-vector")
        vectors.append(vector)

    output = []
    for ping in range(count):
        for axis in range(3):
            output.append(
                base[3 * ping + axis] +
                [vectors[ping][axis] if clock_ping == ping else 0.0
                 for clock_ping in range(count)]
            )
    return output


def propagate_time_aligned_ray_traced_multiping_covariance(
    sensor_chain_jacobians, ray_endpoint_jacobians,
    navigation_time_sensitivities, joint_input_covariance):
    """Propagate ray-traced soundings with correlated navigation epoch errors.

    Input covariance order is [per-ping sensor/angle/travel-time blocks,
    shared sound-speed profile, navigation epoch clock offsets by ping].
    The covariance may retain correlations between any of these groups,
    including epoch offsets and acoustic travel-time errors. A clock-state
    offset covariance can populate the final N-by-N block. The resulting
    3N-by-3N covariance retains profile and time-alignment correlations.
    """
    jacobian = assemble_time_aligned_ray_traced_multiping_jacobian(
        sensor_chain_jacobians, ray_endpoint_jacobians,
        navigation_time_sensitivities)
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
            "[ping-local sensor/angle/travel-time blocks, shared sound-speed "
            "profile, navigation epoch clock offsets by ping]"
        ),
        "covariance_output_order": "[sounding_1, sounding_2, ..., sounding_N]",
    }

def assemble_time_aligned_ray_traced_multiping_jacobian_from_trajectory(
    time_aligned_sensor_chain_results, ray_endpoint_jacobians,
    beam_azimuths_degrees):
    """Compose trajectory-interpolated sensor chains with ray and epoch terms.

    Each result is the mapping returned by
    time_aligned_sensor_chain_sounding_point_and_jacobian: its 3x19
    Jacobian contains the static 18-state sensor-chain block followed by
    the navigation-epoch time-offset sensitivity. The 18-state block has
    15 navigation/calibration columns and three acoustic-vector columns.
    The ray endpoint [horizontal offset, depth] is mapped into that vector
    using the supplied beam azimuth before composing the ray Jacobian.

    Final input order is [per-ping 15 sensor states, launch angle,
    two-way travel time; shared sound-speed profile; per-ping navigation
    epoch offsets]. The acoustic travel-time and navigation epoch effects
    remain distinct inputs.
    """
    if not isinstance(time_aligned_sensor_chain_results, (list, tuple)) or not time_aligned_sensor_chain_results:
        raise ValueError("at least one time-aligned sensor-chain result is required")
    count = len(time_aligned_sensor_chain_results)
    if not isinstance(beam_azimuths_degrees, (list, tuple)) or len(beam_azimuths_degrees) != count:
        raise ValueError("one beam azimuth is required per ping")
    sensor_jacobians = []
    time_sensitivities = []
    for ping, result in enumerate(time_aligned_sensor_chain_results):
        if not isinstance(result, dict) or "jacobian" not in result:
            raise ValueError(f"time_aligned_sensor_chain_results[{ping}] must contain a Jacobian")
        try:
            matrix = [[float(x) for x in row] for row in result["jacobian"]]
        except (TypeError, ValueError):
            raise ValueError(f"time-aligned Jacobian {ping} must be finite and 3x19") from None
        if len(matrix) != 3 or any(len(row) != 19 for row in matrix) or not all(
            math.isfinite(x) for row in matrix for x in row
        ):
            raise ValueError(f"time-aligned Jacobian {ping} must be finite and 3x19")
        try:
            azimuth = math.radians(float(beam_azimuths_degrees[ping]))
        except (TypeError, ValueError):
            raise ValueError(f"beam_azimuths_degrees[{ping}] must be finite") from None
        if not math.isfinite(azimuth):
            raise ValueError(f"beam_azimuths_degrees[{ping}] must be finite")
        mapping = [[math.cos(azimuth), 0.0],
                   [math.sin(azimuth), 0.0],
                   [0.0, 1.0]]
        endpoint_block = [
            [sum(matrix[row][15 + k] * mapping[k][axis] for k in range(3))
             for axis in range(2)]
            for row in range(3)
        ]
        sensor_jacobians.append([
            matrix[row][:15] + endpoint_block[row] for row in range(3)
        ])
        sensitivity = result.get("time_offset_sensitivity", [matrix[row][18] for row in range(3)])
        try:
            sensitivity = [float(x) for x in sensitivity]
        except (TypeError, ValueError):
            raise ValueError(f"time sensitivity {ping} must be a finite 3-vector") from None
        if len(sensitivity) != 3 or not all(math.isfinite(x) for x in sensitivity):
            raise ValueError(f"time sensitivity {ping} must be a finite 3-vector")
        time_sensitivities.append(sensitivity)
    return assemble_time_aligned_ray_traced_multiping_jacobian(
        sensor_jacobians, ray_endpoint_jacobians, time_sensitivities)


def propagate_time_aligned_ray_traced_multiping_covariance_from_trajectory(
    time_aligned_sensor_chain_results, ray_endpoint_jacobians,
    beam_azimuths_degrees, joint_input_covariance):
    """Propagate multi-ping ray covariance directly from interpolated poses."""
    jacobian = assemble_time_aligned_ray_traced_multiping_jacobian_from_trajectory(
        time_aligned_sensor_chain_results, ray_endpoint_jacobians,
        beam_azimuths_degrees)
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
            "[ping-local sensor/angle/travel-time blocks, shared sound-speed "
            "profile, navigation epoch clock offsets by ping]"
        ),
        "covariance_output_order": "[sounding_1, sounding_2, ..., sounding_N]",
    }



def assemble_time_aligned_ray_traced_stochastic_clock_multiping_jacobian_from_trajectory(
    time_aligned_sensor_chain_results, ray_endpoint_jacobians,
    beam_azimuths_degrees, ping_epochs_s, measured_two_way_travel_times_s,
    clock_state_covariance_result):
    """Replace per-ping epoch offsets with the propagated [offset, drift] states.

    The clock-state covariance result must come from
    propagate_clock_state_covariance at the same ping epochs. Clock offset
    shifts the navigation evaluation epoch. Clock drift also changes the
    measured acoustic interval: for a short ping interval with locally
    constant fractional drift, true_time ~= measured_time * (1 - drift).
    Thus the drift column receives -measured_time times the ray travel-time
    sensitivity. This is a first-order local-rate approximation; it does not
    model within-ping drift evolution or transmit/receive clock-state noise.
    """
    from_clock = clock_state_covariance_result
    if not isinstance(from_clock, dict) or "joint_state_covariance" not in from_clock:
        raise ValueError("clock_state_covariance_result must contain joint_state_covariance")
    epochs = from_clock.get("epochs_s")
    count = len(time_aligned_sensor_chain_results)
    if not isinstance(ping_epochs_s, (list, tuple)) or len(ping_epochs_s) != count:
        raise ValueError("one ping epoch is required per trajectory result")
    if not isinstance(epochs, (list, tuple)) or len(epochs) != count:
        raise ValueError("clock-state epochs must match the number of pings")
    try:
        supplied_epochs = [float(value) for value in ping_epochs_s]
        process_epochs = [float(value) for value in epochs]
    except (TypeError, ValueError):
        raise ValueError("ping and clock-state epochs must be finite numbers") from None
    if not all(math.isfinite(value) for value in supplied_epochs + process_epochs):
        raise ValueError("ping and clock-state epochs must be finite numbers")
    if any(abs(a - b) > 1e-9 * max(1.0, abs(a), abs(b))
           for a, b in zip(supplied_epochs, process_epochs)):
        raise ValueError("clock-state epochs must equal the supplied ping epochs")
    _matrix(from_clock["joint_state_covariance"],
            "clock joint state covariance", rows=2 * count, columns=2 * count)
    if not isinstance(measured_two_way_travel_times_s, (list, tuple)) or len(measured_two_way_travel_times_s) != count:
        raise ValueError("one measured two-way travel time is required per ping")
    try:
        travel_times = [float(value) for value in measured_two_way_travel_times_s]
    except (TypeError, ValueError):
        raise ValueError("measured two-way travel times must be finite and non-negative") from None
    if not all(math.isfinite(value) and value >= 0.0 for value in travel_times):
        raise ValueError("measured two-way travel times must be finite and non-negative")
    base = assemble_time_aligned_ray_traced_multiping_jacobian_from_trajectory(
        time_aligned_sensor_chain_results, ray_endpoint_jacobians,
        beam_azimuths_degrees)
    local_width = 17
    prefix = len(base[0]) - count
    if prefix < count * local_width + 1:
        raise ValueError("unexpected trajectory-driven multi-ping Jacobian layout")
    output = []
    for row_index, row in enumerate(base):
        ping = row_index // 3
        axis = row_index % 3
        expanded = row[:prefix] + [0.0] * (2 * count)
        # The 17 local variables are 15 sensor states, launch angle and
        # measured two-way travel time. Fractional clock drift perturbs the
        # true interval by -T_measured * drift to first order.
        travel_time_column = ping * local_width + 16
        expanded[prefix + 2 * ping] = row[prefix + ping]
        expanded[prefix + 2 * ping + 1] = (
            -travel_times[ping] * row[travel_time_column]
        )
        output.append(expanded)
    return output


def propagate_time_aligned_ray_traced_stochastic_clock_multiping_covariance_from_trajectory(
    time_aligned_sensor_chain_results, ray_endpoint_jacobians,
    beam_azimuths_degrees, ping_epochs_s, measured_two_way_travel_times_s,
    clock_state_covariance_result, joint_input_covariance):
    """Propagate survey-line covariance using process-derived clock states.

    Input order is [ping-local sensor/angle/travel-time blocks, shared sound-
    speed profile, (offset_1, drift_1), ..., (offset_N, drift_N)]. The final
    2N-by-2N covariance block must equal the joint state covariance returned
    by propagate_clock_state_covariance. Cross-covariances between clock
    states and all other inputs remain supported in the full joint matrix.
    """
    jacobian = assemble_time_aligned_ray_traced_stochastic_clock_multiping_jacobian_from_trajectory(
        time_aligned_sensor_chain_results, ray_endpoint_jacobians,
        beam_azimuths_degrees, ping_epochs_s, measured_two_way_travel_times_s,
        clock_state_covariance_result)
    size = len(jacobian[0])
    covariance = _matrix(joint_input_covariance, "joint_input_covariance",
                         rows=size, columns=size)
    scale = max(1.0, max(abs(value) for row in covariance for value in row))
    if any(abs(covariance[i][j] - covariance[j][i]) > 1e-10 * scale
           for i in range(size) for j in range(i)):
        raise ValueError("joint_input_covariance must be symmetric")
    count = len(time_aligned_sensor_chain_results)
    prefix = size - 2 * count
    expected = _matrix(
        clock_state_covariance_result["joint_state_covariance"],
        "clock joint state covariance", rows=2 * count, columns=2 * count)
    for i in range(2 * count):
        for j in range(2 * count):
            if abs(covariance[prefix + i][prefix + j] - expected[i][j]) > 1e-10 * max(
                1.0, abs(expected[i][j]), abs(covariance[prefix + i][prefix + j])
            ):
                raise ValueError(
                    "final clock-state covariance block must match the propagated clock process"
                )
    return {
        "jacobian": jacobian,
        "covariance": _multiply(_multiply(jacobian, covariance), _transpose(jacobian)),
        "covariance_input_order": (
            "[ping-local sensor/angle/travel-time blocks, shared sound-speed "
            "profile, (clock offset, clock drift) state by ping]"
        ),
        "covariance_output_order": "[sounding_1, sounding_2, ..., sounding_N]",
        "clock_state_order": "[clock_offset_s, clock_drift_s_per_s] by ping",
    }


def assemble_time_aligned_ray_traced_event_clock_multiping_jacobian_from_trajectory(
    time_aligned_sensor_chain_results, ray_endpoint_jacobians,
    beam_azimuths_degrees, ping_epochs_s, transmit_epochs_s,
    receive_epochs_s, clock_event_covariance_result):
    """Compose ray/trajectory sensitivities with exact transmit/receive clock events.

    The final clock block contains [offset, drift] at every unique event epoch.
    Navigation epoch sensitivity maps to the offset at ping_epochs_s. The
    corrected acoustic interval T = T_measured - (offset_receive-offset_transmit)
    maps +d(sound)/dT to transmit offset and -d(sound)/dT to receive offset.
    Process noise between the two events is represented by their joint state
    covariance, not by an extra independent interval-noise term.
    """
    if not isinstance(clock_event_covariance_result, dict):
        raise ValueError("clock_event_covariance_result must be an event covariance result")
    event_epochs = clock_event_covariance_result.get("event_epochs_s")
    event_covariance = clock_event_covariance_result.get("joint_event_state_covariance")
    if not isinstance(event_epochs, (list, tuple)) or not event_epochs:
        raise ValueError("clock event result must contain event_epochs_s")
    if event_covariance is None:
        raise ValueError("clock event result must contain joint_event_state_covariance")
    count = len(time_aligned_sensor_chain_results)
    if not isinstance(ping_epochs_s, (list, tuple)) or len(ping_epochs_s) != count:
        raise ValueError("one ping epoch is required per trajectory result")
    if not isinstance(transmit_epochs_s, (list, tuple)) or len(transmit_epochs_s) != count:
        raise ValueError("one transmit epoch is required per ping")
    if not isinstance(receive_epochs_s, (list, tuple)) or len(receive_epochs_s) != count:
        raise ValueError("one receive epoch is required per ping")
    try:
        ping_epochs = [float(x) for x in ping_epochs_s]
        transmit = [float(x) for x in transmit_epochs_s]
        receive = [float(x) for x in receive_epochs_s]
        events = [float(x) for x in event_epochs]
    except (TypeError, ValueError):
        raise ValueError("all ping and event epochs must be finite numbers") from None
    if not all(math.isfinite(x) for x in ping_epochs + transmit + receive + events):
        raise ValueError("all ping and event epochs must be finite numbers")
    if any(receive[i] <= transmit[i] for i in range(count)):
        raise ValueError("each receive epoch must be later than its transmit epoch")
    recorded_transmit = clock_event_covariance_result.get("transmit_epochs_s")
    recorded_receive = clock_event_covariance_result.get("receive_epochs_s")
    if not isinstance(recorded_transmit, (list, tuple)) or not isinstance(recorded_receive, (list, tuple)):
        raise ValueError("clock event result must retain its transmit and receive epoch pairing")
    try:
        recorded_transmit = [float(x) for x in recorded_transmit]
        recorded_receive = [float(x) for x in recorded_receive]
    except (TypeError, ValueError):
        raise ValueError("clock event result transmit and receive epochs must be finite numbers") from None
    if (len(recorded_transmit) != count or len(recorded_receive) != count
            or recorded_transmit != transmit or recorded_receive != receive):
        raise ValueError("transmit and receive epochs must match the clock event covariance pairing")
    if any(events[i + 1] <= events[i] for i in range(len(events) - 1)):
        raise ValueError("event epochs must be strictly increasing")
    event_index = {epoch: i for i, epoch in enumerate(events)}
    if any(epoch not in event_index for epoch in ping_epochs + transmit + receive):
        raise ValueError("clock event epochs must include every ping, transmit and receive epoch")
    _matrix(event_covariance, "clock joint event state covariance",
            rows=2 * len(events), columns=2 * len(events))

    base = assemble_time_aligned_ray_traced_multiping_jacobian_from_trajectory(
        time_aligned_sensor_chain_results, ray_endpoint_jacobians,
        beam_azimuths_degrees)
    local_width = 17
    prefix = len(base[0]) - count
    if prefix < count * local_width + 1:
        raise ValueError("unexpected trajectory-driven multi-ping Jacobian layout")
    output = []
    for row_index, row in enumerate(base):
        ping, axis = divmod(row_index, 3)
        expanded = row[:prefix] + [0.0] * (2 * len(events))
        # Navigation pose is evaluated at the ping epoch.
        expanded[prefix + 2 * event_index[ping_epochs[ping]]] += row[prefix + ping]
        # T_true = T_measured - (delta_t_receive - delta_t_transmit).
        travel_column = ping * local_width + 16
        travel_sensitivity = row[travel_column]
        expanded[prefix + 2 * event_index[transmit[ping]]] += travel_sensitivity
        expanded[prefix + 2 * event_index[receive[ping]]] -= travel_sensitivity
        output.append(expanded)
    return output


def propagate_time_aligned_ray_traced_event_clock_multiping_covariance_from_trajectory(
    time_aligned_sensor_chain_results, ray_endpoint_jacobians,
    beam_azimuths_degrees, ping_epochs_s, transmit_epochs_s,
    receive_epochs_s, clock_event_covariance_result, joint_input_covariance):
    """Propagate soundings with one process-derived clock state per event epoch."""
    jacobian = assemble_time_aligned_ray_traced_event_clock_multiping_jacobian_from_trajectory(
        time_aligned_sensor_chain_results, ray_endpoint_jacobians,
        beam_azimuths_degrees, ping_epochs_s, transmit_epochs_s,
        receive_epochs_s, clock_event_covariance_result)
    size = len(jacobian[0])
    covariance = _matrix(joint_input_covariance, "joint_input_covariance",
                         rows=size, columns=size)
    scale = max(1.0, max(abs(x) for row in covariance for x in row))
    if any(abs(covariance[i][j] - covariance[j][i]) > 1e-10 * scale
           for i in range(size) for j in range(i)):
        raise ValueError("joint_input_covariance must be symmetric")
    event_count = len(clock_event_covariance_result["event_epochs_s"])
    prefix = size - 2 * event_count
    expected = _matrix(
        clock_event_covariance_result["joint_event_state_covariance"],
        "clock joint event state covariance",
        rows=2 * event_count, columns=2 * event_count)
    for i in range(2 * event_count):
        for j in range(2 * event_count):
            actual = covariance[prefix + i][prefix + j]
            if abs(actual - expected[i][j]) > 1e-10 * max(1.0, abs(actual), abs(expected[i][j])):
                raise ValueError("final clock event covariance block must match the propagated clock process")
    return {
        "jacobian": jacobian,
        "covariance": _multiply(_multiply(jacobian, covariance), _transpose(jacobian)),
        "covariance_input_order": (
            "[ping-local sensor/angle/measured-travel-time blocks, shared "
            "sound-speed profile, (clock offset, clock drift) by event epoch]"
        ),
        "covariance_output_order": "[sounding_1, sounding_2, ..., sounding_N]",
        "clock_event_epochs_s": list(clock_event_covariance_result["event_epochs_s"]),
    }


def assemble_time_aligned_ray_traced_temporal_profile_multiping_jacobian_from_trajectory(
    time_aligned_sensor_chain_results, ray_endpoint_jacobians,
    beam_azimuths_degrees, ping_profile_epoch_indices,
    temporal_profile_covariance_result):
    """Compose ray/trajectory sensitivities with epoch-specific profile states.

    The temporal profile covariance result is produced by
    build_temporally_correlated_sound_speed_covariance. Each ping is assigned
    to one supplied profile epoch through ping_profile_epoch_indices.

    Input order is [ping-local sensor/angle/travel-time blocks,
    epoch-major sound-speed profile errors, navigation epoch offsets by ping].
    Each ping's ray profile sensitivity is inserted only into its assigned
    epoch block. Cross-epoch and cross-layer correlations are carried by the
    supplied joint profile covariance, including correlations with other
    input groups in the caller's full joint covariance.
    """
    if not isinstance(temporal_profile_covariance_result, dict):
        raise ValueError("temporal_profile_covariance_result must be a mapping")
    epochs = temporal_profile_covariance_result.get("profile_epochs_s")
    profile_covariance = temporal_profile_covariance_result.get(
        "joint_profile_covariance")
    layer_count = temporal_profile_covariance_result.get("layer_count")
    if not isinstance(epochs, (list, tuple)) or not epochs:
        raise ValueError("temporal profile result must contain profile_epochs_s")
    try:
        epochs = [float(value) for value in epochs]
        layer_count = int(layer_count)
    except (TypeError, ValueError, OverflowError):
        raise ValueError("temporal profile epochs and layer count must be valid") from None
    if (not all(math.isfinite(value) for value in epochs)
            or layer_count < 1
            or isinstance(temporal_profile_covariance_result.get("layer_count"), bool)
            or float(temporal_profile_covariance_result["layer_count"]) != layer_count):
        raise ValueError("temporal profile epochs and layer count must be valid")
    if not isinstance(time_aligned_sensor_chain_results, (list, tuple)) or not time_aligned_sensor_chain_results:
        raise ValueError("at least one time-aligned sensor-chain result is required")
    count = len(time_aligned_sensor_chain_results)
    if not isinstance(ping_profile_epoch_indices, (list, tuple)) or len(ping_profile_epoch_indices) != count:
        raise ValueError("one profile epoch index is required per ping")
    indices = []
    for ping, value in enumerate(ping_profile_epoch_indices):
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError(f"ping_profile_epoch_indices[{ping}] must be an integer")
        if value < 0 or value >= len(epochs):
            raise ValueError(f"ping_profile_epoch_indices[{ping}] is outside the profile epoch range")
        indices.append(value)

    profile_matrix = _matrix(
        profile_covariance, "joint_profile_covariance",
        rows=len(epochs) * layer_count, columns=len(epochs) * layer_count)
    profile_scale = max(1.0, max(abs(value) for row in profile_matrix for value in row))
    if any(abs(profile_matrix[i][j] - profile_matrix[j][i]) > 1e-10 * profile_scale
           for i in range(len(profile_matrix)) for j in range(i)):
        raise ValueError("joint_profile_covariance must be symmetric")

    base = assemble_time_aligned_ray_traced_multiping_jacobian_from_trajectory(
        time_aligned_sensor_chain_results, ray_endpoint_jacobians,
        beam_azimuths_degrees)
    local_width = 17 * count
    shared_start = local_width
    if len(base[0]) != local_width + layer_count + count:
        raise ValueError("ray profile layer count must match the temporal profile covariance")
    profile_width = len(epochs) * layer_count
    output = []
    for row_index, row in enumerate(base):
        ping = row_index // 3
        profile_sensitivity = row[shared_start:shared_start + layer_count]
        profile_columns = [0.0] * profile_width
        offset = indices[ping] * layer_count
        profile_columns[offset:offset + layer_count] = profile_sensitivity
        navigation_columns = row[shared_start + layer_count:]
        output.append(
            row[:local_width] + profile_columns + navigation_columns
        )
    return output


def propagate_time_aligned_ray_traced_temporal_profile_multiping_covariance_from_trajectory(
    time_aligned_sensor_chain_results, ray_endpoint_jacobians,
    beam_azimuths_degrees, ping_profile_epoch_indices,
    temporal_profile_covariance_result, joint_input_covariance):
    """Propagate multi-ping sounding covariance with temporal profile states.

    The epoch-major profile covariance block in joint_input_covariance must
    equal the covariance returned by the temporal profile model. All
    cross-covariances with ping-local states and navigation offsets remain
    supported in the full matrix.
    """
    jacobian = assemble_time_aligned_ray_traced_temporal_profile_multiping_jacobian_from_trajectory(
        time_aligned_sensor_chain_results, ray_endpoint_jacobians,
        beam_azimuths_degrees, ping_profile_epoch_indices,
        temporal_profile_covariance_result)
    size = len(jacobian[0])
    covariance = _matrix(
        joint_input_covariance, "joint_input_covariance",
        rows=size, columns=size)
    scale = max(1.0, max(abs(value) for row in covariance for value in row))
    if any(abs(covariance[i][j] - covariance[j][i]) > 1e-10 * scale
           for i in range(size) for j in range(i)):
        raise ValueError("joint_input_covariance must be symmetric")
    count = len(time_aligned_sensor_chain_results)
    profile_width = len(temporal_profile_covariance_result["profile_epochs_s"]) * temporal_profile_covariance_result["layer_count"]
    profile_start = 17 * count
    expected = _matrix(
        temporal_profile_covariance_result["joint_profile_covariance"],
        "joint_profile_covariance", rows=profile_width, columns=profile_width)
    for i in range(profile_width):
        for j in range(profile_width):
            actual = covariance[profile_start + i][profile_start + j]
            if abs(actual - expected[i][j]) > 1e-10 * max(
                1.0, abs(actual), abs(expected[i][j])
            ):
                raise ValueError(
                    "epoch-major profile covariance block must match the temporal profile model"
                )
    return {
        "jacobian": jacobian,
        "covariance": _multiply(
            _multiply(jacobian, covariance), _transpose(jacobian)),
        "covariance_input_order": (
            "[ping-local sensor/angle/travel-time blocks, epoch-major "
            "sound-speed profile errors, navigation epoch offsets by ping]"
        ),
        "covariance_output_order": "[sounding_1, sounding_2, ..., sounding_N]",
        "profile_epochs_s": list(temporal_profile_covariance_result["profile_epochs_s"]),
        "profile_layer_count": temporal_profile_covariance_result["layer_count"],
    }
