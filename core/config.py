from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    HOST_URL: str = "http://localhost:8000"
    HASHID_SALT: str = "your_default_salt_value"
    REDIRECT_STATUS_CODE: int = 302
    GEMINI_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings() #type: ignore