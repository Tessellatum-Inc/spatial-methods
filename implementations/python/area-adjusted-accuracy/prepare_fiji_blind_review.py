#!/usr/bin/env python3
"""Rank label-blind Fiji imagery candidates and prepare a human review worksheet."""
from __future__ import annotations
import argparse, csv, json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

RANK_FIELDS = ["sample_id","candidate_rank","item_id","collection","datetime","month","platform",
"cloud_cover_percent","status","core_10m_complete","all_requested_bands_complete","scl_available",
"analysis_valid_fraction","cloud_shadow_fraction","analysis_valid_pixels","scl_pixels","missing_bands",
"rgb_chip_file","rgb_match_method","rgb_datetime","rgb_datetime_delta_seconds","rgb_chip_sha256","ranking_basis"]
REVIEW_FIELDS = ["sample_id","longitude","latitude","primary_candidate_item_id","primary_candidate_datetime",
"primary_rgb_chip_file","primary_rgb_match_status","primary_rgb_datetime","primary_rgb_datetime_delta_seconds",
"alternate_candidate_item_ids","alternate_candidate_dates","alternate_candidate_rgb_files","rgb_chip_inventory",
"evidence_quality_note","reviewer_id","reviewer_role","review_datetime","interpreted_class","confidence_1_5",
"ambiguity_flag","alternative_class","temporal_consistency","visible_evidence","spectral_context_notes",
"limitations","decision_status","adjudication_notes"]

def read_csv(path):
    with Path(path).open(newline="",encoding="utf-8-sig") as f: return list(csv.DictReader(f))
def parse_json(value,default):
    try: return json.loads(value) if value else default
    except (TypeError,ValueError): return default
def number(value):
    try:
        n=float(value)
        return n if n==n and abs(n)!=float("inf") else None
    except (TypeError,ValueError): return None
def parse_dt(value):
    try: return datetime.fromisoformat(str(value).replace("Z","+00:00"))
    except (TypeError,ValueError): return None
def date_key(value):
    d=parse_dt(value)
    return (d.month,d.isoformat()) if d else (0,str(value or ""))
def chip_path(row):
    return "chips/"+Path(row.get("chip_file","")).name if row.get("chip_file") else ""

def match_rgb(candidate, rows):
    exact=[r for r in rows if r.get("item_id")==candidate.get("item_id")]
    possible=exact or []
    if not possible:
        cdt=parse_dt(candidate.get("datetime"))
        if cdt:
            for r in rows:
                rdt=parse_dt(r.get("datetime"))
                if r.get("platform")==candidate.get("platform") and rdt and abs((rdt-cdt).total_seconds())<=2:
                    possible.append(r)
    if not possible: return None
    chosen=possible[0] if exact else min(possible,key=lambda r:abs((parse_dt(r["datetime"])-parse_dt(candidate["datetime"])).total_seconds()))
    delta=abs((parse_dt(chosen["datetime"])-parse_dt(candidate["datetime"])).total_seconds())
    return {"file":chip_path(chosen),"method":"exact_item_id" if exact else "same_platform_datetime_within_2s",
            "datetime":chosen.get("datetime",""),"delta":f"{delta:.3f}","sha":chosen.get("chip_sha256","")}

