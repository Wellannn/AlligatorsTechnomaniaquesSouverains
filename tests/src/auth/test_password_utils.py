import unittest
from src.auth.password_utils import *

class TestPassword(unittest.TestCase):
    
    def test_hash_password(self):
        # Test hash password
        result = hash_password("test123")
        
        # Check result is not empty
        self.assertIsNotNone(result)
        
        # Check same password gives same result
        result2 = hash_password("test123")
        self.assertEqual(result, result2)
    
    def test_generate_password(self):
        # Test generate password
        password = generate_password()
        
        # Check password is created
        self.assertIsNotNone(password)
        
        # Check password has 10 characters
        self.assertEqual(len(password), 10)
    
    def test_generate_key(self):
        # Test generate key
        key = generate_key()
        
        # Check key is created
        self.assertIsNotNone(key)
        
        # Check key starts with "key"
        self.assertTrue(key.startswith("key"))

if __name__ == "__main__":
    unittest.main()