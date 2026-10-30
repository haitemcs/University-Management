from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "University Management API"
    database_url: str = "postgresql+psycopg2://university:university@localhost:5432/university_db"
    secret_key: str = "development-only-change-me"
    access_token_expire_minutes: int = 30
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
