import unittest
from flask_app.model import GetData

class TestGetData(unittest.TestCase):

    def setUp(self):
        self.test_hash = "abcd1234"
        self.get_data_instance = GetData(self.test_hash)
        

    def test_initialization(self):
        self.assertEqual(self.get_data_instance._hash, self.test_hash)

    def test_get_hash(self):
        pass
        #self.assertEqual(self.get_data_instance.get_hash, self.test_hash)

    def test_retrieve_data(self):
        self.assertEqual(self.get_data_instance.get_secret(), "This is the secret :)")

if __name__ == '__main__':
    unittest.main()
