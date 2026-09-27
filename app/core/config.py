from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


    weather_api_key: str
    telegram_bot_token: str
    openrouter_api_key: str
    default_llm_model: str
    
    redis_host: str = "localhost"
    redis_port: int = 6379

    api_base_url: str = "http://127.0.0.1:8000"
    telegram_proxy: str | None = None


settings = Settings()
