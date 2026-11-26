#!/usr/bin/env python3
"""Auditable two-stage probability sampling and weighted accuracy analysis.

Frame CSV columns: unit_id,stratum,psu_id (optional: x,y,map_class,confidence).
Draw specification JSON maps each stratum to n_psu and n_units_per_psu.
Stage 1: SRS without replacement of PSUs within stratum.
Stage 2: SRS without replacement of units within selected PSU.
Inclusion probability = (n_psu / N_psu) * (n_units / N_units_in_selected_psu).
Analysis is Horvitz-Thompson weighted descriptive estimation; variance estimation
for clustered designs is intentionally not implemented and is not implied.
"""
from __future__ import annotations
import argparse, csv, json, math, random
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

REQUIRED = {"unit_id", "stratum", "psu_id"}

def read_csv(path):
    with Path(path).open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def write_csv(path, rows):
    rows=list(rows)
    if not rows: raise ValueError("Refusing to write empty CSV.")
    p=Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", newline="", encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)

def audit_frame(rows):
    if not rows: raise ValueError("Sampling frame is empty.")
    missing=REQUIRED-set(rows[0])
    if missing: raise ValueError(f"Missing required frame columns: {sorted(missing)}")
    seen=set(); groups=defaultdict(lambda: defaultdict(list))
    for i,r in enumerate(rows,1):
        uid=str(r.get("unit_id","")).strip(); s=str(r.get("stratum","")).strip(); p=str(r.get("psu_id","")).strip()
        if not uid or not s or not p: raise ValueError(f"Frame row {i}: unit_id, stratum and psu_id required.")
        if uid in seen: raise ValueError(f"Duplicate unit_id: {uid}")
        seen.add(uid); groups[s][p].append(r)
        for field in ("x","y"):
            if field in r and r[field] not in ("",None):
                try: v=float(r[field])
                except ValueError as e: raise ValueError(f"Frame row {i}: {field} must be numeric.") from e
                if not math.isfinite(v): raise ValueError(f"Frame row {i}: {field} must be finite.")
    report={"total_units":len(rows),"strata":{}}
    for s,psus in sorted(groups.items()):
        report["strata"][s]={"population_units":sum(len(v) for v in psus.values()),"psu_count":len(psus),"psus":{p:len(v) for p,v in sorted(psus.items())}}
    return report

def draw_sample(rows, specification, seed):
    report=audit_frame(rows)
    rng=random.Random(int(seed))
    groups=defaultdict(lambda: defaultdict(list))
    for row in rows: groups[row["stratum"]][row["psu_id"]].append(row)
    if set(specification)!=set(groups):
        raise ValueError("Draw specification must include exactly every frame stratum.")
    output=[]
    for s,psus in sorted(groups.items()):
        cfg=specification[s]
        n_psu=int(cfg["n_psu"]); n_units=int(cfg["n_units_per_psu"])
        all_psus=sorted(psus)
        if n_psu<1 or n_psu>len(all_psus): raise ValueError(f"{s}: n_psu outside PSU population.")
        selected=rng.sample(all_psus,n_psu)
        pi1=n_psu/len(all_psus)
        for p in sorted(selected):
            population=sorted(psus[p],key=lambda r:r["unit_id"])
            if n_units<1 or n_units>len(population): raise ValueError(f"{s}/{p}: n_units_per_psu outside PSU population.")
            selected_units=rng.sample(population,n_units)
            pi2=n_units/len(population)
            for r in selected_units:
                out=dict(r)
                out.update({"draw_seed":int(seed),"stage1_inclusion_probability":pi1,"stage2_inclusion_probability":pi2,"overall_inclusion_probability":pi1*pi2,"analysis_weight":1/(pi1*pi2),"selected_psu_count":n_psu,"psu_population_count":len(all_psus),"selected_units_per_psu":n_units,"psu_unit_population_count":len(population)})
                output.append(out)
    output.sort(key=lambda r:(r["stratum"],r["psu_id"],r["unit_id"]))
    return output,report

def weighted_accuracy(rows, map_field="map_class", ref_field="reference_class", weight_field="analysis_weight"):
    if not rows: raise ValueError("No labelled sampled rows.")
    matrix=defaultdict(float); map_tot=defaultdict(float); ref_tot=defaultdict(float); total=0.0
    classes=set()
    for i,r in enumerate(rows,1):
        m=str(r.get(map_field,"")).strip(); ref=str(r.get(ref_field,"")).strip()
        try: w=float(r.get(weight_field,""))
        except (TypeError,ValueError) as e: raise ValueError(f"Row {i}: invalid weight.") from e
        if not m or not ref or not math.isfinite(w) or w<=0: raise ValueError(f"Row {i}: classes and positive finite weight required.")
        matrix[(m,ref)]+=w; map_tot[m]+=w; ref_tot[ref]+=w; total+=w; classes|={m,ref}
    labels=sorted(classes)
    cells={m:{r:matrix[(m,r)]/total for r in labels} for m in labels}
    diagonal=sum(matrix[(c,c)] for c in labels)
    ua={m: (matrix[(m,m)]/map_tot[m] if map_tot[m] else None) for m in labels}
    pa={r: (matrix[(r,r)]/ref_tot[r] if ref_tot[r] else None) for r in labels}
    return {"total_weight":total,"weighted_confusion_matrix_proportions":cells,"overall_accuracy":diagonal/total,"users_accuracy":ua,"producers_accuracy":pa,"weighted_map_class_proportions":{k:v/total for k,v in map_tot.items()},"weighted_reference_class_proportions":{k:v/total for k,v in ref_tot.items()},"variance_or_confidence_intervals":"NOT ESTIMATED: this implementation does not provide design-based variance for two-stage clustered sampling."}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest="command",required=True)
    a=sub.add_parser("audit-frame"); a.add_argument("frame"); a.add_argument("--json-out",required=True)
    d=sub.add_parser("draw"); d.add_argument("frame"); d.add_argument("specification"); d.add_argument("--seed",type=int,required=True); d.add_argument("--csv-out",required=True); d.add_argument("--json-out",required=True)
    z=sub.add_parser("analyze"); z.add_argument("sample"); z.add_argument("--json-out",required=True)
    args=p.parse_args()
    if args.command=="audit-frame":
        result=audit_frame(read_csv(args.frame))
    elif args.command=="draw":
        rows=read_csv(args.frame); spec=json.loads(Path(args.specification).read_text())
        sample,report=draw_sample(rows,spec,args.seed); write_csv(args.csv_out,sample)
        result={"generated_at_utc":datetime.now(timezone.utc).isoformat(),"seed":args.seed,"frame_audit":report,"sample_count":len(sample),"design":"Two-stage stratified SRSWOR of PSUs and units within selected PSUs","limitations":["This is not spatially balanced sampling.","PSUs are assumed to be non-overlapping units defined in the frame.","Analysis weights are inverse inclusion probabilities.","No clustered design variance estimator is provided."]}
    else: result=weighted_accuracy(read_csv(args.sample))
    out=Path(args.json_out); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))
if __name__=="__main__": main()
