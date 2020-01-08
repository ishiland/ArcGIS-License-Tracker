from tests.base import BaseTestCase
from app.arcgis_config import products
from app.models import Server, Product, Updates, History, User, Workstation
from app import db

class TestProduct(BaseTestCase):
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


class TestWorkstation(BaseTestCase):
    def test_add(self):
        result1 = Workstation.add('WIN10-SHILAND')
        result2 = Workstation.add('WIN10-SHILAND1')
        self.assertEqual(result1, result2 - 1)


class TestServer(BaseTestCase):
    def test_upsert(self):
        result1 = Server.upsert('test1', 27000)
        result1_same = Server.upsert('test1', 27000)
        self.assertEqual(result1, result1_same)
        result2 = Server.upsert('test2', 27000)
        self.assertEqual(result1, result2 - 1)


class TestUpdates(BaseTestCase):

    def test_end(self):
        # test start update
        start_id = Updates.start(server_id=1)
        self.assertEqual(start_id, 1)

        # test end update
        Updates.end(start_id, 'UP', 'test-message')
        query = Updates.query.order_by(Updates.id.desc()).limit(1).first()
        self.assertEqual(query.id, 1)
        self.assertEqual(query.status, 'UP')
        self.assertEqual(query.info, 'test-message')

