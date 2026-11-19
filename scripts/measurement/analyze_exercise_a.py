#!/usr/bin/env python3
"""Reproduce the calculations in Exercise A using only the Python standard library."""
import csv
import math
from collections import defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parents[2] / "data" / "measurement" / "exercise-a-synthetic-observations.csv"


def mean(values):
    return sum(values) / len(values)


def sample_sd(values):
    m = mean(values)
    return math.sqrt(sum((x - m) ** 2 for x in values) / (len(values) - 1))


def circular_mean_deg(values):
    radians = [math.radians(x) for x in values]
    return math.degrees(math.atan2(mean([math.sin(x) for x in radians]),
                                   mean([math.cos(x) for x in radians]))) % 360.0


def wrap_degrees(value):
    return (value + 180.0) % 360.0 - 180.0


def dms_string(degrees):
    total_seconds = degrees * 3600.0
    d = int(total_seconds // 3600)
    remainder = total_seconds - d * 3600
    m = int(remainder // 60)
    s = remainder - m * 60
    return f"{d}° {m:02d}′ {s:06.3f}″"


with DATA.open(newline="", encoding="utf-8") as handle:
    rows = list(csv.DictReader(handle))

distances = [float(row["distance_m"]) for row in rows]
angles = [float(row["horizontal_angle_deg"]) for row in rows]
blocks = defaultdict(list)
for row in rows:
    blocks[row["block"]].append(row)

n = len(rows)
d_mean = mean(distances)
d_sd = sample_sd(distances)
d_sem = d_sd / math.sqrt(n)

a_mean = circular_mean_deg(angles)
a_residuals_sec = [wrap_degrees(value - a_mean) * 3600.0 for value in angles]
a_sd_sec = sample_sd(a_residuals_sec)
a_sem_sec = a_sd_sec / math.sqrt(n)

# Illustrative Type B standard uncertainties, not real instrument specifications.
u_resolution_mm = 0.5 / math.sqrt(3.0)
u_prism_mm = 0.5
u_scale_mm = 2.0e-6 * d_mean * 1000.0
u_type_a_mm = d_sem * 1000.0
u_combined_mm = math.sqrt(u_type_a_mm**2 + u_resolution_mm**2 +
                          u_prism_mm**2 + u_scale_mm**2)

print("SYNTHETIC DATA ONLY — NOT FIELD EVIDENCE")
print(f"Observations: {n}")
print(f"Distance mean: {d_mean:.6f} m")
print(f"Distance sample SD: {d_sd*1000:.3f} mm")
print(f"Distance standard uncertainty of mean (Type A): {d_sem*1000:.3f} mm")
print(f"Distance range: {min(distances):.3f} to {max(distances):.3f} m")
print(f"Angle circular mean: {dms_string(a_mean)}")
print(f"Angle sample SD: {a_sd_sec:.3f} arcsec")
print(f"Angle standard uncertainty of mean (Type A): {a_sem_sec:.3f} arcsec")
print("Block means:")
for block in sorted(blocks):
    block_rows = blocks[block]
    print(f"  {block}: distance={mean([float(r['distance_m']) for r in block_rows]):.6f} m; "
          f"angle={dms_string(circular_mean_deg([float(r['horizontal_angle_deg']) for r in block_rows]))}")
print("Illustrative distance uncertainty budget:")
print(f"  Type A: {u_type_a_mm:.3f} mm")
print(f"  Resolution: {u_resolution_mm:.3f} mm")
print(f"  Prism constant: {u_prism_mm:.3f} mm")
print(f"  EDM scale: {u_scale_mm:.3f} mm")
print(f"  Combined standard uncertainty: {u_combined_mm:.3f} mm")
print(f"  Expanded uncertainty (k=2): {2*u_combined_mm:.3f} mm")
print("Angle result is repeatability-only; no complete angle uncertainty budget is claimed.")
