import gzip
import re
from functools import lru_cache
from pathlib import Path

MIN_PASSWORD_LENGTH = 8

COMMON_PASSWORDS_FILE = (
    Path(__file__).parent / "common-passwords.txt.gz"
)

# Regex rules
UPPERCASE_REGEX = re.compile(r"[A-Z]")
LOWERCASE_REGEX = re.compile(r"[a-z]")
DIGIT_REGEX = re.compile(r"\d")
SPECIAL_CHAR_REGEX = re.compile(r"[^\w\s]")  # symbols only


@lru_cache(maxsize=1)
def load_common_passwords() -> set[str]:
    """
    Load and cache common passwords from gz file.
    Cached in memory after first load.
    """
    passwords: set[str] = set()

    with gzip.open(COMMON_PASSWORDS_FILE, "rt", encoding="utf-8") as f:
        for line in f:
            password = line.strip()
            if password:
                passwords.add(password.lower())

    return passwords


class PasswordValidator:
    @staticmethod
    def validate(value: str) -> str:
        if not value:
            raise ValueError("Password cannot be empty")

        # 1. Minimum length
        if len(value) < MIN_PASSWORD_LENGTH:
            raise ValueError(
                f"Password must be at least {MIN_PASSWORD_LENGTH} characters long"
            )

        # 2. Common password check
        if value.lower() in load_common_passwords():
            raise ValueError("Password is too common")

        # 3. Numeric-only check
        if value.isdigit():
            raise ValueError("Password cannot be entirely numeric")

        # 4. Strength rules
        if not UPPERCASE_REGEX.search(value):
            raise ValueError("Password must contain at least one uppercase letter")

        if not LOWERCASE_REGEX.search(value):
            raise ValueError("Password must contain at least one lowercase letter")

        if not DIGIT_REGEX.search(value):
            raise ValueError("Password must contain at least one number")

        if not SPECIAL_CHAR_REGEX.search(value):
            raise ValueError("Password must contain at least one special character")

        return value
