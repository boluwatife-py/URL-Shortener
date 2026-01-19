from pydantic import BaseModel, field_validator
from core.validators import UsernameValidator, PasswordValidator


class UsernameSchema(BaseModel):
    username: str = "your_username"

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        return UsernameValidator.validate(v)


class RegisterRequest(UsernameSchema):
    password: str = "SuperSecurePassword1@"

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        return PasswordValidator.validate(v)


class LoginRequest(UsernameSchema):
    password: str



class LoginResponse(BaseModel):
    access_token: str
    username: str
    id: str
    token_type: str = "bearer"
