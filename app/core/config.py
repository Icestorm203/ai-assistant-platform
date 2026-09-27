from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    weather_api_key: str
    telegram_bot_token: str
    openrouter_api_key: str
    default_llm_model: str
    
    redis_host: str = "localhost"
    redis_port: int = 6379

    api_base_url: str = "http://127.0.0.1:8000"
    telegram_proxy: str | None = None
    
    class Config:
        env_file = ".env"


settings = Settings()
