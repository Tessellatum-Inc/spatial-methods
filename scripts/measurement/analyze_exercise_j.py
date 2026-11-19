#!/usr/bin/env python3
"""Exercise J: Monte Carlo comparison of LS, iterative snooping and Huber IRLS.
Standard library only. All simulated observations and injected errors are synthetic.
"""
import csv, math, random
from pathlib import Path

DATA = Path(__file__).resolve().parents[2] / "data" / "measurement" / "exercise-c-synthetic-control-network.csv"
POINTS = ("B", "C", "D", "E")
TRUE = (101.2, 102.0, 101.7, 102.4)
ALPHA, HUBER_C, TRIALS, SEED = 0.01, 1.345, 500, 20261119

def solve(matrix, rhs):
    n=len(rhs); a=[list(map(float,matrix[i]))+[float(rhs[i])] for i in range(n)]
    for c in range(n):
        k=max(range(c,n),key=lambda r:abs(a[r][c]))
        if abs(a[k][c])<1e-18: raise ValueError("Singular or underconstrained adjustment")
        a[c],a[k]=a[k],a[c]; z=a[c][c]; a[c]=[v/z for v in a[c]]
        for r in range(n):
            if r!=c:
                z=a[r][c]; a[r]=[a[r][j]-z*a[c][j] for j in range(n+1)]
    return [a[i][-1] for i in range(n)]

def inverse(matrix):
    n=len(matrix); cols=[solve(matrix,[float(i==j) for i in range(n)]) for j in range(n)]
    return [[cols[j][i] for j in range(n)] for i in range(n)]

def normal_cdf(x): return .5*(1+math.erf(x/math.sqrt(2)))
def normal_quantile(p):
    lo,hi=-9.,9.
    for _ in range(70):
        mid=(lo+hi)/2
        if normal_cdf(mid)<p: lo=mid
        else: hi=mid
    return (lo+hi)/2

def load_rows():
    with DATA.open(newline="",encoding="utf-8") as f: rows=list(csv.DictReader(f))
    for r in rows: r["sigma"]=float(r["assumed_sigma_mm"])/1000
    return rows

def true_difference(a,b):
    return (100. if b=="A" else TRUE[POINTS.index(b)])-(100. if a=="A" else TRUE[POINTS.index(a)])

def model(rows):
    X=[]; y=[]; sig=[]
    for r in rows:
        v=[0.]*4; fixed=0.
        for point,sign in ((r["from_point"],-1.),(r["to_point"],1.)):
            if point=="A": fixed+=sign*100.
            else: v[POINTS.index(point)]+=sign
        X.append(v); y.append(r["observed_delta_h_m"]-fixed); sig.append(r["sigma"])
    return X,y,sig

def fit(rows,multipliers=None):
    X,y,sig=model(rows); n=len(y); u=4
    if n<=u: raise ValueError("No residual redundancy remains")
    mult=multipliers or [1.]*n; w=[mult[i]/sig[i]**2 for i in range(n)]
    N=[[sum(X[k][i]*w[k]*X[k][j] for k in range(n)) for j in range(u)] for i in range(u)]
    Q=inverse(N); rhs=[sum(X[k][i]*w[k]*y[k] for k in range(n)) for i in range(u)]
    x=solve(N,rhs); residuals=[sum(X[k][j]*x[j] for j in range(u))-y[k] for k in range(n)]
    z=[]
    for k in range(n):
        q=sum(X[k][i]*Q[i][j]*X[k][j] for i in range(u) for j in range(u))
        z.append(residuals[k]/math.sqrt(max(1e-24,sig[k]**2-q)))
    return x,residuals,z

def snooping(rows):
    active=list(range(len(rows))); removed=[]
    while True:
        subset=[rows[i] for i in active]; x,_,z=fit(subset); n=len(active)
        critical=normal_quantile(1-ALPHA/(2*n)); worst=max(range(n),key=lambda j:abs(z[j]))
        if abs(z[worst])<=critical or n-1<=4: return x,removed
        removed.append(active.pop(worst))

