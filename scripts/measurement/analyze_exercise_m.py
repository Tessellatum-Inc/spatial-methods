#!/usr/bin/env python3
"""Exercise M: repeated multi-session network adjustment and block robustness.
Standard library only. All simulations and injected errors are synthetic.
"""
import csv, math, random
from pathlib import Path

DATA = Path(__file__).resolve().parents[2] / "data" / "measurement" / "exercise-d-stochastic-control-network.csv"
POINTS = ("B", "C", "D", "E")
TRUE = {"A":100.0, "B":101.2, "C":102.0, "D":101.7, "E":102.4}
SESSIONS, TRIALS, SEED = 12, 3000, 20261119
COMMON_SIGMA_MM, HUBER_C = 0.50, 1.5

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
        if abs(m[p][c])<1e-20: raise ValueError("Singular matrix")
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
def forward(l,b):
    x=[]
    for i in range(len(b)):
        x.append((b[i]-sum(l[i][j]*x[j] for j in range(i)))/l[i][i])
    return x

def load_network():
    with DATA.open(newline="",encoding="utf-8") as f: rows=list(csv.DictReader(f))
    for r in rows: r["sigma"]=float(r["assumed_sigma_mm"])/1000.0
    a=[]; truth=[]
    for r in rows:
        v=[0.0]*4
        if r["from_point"]!="A": v[POINTS.index(r["from_point"]) ]-=1.0
        if r["to_point"]!="A": v[POINTS.index(r["to_point"]) ]+=1.0
        a.append(v)
        truth.append(TRUE[r["to_point"]]-TRUE[r["from_point"]])
    return rows,a,truth

def prepare(rows,a):
    n=len(rows); q=[[0.0]*n for _ in range(n)]
    # Each replicate is one independent session: all nine observations share
    # one common additive session effect, plus independent row-specific noise.
    for i,r in enumerate(rows):
        q[i][i]=r["sigma"]**2
        for j in range(n): q[i][j]+= (COMMON_SIGMA_MM/1000.0)**2
    l=cholesky(q)
    aw=transpose([forward(l,col) for col in transpose(a)])
    ad=[[a[i][j]/rows[i]["sigma"] for j in range(n)] for i in range(n)]
    return q,l,aw,ad

def fit(aw,ad,l,rows,blocks,mode):
    robust=(mode=="block")
    design=aw if mode in ("gls","block") else ad
    whitened=[]
    for obs in blocks:
        if mode in ("gls","block"): whitened.append(forward(l,obs))
        else: whitened.append([obs[i]/rows[i]["sigma"] for i in range(len(obs))])
    weights=[1.0]*len(blocks); x=[0.0]*4
    at=transpose(design); ng=matmul(at,design)
    for _ in range(50 if robust else 1):
        normal=[[0.0]*4 for _ in range(4)]; rhs=[0.0]*4
        for g,y in enumerate(whitened):
            rg=matvec(at,y)
            for i in range(4):
                rhs[i]+=weights[g]*rg[i]
                for j in range(4): normal[i][j]+=weights[g]*ng[i][j]
        xn=solve(normal,rhs)
        if not robust:
            x=xn; break
        updated=[]
        for y in whitened:
            residual=[y[i]-dot(design[i],xn) for i in range(len(y))]
            score=math.sqrt(sum(v*v for v in residual)/len(residual))
            updated.append(1.0 if score<=HUBER_C else HUBER_C/score)
        delta=max(abs(updated[i]-weights[i]) for i in range(len(weights)))
        x,weights=xn,updated
        if delta<1e-8: break
    return x,weights

def coordinate_rmse(x):
    return math.sqrt(sum((x[i]-(TRUE[POINTS[i]]-TRUE["A"]))**2 for i in range(4))/4)*1000.0

def main():
    rows,a,truth=load_network()
    q,l,aw,ad=prepare(rows,a)
    rng=random.Random(SEED)
    scenarios=("clean","one_row_plus_20mm","one_session_plus_4mm",
               "two_sessions_opposing_3mm","three_sessions_plus_3mm")
    methods=(("GLS","gls"),("Diagonal_WLS","diag"),("Block_Huber_GLS","block"))
    totals={s:{m:0.0 for m,_ in methods} for s in scenarios}
    squares={s:{m:0.0 for m,_ in methods} for s in scenarios}
    weights={s:[0.0]*SESSIONS for s in scenarios}
    low={s:[0.0]*SESSIONS for s in scenarios}
    for _ in range(TRIALS):
        generated=[]
        for _g in range(SESSIONS):
            z=[rng.gauss(0.0,1.0) for _ in rows]
            noise=matvec(l,z)
            generated.append([truth[i]+noise[i] for i in range(len(rows))])
        for scenario in scenarios:
            obs=[list(b) for b in generated]
            if scenario=="one_row_plus_20mm": obs[2][8]+=0.020
            elif scenario=="one_session_plus_4mm": obs[3]=[v+0.004 for v in obs[3]]
            elif scenario=="two_sessions_opposing_3mm":
                obs[2]=[v+0.003 for v in obs[2]]
                obs[8]=[v-0.003 for v in obs[8]]
            elif scenario=="three_sessions_plus_3mm":
                for g in (1,5,10): obs[g]=[v+0.003 for v in obs[g]]
            for name,mode in methods:
                x,w=fit(aw,ad,l,rows,obs,mode)
                e=coordinate_rmse(x)
                totals[scenario][name]+=e
                squares[scenario][name]+=e*e
                if mode=="block":
                    for g,value in enumerate(w):
                        weights[scenario][g]+=value/TRIALS
                        if value<0.8: low[scenario][g]+=1.0/TRIALS
    print("EXERCISE M — REPEATED MULTI-SESSION NETWORK")
    print(f"sessions={SESSIONS}; observations_per_session={len(rows)}; trials={TRIALS}; seed={SEED}")
    print(f"session_common_sigma_mm={COMMON_SIGMA_MM}; block_Huber_c={HUBER_C}")
    print("scenario,method,mean_coordinate_RMSE_mm,MC_SE_mm")
    for s in scenarios:
        for name,_ in methods:
            mean=totals[s][name]/TRIALS
            var=max(0.0,squares[s][name]/TRIALS-mean*mean)
            print(f"{s},{name},{mean:.3f},{math.sqrt(var/TRIALS):.3f}")
    print("\nMean block weights (sessions 01–12; 1.0 = no downweighting):")
    for s in scenarios: print(s+","+",".join(f"{v:.3f}" for v in weights[s]))
    print("\nFraction of trials each session received weight below 0.8:")
    for s in scenarios: print(s+","+",".join(f"{v:.3f}" for v in low[s]))
    print("\nSynthetic-only results. The robust score is a block residual RMS after covariance whitening.")
if __name__=="__main__": main()
