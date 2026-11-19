#!/usr/bin/env python3
"""Exercise N: MINQUE-style variance-component estimation for repeated networks.
Standard library only. Synthetic data; no field or calibration claims.
"""
import csv, math, random, statistics
from pathlib import Path
DATA = Path(__file__).resolve().parents[2] / "data" / "measurement" / "exercise-d-stochastic-control-network.csv"
POINTS=("B","C","D","E")
TRUE={"A":100.0,"B":101.2,"C":102.0,"D":101.7,"E":102.4}
TRIALS, SEED = 2000, 20261119
SESSION_COUNTS=(3,6,12,24,48)
TRUE_INDEPENDENT_SCALE=1.0
TRUE_COMMON_VARIANCE_MM2=0.25

def transpose(a): return [list(v) for v in zip(*a)]
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def matmul(a,b):
    bt=transpose(b)
    return [[dot(row,col) for col in bt] for row in a]
def matvec(a,x): return [dot(row,x) for row in a]
def solve(a,b):
    n=len(b); m=[list(map(float,a[i]))+[float(b[i])] for i in range(n)]
    for c in range(n):
        p=max(range(c,n),key=lambda r:abs(m[r][c]))
        if abs(m[p][c])<1e-18: raise ValueError("Singular matrix")
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
                if v<=0: raise ValueError("Covariance not positive definite")
                l[i][j]=math.sqrt(v)
            else: l[i][j]=v/l[j][j]
    return l
def mat_trace(a): return sum(a[i][i] for i in range(len(a)))
def quadratic(y,m): return dot(y,matvec(m,y))

def load_model():
    with DATA.open(newline="",encoding="utf-8") as f: rows=list(csv.DictReader(f))
    n=len(rows); a=[]; truth=[]; d0=[[0.0]*n for _ in range(n)]
    for i,r in enumerate(rows):
        v=[0.0]*4
        if r["from_point"]!="A": v[POINTS.index(r["from_point"])]-=1.0
        if r["to_point"]!="A": v[POINTS.index(r["to_point"])]+=1.0
        a.append(v)
        truth.append((TRUE[r["to_point"]]-TRUE[r["from_point"]])*1000.0)
        d0[i][i]=float(r["assumed_sigma_mm"])**2
    w=inverse(d0); at=transpose(a); normal=matmul(matmul(at,w),a)
    ni=inverse(normal)
    # P = W - W A (A' W A)^-1 A' W
    wa=matmul(w,a); atw=matmul(at,w); correction=matmul(matmul(wa,ni),atw)
    p=[[w[i][j]-correction[i][j] for j in range(n)] for i in range(n)]
    c1=d0; c2=[[1.0]*n for _ in range(n)]
    pc=[matmul(p,c) for c in (c1,c2)]
    pc_p=[matmul(v,p) for v in pc]
    # H_ij = tr(P C_i P C_j); q_i = sum_g y_g' P C_i P y_g
    h=[[mat_trace(matmul(pc[i],pc[j])) for j in range(2)] for i in range(2)]
    return rows,truth,d0,pc_p,h

def estimate_components(blocks,pc_p,h):
    q=[sum(quadratic(y,m) for y in blocks) for m in pc_p]
    hh=[[len(blocks)*h[i][j] for j in range(2)] for i in range(2)]
    return solve(hh,q)

def generate_block(rng,truth,d0,theta1,theta2):
    n=len(truth)
    cov=[[theta1*d0[i][j]+theta2 for j in range(n)] for i in range(n)]
    l=cholesky(cov); z=[rng.gauss(0.0,1.0) for _ in range(n)]
    noise=matvec(l,z)
    return [truth[i]+noise[i] for i in range(n)]

def main():
    rows,truth,d0,pc_p,h=load_model()
    rng=random.Random(SEED)
    print("EXERCISE N — VARIANCE-COMPONENT ESTIMATION")
    print(f"trials_per_session_count={TRIALS}; seed={SEED}; true_independent_scale={TRUE_INDEPENDENT_SCALE:.3f}; true_common_variance_mm2={TRUE_COMMON_VARIANCE_MM2:.3f}")
    print("sessions,component,mean_estimate,sd_estimate,RMSE,negative_fraction")
    for ng in SESSION_COUNTS:
        estimates=[[],[]]
        for _ in range(TRIALS):
            blocks=[generate_block(rng,truth,d0,TRUE_INDEPENDENT_SCALE,TRUE_COMMON_VARIANCE_MM2) for _ in range(ng)]
            th=estimate_components(blocks,pc_p,h)
            estimates[0].append(th[0]); estimates[1].append(th[1])
        for idx,name in enumerate(("independent_scale","session_common_variance_mm2")):
            vals=estimates[idx]; target=1.0 if idx==0 else TRUE_COMMON_VARIANCE_MM2
            mean=statistics.fmean(vals); sd=statistics.stdev(vals)
            rmse=math.sqrt(statistics.fmean((v-target)**2 for v in vals))
            neg=sum(v<0 for v in vals)/TRIALS
            print(f"{ng},{name},{mean:.4f},{sd:.4f},{rmse:.4f},{neg:.4f}")
    print("\nMethod: two-component MINQUE-style quadratic estimation using the base diagonal covariance as the working metric.")
    print("Negative unconstrained estimates are retained and counted; truncating them to zero changes estimator properties.")
    print("Synthetic-only results. Components are not instrument calibration certificates or field-derived stochastic models.")

if __name__=="__main__": main()
