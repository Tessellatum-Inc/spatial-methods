#!/usr/bin/env python3
"""Download and checksum OPERA RTC-S1 plus RTC-STATIC assets for Nairobi R130."""
from __future__ import annotations
import argparse, hashlib, json, os, shutil, sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ALLOWED_HOSTS={"cumulus.asf.earthdatacloud.nasa.gov","datapool.asf.alaska.edu"}
RTC_SUFFIXES=(".h5",".iso.xml","_VV.tif","_VH.tif","_mask.tif")
STATIC_SUFFIXES=(".iso.xml","_incidence_angle.tif","_local_incidence_angle.tif","_mask.tif",
                 "_number_of_looks.tif","_rtc_anf_gamma0_to_beta0.tif","_rtc_anf_gamma0_to_sigma0.tif")


def select_assets(report:dict)->list[dict]:
    rtc=report.get("features",[])
    static=report.get("static_layer_query",{}).get("features",[])
    expected_bursts=sorted({b for g in report.get("acquisition_groups",[]) for b in g.get("burst_ids",[])})
    if len(rtc)!=15: raise ValueError(f"Expected 15 time-matched R130 RTC burst products, found {len(rtc)}")
    if len(expected_bursts)!=3: raise ValueError(f"Expected three target IW3 bursts, found {len(expected_bursts)}")
    static_ids={x.get("burst_id","").replace("-","_") for x in static}
    wanted={x.replace("-","_") for x in expected_bursts}
    if static_ids!=wanted: raise ValueError(f"RTC-STATIC burst coverage mismatch: expected {sorted(wanted)}, got {sorted(static_ids)}")
    assets=[]
    for kind,features,suffixes in (("rtc",rtc,RTC_SUFFIXES),("static",static,STATIC_SUFFIXES)):
        for feature in features:
            props=feature["properties"]
            candidates=list(props.get("additionalUrls",[]))
            if props.get("url"): candidates.append(props["url"])
            selected=set()
            for url in candidates:
                parsed=urlparse(url)
                if parsed.scheme!="https" or parsed.hostname not in ALLOWED_HOSTS: continue
                name=Path(parsed.path).name
                if any(name.endswith(s) for s in suffixes): selected.add(url)
            sizes=props.get("bytes",{})
            product_id=feature.get("file_id") or props.get("fileID") or props.get("sceneName")
            for url in sorted(selected):
                name=Path(urlparse(url).path).name
                record=sizes.get(name,{})
                assets.append({"product_type":kind,"product_id":product_id,"burst_id":feature.get("burst_id"),
                    "acquisition_datetime_utc":feature.get("acquisition_datetime_utc"),
                    "url":url,"filename":name,"expected_size_bytes":record.get("bytes")})
    if not assets: raise ValueError("No OPERA science assets selected")
    names=[x["filename"] for x in assets]
    if len(names)!=len(set(names)): raise ValueError("Duplicate asset filenames selected")
    return assets


def sha256_file(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1024*1024),b""): h.update(block)
    return h.hexdigest()


def download_assets(assets,output_dir:Path,token:str):
    if not token.strip(): raise ValueError("EARTHDATA_TOKEN is required")
    manifest=[]
    for asset in assets:
        folder=output_dir/asset["product_type"]; folder.mkdir(parents=True,exist_ok=True)
        dest=folder/asset["filename"]
        req=Request(asset["url"],headers={"Authorization":f"Bearer {token.strip()}",
            "User-Agent":"Tessellatum-Spatial-Methods/1.0"})
        try:
            with urlopen(req,timeout=180) as response,dest.open("wb") as out: shutil.copyfileobj(response,out)
        except HTTPError as e: raise RuntimeError(f"Earthdata download failed for {dest.name}: HTTP {e.code}") from e
        except (URLError,TimeoutError,OSError) as e: raise RuntimeError(f"Download failed for {dest.name}: {e}") from e
        size=dest.stat().st_size
        expected=asset.get("expected_size_bytes")
        if expected is not None and size!=expected: raise RuntimeError(f"Size mismatch for {dest.name}: expected {expected}, got {size}")
        manifest.append({**asset,"local_path":str(dest),"actual_size_bytes":size,
            "sha256":sha256_file(dest),"status":"downloaded_and_size_verified"})
        print(f"Downloaded {asset['product_type']}/{dest.name} ({size:,} bytes)")
    return manifest


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--report",type=Path,default=Path("data/asf/nairobi_r130/opera_rtc_catalogue.json"))
    p.add_argument("--output-dir",type=Path,default=Path("data/asf/nairobi_r130/downloaded"))
    a=p.parse_args(argv)
    try:
        report=json.loads(a.report.read_text(encoding="utf-8"))
        assets=select_assets(report)
        manifest=download_assets(assets,a.output_dir,os.environ.get("EARTHDATA_TOKEN",""))
    except (OSError,ValueError,RuntimeError,json.JSONDecodeError) as e:
        print(f"OPERA Nairobi R130 download failed: {e}",file=sys.stderr); return 2
    out={"schema":"tessellatum.opera-nairobi-r130-download-manifest.v1",
         "source_discovery_report":str(a.report),"asset_count":len(manifest),"assets":manifest,
         "interpretation_limits":["Checksum and byte-count verification do not establish source-scene identity or raster alignment.",
          "RTC-STATIC ellipsoid incidence and local incidence are distinct geometry conventions.",
          "Verify the source SLC product identifiers in HDF5 metadata before comparing with Sentinel Hub GRD."]}
    a.output_dir.mkdir(parents=True,exist_ok=True)
    path=a.output_dir/"download_manifest.json"
    path.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print(f"Downloaded and verified {len(manifest)} OPERA assets. Manifest: {path}")
    return 0

if __name__=="__main__": raise SystemExit(main())
