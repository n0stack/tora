import unittest
import requests
import json

class TestGetApi(unittest.TestCase):
    def test_vm(self):
        response = requests.get('http://localhost:5000/vm')
        self.assertEqual(response.status_code, 200)
        assert json.loads(response.text)
        
    
if __name__ == "__main__":
    unittest.main()
