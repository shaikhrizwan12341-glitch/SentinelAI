from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError


password_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    """Hash a plain-text password using Argon2."""

    if not password:
        raise ValueError("Password cannot be empty.")

    return password_hasher.hash(password)


def verify_password(
    password: str,
    password_hash: str,
) -> bool:
    """Verify a password against an Argon2 password hash."""

    if not password or not password_hash:
        return False

    try:
        return password_hasher.verify(
            password_hash,
            password,
        )

    except (VerifyMismatchError, VerificationError):
        return False