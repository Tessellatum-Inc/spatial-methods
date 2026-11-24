#!/usr/bin/env python3
"""Cross-processor terrain/ellipsoid gamma0 comparison for Nairobi R130."""
from __future__ import annotations
import argparse,json,re,sys
from pathlib import Path
import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.warp import reproject

BURST_RE=re.compile(r"(T130[-_]\d{6}[-_]IW3)",re.I)
DATE_RE=re.compile(r"(20\d{6})T\d{6}Z")
POLARIZATIONS=("VV","VH")
DB_FLOOR=1e-12
SUPPORT_THRESHOLD=0.95
MIN_COMMON_PIXELS=1000

def db(x):return 10*np.log10(np.maximum(np.asarray(x,dtype=np.float64),DB_FLOOR))
def metrics(x):
    v=np.asarray(x,dtype=np.float64);v=v[np.isfinite(v)]
    if not v.size:raise ValueError("No finite residual values")
    q=np.percentile(v,[5,50,95]);a=np.abs(v)
    return {"count":int(v.size),"bias_mean_db":float(v.mean()),"bias_median_db":float(q[1]),
      "mae_db":float(a.mean()),"rmse_db":float(np.sqrt(np.mean(v*v))),
      "std_db":float(v.std()),"p05_db":float(q[0]),"p95_db":float(q[2]),
      "p95_absolute_db":float(np.percentile(a,95)),"max_absolute_db":float(a.max())}
def reproject_average(values,src,dst):
    out=np.full((dst.height,dst.width),np.nan,dtype=np.float32)
    reproject(source=np.asarray(values,dtype=np.float32),destination=out,
      src_transform=src.transform,src_crs=src.crs,src_nodata=np.nan,
      dst_transform=dst.transform,dst_crs=dst.crs,dst_nodata=np.nan,
      resampling=Resampling.average,init_dest_nodata=True)
    return out
def unique(folder,pattern,label):
    found=sorted(folder.glob(pattern))
    if len(found)!=1:raise ValueError(f"Expected one {label}; found {[x.name for x in found]}")
    return found[0]
def process_one(opera_dir,sh_dir,date,burst):
    iso=f"{date[:4]}-{date[4:6]}-{date[6:8]}"
    rtc=opera_dir/"rtc";static=opera_dir/"static"
    def dynamic(pol):return unique(rtc,f"OPERA_L2_RTC-S1_{burst}_{date}T*_{'S1D'}_30_v1.0_{pol}.tif",f"{burst} {iso} {pol}")
    def static_layer(suffix):
        found=[p for p in static.glob("*.tif") if burst in p.name and p.name.endswith(suffix)
          and not(suffix=="_incidence_angle.tif" and p.name.endswith("_local_incidence_angle.tif"))]
        if len(found)!=1:raise ValueError(f"Expected one static {suffix} for {burst}; found {[p.name for p in found]}")
        return found[0]
    ell_path=sh_dir/f"nairobi_r130_{iso}_gamma0-ellipsoid.tif"
    terrain_path=sh_dir/f"nairobi_r130_{iso}_gamma0-terrain-rtc.tif"
    if not ell_path.is_file() or not terrain_path.is_file():raise FileNotFoundError(f"Missing Sentinel Hub pair for {iso}")
    with rasterio.open(dynamic("VV")) as vv,rasterio.open(dynamic("VH")) as vh,\
      rasterio.open(unique(rtc,f"OPERA_L2_RTC-S1_{burst}_{date}T*_S1D_30_v1.0_mask.tif","OPERA dynamic mask")) as dm,\
      rasterio.open(static_layer("_rtc_anf_gamma0_to_beta0.tif")) as anf,\
      rasterio.open(static_layer("_incidence_angle.tif")) as inc,\
      rasterio.open(static_layer("_mask.tif")) as sm,\
      rasterio.open(ell_path) as ell,rasterio.open(terrain_path) as shrtc:
        for label,ds in [("VH",vh),("dynamic mask",dm),("ANF",anf),("ellipsoid incidence",inc),("static mask",sm)]:
            if (ds.crs,ds.transform,ds.width,ds.height)!=(vv.crs,vv.transform,vv.width,vv.height):
                raise ValueError(f"OPERA {label} grid mismatch")
        if ell.count!=3 or shrtc.count!=6:raise ValueError("Unexpected Sentinel Hub band schema")
        if (ell.crs,ell.transform,ell.width,ell.height)!=(shrtc.crs,shrtc.transform,shrtc.width,shrtc.height):
            raise ValueError("Sentinel Hub ellipsoid and terrain grids differ")
        dynamic_mask=dm.read(1);static_mask=sm.read(1)
        theta=np.deg2rad(inc.read(1).astype(np.float32))
        anf_values=anf.read(1).astype(np.float32)
        op_mask=(dynamic_mask==0)&(static_mask==0)&np.isfinite(anf_values)&(anf_values>0)&np.isfinite(theta)&(theta>0)&(theta<np.pi/2)
        sh_mask=(ell.read(3)>0.5)&(shrtc.read(6)>0.5)&(shrtc.read(5)<0.5)
        sh_mask &= np.isfinite(ell.read(1))&np.isfinite(ell.read(2))
        sh_mask &= np.isfinite(shrtc.read(1))&np.isfinite(shrtc.read(2))
        support=reproject_average(sh_mask.astype(np.float32),ell,vv)
        sh_support=np.isfinite(support)&(support>=SUPPORT_THRESHOLD)
        pol_report={};all_residuals={}
        for idx,pol in enumerate(POLARIZATIONS,1):
            opera_terrain=vv.read(1) if pol=="VV" else vh.read(1)
            opera_ellipsoid=opera_terrain*anf_values*np.tan(theta)
            sh_ellipsoid=reproject_average(np.where(sh_mask,ell.read(idx),np.nan),ell,vv)
            sh_terrain=reproject_average(np.where(sh_mask,shrtc.read(idx),np.nan),ell,vv)
            valid=op_mask&sh_support&np.isfinite(opera_terrain)&(opera_terrain>0)&np.isfinite(opera_ellipsoid)&(opera_ellipsoid>0)
            valid &= np.isfinite(sh_ellipsoid)&(sh_ellipsoid>0)&np.isfinite(sh_terrain)&(sh_terrain>0)
            n=int(valid.sum())
            if n<MIN_COMMON_PIXELS:raise ValueError(f"{iso} {burst} {pol}: only {n} common pixels (<{MIN_COMMON_PIXELS})")
            delta_opera=db(opera_terrain[valid])-db(opera_ellipsoid[valid])
            delta_sh=db(sh_terrain[valid])-db(sh_ellipsoid[valid])
            residual=delta_sh-delta_opera
            pol_report[pol]={"common_valid_pixels":n,"common_fraction_of_opera_grid":float(n/(vv.width*vv.height)),
              "opera_valid_fraction":float(op_mask.mean()),"sentinelhub_source_valid_fraction":float(sh_mask.mean()),
              "sentinelhub_support_threshold":SUPPORT_THRESHOLD,
              "opera_terrain_minus_reconstructed_ellipsoid_db":metrics(delta_opera),
              "sentinelhub_terrain_minus_ellipsoid_db":metrics(delta_sh),
              "cross_processor_delta_residual_db":metrics(residual)}
            all_residuals[pol]=residual.astype(np.float32)
        return {"date":iso,"burst_id":burst,"crs":vv.crs.to_string(),"width":vv.width,"height":vv.height,
          "polarizations":pol_report},all_residuals

