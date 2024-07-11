from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


BASE_DIR = Path()


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env',
        case_sensitive=False
    )


class W3Settings(Config):
    api_key: str
    token_address: str
    provider_url: str = 'https://polygon-rpc.com/'


class Settings(BaseSettings):
    w3: W3Settings = W3Settings()


settings = Settings()
