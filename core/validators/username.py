import re

USERNAME_REGEX = re.compile(
    r"^(?=.{3,20}$)[a-zA-Z0-9]+(_[a-zA-Z0-9]+)*$"
)


class UsernameValidator:
    @staticmethod
    def validate(value: str) -> str:
        value = value.lower()
        if not USERNAME_REGEX.match(value):
            raise ValueError(
                "Username must be 3–20 characters, "
                "contain only letters, numbers, and underscores, "
                "and must not start or end with an underscore."
            )
        return value
