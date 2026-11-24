#!/usr/bin/env python3
"""Verify OPERA SLC and Sentinel Hub GRD candidates share Sentinel-1 datatakes."""
from __future__ import annotations
import argparse,json,re,sys
from datetime import datetime
from pathlib import Path

PRODUCT_RE=re.compile(
 r"^(S1[ABCD])_IW_(SLC|GRDH)_+([A-Z0-9]+)_(\d{8}T\d{6})_(\d{8}T\d{6})_(\d{6})_([0-9A-F]{6})_([0-9A-F]{4})(?:_COG)?(?:\.SAFE|\.zip)$",
 re.I)

def parse_product(value):
    if not isinstance(value,str): return None
    name=Path(value).name
    m=PRODUCT_RE.match(name)
    if not m: return None
    platform,level,mode,start,end,orbit,datatake,product_id=m.groups()
    return {"platform":platform.upper(),"product_level":level.upper(),"mode_polarization":mode.upper(),
      "start_time":start,"end_time":end,"absolute_orbit":int(orbit),
      "datatake_id":datatake.upper(),"product_unique_id":product_id.upper(),"filename":name}

def parse_product_start(value):
    return datetime.strptime(value,"%Y%m%dT%H%M%S")

def verify(audit,catalogue,start_tolerance_seconds=2):
    opera=[]
    for item in audit.get("hdf5",[]):
        md=item.get("metadata",{})
        for source in md.get("source_slc_granules") or []:
            parsed=parse_product(source)
            if parsed:
                opera.append({"hdf5_file":item["file"],"burst_id":md.get("burst_id"),
                    "hdf5_absolute_orbit":md.get("absolute_orbit"),"hdf5_platform":md.get("platform"),
                    "hdf5_source_start":md.get("source_start"),"source_slc":parsed})
    matches=[]
    for group in catalogue.get("acquisition_date_matches",[]):
        for candidate in group.get("qualified_candidates",[]):
            grd=parse_product(candidate.get("catalog_item_id") or candidate.get("source_product_identifier"))
            if not grd: continue
            linked=[x for x in opera if x["source_slc"]["absolute_orbit"]==grd["absolute_orbit"]
                and x["source_slc"]["datatake_id"]==grd["datatake_id"]
                and x["source_slc"]["platform"]==grd["platform"]
                and abs((parse_product_start(x["source_slc"]["start_time"])-parse_product_start(grd["start_time"])).total_seconds())<=start_tolerance_seconds]
            matches.append({"acquisition_date_utc":group.get("acquisition_date_utc"),
                "sentinelhub_grd":grd,"linked_opera_burst_count":len(linked),
                "linked_opera_bursts":sorted({x.get("burst_id") for x in linked}),
                "linked_opera_slc_granules":sorted({x["source_slc"]["filename"] for x in linked}),
                "maximum_source_start_difference_seconds":max((abs((parse_product_start(x["source_slc"]["start_time"])-parse_product_start(grd["start_time"])).total_seconds()) for x in linked),default=None),
                "datatake_match_passed":len(linked)==3 and len({x.get("burst_id") for x in linked})==3})
    report={"schema":"tessellatum.opera-nairobi-r130-source-datatake-verification.v1",
      "opera_source_slc_granule_count":len(opera),"sentinelhub_grd_candidate_count":len(matches),
      "date_matches":matches,
      "checks":{"all_five_dates_have_one_grd_candidate":len(matches)==5,
        "all_five_dates_link_all_three_opera_bursts":len(matches)==5 and all(x["datatake_match_passed"] for x in matches)},
      "source_start_time_tolerance_seconds":start_tolerance_seconds,
      "interpretation":"OPERA SLC and Sentinel Hub GRD are distinct product levels. A shared platform, IW mode, start time, absolute orbit and datatake identifier establishes that both processors used the same Sentinel-1 datatake, not that their processed pixels are identical.",
      "limitations":["The Sentinel Hub item is a GRD COG product; OPERA's input is an SLC granule.",
        "The SLC and GRD product start/stop timestamps may differ slightly due to product packaging; this crosswalk uses a two-second start-time tolerance plus exact orbit and datatake identity.",
        "The crosswalk establishes source acquisition correspondence only; it is not a radiometric validation result."]}
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--audit",type=Path,default=Path("opera-assets-audit.json"))
    p.add_argument("--catalogue",type=Path,default=Path("candidate-catalogue/opera_sentinelhub_candidate_matches.json"))
    p.add_argument("--output",type=Path,default=Path("source-datatake-verification.json"))
    a=p.parse_args()
    audit=json.loads(a.audit.read_text()); catalogue=json.loads(a.catalogue.read_text())
    report=verify(audit,catalogue)
    a.output.write_text(json.dumps(report,indent=2)+"\n")
    for x in report["date_matches"]:
        print(f"{x['acquisition_date_utc']} | orbit={x['sentinelhub_grd']['absolute_orbit']} | datatake={x['sentinelhub_grd']['datatake_id']} | OPERA bursts={x['linked_opera_burst_count']} | matched={x['datatake_match_passed']}")
    print("Checks:",json.dumps(report["checks"],sort_keys=True))
    return 0 if all(report["checks"].values()) else 1

if __name__=="__main__":
    try: raise SystemExit(main())
    except Exception as e: print(f"Source datatake verification failed: {e}",file=sys.stderr); raise