def run(opera_dir,sh_dir,output):
    keys=set()
    for p in (opera_dir/"rtc").glob("*_VV.tif"):
        b=BURST_RE.search(p.name);d=DATE_RE.search(p.name)
        if b and d:keys.add((d.group(1),b.group(1).replace("_","-")))
    if len(keys)!=15:raise ValueError(f"Expected 15 OPERA date/burst combinations; found {len(keys)}")
    records=[];pooled={"VV":[],"VH":[]}
    for date,burst in sorted(keys):
        record,residuals=process_one(opera_dir,sh_dir,date,burst);records.append(record)
        for pol in POLARIZATIONS:pooled[pol].append(residuals[pol])
        print(f"{record['date']} {burst} | VV={record['polarizations']['VV']['common_valid_pixels']:,} | VH={record['polarizations']['VH']['common_valid_pixels']:,}",flush=True)
    aggregate={}
    for pol in POLARIZATIONS:
        vals=np.concatenate(pooled[pol]).astype(np.float64)
        aggregate[pol]=metrics(vals)
    report={"schema":"tessellatum.opera-nairobi-r130-cross-processor-comparison.v1",
      "study_area":"Nairobi County and environs, Kenya","platform":"Sentinel-1D","relative_orbit":130,
      "orbit_direction":"ASCENDING","date_count":5,"burst_count":3,"date_burst_count":len(records),
      "polarizations":list(POLARIZATIONS),
      "estimand":"Sentinel Hub (terrain gamma0 - ellipsoid gamma0) minus OPERA (terrain gamma0 - reconstructed ellipsoid gamma0), in dB after masked linear-power aggregation onto native OPERA burst grids.",
      "reconstruction":"OPERA reconstructed ellipsoid gamma0 = OPERA terrain gamma0 * ANF(gamma0->beta0) * tan(ellipsoid incidence angle).",
      "support":{"sentinelhub_average_resampling":"area average in linear power","minimum_source_valid_support_fraction":SUPPORT_THRESHOLD,
        "minimum_common_pixels_per_burst_date_polarization":MIN_COMMON_PIXELS},
      "reflector_exclusion_applied":False,
      "per_burst_date":records,"pooled_pixel_residual_metrics":aggregate,
      "checks":{"all_15_burst_date_combinations_processed":len(records)==15,
        "all_30_polarization_sample_gates_pass":True},
      "limitations":["This is a cross-processor relationship comparison, not an absolute calibration or proof of interchangeable backscatter.",
        "OPERA uses SLC-derived RTC; Sentinel Hub uses GRD processing. Shared source datatakes do not imply identical processing or resolution.",
        "No corner-reflector inventory or absolute RCS calibration is asserted for Nairobi.",
        "The study rectangle includes urban and peri-urban land cover; results must be interpreted within this footprint/orbit/date scope.",
        "Adjacent OPERA bursts are processed on their native grids and not mosaicked."]}
    output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(report,indent=2)+"\n")
    print("Pooled pixel residual metrics:",json.dumps(aggregate,sort_keys=True),flush=True)
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--opera-dir",type=Path,default=Path("opera-assets"))
    p.add_argument("--sentinelhub-dir",type=Path,default=Path("data/sentinelhub/nairobi/r130"))
    p.add_argument("--output",type=Path,default=Path("data/sentinelhub/nairobi/r130/cross-processor-comparison.json"))
    a=p.parse_args()
    try:r=run(a.opera_dir,a.sentinelhub_dir,a.output)
    except Exception as e:print(f"Nairobi R130 comparison failed: {type(e).__name__}: {e}",file=sys.stderr);return 2
    return 0 if all(r["checks"].values()) else 1
if __name__=="__main__":raise SystemExit(main())
