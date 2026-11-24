#!/usr/bin/env python3
"""Match OPERA Nairobi R130 acquisition dates to Sentinel Hub GRD catalogue items.

Matches are candidates only. A timestamp/orbit/platform match does not prove
source-scene identity; original Sentinel-1 identifiers must be reconciled later.
"""
from __future__ import annotations
import argparse, importlib.util, json, os, sys
from datetime import datetime, timezone
from pathlib import Path

RADAR=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("query_sentinelhub_sentinel1",RADAR/"query_sentinelhub_sentinel1.py")
if spec is None or spec.loader is None: raise RuntimeError("Cannot load Sentinel Hub catalogue client")
CAT=importlib.util.module_from_spec(spec); spec.loader.exec_module(CAT)
BBOX=[36.65,-1.45,37.05,-1.15]
TIME_TOLERANCE_SECONDS=300


def parse_time(value):
    if not isinstance(value,str): return None
    try:
        dt=datetime.fromisoformat(value.replace("Z","+00:00"))
        if dt.tzinfo is None: return None
        return dt.astimezone(timezone.utc)
    except ValueError: return None


def collect_sentinelhub(token,start,end,timeout=60):
    payload=CAT.build_search_payload(start,end,100)
    features={}
    for _ in range(50):
        page=CAT.search_catalog(token,payload,timeout=timeout)
        for f in page["features"]: features[f["id"]]=f
        nxt=page.get("context",{}).get("next")
        if nxt is None: break
        payload={**payload,"next":nxt}
    else: raise RuntimeError("Sentinel Hub catalogue pagination exceeded 50 pages")
    return sorted(features.values(),key=lambda f:f.get("properties",{}).get("datetime",""))


def normalize_platform(value):
    if not isinstance(value,str): return None
    value=value.lower().replace("_","").replace("-","").replace(" ","")
    return value if value.startswith("sentinel1") else None


