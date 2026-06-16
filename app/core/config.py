from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "GLF API"
    debug: bool = False

    database_url: str
    secret_key: str

    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    SUPABASE_URL: str
    SUPABASE_SERVICE_ROLE_KEY: str
    SUPABASE_BUCKET: str = "GLF-images"
    RESEND_API_KEY: str
    CONTACT_RECEIVER_EMAILS: str = ""


settings = Settings()
