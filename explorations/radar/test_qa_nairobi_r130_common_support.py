import unittest
from explorations.radar.qa_nairobi_r130_common_support import BURST_RE, DATE_RE, SUPPORT_THRESHOLD, MIN_COMMON_PIXELS

class CommonSupportQATests(unittest.TestCase):
    def test_parses_opera_burst_and_date(self):
        name="OPERA_L2_RTC-S1_T130-279214-IW3_20261006T155542Z_20261012T171313Z_S1D_30_v1.0_VV.tif"
        self.assertEqual(BURST_RE.search(name).group(1),"T130-279214-IW3")
        self.assertEqual(DATE_RE.search(name).group(1),"20261006")
    def test_declared_support_gates(self):
        self.assertEqual(SUPPORT_THRESHOLD,0.95)
        self.assertGreaterEqual(MIN_COMMON_PIXELS,1000)

if __name__=="__main__":unittest.main()
