from tests.base import BaseTestCase
from app.arcgis_config import products
from app import db
from app.models import Server, Product, Updates, History, User, Workstation

from app.read_licenses import split_license_data, parse_server_info, product_has_users

class TestUpsert(BaseTestCase):

    def test_upsert(self):
        # insert
        dummy_p1 = products['ARC/INFO']
        dummy_p1['server_id'] = 1
        dummy_p1['internal_name'] = "ARC/INFO"
        dummy_p1['license_out'] = 1
        dummy_p1['license_total'] = 2
        result = Product.upsert(**dummy_p1)
        self.assertEqual(result, 1)

        # insert
        dummy_p2 = products['EDITOR']
        dummy_p2['server_id'] = 1
        dummy_p2['internal_name'] = "EDITOR"
        dummy_p2['license_out'] = 5
        dummy_p2['license_total'] = 10
        result = Product.upsert(**dummy_p2)
        self.assertEqual(result, 2)

        # insert
        dummy_p3 = products['VIEWER']
        dummy_p3['server_id'] = 1
        dummy_p3['internal_name'] = "VIEWER"
        dummy_p3['license_out'] = 2
        dummy_p3['license_total'] = 4
        result = Product.upsert(**dummy_p3)
        self.assertEqual(result, 3)

        # update
        dummy_p3['expires'] = "permanent(no expiration date)".upper()
        dummy_p3['version'] = "10.1"
        result = Product.upsert(**dummy_p3)
        self.assertEqual(result, 3)

class TestFunctions(BaseTestCase):

    def test_product_has_users(self):

        data1 = 'LMUTIL - COPYRIGHT (C) 1989-2018 FLEXERA. ALL RIGHTS RESERVED.\nFLEXIBLE LICENSE MANAGER STATUS ON MON 12/23/2019 12:03\n[DETECTING LMGRD PROCESSES...]\nLICENSE SERVER STATUS: 27000@GV-GISLICENSE\n\n    LICENSE FILE(S) ON GV-GISLICENSE: C:\PROGRAM FILES (X86)\ARCGIS\LICENSEMANAGER\BIN\SERVICE.TXT:\nGV-GISLICENSE: LICENSE SERVER UP (MASTER) V11.16.2\nVENDOR DAEMON STATUS (ON GV-GISLICENSE):\nARCGIS: UP V11.16.2\nFEATURE USAGE INFO:\n'
        data2 = ' DESKTOPADVP:  (TOTAL OF 1 LICENSE ISSUED;  TOTAL OF 0 LICENSES IN USE)\n'
        data3 = 'DESKTOPBASICP:  (TOTAL OF 10 LICENSES ISSUED;  TOTAL OF 1 LICENSE IN USE)\n"DESKTOPBASICP" V10.1, VENDOR: ARCGIS, EXPIRY: PERMANENT(NO EXPIRATION DATE)\nFLOATING LICENSE\nSHILANDI WIN10-SHILANDI WIN10-SHILANDI (V10.1) (GV-GISLICENSE/27000 531), START MON 12/23 11:55\n'

        # result1 = product_has_users(data1, 1)
        # result2 = product_has_users(data2, 1)
        result3 = product_has_users(data3, 1)

        # self.assertIsNone(result1)
        # self.assertIsNone(result2)
        self.assertIsNotNone(result3)


class TestParsing(BaseTestCase):

    def test_product_splitting(self):

        result = split_license_data(self.lines)
        self.assertEqual(len(result), 21)
