#!/usr/bin/env python3
"""Exercise G: internal/external reliability and simple network design scenarios.

Standard-library only. All observations and proposed additions are synthetic.
The normal-theory design criterion is a nominal two-sided single-test alpha
of 0.001 and power 0.80, represented by noncentrality delta0 ~= 4.13.
This is not a family-wise nine-test guarantee or a survey standard.
"""
import csv
import math
from pathlib import Path

DATA = Path(__file__).resolve().parents[2] / "data" / "measurement" / "exercise-c-synthetic-control-network.csv"
POINTS = ("B", "C", "D", "E")
FIXED_POINT = "A"
DELTA0 = 4.13
BASE_SIGMA_SCALE = 1.0
PRECISION_IMPROVEMENT_SCALE = 0.80
# Proposed new independent B-E height-difference observation.
PROPOSED_BE = {
    "observation_id": "BE",
    "from_point": "B",
    "to_point": "E",
    "length_km": 1.1,
    "observed_delta_h_m": 1.1998,
    "assumed_sigma_mm": 1.6,
}


def solve(matrix, rhs):
    n = len(rhs)
    aug = [list(map(float, matrix[i])) + [float(rhs[i])] for i in range(n)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(aug[r][col]))
        if abs(aug[pivot][col]) < 1e-18:
            raise ValueError("Singular design: datum or connectivity problem")
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [v / scale for v in aug[col]]
        for r in range(n):
            if r != col:
                f = aug[r][col]
                aug[r] = [aug[r][j] - f * aug[col][j] for j in range(n + 1)]
    return [aug[i][-1] for i in range(n)]


def inverse(matrix):
    n = len(matrix)
    cols = [solve(matrix, [1.0 if i == j else 0.0 for i in range(n)])
            for j in range(n)]
    return [[cols[j][i] for j in range(n)] for i in range(n)]


def load_rows():
    with DATA.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        for key in ("length_km", "observed_delta_h_m", "assumed_sigma_mm"):
            row[key] = float(row[key])
    return rows


def design_metrics(rows):
    n, u = len(rows), len(POINTS)
    a_matrix, sigmas = [], []
    for row in rows:
        coeff = [0.0] * u
        for point, sign in ((row["from_point"], -1.0),
                            (row["to_point"], 1.0)):
            if point == FIXED_POINT:
                continue
            if point not in POINTS:
                raise ValueError("Unknown point " + point)
            coeff[POINTS.index(point)] += sign
        sigma = row["assumed_sigma_mm"] / 1000.0
        if sigma <= 0:
            raise ValueError("Uncertainties must be positive")
        a_matrix.append(coeff)
        sigmas.append(sigma)

    # Independent observation model: P is diagonal.
    p_diag = [1.0 / (s * s) for s in sigmas]
    normal = [[sum(a_matrix[k][i] * p_diag[k] * a_matrix[k][j]
                   for k in range(n)) for j in range(u)] for i in range(u)]
    qx = inverse(normal)

    # R = I - A (A' P A)^-1 A' P. Its diagonal entries are redundancy numbers.
    redundancy = []
    for k in range(n):
        absorbed = sum(a_matrix[k][i] * qx[i][j] * a_matrix[k][j]
                       for i in range(u) for j in range(u)) * p_diag[k]
        redundancy.append(1.0 - absorbed)

    if any(r <= 1e-10 for r in redundancy):
        raise ValueError("At least one observation is effectively uncontrolled")

    mdb_mm = [DELTA0 * sigmas[k] * 1000.0 / math.sqrt(redundancy[k])
              for k in range(n)]

    # Parameter effect if an observation contains its own MDB-sized bias.
    # dx = Qx a_i' p_i * MDB_i. Report largest absolute coordinate effect.
    external = []
    for k in range(n):
        dx = [sum(qx[i][j] * a_matrix[k][j] for j in range(u))
              * p_diag[k] * (mdb_mm[k] / 1000.0) * 1000.0
              for i in range(u)]
        external.append(dx)

    return {
        "redundancy": redundancy,
        "mdb_mm": mdb_mm,
        "external_mm": external,
        "qx_mm2": [[v * 1e6 for v in row] for row in qx],
        "dof": n - u,
    }


def report(label, rows):
    m = design_metrics(rows)
    max_external = max(abs(v) for vec in m["external_mm"] for v in vec)
    trace_qx = sum(m["qx_mm2"][i][i] for i in range(len(POINTS)))
    print("\n" + label)
    print(f"observations={len(rows)}; unknowns=4; redundancy/DOF={m['dof']}")
    print(f"minimum redundancy number={min(m['redundancy']):.3f}")
    print(f"maximum MDB={max(m['mdb_mm']):.3f} mm; "
          f"mean MDB={sum(m['mdb_mm'])/len(m['mdb_mm']):.3f} mm")
    print(f"maximum absolute coordinate effect at MDB={max_external:.3f} mm")
    print(f"trace of formal parameter covariance={trace_qx:.3f} mm^2")
    print("id,redundancy_number,MDB_mm,max_abs_coordinate_effect_mm")
    for row, r, mdb, ext in zip(rows, m["redundancy"], m["mdb_mm"],
                                m["external_mm"]):
        print(f"{row['observation_id']},{r:.3f},{mdb:.3f},"
              f"{max(abs(v) for v in ext):.3f}")
    return m


def main():
    base = load_rows()
    proposed = dict(PROPOSED_BE)
    precision = [dict(r) for r in base]
    for row in precision:
        row["assumed_sigma_mm"] *= PRECISION_IMPROVEMENT_SCALE

    print("SYNTHETIC NETWORK-DESIGN STUDY — NOT A FIELD SURVEY")
    print("A is treated as exact; observation errors are independent.")
    print(f"MDB design noncentrality delta0={DELTA0:.2f}; approximate")
    print("two-sided single-test alpha=0.001 and power=0.80 normal criterion.")
    print("This is not a simultaneous family-wise error guarantee.")
    original = report("A. Existing nine-observation network", base)
    augmented = report("B. Add one independent B-E observation (sigma=1.6 mm)",
                       base + [proposed])
    improved = report("C. Improve every original observation sigma by 20%",
                      precision)

    print("\nD. Design comparison")
    for label, m in (("existing", original), ("add_BE", augmented),
                     ("precision_minus_20pct", improved)):
        print(f"{label}: min_r={min(m['redundancy']):.3f}; "
              f"max_MDB={max(m['mdb_mm']):.3f} mm; "
              f"trace_Qx={sum(m['qx_mm2'][i][i] for i in range(4)):.3f} mm^2")
    print("\nInterpretation:")
    print("- The B-E link improves the weakest redundancy number and formal precision.")
    print("- Improving all observation precisions reduces MDB and parameter covariance,")
    print("  but does not change the redundancy numbers because geometry is unchanged.")
    print("- These are design diagnostics under the assumed model, not guarantees.")
    print("- Real planning must include control uncertainty, correlated errors, access,")
    print("  occupation/session independence, costs and field-specific tolerances.")


if __name__ == "__main__":
    main()
