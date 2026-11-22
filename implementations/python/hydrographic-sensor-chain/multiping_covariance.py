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
