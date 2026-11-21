#!/usr/bin/env python3
"""Rank label-blind Fiji imagery candidates and prepare a human review worksheet."""
from __future__ import annotations
import argparse, csv, json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

RANK_FIELDS = ["sample_id","candidate_rank","item_id","collection","datetime","month","platform",
"cloud_cover_percent","status","core_10m_complete","all_requested_bands_complete","scl_available",
"analysis_valid_fraction","cloud_shadow_fraction","analysis_valid_pixels","scl_pixels",
"missing_bands","rgb_chip_file","rgb_chip_sha256","ranking_basis"]
REVIEW_FIELDS = ["sample_id","longitude","latitude","primary_candidate_item_id","primary_candidate_datetime",
"primary_rgb_chip_file","alternate_candidate_item_ids","alternate_candidate_dates","evidence_quality_note",
"reviewer_id","reviewer_role","review_datetime","interpreted_class","confidence_1_5","ambiguity_flag",
"alternative_class","temporal_consistency","visible_evidence","spectral_context_notes","limitations",
"decision_status","adjudication_notes"]

def read_csv(path):
    with Path(path).open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def parse_json(value, default):
    try: return json.loads(value) if value else default
    except (TypeError, ValueError): return default

def number(value):
    try:
        n=float(value)
        return n if n == n and abs(n) != float("inf") else None
    except (TypeError, ValueError): return None

def date_key(value):
    try:
        d=datetime.fromisoformat(value.replace("Z","+00:00"))
        return (d.month,d.isoformat())
    except (TypeError,ValueError): return (0,str(value or ""))

def prepare(multispectral_csv, blind_points_csv, output_dir, rgb_csv=None):
    spectral=read_csv(multispectral_csv); points=read_csv(blind_points_csv)
    if not points or not {"sample_id","longitude","latitude"}.issubset(points[0]):
        raise ValueError("Blind points CSV must contain sample_id, longitude, latitude")
    if spectral and not {"sample_id","item_id","datetime","status","bands_read","missing_bands","indices"}.issubset(spectral[0]):
        raise ValueError("Multispectral CSV is missing required provenance columns")
    rgb={}
    if rgb_csv and Path(rgb_csv).exists():
        for r in read_csv(rgb_csv):
            if r.get("sample_id") and r.get("item_id") and r.get("chip_file"):
                rgb[(r["sample_id"],r["item_id"])]=r
    grouped=defaultdict(list)
    for r in spectral:
        bands=set(parse_json(r.get("bands_read"),[])); missing=parse_json(r.get("missing_bands"),[])
        indices=parse_json(r.get("indices"),{}); scl=indices.get("SCL_QA_20m",{}) if isinstance(indices,dict) else {}
        scl_ok=isinstance(scl,dict) and "analysis_valid_fraction" in scl
        valid=number(scl.get("analysis_valid_fraction")) if scl_ok else None
        shadow=number(scl.get("cloud_shadow_fraction")) if scl_ok else None
        core={"B02","B03","B04","B08"}.issubset(bands)
        all_bands=len(bands)==11 and not missing
        chip=rgb.get((r.get("sample_id",""),r.get("item_id","")),{})
        x={"sample_id":r.get("sample_id",""),"item_id":r.get("item_id",""),
        "collection":r.get("collection",""),"datetime":r.get("datetime",""),
        "month":date_key(r.get("datetime",""))[0],"platform":r.get("platform",""),
        "cloud_cover_percent":r.get("cloud_cover_percent",""),"status":r.get("status",""),
        "core_10m_complete":str(core).lower(),"all_requested_bands_complete":str(all_bands).lower(),
        "scl_available":str(scl_ok).lower(),"analysis_valid_fraction":"" if valid is None else valid,
        "cloud_shadow_fraction":"" if shadow is None else shadow,
        "analysis_valid_pixels":scl.get("analysis_valid_pixel_count","") if scl_ok else "",
        "scl_pixels":scl.get("pixel_count","") if scl_ok else "",
        "missing_bands":json.dumps(missing),"rgb_chip_file":chip.get("chip_file",""),
        "rgb_chip_sha256":chip.get("chip_sha256",""),
        "_sort":(not core,not scl_ok,-(valid if valid is not None else -1),
        shadow if shadow is not None else 2,len(missing) if isinstance(missing,list) else 99,
        number(r.get("cloud_cover_percent")) if number(r.get("cloud_cover_percent")) is not None else 100,
        date_key(r.get("datetime",""))[1],r.get("item_id",""))}
        grouped[x["sample_id"]].append(x)
    ranking=[]; worksheet=[]
    for p in points:
        candidates=sorted(grouped.get(p["sample_id"],[]),key=lambda x:x["_sort"])
        for rank,x in enumerate(candidates,1):
            x["candidate_rank"]=rank
            x["ranking_basis"]="Lexicographic evidence ordering: core 10m bands, SCL availability, local valid fraction, local cloud/shadow fraction, missing bands, scene cloud metadata, date. Review aid only."
            ranking.append({k:x.get(k,"") for k in RANK_FIELDS})
        chosen=candidates[:3]; primary=chosen[0] if chosen else {}
        alternates=chosen[1:]
        row={"sample_id":p["sample_id"],"longitude":p["longitude"],"latitude":p["latitude"],
        "primary_candidate_item_id":primary.get("item_id",""),
        "primary_candidate_datetime":primary.get("datetime",""),
        "primary_rgb_chip_file":primary.get("rgb_chip_file",""),
        "alternate_candidate_item_ids":" | ".join(x["item_id"] for x in alternates),
        "alternate_candidate_dates":" | ".join(x["datetime"] for x in alternates),
        "evidence_quality_note":"Ranking is not a class prediction. Inspect alternate dates and all available context before recording an interpretation." if candidates else "No multispectral candidates; consult catalogue and retrieval errors."}
        for field in REVIEW_FIELDS:
            row.setdefault(field,"")
        worksheet.append(row)
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=True)
    rank_path=out/"fiji-review-candidate-ranking.csv"; review_path=out/"fiji-blind-review-worksheet.csv"
    for path,fields,rows in ((rank_path,RANK_FIELDS,ranking),(review_path,REVIEW_FIELDS,worksheet)):
        with path.open("w",newline="",encoding="utf-8") as f:
            w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
    return {"points":len(points),"points_with_candidates":sum(bool(grouped.get(p["sample_id"])) for p in points),
    "candidate_rows":len(ranking),"points_with_rgb_primary":sum(bool(r["primary_rgb_chip_file"]) for r in worksheet),
    "ranking_csv":str(rank_path),"review_worksheet_csv":str(review_path)}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--multispectral",required=True)
    p.add_argument("--blind-points",default="data/fiji-worldcover-legend-adjudication-blind-review.csv")
    p.add_argument("--rgb-provenance")
    p.add_argument("--output-dir",default="/tmp/fiji-blind-review")
    a=p.parse_args()
    print(json.dumps(prepare(a.multispectral,a.blind_points,a.output_dir,a.rgb_provenance),indent=2))
    return 0
if __name__=="__main__": raise SystemExit(main())
