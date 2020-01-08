import datetime
from tests.base import BaseTestCase
from app.read_licenses import split_license_data, parse_server_info, add_product, add_users_and_workstations, \
    map_product_id, parse_product_info, parse_version_info, parse_users_and_workstations


class TestFunctions(BaseTestCase):
    def test_parse_server_info(self):
        result = parse_server_info(self.lines)
        self.assertEqual(result[2], 'UP')

    def test_reset_year(self):
        pass

    def test_split_license_data(self):
        result = split_license_data(self.lines)
        self.assertEqual(len(result), 21)

    def test_add_product(self):
        line = ' DESKTOPBASICP:  (TOTAL OF 10 LICENSES ISSUED;  TOTAL OF 1 LICENSE IN USE)\n  "DESKTOPBASICP" V10.1, VENDOR: ARCGIS, EXPIRY: PERMANENT(NO EXPIRATION DATE)\n  FLOATING LICENSE\n    SHILANDI WIN10-SHILANDI WIN10-SHILANDI (V10.1) (GV-GISLICENSE/27000 531), START MON 12/23 11:55'
        result = add_product(line, server_id=1)
        self.assertEqual(result, 1)

    def test_parse_product_info(self):
        lines = '    SHILANDI WIN10-SHILANDI WIN10-SHILANDI (V10.1) (GV-GISLICENSE/27000 1421), START THU 12/25 11:50\n' \
                '    TESTUSER WIN10-TESTUSER ,?UAH<J{7ONRGN+Q?-O (V10.1) (GV-GISLICENSE/27000 1421), START THU 12/26 13:50\n' \
                '    SHILANDI WIN10-SHILANDI-1 ,?UAH<Xt/TKm)-)m:(a1&f` (V10.1) (GV-GISLICENSE/27000 1421), START THU 12/25 11:50\n'

        parsed = parse_users_and_workstations(lines)

        item1 = next(parsed)
        self.assertEqual(item1[0], 'SHILANDI')
        self.assertEqual(item1[1], 'WIN10-SHILANDI')

        item2 = next(parsed)
        self.assertEqual(item2[0], 'TESTUSER')
        self.assertEqual(item2[1], 'WIN10-TESTUSER')

        item3 = next(parsed)
        self.assertEqual(item3[0], 'SHILANDI')
        self.assertEqual(item3[1], 'WIN10-SHILANDI-1')

    def test_parse_version_info(self):
        pass

    def test_add_users_and_workstations(self):
        line = '  VIEWER:  (TOTAL OF 14 LICENSES ISSUED;  TOTAL OF 1 LICENSE IN USE)\n' \
               '  "VIEWER" V10.1, VENDOR: ARCGIS, EXPIRY: PERMANENT(NO EXPIRATION DATE)\n' \
               '  FLOATING LICENSE\n' \
               '    SACHSJ WIN10-SACHSJ ,?UAH<J{7ONRGN+Q?-O (V10.1) (GV-GISLICENSE/27000 1421), START THU 12/26 13:50\n' \
               '    SHILANDI WIN10-SHILANDI WIN10-SHILANDI (V10.1) (GV-GISLICENSE/27000 1421), START THU 12/25 11:50\n' \
               '    SHILANDI WIN10-SHILANDI-1 WIN10-SHILANDI (V10.1) (GV-GISLICENSE/27000 1421), START THU 12/25 11:50\n'

        result = add_users_and_workstations(line)
        self.assertEqual(result[1]['user_id'], result[0]['user_id'] + 1)
        self.assertEqual(result[1]['user_id'], result[2]['user_id'])
        self.assertEqual(result[1]['workstation_id'], result[0]['workstation_id'] + 1)
        self.assertNotEqual(result[2]['workstation_id'], result[1]['workstation_id'])
        self.assertEqual(result[0]['time_out'], datetime.datetime(datetime.datetime.now().year, 12, 26, 13, 50))
        self.assertEqual(result[1]['time_out'], datetime.datetime(datetime.datetime.now().year, 12, 25, 11, 50))

    def test_map_product_id(self):
        arr = [{'user_id': 1, 'workstation_id': 1,
                'time_out': datetime.datetime(datetime.datetime.now().year, 12, 25, 1, 31)},
               {'user_id': 2, 'workstation_id': 2,
                'time_out': datetime.datetime(datetime.datetime.now().year, 12, 26, 2, 32)},
               {'user_id': 3, 'workstation_id': 3,
                'time_out': datetime.datetime(datetime.datetime.now().year, 12, 27, 3, 33)}]
        result = map_product_id(2, arr)
        self.assertEqual(result[0]['product_id'], 2)
        self.assertEqual(result[1]['product_id'], 2)
        self.assertEqual(result[2]['product_id'], 2)
