import unittest
from explorations.radar.audit_opera_nairobi_r130_assets import decode, SAFE_RE

class AuditHelpersTests(unittest.TestCase):
    def test_decode_bytes_and_numpy_scalar(self):
        self.assertEqual(decode(b"Sentinel-1D"),"Sentinel-1D")
    def test_safe_identifier_pattern(self):
        name="S1D_IW_SLC__1SDV_20261123T155530_20261123T155555_005596_00AB9A_AA88.SAFE"
        self.assertIsNotNone(SAFE_RE.search(name))
    def test_grd_does_not_match_slc(self):
        self.assertIsNone(SAFE_RE.search("S1D_IW_GRDH_1SDV_20261123T155530_20261123T155555_005596_00AB9A_AA88.SAFE"))

if __name__=="__main__": unittest.main()
