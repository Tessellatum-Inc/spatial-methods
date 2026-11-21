#!/usr/bin/env python3
"""Create point-centred RGB contact sheets and deduplicate catalogue aliases for blind review."""
from __future__ import annotations
import argparse, csv, json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw

def read_rows(path):
    with Path(path).open(newline="",encoding="utf-8-sig") as f:
        return list(csv.DictReader(f)), csv.DictReader

def parse_dt(value):
    try: return datetime.fromisoformat(str(value).replace("Z","+00:00"))
    except (TypeError,ValueError): return None

def deduplicate(rows, tolerance_seconds=2.0):
    groups=[]
    for row in sorted(rows,key=lambda r:parse_dt(r.get("datetime")) or datetime.min.replace(tzinfo=None)):
        current=parse_dt(row.get("datetime")); match=None
        for group in groups:
            first=group[0]; previous=parse_dt(first.get("datetime"))
            if row.get("platform")==first.get("platform") and current and previous and abs((current-previous).total_seconds())<=tolerance_seconds:
                match=group; break
        if match is None: groups.append([row])
        else: match.append(row)
    return groups

def add_center_marker(image):
    image=image.convert("RGB"); draw=ImageDraw.Draw(image)
    x,y=image.width//2,image.height//2
    draw.line((x-10,y,x+10,y),fill=(0,0,0),width=3)
    draw.line((x,y-10,x,y+10),fill=(0,0,0),width=3)
    draw.line((x-10,y,x+10,y),fill=(255,255,255),width=1)
    draw.line((x,y-10,x,y+10),fill=(255,255,255),width=1)
    return image

def build(worksheet_path,provenance_path,chips_dir,output_dir):
    with Path(worksheet_path).open(newline="",encoding="utf-8-sig") as f:
        reader=csv.DictReader(f); fields=list(reader.fieldnames or []); worksheet=list(reader)
    with Path(provenance_path).open(newline="",encoding="utf-8-sig") as f:
        provenance=list(csv.DictReader(f))
    if not {"sample_id","longitude","latitude"}.issubset(set(fields)):
        raise ValueError("Worksheet must contain sample_id, longitude, latitude")
    if not {"sample_id","platform","datetime","status","chip_file"}.issubset(set(provenance[0] if provenance else [])):
        raise ValueError("RGB provenance is missing required columns")
    if "review_contact_sheet" not in fields: fields.append("review_contact_sheet")
    if "rgb_chip_inventory" not in fields: fields.append("rgb_chip_inventory")
    by_point=defaultdict(list)
    for row in provenance:
        if row.get("status")=="chip_created" and row.get("chip_file"):
            by_point[row["sample_id"]].append(row)
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=True)
    chips=Path(chips_dir)
    summaries=[]
    for point in worksheet:
        sample=point["sample_id"]
        groups=deduplicate(by_point.get(sample,[]))
        inventory=[]; tiles=[]
        for aliases in groups:
            row=aliases[0]
            filename=Path(row["chip_file"]).name
            chip=chips/filename
            if not chip.exists():
                raise FileNotFoundError(f"Missing RGB chip for {sample}: {chip}")
            with Image.open(chip) as source:
                image=add_center_marker(source.copy())
            inventory.append({
                "chip_file":"chips/"+filename,"datetime":row.get("datetime",""),
                "platform":row.get("platform",""),"item_ids":[r.get("item_id","") for r in aliases],
                "collections":[r.get("collection","") for r in aliases],
                "catalogue_alias_count":len(aliases),"cloud_cover_percent":row.get("cloud_cover_percent",""),
                "sha256":row.get("chip_sha256",""),"source_grid":row.get("source_grid",""),
                "display_stretch":row.get("stretch",""),
            })
            tiles.append((image,row))
        width=256; header=30; footer=18
        sheet=Image.new("RGB",(max(1,len(tiles))*width,header+(tiles[0][0].height if tiles else 1)+footer),(245,245,245))
        draw=ImageDraw.Draw(sheet)
        for index,(image,row) in enumerate(tiles):
            x=index*width; sheet.paste(image,(x,header))
            draw.text((x+5,7),f'{row.get("datetime","")[:10]} | {row.get("platform","")}',fill=(0,0,0))
            try: cloud=f'{float(row.get("cloud_cover_percent","")):.1f}%'
            except (TypeError,ValueError): cloud=row.get("cloud_cover_percent","")
            draw.text((x+5,header+image.height+2),f"Scene cloud metadata: {cloud}",fill=(0,0,0))
        contact=out/f"{sample}_contact.png"
        sheet.save(contact,optimize=True)
        point["rgb_chip_inventory"]=json.dumps(inventory,sort_keys=True)
        point["review_contact_sheet"]="review-chips/"+contact.name
        summaries.append({"sample_id":sample,"unique_rgb_acquisitions":len(groups),"source_chip_records":sum(len(g) for g in groups)})
    with Path(worksheet_path).open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=fields); writer.writeheader(); writer.writerows(worksheet)
    return {"points":len(worksheet),"contact_sheets":len(summaries),
            "unique_rgb_acquisitions":sum(x["unique_rgb_acquisitions"] for x in summaries),
            "source_chip_records":sum(x["source_chip_records"] for x in summaries),
            "contact_sheet_dir":str(out)}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--worksheet",required=True); p.add_argument("--rgb-provenance",required=True)
    p.add_argument("--chips-dir",required=True); p.add_argument("--output-dir",required=True)
    a=p.parse_args(); print(json.dumps(build(a.worksheet,a.rgb_provenance,a.chips_dir,a.output_dir),indent=2)); return 0
if __name__=="__main__": raise SystemExit(main())
