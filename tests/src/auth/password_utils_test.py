import unittest
from src.auth.password_utils import Password

class TestPasswordUtils(unittest.TestCase):

    def test_hash_password_consistency(self):
        password = "TestPassword123!"
        hash1 = Password.hash_password(password)
        hash2 = Password.hash_password(password)
        self.assertEqual(hash1, hash2)
        self.assertIsInstance(hash1, str)
        self.assertEqual(len(hash1), 64)

    def test_hash_password_different_inputs(self):
        hash1 = Password.hash_password("password1")
        hash2 = Password.hash_password("password2")
        self.assertNotEqual(hash1, hash2)

    def test_hash_password_empty_string(self):
        hash1 = Password.hash_password("")
        hash2 = Password.hash_password("")
        self.assertEqual(hash1, hash2)
        self.assertEqual(len(hash1), 64)

    def test_hash_password_unicode(self):
        password = "pässwördÜñîçødë"
        hash1 = Password.hash_password(password)
        hash2 = Password.hash_password(password)
        self.assertEqual(hash1, hash2)
        self.assertEqual(len(hash1), 64)

    def test_generate_password_default_length(self):
        pwd = Password.generate_password()
        self.assertIsInstance(pwd, str)
        self.assertEqual(len(pwd), 12)
        self.assertTrue(all(c in Password.ALLOWED_CHARS for c in pwd))

    def test_generate_password_custom_length(self):
        for length in [1, 8, 20, 100]:
            pwd = Password.generate_password(length)
            self.assertEqual(len(pwd), length)
            self.assertTrue(all(c in Password.ALLOWED_CHARS for c in pwd))

    def test_generate_password_randomness(self):
        pwd1 = Password.generate_password()
        pwd2 = Password.generate_password()
        self.assertNotEqual(pwd1, pwd2)

    def test_generate_password_all_allowed_chars(self):
        found = set()
        for _ in range(1000):
            pwd = Password.generate_password(32)
            found.update(set(pwd))
            if set(Password.ALLOWED_CHARS).issubset(found):
                break
        self.assertTrue(set(Password.ALLOWED_CHARS).issubset(found))

    def test_generate_key_default(self):
        key = Password.generate_key()
        self.assertTrue(key.startswith("key"))
        self.assertEqual(len(key), 3 + 32)
        self.assertTrue(all(c in Password.ALLOWED_CHARS for c in key[3:]))

    def test_generate_key_custom_prefix_and_length(self):
        prefix = "auth_"
        length = 16
        key = Password.generate_key(prefix=prefix, length=length)
        self.assertTrue(key.startswith(prefix))
        self.assertEqual(len(key), len(prefix) + length)
        self.assertTrue(all(c in Password.ALLOWED_CHARS for c in key[len(prefix):]))

    def test_generate_key_empty_prefix(self):
        key = Password.generate_key(prefix="", length=10)
        self.assertEqual(len(key), 10)
        self.assertTrue(all(c in Password.ALLOWED_CHARS for c in key))

    def test_generate_key_zero_length(self):
        key = Password.generate_key(length=0)
        self.assertEqual(key, "key")

    def test_generate_key_long_prefix(self):
        prefix = "p" * 100
        key = Password.generate_key(prefix=prefix, length=5)
        self.assertTrue(key.startswith(prefix))
        self.assertEqual(len(key), 100 + 5)

    def test_generate_password_invalid_length(self):
        with self.assertRaises(ValueError):
            Password.generate_password(-1)

    def test_generate_key_invalid_length(self):
        with self.assertRaises(ValueError):
            Password.generate_key(length=-5)

if __name__ == "__main__":
    unittest.main()
