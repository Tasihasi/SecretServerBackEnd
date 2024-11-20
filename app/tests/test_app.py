import unittest
from flask_app import create_app

class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        #self.app.app_context().push()  # Ensure the app context is pushed

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello, World!', response.data)

    def test_secret_get_without_hash(self):
        # This test will pass for the /secret route with no hash
        response = self.client.get('/secret/')
        self.assertEqual(response.status_code, 405)
        self.assertIn(b'Invalid input', response.data)

    def test_secret_get_with_hash(self):
        # GET request with a hash (e.g., /secret/abcd123) should return 200 with the secret data
        response = self.client.get('/secret/abcd123')
        #self.assertEqual(response.status_code, 200)
        #self.assertIn(b"I like big apples.", response.data)  # Assuming this is your placeholder secret text

    def test_secret_post_with_hash(self):
        # POST request with hash
        response = self.client.post('/secret/abcd123')
        self.assertEqual(response.status_code, 405)
        self.assertIn(b'Invalid input', response.data)
    """
    def test_secret_post_without_hash(self):
        # POST request without a hash should return a valid response and the "Hash" field
        response = self.client.post('/secret/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"abcd123", response.data)  # This is assuming the hash generated in your post_data method is 'abcd123'
    """

    def test_secret_post_invalid_data(self):
        """Test POST request without all required fields (should return 405 and invalid input)"""
        form_data = {
            'secret': 'Test secret text',
            # Missing 'expireAfterViews' and 'expireAfter'
        }

        response = self.client.post('/secret/', data=form_data)
        
        self.assertEqual(response.status_code, 405)
        self.assertIn(b'Invalid input', response.data)

    def test_secret_post_invalid_expire_values(self):
        """Test POST request with invalid 'expireAfter' and 'expireAfterViews' values"""
        form_data = {
            'secret': 'Test secret text',
            'expireAfterViews': -1,  # Invalid value
            'expireAfter': -10      # Invalid value
        }

        response = self.client.post('/secret/', data=form_data)
        
        self.assertEqual(response.status_code, 405)  # Assuming validation fails, this should return 405
        self.assertIn(b'Invalid input', response.data)



if __name__ == '__main__':
    unittest.main()
