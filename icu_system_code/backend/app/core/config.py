from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ICU System API"
    api_prefix: str = "/api"
    frontend_origin: str = "http://localhost:3000"
    secret_key: str = "change-me"
    access_token_expire_minutes: int = 60
    database_url: str | None = None
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-2.5-flash"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
