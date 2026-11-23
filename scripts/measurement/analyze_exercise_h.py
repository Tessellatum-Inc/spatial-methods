#!/usr/bin/env python3
"""Exercise H: Monte Carlo validation of single- and multiple-error detection.

Standard-library only. Synthetic linear height-network experiment. It simulates
independent Gaussian observation noise under the a-priori covariance model,
then applies one-shot Bonferroni-corrected Baarda-style standardized-residual
tests. The standardized residuals are correlated; simulation preserves that
dependence because all residuals are formed from the same simulated vector.
"""
import csv
import math
import random
from pathlib import Path

DATA = Path(__file__).resolve().parents[2] / "data" / "measurement" / "exercise-c-synthetic-control-network.csv"
POINTS = ("B", "C", "D", "E")
FIXED_POINT = "A"
SEED = 20261119
TRIALS = 20000
FAMILY_ALPHA = 0.01
TARGET_POWER = 0.80
ERROR_MULTIPLES = (0.5, 1.0, 1.5, 2.0)
DELTA_G = 4.13  # Exercise G: approximate single-test alpha=.001, power=.80


def solve(matrix, rhs):
    n = len(rhs)
    aug = [list(map(float, matrix[i])) + [float(rhs[i])] for i in range(n)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(aug[r][col]))
        if abs(aug[pivot][col]) < 1e-18:
            raise ValueError("Singular design matrix")
        aug[col], aug[pivot] = aug[pivot], aug[col]
        d = aug[col][col]
        aug[col] = [v / d for v in aug[col]]
        for r in range(n):
            if r != col:
                f = aug[r][col]
                aug[r] = [aug[r][j] - f * aug[col][j] for j in range(n + 1)]
    return [aug[i][-1] for i in range(n)]


def inverse(matrix):
    n = len(matrix)
    cols = [solve(matrix, [float(i == j) for i in range(n)]) for j in range(n)]
    return [[cols[j][i] for j in range(n)] for i in range(n)]


