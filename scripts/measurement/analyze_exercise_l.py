#!/usr/bin/env python3
"""Exercise L: block-robust generalized least squares for correlated sessions.
Standard library only. Synthetic teaching simulation; never edits source data.
"""
import csv
import math
import random
from pathlib import Path

DATA = Path(__file__).resolve().parents[2] / "data" / "measurement" / "exercise-d-stochastic-control-network.csv"
POINTS = ("A", "B", "C", "D", "E")
TRUE = (100.0, 101.2, 102.0, 101.7, 102.4)
CONTROL_SIGMA_MM = 2.0
SESSION_COMMON_SIGMA_MM = 0.35
HUBER_C = 1.5
TRIALS = 5000
SEED = 20261119

def transpose(a):
    return [list(v) for v in zip(*a)]

def matmul(a, b):
    bt = transpose(b)
    return [[sum(x*y for x, y in zip(row, col)) for col in bt] for row in a]

def matvec(a, x):
    return [sum(v*w for v, w in zip(row, x)) for row in a]

def solve(a, b):
    n = len(b)
    m = [list(map(float, a[i])) + [float(b[i])] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        if abs(m[p][c]) < 1e-22:
            raise ValueError("Singular normal matrix")
        m[c], m[p] = m[p], m[c]
        z = m[c][c]
        m[c] = [v/z for v in m[c]]
        for r in range(n):
            if r != c:
                z = m[r][c]
                m[r] = [m[r][j] - z*m[c][j] for j in range(n+1)]
    return [m[i][-1] for i in range(n)]

def inverse(a):
    n = len(a)
    cols = [solve(a, [float(i == j) for i in range(n)]) for j in range(n)]
    return [[cols[j][i] for j in range(n)] for i in range(n)]

def cholesky(a):
    n = len(a)
    l = [[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1):
            v = a[i][j] - sum(l[i][k]*l[j][k] for k in range(j))
            if i == j:
                if v <= 0:
                    raise ValueError("Covariance block must be positive definite")
                l[i][j] = math.sqrt(v)
            else:
                l[i][j] = v/l[j][j]
    return l

def forward(l, b):
    x = []
    for i in range(len(b)):
        x.append((b[i] - sum(l[i][j]*x[j] for j in range(i)))/l[i][i])
    return x

def read_rows():
    with DATA.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["observed_delta_h_m"] = float(r["observed_delta_h_m"])
        r["assumed_sigma_mm"] = float(r["assumed_sigma_mm"])
    return rows

def system(rows, observations=None):
    obs = observations or [r["observed_delta_h_m"] for r in rows]
    a, y = [], []
    for r, value in zip(rows, obs):
        v = [0.0]*5
        v[POINTS.index(r["from_point"])] -= 1.0
        v[POINTS.index(r["to_point"])] += 1.0
        a.append(v)
        y.append(value)
    a.append([1.0, 0.0, 0.0, 0.0, 0.0])
    y.append(100.001)
    n = len(rows)+1
    q = [[0.0]*n for _ in range(n)]
    for i, r in enumerate(rows):
        q[i][i] += (r["assumed_sigma_mm"]/1000.0)**2
        for j, other in enumerate(rows):
            if r["session_id"] == other["session_id"]:
                q[i][j] += (SESSION_COMMON_SIGMA_MM/1000.0)**2
    q[-1][-1] = (CONTROL_SIGMA_MM/1000.0)**2
    blocks = []
    for session in sorted({r["session_id"] for r in rows}):
        blocks.append([i for i, r in enumerate(rows) if r["session_id"] == session])
    blocks.append([len(rows)])
    return a, y, q, blocks

def fit_gls(a, y, q):
    p = inverse(q)
    at = transpose(a)
    normal = matmul(matmul(at, p), a)
    cov = inverse(normal)
    x = solve(normal, matvec(matmul(at, p), y))
    return x, cov

def fit_block_huber(a, y, q, blocks):
    aw, yw = [], []
    for ids in blocks:
        qb = [[q[i][j] for j in ids] for i in ids]
        lb = cholesky(qb)
        ab = [[a[i][j] for j in range(len(a[0]))] for i in ids]
        aw.append([forward(lb, col) for col in transpose(ab)])
        yw.append(forward(lb, [y[i] for i in ids]))
    weights = [1.0]*len(blocks)
    for _ in range(100):
        normal = [[0.0]*5 for _ in range(5)]
        rhs = [0.0]*5
        for k in range(len(blocks)):
            at = transpose(aw[k])
            nb = matmul(at, aw[k])
            rb = matvec(at, yw[k])
            for i in range(5):
                rhs[i] += weights[k]*rb[i]
                for j in range(5):
                    normal[i][j] += weights[k]*nb[i][j]
        x = solve(normal, rhs)
        updated = []
        for k in range(len(blocks)):
            residual = [sum(aw[k][i][j]*x[j] for j in range(5))-yw[k][i] for i in range(len(yw[k]))]
            scaled_norm = math.sqrt(sum(v*v for v in residual)/len(residual))
            updated.append(1.0 if scaled_norm <= HUBER_C else HUBER_C/scaled_norm)
        if max(abs(updated[i]-weights[i]) for i in range(len(weights))) < 1e-9:
            weights = updated
            break
        weights = updated
    return x, weights

def true_difference(r):
    return TRUE[POINTS.index(r["to_point"])]-TRUE[POINTS.index(r["from_point"])]

def rmse_mm(x):
    return math.sqrt(sum((1000*(x[i]-TRUE[i]))**2 for i in range(5))/5)

def mean_se(values):
    mean = sum(values)/len(values)
    variance = sum((v-mean)**2 for v in values)/(len(values)-1)
    return mean, math.sqrt(variance/len(values))

def main():
    rows = read_rows()
    a, y0, q, blocks = system(rows)
    xg, _ = fit_gls(a, y0, q)
    print("EXERCISE L — SYNTHETIC CORRELATED-ERROR ROBUST ADJUSTMENT")
    print(f"trials={TRIALS}; seed={SEED}; common_session_sigma={SESSION_COMMON_SIGMA_MM:.2f} mm; Huber_c={HUBER_C}")
    print("case,method,mean_coordinate_RMSE_mm,MC_SE_mm")
    scenarios = ("clean", "CE_plus_20mm", "S1_common_plus_4mm", "S1_plus_3_S2_minus_3mm")
    rng = random.Random(SEED)
    results = {case: {m: [] for m in ("GLS", "Diagonal_WLS", "Block_Huber_GLS")} for case in scenarios}
    block_weight_means = {case: [0.0]*len(blocks) for case in scenarios}
    for _ in range(TRIALS):
        # Generate noise from the full covariance, including shared session effects.
        independent = [rng.gauss(0.0, 1.0) for _ in range(len(q))]
        lower = cholesky(q)
        noise = [sum(lower[i][j]*independent[j] for j in range(i+1)) for i in range(len(q))]
        base = [true_difference(r)+noise[i] for i, r in enumerate(rows)]
        base.append(100.0+noise[-1])
        for case in scenarios:
            obs = list(base)
            if case == "CE_plus_20mm":
                obs[8] += 0.020
            elif case == "S1_common_plus_4mm":
                for i, r in enumerate(rows):
                    if r["session_id"] == "S1":
                        obs[i] += 0.004
            elif case == "S1_plus_3_S2_minus_3mm":
                for i, r in enumerate(rows):
                    obs[i] += 0.003 if r["session_id"] == "S1" else -0.003
            for method in ("GLS", "Diagonal_WLS"):
                qq = q if method == "GLS" else [[q[i][i] if i == j else 0.0 for j in range(len(q))] for i in range(len(q))]
                estimate, _ = fit_gls(a, obs, qq)
                results[case][method].append(rmse_mm(estimate))
            estimate, weights = fit_block_huber(a, obs, q, blocks)
            results[case]["Block_Huber_GLS"].append(rmse_mm(estimate))
            for i, w in enumerate(weights):
                block_weight_means[case][i] += w/TRIALS
    for case in scenarios:
        for method in ("GLS", "Diagonal_WLS", "Block_Huber_GLS"):
            m, se = mean_se(results[case][method])
            print(f"{case},{method},{m:.3f},{se:.3f}")
    print("\nMean final block weights for Block Huber GLS (1.0 means no downweighting):")
    for case in scenarios:
        print(case+","+",".join(f"{v:.3f}" for v in block_weight_means[case]))
    print("\nBlock order: S1, S2, stochastic control.")
    print("The robust loss acts on each whitened session block as a whole, not on raw rows independently.")
    print("This is an illustrative block-Huber objective, not a calibrated hypothesis test or universal robust GLS solution.")
    print("Only two session groups are available; performance and tuning are highly scenario-dependent.")
    print("Source CSV is read-only. All generated noise and gross errors are synthetic.")

if __name__ == "__main__":
    main()
