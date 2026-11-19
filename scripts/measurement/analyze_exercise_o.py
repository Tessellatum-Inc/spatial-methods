#!/usr/bin/env python3
"""Exercise O: covariance-model selection by restricted likelihood.
Synthetic teaching experiment; standard library only.
"""
import csv, math, random
from pathlib import Path
DATA=Path(__file__).resolve().parents[2]/"data"/"measurement"/"exercise-d-stochastic-control-network.csv"
PTS=("B","C","D","E"); TRUE={"A":100.,"B":101.2,"C":102.,"D":101.7,"E":102.4}
TRIALS=250; SEED=20261119; GRID=[i*0.15 for i in range(11)]
TAU=0.50; AR_SIGMA=0.50; RHO=0.60

def tr(a): return [list(x) for x in zip(*a)]
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def mm(a,b):
 bt=tr(b); return [[dot(x,y) for y in bt] for x in a]
def mv(a,x): return [dot(r,x) for r in a]
def solve(a,b):
 n=len(b); z=[list(map(float,a[i]))+[float(b[i])] for i in range(n)]
 for c in range(n):
  p=max(range(c,n),key=lambda i:abs(z[i][c])); z[c],z[p]=z[p],z[c]
  if abs(z[c][c])<1e-16: raise ValueError("singular")
  d=z[c][c]; z[c]=[v/d for v in z[c]]
  for r in range(n):
   if r!=c:
    d=z[r][c]; z[r]=[z[r][j]-d*z[c][j] for j in range(n+1)]
 return [z[i][-1] for i in range(n)]
def inv(a):
 n=len(a); cols=[solve(a,[float(i==j) for i in range(n)]) for j in range(n)]
 return [[cols[j][i] for j in range(n)] for i in range(n)]
def chol(a):
 n=len(a); l=[[0.]*n for _ in range(n)]
 for i in range(n):
  for j in range(i+1):
   v=a[i][j]-sum(l[i][k]*l[j][k] for k in range(j))
   if i==j: l[i][j]=math.sqrt(max(v,1e-15))
   else: l[i][j]=v/l[j][j]
 return l
def logdet_chol(l): return 2*sum(math.log(l[i][i]) for i in range(len(l)))
def forward(l,b):
 x=[]
 for i in range(len(b)): x.append((b[i]-sum(l[i][j]*x[j] for j in range(i)))/l[i][i])
 return x
def load():
 with DATA.open(newline="",encoding="utf-8") as f: rows=list(csv.DictReader(f))
 a=[]; truth=[]; d=[]
 for r in rows:
  v=[0.]*4
  if r["from_point"]!="A": v[PTS.index(r["from_point"])]-=1
  if r["to_point"]!="A": v[PTS.index(r["to_point"])]+=1
  a.append(v); truth.append((TRUE[r["to_point"]]-TRUE[r["from_point"]])*1000)
  d.append(float(r["assumed_sigma_mm"])**2)
 return rows,a,truth,d
def cov(d,kind,sess,arsig,rho):
 n=len(d); q=[[0.]*n for _ in range(n)]
 for i in range(n):
  for j in range(n):
   q[i][j]=(d[i] if i==j else 0.)
   if kind in ("session","both"): q[i][j]+=sess*sess
   if kind in ("ar1","both"): q[i][j]+=arsig*arsig*(rho**abs(i-j))
 return q
def score(blocks,a,d,kind,sess,arsig):
 q=cov(d,kind,sess,arsig,RHO); l=chol(q)
 aw=tr([forward(l,col) for col in tr(a)])
 nmat=mm(tr(aw),aw); ni=inv(nmat); logn=logdet_chol(chol(nmat))
 total=0.
 for y in blocks:
  yw=forward(l,y); rhs=mv(tr(aw),yw); x=mv(ni,rhs)
  res=[yw[i]-dot(aw[i],x) for i in range(len(yw))]
  total+=dot(res,res)
 return len(blocks)*logdet_chol(l)+len(blocks)*logn+total
def fit(blocks,a,d,kind):
 best=(float("inf"),None,None)
 sg=GRID if kind in ("session","both") else [0.]
 ag=GRID if kind in ("ar1","both") else [0.]
 for s in sg:
  for v in ag:
   z=score(blocks,a,d,kind,s,v)
   if z<best[0]: best=(z,s,v)
 return best
def generate(rng,truth,d,scenario):
 n=len(d); ses=rng.gauss(0,TAU) if scenario in ("session","both") else 0.
 # AR(1) process with stationary marginal standard deviation AR_SIGMA
 ar=[0.]*n
 if scenario in ("ar1","both"):
  ar[0]=rng.gauss(0,AR_SIGMA)
  for i in range(1,n):
   ar[i]=RHO*ar[i-1]+rng.gauss(0,AR_SIGMA*math.sqrt(1-RHO*RHO))
 return [truth[i]+ses+ar[i]+rng.gauss(0,math.sqrt(d[i])) for i in range(n)]
def main():
 rows,a,truth,d=load(); rng=random.Random(SEED)
 kinds=("independent","session","ar1","both")
 scenarios=("independent","session","ar1","both")
 print("EXERCISE O — COVARIANCE MODEL SELECTION")
 print(f"trials={TRIALS}; seed={SEED}; tau_session_mm={TAU}; ar1_sigma_mm={AR_SIGMA}; rho={RHO}")
 print("truth,selected_model,selection_fraction")
 for truth_kind in scenarios:
  counts={k:0 for k in kinds}
  for _ in range(TRIALS):
   blocks=[generate(rng,truth,d,truth_kind) for _ in range(12)]
   scores={k:fit(blocks,a,d,k)[0] for k in kinds}
   counts[min(scores,key=scores.get)]+=1
  for k in kinds: print(f"{truth_kind},{k},{counts[k]/TRIALS:.3f}")
 print("\nGrid estimates (mean over trials) for the correctly specified model:")
 for truth_kind in scenarios:
  if truth_kind=="independent": continue
  vals=[]
  for _ in range(TRIALS):
   blocks=[generate(rng,truth,d,truth_kind) for _ in range(12)]
   _,s,v=fit(blocks,a,d,truth_kind); vals.append((s,v))
  print(f"{truth_kind},session_sd_mm={sum(x[0] for x in vals)/TRIALS:.3f},ar1_sd_mm={sum(x[1] for x in vals)/TRIALS:.3f}")
 print("Scores are REML-style profile criteria over a coarse fixed grid; ties favour first model in declared order.")
 print("Synthetic-only; candidate covariance structures and rho are specified in advance.")
if __name__=="__main__": main()