def candidate_matches(opera_report,features,orbit=130,direction="ASCENDING",tolerance=TIME_TOLERANCE_SECONDS):
    selected=[]
    for f in features:
        p=f.get("properties") or {}
        if str(p.get("sat:orbit_state","")).upper()!=direction: continue
        try: rel=int(p.get("sat:relative_orbit"))
        except (TypeError,ValueError): continue
        if rel!=orbit: continue
        pols=p.get("sar:polarizations") or []
        if not {"VV","VH"}.issubset(set(pols)): continue
        dt=parse_time(p.get("datetime"))
        if dt is None: continue
        selected.append({"catalog_item_id":f.get("id"),"datetime_utc":dt.isoformat().replace("+00:00","Z"),
            "platform":p.get("platform"),"relative_orbit":rel,"orbit_state":direction,
            "polarizations":sorted(pols),"source_product_identifier":p.get("s1:product_identifier"),
            "datatake_id":p.get("s1:datatake_id"),"absolute_orbit":p.get("sat:absolute_orbit"),
            "geometry":f.get("geometry")})
    groups=[]
    for g in opera_report.get("acquisition_groups",[]):
        date=g.get("acquisition_date_utc")
        starts=[parse_time(x) for x in g.get("burst_start_times_utc",[])]
        starts=[x for x in starts if x]
        day_candidates=[x for x in selected if x["datetime_utc"].startswith(date or "")]
        ranked=[]
        for scene in day_candidates:
            sh_dt=parse_time(scene["datetime_utc"])
            delta=min((abs((sh_dt-t).total_seconds()) for t in starts),default=None)
            opera_platforms={normalize_platform(x.get("platform")) for x in g.get("products",[])}
            sh_platform=normalize_platform(scene.get("platform"))
            ranked.append({**scene,"nearest_opera_burst_difference_seconds":delta,
                "platform_matches":bool(sh_platform and sh_platform in opera_platforms),
                "within_time_tolerance":bool(delta is not None and delta<=tolerance)})
        ranked.sort(key=lambda x:(not x["platform_matches"],x["nearest_opera_burst_difference_seconds"] if x["nearest_opera_burst_difference_seconds"] is not None else 1e12))
        qualified=[x for x in ranked if x["platform_matches"] and x["within_time_tolerance"]]
        groups.append({"acquisition_date_utc":date,"opera_burst_count":len(g.get("burst_ids",[])),
            "opera_burst_ids":g.get("burst_ids",[]),"opera_platforms":sorted({x.get("platform") for x in g.get("products",[]) if x.get("platform")}),
            "sentinelhub_candidate_count":len(ranked),"qualified_candidate_count":len(qualified),
            "qualified_candidates":qualified,"all_same_date_candidates":ranked})
    return {"schema":"tessellatum.sentinel1.opera-nairobi-r130-cross-provider-candidate-match.v1",
        "query":{"aoi_bbox_wgs84":BBOX,"relative_orbit":orbit,"orbit_direction":direction,
            "time_tolerance_seconds":tolerance,"sentinelhub_collection":"sentinel-1-grd"},
        "sentinelhub_catalogue_feature_count":len(features),
        "sentinelhub_r130_iw_vv_vh_candidate_count":len(selected),
        "acquisition_date_matches":groups,
        "qualified_date_count":sum(1 for x in groups if x["qualified_candidate_count"]),
        "interpretation":"Candidate matching only. Require original source product identity and burst-level source reconciliation before downloading or comparing rasters.",
        "limitations":["STAC datetime and platform metadata are screening evidence, not definitive source identity.",
          "Relative orbit and orbit direction must be verified against source SAFE/HDF5 metadata.",
          "A matched scene footprint must still be checked against each OPERA burst and the raster-valid masks.",
          "This catalogue comparison does not establish radiometric equivalence."]}


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--opera-report",type=Path,default=Path("data/asf/nairobi_r130/opera_rtc_catalogue.json"))
    p.add_argument("--start",default="2026-10-01T00:00:00Z"); p.add_argument("--end",default="2026-11-24T00:00:00Z")
    p.add_argument("--output",type=Path,default=Path("data/asf/nairobi_r130/opera_sentinelhub_candidate_matches.json"))
    p.add_argument("--timeout",type=int,default=60); a=p.parse_args(argv)
    try:
        opera=json.loads(a.opera_report.read_text(encoding="utf-8"))
        token=CAT.request_access_token(os.environ.get("SENTINEL_HUB_CLIENT_ID",""),os.environ.get("SENTINEL_HUB_CLIENT_SECRET",""),timeout=30)
        features=collect_sentinelhub(token,a.start,a.end,a.timeout)
        report=candidate_matches(opera,features)
    except (OSError,ValueError,RuntimeError,json.JSONDecodeError) as e:
        print(f"Cross-provider catalogue match failed: {e}",file=sys.stderr); return 2
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(f"Sentinel Hub catalogue features: {report['sentinelhub_catalogue_feature_count']}")
    print(f"R130 ascending VV/VH candidates: {report['sentinelhub_r130_iw_vv_vh_candidate_count']}")
    print(f"OPERA dates with qualified platform/time candidates: {report['qualified_date_count']}/{len(report['acquisition_date_matches'])}")
    for g in report["acquisition_date_matches"]:
        print(f"{g['acquisition_date_utc']} | OPERA bursts={g['opera_burst_count']} | SH candidates={g['sentinelhub_candidate_count']} | qualified={g['qualified_candidate_count']}")
        for scene in g["qualified_candidates"]:
            print(f"  {scene['catalog_item_id']} | {scene['datetime_utc']} | dt={scene['nearest_opera_burst_difference_seconds']}s | product={scene['source_product_identifier']} | datatake={scene['datatake_id']} | abs_orbit={scene['absolute_orbit']}")
    print(f"Report: {a.output}")
    return 0

if __name__=="__main__": raise SystemExit(main())
