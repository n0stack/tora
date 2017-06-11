import unittest
import requests
import json


class TestGetApi(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://localhost:5000'

    def tearDown(self):
        pass

    def test_vm(self):
        response = requests.get(self.base_url+'/vm')
        self.assertEqual(response.status_code, 200)
        assert json.loads(response.text)

    def test_vm_name(self):
        """
        get <vm_name>'s information
        """
        pass

    def test_pool(self):
        response = requests.get(self.base_url+'/pool')
        self.assertEqual(response.status_code, 200)
        assert json.loads(response.text)

    def test_pool_name(self):
        """
        get <pool_name>'s information
        """
        pass


class TestPostApi(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://localhost:5000'

    def tearDown(self):
        pass

    def test_vm(self):
        """
        create vm
        """

    def test_pool(self):
        """
        create pool
        """

class TestPutApi(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://localhost:5000'

    def tearDown(self):
        pass

    def test_vm(self):
        """
        change vm's power_status
        """

if __name__ == "__main__":
    unittest.main()
