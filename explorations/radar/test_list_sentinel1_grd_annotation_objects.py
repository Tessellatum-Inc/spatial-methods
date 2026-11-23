from __future__ import annotations
import importlib.util
import unittest
from pathlib import Path

P=Path(__file__).with_name("list_sentinel1_grd_annotation_objects.py")
S=importlib.util.spec_from_file_location("annotation_object_inventory",P)
M=importlib.util.module_from_spec(S); S.loader.exec_module(M)

class TestAnnotationObjectInventory(unittest.TestCase):
    def test_parse_s3_asset_prefix(self):
        bucket,prefix=M.parse_s3_uri("s3://eodata/Sentinel-1/SAR/IW_GRDH_1S-COG/2025/01/08/product.SAFE")
        self.assertEqual(bucket,"eodata")
        self.assertEqual(prefix,"Sentinel-1/SAR/IW_GRDH_1S-COG/2025/01/08/product.SAFE/")

    def test_reject_non_s3_asset_uri(self):
        with self.assertRaises(ValueError):
            M.parse_s3_uri("https://example.com/product.SAFE")

    def test_annotation_xml_filter_is_narrow(self):
        self.assertTrue(M.annotation_object("product.SAFE/annotation/s1a-iw-grd-vv.xml"))
        self.assertFalse(M.annotation_object("product.SAFE/measurement/data.tiff"))
        self.assertFalse(M.annotation_object("product.SAFE/manifest.safe"))

if __name__=="__main__": unittest.main()
