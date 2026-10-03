from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Application metadata
    APP_NAME: str = "Ticketing Engine API Gateway"
    DEBUG: bool = False
    
    # Infrastructure connections
    DATABASE_URL: str
    REDIS_URL: str
    
    # Consul Service Discovery
    CONSUL_HOST: str = "localhost"
    CONSUL_PORT: int = 8500

    # Pydantic v2 configuration to load the .env file automatically
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"  # Ignores extra environment variables gracefully
    )

# Instantiate a global settings object to import across your app
settings = Settings()