def normal_cdf(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def normal_quantile(p):
    lo, hi = -9.0, 9.0
    for _ in range(100):
        mid = (lo + hi) / 2.0
        if normal_cdf(mid) < p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def load_rows():
    with DATA.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        row["assumed_sigma_mm"] = float(row["assumed_sigma_mm"])
    return rows


def make_design(rows):
    n, u = len(rows), len(POINTS)
    a, sigmas = [], []
    for row in rows:
        coeff = [0.0] * u
        for point, sign in ((row["from_point"], -1.0), (row["to_point"], 1.0)):
            if point != FIXED_POINT:
                coeff[POINTS.index(point)] += sign
        a.append(coeff)
        sigmas.append(row["assumed_sigma_mm"] / 1000.0)
    p = [1.0 / (s*s) for s in sigmas]
    normal = [[sum(a[k][i]*p[k]*a[k][j] for k in range(n))
               for j in range(u)] for i in range(u)]
    qx = inverse(normal)
    # B maps observation errors to least-squares residuals: v = (H-I)e.
    b = []
    for i in range(n):
        row = []
        for j in range(n):
            h = p[j] * sum(a[i][k]*qx[k][m]*a[j][m]
                           for k in range(u) for m in range(u))
            row.append(h - (1.0 if i == j else 0.0))
        b.append(row)
    qvv_diag = [sum(b[i][j]**2 * sigmas[j]**2 for j in range(n))
                for i in range(n)]
    standardizers_mm = [math.sqrt(v) * 1000.0 for v in qvv_diag]
    # Standardized-residual response to a +1 mm bias in each observation.
    response = [[b[i][j] / standardizers_mm[i] for j in range(n)]
                for i in range(n)]
    redundancy = [qvv_diag[i] / (sigmas[i]**2) for i in range(n)]
    mdb_g_mm = [DELTA_G * sigmas[i] * 1000.0 / math.sqrt(redundancy[i])
                for i in range(n)]
    return {"rows": rows, "sigmas": sigmas, "response": response,
            "redundancy": redundancy, "mdb_g": mdb_g_mm, "dof": n-u}


def simulate(model, bias_mm_by_index, trials, rng, critical):
    n = len(model["rows"])
    sigma = model["sigmas"]
    response = model["response"]
    true_ids = set(bias_mm_by_index)
    any_detect = all_detect = exact_set = false_alarm = missed = wrong_only = 0
    for _ in range(trials):
        errors_mm = [rng.gauss(0.0, sigma[i]*1000.0) +
                     bias_mm_by_index.get(i, 0.0) for i in range(n)]
        w = [sum(response[i][j] * errors_mm[j] for j in range(n))
             for i in range(n)]
        flagged = {i for i, value in enumerate(w) if abs(value) > critical}
        detected_true = flagged & true_ids
        any_detect += int(bool(flagged))
        all_detect += int(detected_true == true_ids and bool(true_ids))
        exact_set += int(flagged == true_ids)
        false_alarm += int(bool(flagged - true_ids))
        missed += int(bool(true_ids - flagged))
        wrong_only += int(bool(flagged) and not bool(detected_true))
    rate = lambda x: x / trials
    return {"any_flag": rate(any_detect), "all_true_detected": rate(all_detect),
            "exact_set": rate(exact_set), "false_alarm_any": rate(false_alarm),
            "miss_any": rate(missed), "wrong_only": rate(wrong_only)}


def mc_se(p, n):
    return math.sqrt(p*(1.0-p)/n)


def pct(p):
    return f"{100*p:.1f}%"


def main():
    base = load_rows()
    proposed = dict(observation_id="BE", from_point="B", to_point="E",
                    assumed_sigma_mm=1.6)
    designs = [("Baseline 9 observations", base),
               ("Augmented 10 observations (+ B-E)", base + [proposed])]
    rng = random.Random(SEED)
    print("EXERCISE H — MONTE CARLO RELIABILITY SIMULATION")
    print("SYNTHETIC ONLY — NOT FIELD PERFORMANCE OR A SURVEY SPECIFICATION")
    print(f"Seed={SEED}; trials per scenario={TRIALS:,}; family-wise alpha={FAMILY_ALPHA:.3f}")
    print("Independent Gaussian observation errors use the stated a-priori sigmas.")
    print("All standardized residuals are computed together from each simulated vector;")
    print("their dependence is therefore retained, not simulated as independent tests.")
    print("Decision: one-shot two-sided standardized-residual test with Bonferroni")
    print("critical value controlling the family-wise false-alarm probability.")
    for label, rows in designs:
        model = make_design(rows)
        n = len(rows)
        critical = normal_quantile(1.0 - FAMILY_ALPHA/(2.0*n))
        delta_family = critical + normal_quantile(TARGET_POWER)
        mdb_family = [delta_family * s * 1000.0 / math.sqrt(r)
                      for s, r in zip(model["sigmas"], model["redundancy"])]
        print(f"\n{label}: n={n}, unknowns=4, dof={model['dof']}, critical={critical:.3f}")
        null = simulate(model, {}, TRIALS, rng, critical)
        print(f"Noise-only simulation (FWER): {pct(null['false_alarm_any'])} "
              f"(Monte Carlo SE {100*mc_se(null['false_alarm_any'], TRIALS):.2f} percentage points)")
        print("Observation-level design and single-error detection")
        print("id,r,MDB_G_mm,MDB_FWER80_mm")
        for i, row in enumerate(rows):
            print(f"{row['observation_id']},{model['redundancy'][i]:.3f},"
                  f"{model['mdb_g'][i]:.2f},{mdb_family[i]:.2f}")
        weak = min(range(n), key=lambda i: model["redundancy"][i])
        strong = max(range(n), key=lambda i: model["redundancy"][i])
        for idx in sorted(set((weak, strong))):
            print(f"  Inject {rows[idx]['observation_id']} gross error:")
            for mult in ERROR_MULTIPLES:
                bias = {idx: mult*mdb_family[idx]}
                result = simulate(model, bias, TRIALS, rng, critical)
                print(f"    {mult:.1f}x family-wise MDB ({bias[idx]:.2f} mm): "
                      f"true observation detected={pct(result['all_true_detected'])}; "
                      f"exactly correct flagged set={pct(result['exact_set'])}; "
                      f"false flag elsewhere={pct(result['false_alarm_any'])}; "
                      f"missed={pct(result['miss_any'])}; "
                      f"wrong-only identification={pct(result['wrong_only'])}")
        pair = sorted(range(n), key=lambda i: model["redundancy"][i])[:2]
        for sign, label2 in ((1.0, "same-sign"), (-1.0, "opposite-sign")):
            biases = {pair[0]: mdb_family[pair[0]],
                      pair[1]: sign*mdb_family[pair[1]]}
            result = simulate(model, biases, TRIALS, rng, critical)
            print(f"  Two-error stress ({label2}; "
                  f"{rows[pair[0]]['observation_id']} and {rows[pair[1]]['observation_id']}): "
                  f"both detected={pct(result['all_true_detected'])}; "
                  f"exactly correct flagged set={pct(result['exact_set'])}; "
                  f"missed at least one={pct(result['miss_any'])}; "
                  f"false flag elsewhere={pct(result['false_alarm_any'])}; "
                  f"wrong-only identification={pct(result['wrong_only'])}")
    print("\nInterpretation guardrails:")
    print("- Exercise G MDB (delta0=4.13) and this family-wise MDB are different")
    print("  because the latter uses a stricter per-test Bonferroni threshold.")
    print("- The family-wise MDB is a normal-theory planning approximation; empirical")
    print("  detection rates need not equal 80% exactly because residual tests are")
    print("  correlated and the largest-residual selection is a joint decision.")
    print("- 'True observation detected' means each injected observation crossed the")
    print("  threshold; 'exact set' additionally requires no innocent observation flagged.")
    print("- Two simultaneous biases violate the single-outlier alternative underlying")
    print("  the simple MDB formula; masking/swamping are assessed empirically.")
    print("- No observations are automatically deleted. Investigation and independent")
    print("  checks remain necessary.")


if __name__ == "__main__":
    main()
