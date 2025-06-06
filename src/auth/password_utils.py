import hashlib
import secrets
import string


class Password:
    """
    A class to handle password-related utilities such as hashing and generating secure passwords.
    """
    ALLOWED_CHARS = string.ascii_letters + string.digits

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hashes a password using SHA-256.
        Args:
            password (str): The password to hash.
        Returns:
            str: The hexadecimal SHA-256 hash of the password.
        """
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    @staticmethod
    def generate_password(length: int = 12) -> str:
        """
        Generates a secure random password using letters and digits.
        Args:
            length (int): The length of the password (default is 12).
        Returns:
            str: A secure random password.
        Raises:
            ValueError: If the length is negative.
        """
        if length < 0:
            raise ValueError("Password length must be non-negative.")
        return ''.join(secrets.choice(Password.ALLOWED_CHARS) for _ in range(length))

    @staticmethod
    def generate_key(prefix: str = "key", length: int = 32) -> str:
        """
        Generates a secure random authentication key with a custom prefix.
        Args:
            prefix (str): Prefix to prepend to the key (default is "key").
            length (int): Length of the random part of the key (default is 32).
        Returns:
            str: A secure authentication key.
        Raises:
            ValueError: If the length is negative.
        """
        if length < 0:
            raise ValueError("Key length must be non-negative.")
        random_part = ''.join(secrets.choice(Password.ALLOWED_CHARS) for _ in range(length))
        return f"{prefix}{random_part}"