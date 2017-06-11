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
        will
        """
        pass

    def test_pool(self):
        response = requests.get(self.base_url+'/pool')
        self.assertEqual(response.status_code, 200)
        assert json.loads(response.text)


    
if __name__ == "__main__":
    unittest.main()
