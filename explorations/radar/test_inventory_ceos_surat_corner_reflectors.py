import unittest
from explorations.radar.inventory_ceos_surat_corner_reflectors import parse_surat_targets

def kml(names):
    placemarks=[]
    for i,name in enumerate(names):
        placemarks.append(f"<Placemark><name>{name}</name><Point><coordinates>{150+i*0.001},-26.5,0</coordinates></Point></Placemark>")
    return ("<kml xmlns='http://www.opengis.net/kml/2.2'><Document>"+"".join(placemarks)+"</Document></kml>").encode()

class CeosSuratInventoryTests(unittest.TestCase):
    def test_extracts_all_40_targets(self):
        targets=parse_surat_targets(kml([f"Surat Basin {i:02d}" for i in range(1,41)]))
        self.assertEqual(len(targets),40)
        self.assertEqual(targets[0]["name"],"Surat Basin 01")
        self.assertAlmostEqual(targets[0]["longitude"],150.0)

    def test_rejects_incomplete_collection(self):
        with self.assertRaises(ValueError):
            parse_surat_targets(kml([f"Surat Basin {i:02d}" for i in range(1,40)]))

    def test_ignores_other_target_collections(self):
        xml=kml([f"Surat Basin {i:02d}" for i in range(1,41)])+b""
        xml=xml.replace(b"</Document>",b"<Placemark><name>Wettzell CR</name><Point><coordinates>12,49,0</coordinates></Point></Placemark></Document>")
        self.assertEqual(len(parse_surat_targets(xml)),40)

if __name__=="__main__": unittest.main()
