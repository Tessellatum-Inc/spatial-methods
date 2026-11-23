#!/usr/bin/env python3
"""List only Sentinel-1 GRD annotation XML objects needed for ellipsoid-angle QA.

No SAFE product or imagery raster is downloaded. S3 credentials are read from
CDSE_S3_ACCESS_KEY and CDSE_S3_SECRET_KEY and are never printed or persisted.
"""
from __future__ import annotations
import argparse, importlib.util, json, os, sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

RADAR=Path(__file__).resolve().parent
SPEC=importlib.util.spec_from_file_location("query_sentinelhub_sentinel1",RADAR/"query_sentinelhub_sentinel1.py")
if SPEC is None or SPEC.loader is None: raise RuntimeError("Cannot load Sentinel Hub catalogue client")
CAT=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(CAT)

PRODUCT_IDS={
"S1A_IW_GRDH_1SDV_20250108T154826_20250108T154851_057354_070F02_69BA_COG.SAFE",
"S1A_IW_GRDH_1SDV_20250120T154825_20250120T154850_057529_0715F0_AEAD_COG.SAFE",
"S1A_IW_GRDH_1SDV_20250201T154824_20250201T154849_057704_071CDD_B2FC_COG.SAFE",
"S1A_IW_GRDH_1SDV_20250213T154824_20250213T154849_057879_0723E0_AE16_COG.SAFE",
"S1A_IW_GRDH_1SDV_20250101T155624_20250101T155649_057252_070AFB_CF43_COG.SAFE",
"S1A_IW_GRDH_1SDV_20250113T155623_20250113T155648_057427_0711E7_D8F0_COG.SAFE",
"S1A_IW_GRDH_1SDV_20250125T155622_20250125T155647_057602_0718DC_43D7_COG.SAFE",
"S1A_IW_GRDH_1SDV_20250206T155622_20250206T155647_057777_071FCA_BA90_COG.SAFE",
}

def parse_s3_uri(uri:str):
    parsed=urlparse(uri)
    if parsed.scheme!="s3" or not parsed.netloc or not parsed.path.lstrip("/"):
        raise ValueError(f"Expected an s3://bucket/prefix URI, got {uri!r}")
    return parsed.netloc,parsed.path.lstrip("/").rstrip("/")+"/"

def annotation_object(key:str):
    lower=key.lower()
    return lower.endswith(".xml") and ("/annotation/" in lower or "/annotation" in lower)

def collect_catalog_items(token,start,end):
    payload=CAT.build_search_payload(start,end,100); found={}
    for _ in range(50):
        page=CAT.search_catalog(token,payload,timeout=60)
        for feature in page["features"]:
            if feature.get("id") in PRODUCT_IDS: found[feature["id"]]=feature
        nxt=page.get("context",{}).get("next")
        if nxt is None: return found
        payload={**payload,"next":nxt}
    raise RuntimeError("Catalogue pagination exceeded 50 pages")

def inspect_items(features,s3_access_key,s3_secret_key):
    try:
        import boto3
        from botocore.config import Config
    except ImportError as exc:
        raise RuntimeError("Install requirements-sentinel1-s3-metadata.txt before running") from exc
    resource=boto3.resource("s3",endpoint_url="https://eodata.dataspace.copernicus.eu",
        aws_access_key_id=s3_access_key,aws_secret_access_key=s3_secret_key,
        region_name="default",config=Config(signature_version="s3v4"))
    results=[]
    for item_id in sorted(PRODUCT_IDS):
        feature=features.get(item_id)
        if feature is None: raise RuntimeError(f"Catalogue item not found for processed scene: {item_id}")
        href=(feature.get("assets") or {}).get("data",{}).get("href")
        if not isinstance(href,str): raise RuntimeError(f"Catalogue data asset missing for {item_id}")
        bucket_name,prefix=parse_s3_uri(href)
        bucket=resource.Bucket(bucket_name)
        keys=[]
        for obj in bucket.objects.filter(Prefix=prefix):
            if annotation_object(obj.key) or obj.key.lower().endswith("/manifest.safe"):
                keys.append({"key":obj.key,"size_bytes":int(obj.size)})
        results.append({"item_id":item_id,"datetime_utc":feature.get("properties",{}).get("datetime"),
            "platform":feature.get("properties",{}).get("platform"),
            "relative_orbit":feature.get("properties",{}).get("sat:relative_orbit"),
            "s3_prefix":href,"annotation_and_manifest_objects":keys,
            "annotation_xml_count":sum(x["key"].lower().endswith(".xml") for x in keys)})
    return results

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--start",default="2025-01-01T00:00:00Z")
    p.add_argument("--end",default="2025-02-20T00:00:00Z")
    p.add_argument("--output",type=Path,default=Path("data/sentinelhub/nairobi/sentinel1_grd_annotation_object_inventory.json"))
    a=p.parse_args(argv)
    access=os.environ.get("CDSE_S3_ACCESS_KEY",""); secret=os.environ.get("CDSE_S3_SECRET_KEY","")
    if not access or not secret:
        print("Set CDSE_S3_ACCESS_KEY and CDSE_S3_SECRET_KEY as GitHub Actions secrets; do not paste them into chat or commit them.",file=sys.stderr)
        return 2
    try:
        token=CAT.request_access_token(os.environ.get("SENTINEL_HUB_CLIENT_ID",""),
            os.environ.get("SENTINEL_HUB_CLIENT_SECRET",""),timeout=30)
        features=collect_catalog_items(token,a.start,a.end)
        results=inspect_items(features,access,secret)
    except (OSError,ValueError,RuntimeError) as exc:
        print(f"Annotation object inventory failed: {exc}",file=sys.stderr); return 2
    report={"schema":"tessellatum.sentinel1.grd-annotation-object-inventory.v1",
        "items":results,"analysis_ready":False,
        "purpose":"Locate source GRD geolocation-grid XML containing ellipsoid incidenceAngle values; no SAFE or imagery download performed.",
        "limitations":["Object listing is not yet an incidence-angle extraction or interpolation.",
        "The geolocation grid must be checked for complete coverage and interpolation accuracy before use."]}
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    total=sum(x["annotation_xml_count"] for x in results)
    print(f"Products inspected: {len(results)}; annotation XML objects found: {total}")
    for row in results:
        print(f"{row['item_id']}: {row['annotation_xml_count']} annotation XML files")
        for obj in row["annotation_and_manifest_objects"]:
            print(f"  {obj['key']} ({obj['size_bytes']} bytes)")
    print(f"Report: {a.output}; analysis_ready=false")
    return 0
if __name__=="__main__": raise SystemExit(main())
