"""Design-based four-outcome and exploratory spatial analysis for Fiji–WorldCover."""
from __future__ import annotations
import argparse, csv, hashlib, json, math
from collections import Counter, defaultdict
from pathlib import Path

OUTCOMES = ("both_correct", "fiji_only_correct", "worldcover_only_correct", "both_wrong")
EARTH_RADIUS_KM = 6371.0088

def read_sample(path):
    data = Path(path).read_bytes()
    rows = list(csv.DictReader(data.decode("utf-8-sig").splitlines()))
    required = {"sample_id","sampling_stratum","map_class","reference_class","longitude","latitude"}
    if not rows or not required.issubset(rows[0]):
        raise ValueError("CSV must contain sample_id,sampling_stratum,map_class,reference_class,longitude,latitude.")
    seen, parsed = set(), []
    for i, row in enumerate(rows, 1):
        sid = row["sample_id"].strip()
        if not sid or sid in seen: raise ValueError(f"Row {i}: sample_id must be unique and non-empty.")
        seen.add(sid)
        h, mc, ref = (row[k].strip() for k in ("sampling_stratum","map_class","reference_class"))
        if not h or not mc or not ref: raise ValueError(f"Row {i}: missing class label.")
        try: lon, lat = float(row["longitude"]), float(row["latitude"])
        except (TypeError, ValueError) as exc: raise ValueError(f"Row {i}: invalid coordinates.") from exc
        if not math.isfinite(lon) or not math.isfinite(lat) or not -180 <= lon <= 180 or not -90 <= lat <= 90:
            raise ValueError(f"Row {i}: coordinates outside longitude/latitude bounds.")
        parsed.append({"sample_id":sid,"sampling_stratum":h,"map_class":mc,"reference_class":ref,
                       "longitude":lon,"latitude":lat,"worldcover_code":int(row["worldcover_code"]) if row.get("worldcover_code") else None,
                       "source_tile":row.get("source_tile","")})
    return parsed, hashlib.sha256(data).hexdigest()

def haversine_km(a,b):
    lat1,lat2=math.radians(a["latitude"]),math.radians(b["latitude"])
    dlat=lat2-lat1
    dlon=math.radians(((b["longitude"]-a["longitude"]+180)%360)-180)
    q=math.sin(dlat/2)**2+math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    return 2*EARTH_RADIUS_KM*math.asin(min(1.0,math.sqrt(q)))

def quantile(values,p):
    if not values:return None
    v=sorted(values); pos=(len(v)-1)*p; lo=math.floor(pos); hi=math.ceil(pos)
    return v[lo] if lo==hi else v[lo]+(v[hi]-v[lo])*(pos-lo)

def nearest_neighbour_summary(rows):
    if len(rows)<2:return {"point_count":len(rows),"nearest_neighbour_km":None}
    ds=[min(haversine_km(a,b) for j,b in enumerate(rows) if i!=j) for i,a in enumerate(rows)]
    return {"point_count":len(rows),"nearest_neighbour_km":{"minimum":min(ds),"p25":quantile(ds,.25),
            "median":quantile(ds,.5),"p75":quantile(ds,.75),"maximum":max(ds),"mean":sum(ds)/len(ds)}}

