import unittest
from explorations.radar.extract_sentinel1_grd_incidence_grids import parse_geolocation_grid

class ExtractGeolocationGridTests(unittest.TestCase):
    def test_parses_complete_grid_and_retains_tie_points(self):
        xml=b"""<root xmlns='urn:test'><geolocationGrid><geolocationGridPoint><line>0</line><pixel>0</pixel><latitude>-1</latitude><longitude>36</longitude><height>100</height><incidenceAngle>30</incidenceAngle><elevationAngle>2</elevationAngle></geolocationGridPoint><geolocationGridPoint><line>0</line><pixel>10</pixel><latitude>-1</latitude><longitude>36.1</longitude><height>100</height><incidenceAngle>31</incidenceAngle><elevationAngle>2</elevationAngle></geolocationGridPoint><geolocationGridPoint><line>10</line><pixel>0</pixel><latitude>-1.1</latitude><longitude>36</longitude><height>100</height><incidenceAngle>32</incidenceAngle><elevationAngle>2</elevationAngle></geolocationGridPoint><geolocationGridPoint><line>10</line><pixel>10</pixel><latitude>-1.1</latitude><longitude>36.1</longitude><height>100</height><incidenceAngle>33</incidenceAngle><elevationAngle>2</elevationAngle></geolocationGridPoint></geolocationGrid></root>"""
        result=parse_geolocation_grid(xml)
        self.assertEqual(result["point_count"],4)
        self.assertTrue(result["grid_complete"])
        self.assertEqual(result["incidence_angle_degrees"]["median"],31.5)
        self.assertEqual(result["points"][2]["line"],10.0)

    def test_rejects_empty_grid(self):
        with self.assertRaises(ValueError):
            parse_geolocation_grid(b"<root/>")

if __name__=="__main__": unittest.main()