def huber(rows):
    n=len(rows); sig=[r["sigma"] for r in rows]; weights=[1.]*n
    for _ in range(100):
        _,residuals,_=fit(rows,weights)
        updated=[1. if abs(residuals[i]/sig[i])<=HUBER_C else HUBER_C/abs(residuals[i]/sig[i]) for i in range(n)]
        change=max(abs(updated[i]-weights[i]) for i in range(n)); weights=updated
        if change<1e-9: break
    return fit(rows,weights)[0]

def coordinate_rmse(x):
    return math.sqrt(sum((1000*(x[i]-TRUE[i]))**2 for i in range(4))/4)

def mean_se(values):
    n=len(values); m=sum(values)/n
    return m,math.sqrt(sum((v-m)**2 for v in values)/(n-1)/n) if n>1 else 0.

def main():
    base=load_rows(); augmented=[dict(r) for r in base]
    augmented.append({"observation_id":"BE*","from_point":"B","to_point":"E","observed_delta_h_m":TRUE[3]-TRUE[0],"sigma":.0016})
    designs={"baseline":base,"augmented":augmented}
    cases=[("clean",[],0.),("CE_plus_20mm",[8],.020),("AB_plus_20mm",[0],.020),
           ("two_same_sign_15mm",[3,8],.015),("two_opposite_sign_15mm",[3,8],.015)]
    rng=random.Random(SEED)
    print("EXERCISE J — SYNTHETIC MONTE CARLO ONLY")
    print(f"trials_per_design_case={TRIALS}; seed={SEED}; alpha={ALPHA}; Huber_c={HUBER_C}")
    print("Augmented design adds a hypothetical independent B-E observation (sigma=1.6 mm).")
    print("case,design,method,mean_trial_coordinate_RMSE_mm,MC_SE_mm,snooping_false_flag_or_exact_ID_rate,rate_MC_SE")
    for dname,template in designs.items():
        for cname,indices,magnitude in cases:
            errors={m:[] for m in ("LS","Snooping","Huber")}; rates=[]
            for _ in range(TRIALS):
                rows=[dict(r) for r in template]
                for r in rows:
                    r["observed_delta_h_m"]=true_difference(r["from_point"],r["to_point"])+rng.gauss(0,r["sigma"])
                injected=set()
                for idx in indices:
                    if idx<len(rows):
                        sign=-1 if cname=="two_opposite_sign_15mm" and idx==8 else 1
                        rows[idx]["observed_delta_h_m"]+=sign*magnitude; injected.add(idx)
                errors["LS"].append(coordinate_rmse(fit(rows)[0]))
                sx,removed=snooping(rows); errors["Snooping"].append(coordinate_rmse(sx))
                errors["Huber"].append(coordinate_rmse(huber(rows)))
                if not injected: rates.append(bool(removed))
                else: rates.append(injected.issubset(set(removed)))
            for method,values in errors.items():
                mean,se=mean_se(values); rate=sum(rates)/TRIALS if method=="Snooping" else ""
                rate_se=math.sqrt(rate*(1-rate)/TRIALS) if method=="Snooping" else ""
                print(f"{cname},{dname},{method},{mean:.3f},{se:.3f},{rate},{rate_se}")
    print("\nRates: clean = family-wise false-flag frequency; contaminated = exact identification of every injected observation.")
    print("Monte Carlo SE is the standard error of the reported mean RMSE or binomial rate.")
    print("Exact-set identification is stricter than detecting at least one injected error.")
    print("Model: independent Gaussian errors, known sigmas, exact datum, linear network; no shared systematics or correlated groups.")
    print("Sequential snooping is the Exercise I diagnostic heuristic, not an exact sequential family-wise procedure.")
    print("Huber downweighting is not proof of a physical blunder. Preserve raw observations.")

if __name__=="__main__": main()