def analyse(rows, area_weights, population_sizes):
    weights={str(k):float(v) for k,v in area_weights.items()}
    pops={str(k):int(v) for k,v in population_sizes.items()}
    if not weights or set(weights)!=set(pops):raise ValueError("Weight and population keys must match and be non-empty.")
    if any(not math.isfinite(v) or v<=0 for v in weights.values()) or not math.isclose(sum(weights.values()),1,abs_tol=1e-9):
        raise ValueError("Area weights must be positive and sum to one.")
    if any(v<=0 for v in pops.values()):raise ValueError("Population sizes must be positive.")
    grouped=defaultdict(list); counts={h:Counter() for h in weights}; outcome_rows={k:[] for k in OUTCOMES}
    disagree=[]; both_wrong_same=both_wrong_different=0
    for i,raw in enumerate(rows,1):
        h=raw["sampling_stratum"]
        if h not in weights:raise ValueError(f"Row {i}: unknown stratum {h!r}.")
        fiji, wc, ref=h, raw["map_class"], raw["reference_class"]
        fc,wc_ok=fiji==ref,wc==ref
        outcome="both_correct" if fc and wc_ok else "fiji_only_correct" if fc else "worldcover_only_correct" if wc_ok else "both_wrong"
        if outcome=="both_wrong":
            if fiji==wc:both_wrong_same+=1
            else:both_wrong_different+=1
        row={**raw,"fiji_map_class":fiji,"outcome":outcome,"maps_disagree":fiji!=wc}
        grouped[h].append(row); counts[h][outcome]+=1; outcome_rows[outcome].append(row)
        if row["maps_disagree"]:disagree.append(row)
    if set(grouped)!=set(weights) or any(len(grouped[h])<2 for h in weights):
        raise ValueError("Every weighted stratum must contain at least two observations.")
    if any(pops[h]<len(grouped[h]) for h in weights):raise ValueError("Population size smaller than sample size.")
    estimates={}; stratum_diag={}
    for outcome in OUTCOMES:
        est,var=0.0,0.0
        for h,w in weights.items():
            n=len(grouped[h]); p=counts[h][outcome]/n; fpc=1-n/pops[h]
            contribution=w*p; varpart=w*w*p*(1-p)/(n-1)*fpc
            est+=contribution; var+=varpart
            stratum_diag.setdefault(h,{})[outcome]={"sample_count":counts[h][outcome],"sample_proportion":p,
                "weighted_estimate_contribution":contribution,"finite_population_correction":fpc}
        se=math.sqrt(max(0,var))
        estimates[outcome]={"estimate":est,"standard_error":se,"ci95_wald":[max(0,est-1.96*se),min(1,est+1.96*se)],
                            "unweighted_sample_count":sum(counts[h][outcome] for h in weights)}
    d_est=sum(weights[h]*sum(r["maps_disagree"] for r in grouped[h])/len(grouped[h]) for h in weights)
    d_var=sum(weights[h]**2*(sum(r["maps_disagree"] for r in grouped[h])/len(grouped[h]))*
              (1-sum(r["maps_disagree"] for r in grouped[h])/len(grouped[h]))/(len(grouped[h])-1)*
              (1-len(grouped[h])/pops[h]) for h in weights)
    d_se=math.sqrt(max(0,d_var))
    report={"analysis":"Fiji–WorldCover four-outcome and exploratory spatial disagreement analysis","sample_size":len(rows),
      "input_design":"stratified simple random sampling without replacement within original Fiji mapped-class strata",
      "baseline_map_class_source":"sampling_stratum (the original Fiji map defined the sample)",
      "sampling_stratum_area_proportions":weights,"stratum_population_sizes":pops,
      "sample_counts_by_stratum":{h:len(grouped[h]) for h in weights},"four_outcome_estimates":estimates,
      "direct_map_label_disagreement":{"sample_count":len(disagree),"sample_proportion_unweighted":len(disagree)/len(rows),
        "design_weighted_estimate":d_est,"standard_error":d_se,"ci95_wald":[max(0,d_est-1.96*d_se),min(1,d_est+1.96*d_se)],
        "both_wrong_same_map_class_count":both_wrong_same,"both_wrong_different_map_classes_count":both_wrong_different},
      "stratum_outcome_diagnostics":stratum_diag,
      "exploratory_spatial_summary":{"method":"great-circle nearest-neighbour distances within point subsets","units":"kilometres",
        "map_label_disagreement_points":nearest_neighbour_summary(disagree),
        "map_label_agreement_points":nearest_neighbour_summary([r for r in rows if r["sampling_stratum"]==r["map_class"]]),
        "interpretation":"Descriptive only; not a cluster test and not adjusted for stratified sampling or unequal stratum weights."},
      "interpretation_limits":[
        "Target domain is the eligible Fiji frame excluding Tikinas used for training samples.",
        "Reference labels are supplied visual interpretations, not independently field-verified here.",
        "WorldCover uses the single raster cell containing each point; positional tolerance and mixed-pixel uncertainty are not modelled.",
        "Intervals reflect within-stratum SRS sampling variance only, not reference, crosswalk, positional, temporal or area-weight uncertainty.",
        "Nearest-neighbour summaries are descriptive and are not significance tests for spatial clustering.",
        "No administrative-region field is present in the sample attributes; no named region is inferred.",
        "The strict eight-class working crosswalk remains provisional."
      ]}
    features=[]
    for r in rows:
        h=r["sampling_stratum"]; fiji=h; wc=r["map_class"]; ref=r["reference_class"]
        correct_f,correct_w=fiji==ref,wc==ref
        outcome="both_correct" if correct_f and correct_w else "fiji_only_correct" if correct_f else "worldcover_only_correct" if correct_w else "both_wrong"
        features.append({"type":"Feature","geometry":{"type":"Point","coordinates":[r["longitude"],r["latitude"]]},
          "properties":{"sample_id":r["sample_id"],"sampling_stratum":h,"fiji_map_class":fiji,"worldcover_map_class":wc,
            "reference_class":ref,"outcome":outcome,"maps_disagree":fiji!=wc,"worldcover_code":r["worldcover_code"],"source_tile":r["source_tile"]}})
    geojson={"type":"FeatureCollection","name":"Fiji WorldCover sample disagreement outcomes",
      "crs":{"type":"name","properties":{"name":"urn:ogc:def:crs:OGC:1.3:CRS84"}},"features":features}
    return report,geojson

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("observations_csv")
    p.add_argument("--stratum-area-weights",required=True);p.add_argument("--stratum-population-sizes",required=True)
    p.add_argument("--json-out",required=True);p.add_argument("--geojson-out",required=True);a=p.parse_args()
    try:
        rows,digest=read_sample(a.observations_csv);weights=json.loads(a.stratum_area_weights);pops=json.loads(a.stratum_population_sizes)
        if not isinstance(weights,dict) or not isinstance(pops,dict):raise ValueError("Weights and populations must be JSON objects.")
        report,geo=analyse(rows,weights,pops);report["input_csv_sha256"]=digest
        Path(a.json_out).write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8")
        Path(a.geojson_out).write_text(json.dumps(geo,indent=2,sort_keys=True)+"\n",encoding="utf-8")
        print(json.dumps({"sample_size":report["sample_size"],"four_outcome_estimates":report["four_outcome_estimates"],
          "direct_map_label_disagreement":report["direct_map_label_disagreement"]},indent=2))
    except (OSError,ValueError,TypeError,json.JSONDecodeError) as exc:p.error(str(exc))
    return 0
if __name__=="__main__":raise SystemExit(main())