def prepare(multispectral_csv,blind_points_csv,output_dir,rgb_csv=None):
    spectral=read_csv(multispectral_csv); points=read_csv(blind_points_csv)
    if not points or not {"sample_id","longitude","latitude"}.issubset(points[0]):
        raise ValueError("Blind points CSV must contain sample_id, longitude, latitude")
    required={"sample_id","item_id","datetime","status","bands_read","missing_bands","indices"}
    if spectral and not required.issubset(spectral[0]): raise ValueError(f"Multispectral CSV must contain {sorted(required)}")
    rgb_by_point=defaultdict(list)
    if rgb_csv and Path(rgb_csv).exists():
        for r in read_csv(rgb_csv):
            if r.get("sample_id") and r.get("chip_file") and r.get("status")=="chip_created":
                rgb_by_point[r["sample_id"]].append(r)
    grouped=defaultdict(list)
    for r in spectral:
        bands=set(parse_json(r.get("bands_read"),[])); missing=parse_json(r.get("missing_bands"),[])
        indices=parse_json(r.get("indices"),{}); scl=indices.get("SCL_QA_20m",{}) if isinstance(indices,dict) else {}
        scl_ok=isinstance(scl,dict) and "analysis_valid_fraction" in scl
        valid=number(scl.get("analysis_valid_fraction")) if scl_ok else None
        shadow=number(scl.get("cloud_shadow_fraction")) if scl_ok else None
        core={"B02","B03","B04","B08"}.issubset(bands)
        cloud=number(r.get("cloud_cover_percent"))
        x={"sample_id":r.get("sample_id",""),"item_id":r.get("item_id",""),"collection":r.get("collection",""),
        "datetime":r.get("datetime",""),"month":date_key(r.get("datetime",""))[0],"platform":r.get("platform",""),
        "cloud_cover_percent":r.get("cloud_cover_percent",""),"status":r.get("status",""),
        "core_10m_complete":str(core).lower(),"all_requested_bands_complete":str(len(bands)>=11 and not missing).lower(),
        "scl_available":str(scl_ok).lower(),"analysis_valid_fraction":"" if valid is None else valid,
        "cloud_shadow_fraction":"" if shadow is None else shadow,
        "analysis_valid_pixels":scl.get("analysis_valid_pixel_count","") if scl_ok else "",
        "scl_pixels":scl.get("pixel_count","") if scl_ok else "","missing_bands":json.dumps(missing,sort_keys=True)}
        x["_sort"]=(not core,not scl_ok,-(valid if valid is not None else -1),
        shadow if shadow is not None else 2,len(missing) if isinstance(missing,list) else 99,
        cloud if cloud is not None else 100,date_key(x["datetime"])[1],x["item_id"])
        x["_rgb"]=match_rgb(x,rgb_by_point[x["sample_id"]])
        m=x["_rgb"] or {}
        x.update({"rgb_chip_file":m.get("file",""),"rgb_match_method":m.get("method",""),
        "rgb_datetime":m.get("datetime",""),"rgb_datetime_delta_seconds":m.get("delta",""),"rgb_chip_sha256":m.get("sha","")})
        grouped[x["sample_id"]].append(x)
    rankings=[]; worksheets=[]
    for p in points:
        candidates=sorted(grouped.get(p["sample_id"],[]),key=lambda x:x["_sort"])
        for rank,x in enumerate(candidates,1):
            x["candidate_rank"]=rank
            x["ranking_basis"]="Lexicographic evidence ordering: core 10m bands, SCL availability, local valid fraction, local cloud/shadow fraction, missing bands, scene cloud metadata, date. Review aid only."
            rankings.append({k:x.get(k,"") for k in RANK_FIELDS})
        chosen=candidates[:3]; primary=chosen[0] if chosen else {}; alts=chosen[1:]
        inventory=[{"chip_file":chip_path(r),"datetime":r.get("datetime",""),"platform":r.get("platform",""),
        "item_id":r.get("item_id",""),"cloud_cover_percent":r.get("cloud_cover_percent",""),
        "sha256":r.get("chip_sha256",""),"display_stretch":r.get("stretch","")}
        for r in sorted(rgb_by_point[p["sample_id"]],key=lambda q:date_key(q.get("datetime",""))[1])]
        pm=primary.get("_rgb") or {}
        row={"sample_id":p["sample_id"],"longitude":p["longitude"],"latitude":p["latitude"],
        "primary_candidate_item_id":primary.get("item_id",""),"primary_candidate_datetime":primary.get("datetime",""),
        "primary_rgb_chip_file":pm.get("file",""),"primary_rgb_match_status":pm.get("method","no_same_acquisition_rgb_chip"),
        "primary_rgb_datetime":pm.get("datetime",""),"primary_rgb_datetime_delta_seconds":pm.get("delta",""),
        "alternate_candidate_item_ids":" | ".join(x["item_id"] for x in alts),
        "alternate_candidate_dates":" | ".join(x["datetime"] for x in alts),
        "alternate_candidate_rgb_files":" | ".join((x.get("_rgb") or {}).get("file","") for x in alts),
        "rgb_chip_inventory":json.dumps(inventory,sort_keys=True),
        "evidence_quality_note":"Candidate ordering is not a class prediction. Inspect alternate dates and the full RGB inventory. RGB is linked to a candidate only for the same item or same-platform acquisition within two seconds." if candidates else "No multispectral candidates; consult catalogue and retrieval errors."}
        for f in REVIEW_FIELDS: row.setdefault(f,"")
        worksheets.append(row)
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=True)
    rp=out/"fiji-review-candidate-ranking.csv"; wp=out/"fiji-blind-review-worksheet.csv"
    for path,fields,rows in ((rp,RANK_FIELDS,rankings),(wp,REVIEW_FIELDS,worksheets)):
        with path.open("w",newline="",encoding="utf-8") as f:
            w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
    return {"points":len(points),"points_with_candidates":sum(bool(grouped.get(p["sample_id"])) for p in points),
    "candidate_rows":len(rankings),"points_with_primary_same_acquisition_rgb":sum(bool(r["primary_rgb_chip_file"]) for r in worksheets),
    "points_with_any_rgb_inventory":sum(r["rgb_chip_inventory"]!="[]" for r in worksheets),
    "ranking_csv":str(rp),"review_worksheet_csv":str(wp)}

def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument("--multispectral",required=True)
    p.add_argument("--blind-points",default="data/fiji-worldcover-legend-adjudication-blind-review.csv")
    p.add_argument("--rgb-provenance"); p.add_argument("--output-dir",default="/tmp/fiji-blind-review")
    a=p.parse_args(); print(json.dumps(prepare(a.multispectral,a.blind_points,a.output_dir,a.rgb_provenance),indent=2)); return 0
if __name__=="__main__": raise SystemExit(main())
