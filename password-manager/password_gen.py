"""
password_gen.py — Cryptographically secure password generator.

Uses Python's `secrets` module (backed by the OS CSPRNG) instead of
`random`, ensuring passwords are suitable for security-sensitive use.
"""

import secrets
import string


def generate_password(
    length: int = 16,
    use_uppercase: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
) -> str:
    """
    Generate a cryptographically secure random password.

    Args:
        length:        Total number of characters (min 8).
        use_uppercase: Include uppercase letters (A-Z).
        use_digits:    Include digits (0-9).
        use_symbols:   Include special characters (!@#$%^&*...).

    Returns:
        A random password string of the requested length.
    """
    if length < 8:
        raise ValueError("Password length must be at least 8 characters.")

    pool = string.ascii_lowercase
    required = []

    if use_uppercase:
        pool += string.ascii_uppercase
        required.append(secrets.choice(string.ascii_uppercase))
    if use_digits:
        pool += string.digits
        required.append(secrets.choice(string.digits))
    if use_symbols:
        symbols = "!@#$%^&*()-_=+[]{}|;:,.<>?"
        pool += symbols
        required.append(secrets.choice(symbols))

    # Fill the remaining length with random picks from the full pool
    remaining = [secrets.choice(pool) for _ in range(length - len(required))]

    # Shuffle to avoid predictable positions for required chars
    password_chars = required + remaining
    secrets.SystemRandom().shuffle(password_chars)

    return "".join(password_chars)
