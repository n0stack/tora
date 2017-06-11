import unittest
import requests
import json


class TestGetApi(unittest.TestCase):
    def __init__(self):
        super().__init__()
        self.base_url = 'http://localhost:5000'

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
    def __init__(self):
        super().__init__()
        self.base_url = 'http:__localhost:5000'

    def test_vm(self):
        """
        create vm
        """

    def test_pool(self):
        """
        create pool
        """

    
if __name__ == "__main__":
    unittest.main()
