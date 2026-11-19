#!/usr/bin/env python3
"""Exercise K: covariance-aware adjustment with shared session errors.
Standard library only. Synthetic observations and Monte Carlo trials only.
"""
import csv, math, random
from pathlib import Path

DATA = Path(__file__).resolve().parents[2] / "data" / "measurement" / "exercise-d-stochastic-control-network.csv"
POINTS=("A","B","C","D","E")
TRUE={"A":100.0,"B":101.2,"C":102.0,"D":101.7,"E":102.4}
CONTROL_SIGMA_MM=2.0
SESSION_COMMON_SIGMA_MM=0.35
TRIALS=5000
SEED=20261119

def transpose(a): return [list(x) for x in zip(*a)]
def multiply(a,b):
    bt=transpose(b)
    return [[sum(x*y for x,y in zip(row,col)) for col in bt] for row in a]
def matvec(a,x): return [sum(v*w for v,w in zip(row,x)) for row in a]
def solve(a,b):
    n=len(b); m=[list(map(float,a[i]))+[float(b[i])] for i in range(n)]
    for c in range(n):
        p=max(range(c,n),key=lambda r:abs(m[r][c]))
        if abs(m[p][c])<1e-22: raise ValueError("Singular normal matrix")
        m[c],m[p]=m[p],m[c]; z=m[c][c]; m[c]=[v/z for v in m[c]]
        for r in range(n):
            if r!=c:
                z=m[r][c]; m[r]=[m[r][j]-z*m[c][j] for j in range(n+1)]
    return [m[i][-1] for i in range(n)]
def inverse(a):
    n=len(a); cols=[solve(a,[float(i==j) for i in range(n)]) for j in range(n)]
    return [[cols[j][i] for j in range(n)] for i in range(n)]
def cholesky(a):
    n=len(a); l=[[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1):
            v=a[i][j]-sum(l[i][k]*l[j][k] for k in range(j))
            if i==j:
                if v<=0: raise ValueError("Covariance must be positive definite")
                l[i][j]=math.sqrt(v)
            else: l[i][j]=v/l[j][j]
    return l
def forward(l,b):
    x=[]
    for i in range(len(b)):
        x.append((b[i]-sum(l[i][j]*x[j] for j in range(i)))/l[i][i])
    return x
def read_rows():
    with DATA.open(newline="",encoding="utf-8") as f: rows=list(csv.DictReader(f))
    for r in rows:
        r["length_km"]=float(r["length_km"])
        r["observed_delta_h_m"]=float(r["observed_delta_h_m"])
        r["assumed_sigma_mm"]=float(r["assumed_sigma_mm"])
    return rows
def build_system(rows, observations=None, tau_mm=SESSION_COMMON_SIGMA_MM):
    obs=observations or [r["observed_delta_h_m"] for r in rows]
    a=[]; y=[]; sig=[]
    for r,val in zip(rows,obs):
        v=[0.0]*5; v[POINTS.index(r["from_point"])]-=1
        v[POINTS.index(r["to_point"])]+=1
        a.append(v); y.append(val); sig.append(r["assumed_sigma_mm"]/1000)
    a.append([1.,0.,0.,0.,0.]); y.append(100.001); sig.append(CONTROL_SIGMA_MM/1000)
    n=len(rows)+1; q=[[0.0]*n for _ in range(n)]
    for i in range(len(rows)):
        for j in range(len(rows)):
            if i==j: q[i][j]+=sig[i]**2
            if rows[i]["session_id"]==rows[j]["session_id"]:
                q[i][j]+=(tau_mm/1000)**2
    q[-1][-1]=sig[-1]**2
    return a,y,q
def adjust(a,y,q):
    p=inverse(q); at=transpose(a); n=multiply(multiply(at,p),a)
    cov=inverse(n); x=solve(n,matvec(multiply(at,p),y))
    return x,cov
def diagonal(q):
    return [[q[i][j] if i==j else 0.0 for j in range(len(q))] for i in range(len(q))]
def true_dh(r): return TRUE[r["to_point"]]-TRUE[r["from_point"]]
def mc():
    rows=read_rows(); a,_,q=build_system(rows)
    cov_gls=inverse(multiply(multiply(transpose(a),inverse(q)),a))
    cov_naive=inverse(multiply(multiply(transpose(a),inverse(diagonal(q))),a))
    l=cholesky(q); rng=random.Random(SEED)
    methods={"GLS": [0.0]*5,"Diagonal WLS": [0.0]*5}
    sums={k:[0.0]*5 for k in methods}; sq={k:[0.0]*5 for k in methods}
    covered={k:[0]*5 for k in methods}
    for _ in range(TRIALS):
        noise=[rng.gauss(0,1) for _ in range(len(q))]
        err=matvec(l,noise)
        y=[true_dh(r)+err[i] for i,r in enumerate(rows)]
        y.append(100.0+err[-1])
        for name,qq in (("GLS",q),("Diagonal WLS",diagonal(q))):
            x,cov=adjust(a,y,qq)
            for j in range(5):
                e=(x[j]-TRUE[POINTS[j]])*1000
                sums[name][j]+=e; sq[name][j]+=e*e
                if abs(e)<=1.96*math.sqrt(cov[j][j])*1000: covered[name][j]+=1
    print("\nMONTE CARLO — shared session effects generated from the full covariance")
    print(f"trials={TRIALS}; seed={SEED}; session_common_sigma={SESSION_COMMON_SIGMA_MM:.2f} mm; control_sigma={CONTROL_SIGMA_MM:.2f} mm")
    print("method,point,bias_mm,empirical_RMSE_mm,formal_sigma_mm,95pct_interval_coverage")
    for name,cov in (("GLS",cov_gls),("Diagonal WLS",cov_naive)):
        for j,p in enumerate(POINTS):
            bias=sums[name][j]/TRIALS
            rmse=math.sqrt(sq[name][j]/TRIALS)
            formal=math.sqrt(cov[j][j])*1000
            coverage=covered[name][j]/TRIALS
            print(f"{name},{p},{bias:.4f},{rmse:.4f},{formal:.4f},{coverage:.4f}")
    print("\nCoverage is the empirical frequency that the true coordinate lies within estimate +/- 1.96 formal standard uncertainties.")
    print("The diagonal model deliberately ignores non-zero within-session covariance while retaining marginal variances.")
def main():
    rows=read_rows(); a,y,q=build_system(rows)
    xg,cg=adjust(a,y,q); xd,cd=adjust(a,y,diagonal(q))
    print("EXERCISE K — SYNTHETIC CORRELATED-ERROR NETWORK ADJUSTMENT")
    print(f"Session common-mode standard uncertainty: {SESSION_COMMON_SIGMA_MM:.2f} mm; stochastic control sigma: {CONTROL_SIGMA_MM:.2f} mm")
    print("Point,GLS_elevation_m,GLS_formal_u_mm,diagonal_WLS_elevation_m,diagonal_formal_u_mm")
    for i,p in enumerate(POINTS):
        print(f"{p},{xg[i]:.6f},{math.sqrt(cg[i][i])*1000:.3f},{xd[i]:.6f},{math.sqrt(cd[i][i])*1000:.3f}")
    print("\nThe generalized least-squares solution uses the full session covariance matrix.")
    print("Diagonal WLS is a deliberately misspecified comparison, not a recommended substitute.")
    mc()
    print("\nLimitations: two illustrative session groups, common additive session effect, independent within-observation noise, known covariance, exact linear model and synthetic control prior.")
    print("Correlation structure must be justified from acquisition and processing; covariance-aware robust estimation is a separate problem.")
if __name__=="__main__": main()
