import unittest, hashlib
from flask_app.model import PostData  
from datetime import datetime, timedelta

class TestPostData(unittest.TestCase):

    def setUp(self):
        self.secret_text = "This is a secret"
        self.expire_after_views = 5
        self.expire_after = 10  # In minutes
        self.post_data_instance = PostData(self.secret_text, self.expire_after_views, self.expire_after)

    def test_initialization(self):
        """Test that the PostData instance is initialized with the correct values"""
        self.assertEqual(self.post_data_instance.secret_text, self.secret_text)
        self.assertEqual(self.post_data_instance.expire_after_views, self.expire_after_views)
        self.assertEqual(self.post_data_instance.expire_after, self.expire_after)
        self.assertEqual(self.post_data_instance.hash, hashlib.sha256(self.secret_text.encode()).hexdigest())
        self.assertIsInstance(self.post_data_instance.created_at, datetime)
        self.assertEqual(self.post_data_instance.expiration_date, self.post_data_instance.created_at + timedelta(minutes=self.expire_after))

    def test_property_setters(self):
        """Test that the property setters update the values correctly"""
        new_secret_text = "New secret text"
        new_expire_after_views = 10
        new_expire_after = 20

        self.post_data_instance.secret_text = new_secret_text
        self.post_data_instance.expire_after_views = new_expire_after_views
        self.post_data_instance.expire_after = new_expire_after

        self.assertEqual(self.post_data_instance.secret_text, new_secret_text)
        self.assertEqual(self.post_data_instance.expire_after_views, new_expire_after_views)
        self.assertEqual(self.post_data_instance.expire_after, new_expire_after)

    def test_to_dict(self):
        """Test the to_dict method"""
        expected_dict = {
            "hash": self.post_data_instance.hash,
            "secret": self.post_data_instance.secret_text,
            "expire_after_views": self.post_data_instance.expire_after_views,
            "expire_after": self.post_data_instance.expire_after,
            "created_at": self.post_data_instance.created_at.isoformat(),
            "expiration_date": (self.post_data_instance.created_at + timedelta(minutes=self.post_data_instance.expire_after)).isoformat()
        }
        self.assertEqual(self.post_data_instance._to_dict(), expected_dict)

    def test_post_to_db(self):
        """Test the post_to_db method (currently always returns True)"""
        self.assertTrue(self.post_data_instance.post_to_db())

    def test_expire_after_views_validation(self):
        """Test that invalid expire_after_views raises ValueError"""
        with self.assertRaises(ValueError):
            PostData("Test secret", -1, 60)

    def test_expire_after_validation(self):
        """Test that invalid expire_after raises ValueError"""
        with self.assertRaises(ValueError):
            PostData("Test secret", 5, -10)


if __name__ == '__main__':
    unittest.main()
