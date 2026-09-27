from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    weather_api_key: str
    telegram_bot_token: str
    openrouter_api_key: str
    default_llm_model: str
    
    redis_host: str = "localhost"
    redis_port: int = 6379

    class Config:
        env_file = ".env"


settings = Settings()
