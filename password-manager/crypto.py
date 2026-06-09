"""
crypto.py — Key derivation and Fernet encryption helpers.

Security model:
  - Master password is NEVER stored.
  - A random 16-byte salt is generated once and saved to salt.key.
  - PBKDF2-HMAC-SHA256 (480,000 iterations) derives a 32-byte key from
    the master password + salt, which is then base64-encoded for Fernet.
  - All vault data is encrypted with Fernet (AES-128-CBC + HMAC-SHA256).
"""

import os
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet, InvalidToken

SALT_FILE = "salt.key"
ITERATIONS = 480_000


def generate_salt() -> bytes:
    """Generate a cryptographically random 16-byte salt."""
    return os.urandom(16)


def load_or_create_salt() -> bytes:
    """Load existing salt from disk, or create and save a new one."""
    if os.path.exists(SALT_FILE):
        with open(SALT_FILE, "rb") as f:
            return f.read()
    salt = generate_salt()
    with open(SALT_FILE, "wb") as f:
        f.write(salt)
    return salt


def derive_key(master_password: str, salt: bytes) -> bytes:
    """Derive a Fernet-compatible key from the master password and salt."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ITERATIONS,
        backend=default_backend(),
    )
    return base64.urlsafe_b64encode(kdf.derive(master_password.encode()))


def get_fernet(master_password: str) -> Fernet:
    """Return a Fernet instance keyed from the master password."""
    salt = load_or_create_salt()
    key = derive_key(master_password, salt)
    return Fernet(key)


def encrypt(plaintext: str, fernet: Fernet) -> str:
    """Encrypt a plaintext string and return a base64 token string."""
    return fernet.encrypt(plaintext.encode()).decode()


def decrypt(token: str, fernet: Fernet) -> str:
    """Decrypt a token string. Raises InvalidToken if key is wrong."""
    return fernet.decrypt(token.encode()).decode()
