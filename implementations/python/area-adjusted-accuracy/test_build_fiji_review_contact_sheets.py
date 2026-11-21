import csv,json,tempfile,unittest
from pathlib import Path
from PIL import Image
from build_fiji_review_contact_sheets import build,deduplicate

class ContactSheetTests(unittest.TestCase):
 def test_alias_dedup_and_centered_contact_sheet(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d); chips=root/"chips"; chips.mkdir()
   Image.new("RGB",(256,256),(20,80,40)).save(chips/"one.png")
   worksheet=root/"worksheet.csv"
   worksheet.write_text("sample_id,longitude,latitude\nP1,179,-18\n",encoding="utf-8")
   prov=root/"provenance.csv"
   with prov.open("w",newline="",encoding="utf-8") as f:
    fields=["sample_id","platform","datetime","status","chip_file","item_id","collection","cloud_cover_percent","chip_sha256","source_grid","stretch"]
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
    for item,collection,time in [("alias1","old","2021-06-01T00:00:00Z"),("alias2","new","2021-06-01T00:00:01Z")]:
     w.writerow({"sample_id":"P1","platform":"sentinel-2a","datetime":time,"status":"chip_created","chip_file":"/tmp/one.png","item_id":item,"collection":collection,"cloud_cover_percent":"1","chip_sha256":"abc","source_grid":"{}","stretch":"test"})
   result=build(worksheet,prov,chips,root/"review")
   self.assertEqual(result["contact_sheets"],1)
   self.assertEqual(result["unique_rgb_acquisitions"],1)
   with worksheet.open(newline="",encoding="utf-8") as f: row=next(csv.DictReader(f))
   inventory=json.loads(row["rgb_chip_inventory"])
   self.assertEqual(inventory[0]["catalogue_alias_count"],2)
   self.assertTrue((root/"review"/"P1_contact.png").exists())
   with Image.open(root/"review"/"P1_contact.png") as contact:
    self.assertEqual(contact.size,(512,320))
   self.assertIn("320 m",inventory[0]["zoom_crop_extent"])
 def test_distinct_dates_remain_distinct(self):
  rows=[{"platform":"S2","datetime":"2021-01-01T00:00:00Z"},{"platform":"S2","datetime":"2021-01-03T00:00:00Z"}]
  self.assertEqual(len(deduplicate(rows)),2)

if __name__=="__main__": unittest.main()
