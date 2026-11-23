import unittest
from explorations.radar.probe_sentinel1_grd_geolocation_grid import summarize_geolocation_grid

class GeolocationGridProbeTests(unittest.TestCase):
    def test_summarizes_incidence_angle_grid(self):
        xml=b"""<root xmlns='urn:test'><geolocationGrid><geolocationGridPoint><line>0</line><pixel>0</pixel><latitude>-1.0</latitude><longitude>36.0</longitude><incidenceAngle>30</incidenceAngle><elevationAngle>2</elevationAngle></geolocationGridPoint><geolocationGridPoint><line>0</line><pixel>10</pixel><latitude>-1.0</latitude><longitude>36.1</longitude><incidenceAngle>31</incidenceAngle><elevationAngle>2</elevationAngle></geolocationGridPoint><geolocationGridPoint><line>10</line><pixel>0</pixel><latitude>-1.1</latitude><longitude>36.0</longitude><incidenceAngle>32</incidenceAngle><elevationAngle>2</elevationAngle></geolocationGridPoint><geolocationGridPoint><line>10</line><pixel>10</pixel><latitude>-1.1</latitude><longitude>36.1</longitude><incidenceAngle>33</incidenceAngle><elevationAngle>2</elevationAngle></geolocationGridPoint></geolocationGrid></root>"""
        result=summarize_geolocation_grid(xml)
        self.assertEqual(result["geolocation_point_count"],4)
        self.assertEqual(result["unique_line_count"],2)
        self.assertEqual(result["unique_pixel_count"],2)
        self.assertTrue(result["grid_complete"])
        self.assertEqual(result["incidence_angle_degrees"]["median"],31.5)

    def test_rejects_missing_incidence_angle_grid(self):
        with self.assertRaises(ValueError):
            summarize_geolocation_grid(b"<root><geolocationGrid/></root>")

if __name__=="__main__": unittest.main()
