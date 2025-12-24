from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Core
    DATABASE_URL: str
    JWT_SECRET: str

    # OpenRouter
    OPENROUTER_API_KEY: str
    OPENROUTER_MODEL: str
    OPENROUTER_BASE_URL: str

    # DigitalOcean Spaces
    DO_SPACES_KEY: str
    DO_SPACES_SECRET: str
    DO_SPACES_BUCKET: str
    DO_SPACES_REGION: str
    DO_SPACES_ENDPOINT: str

    class Config:
        env_file = ".env"

settings = Settings()
