#==================== Add Library And Package ====================
from pydantic_settings import BaseSettings, SettingsConfigDict


#==================== Settings ====================
class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL : str
    JWT_SECRET_KEY : str
    JWT_ALGORITHM : str

    model_config = SettingsConfigDict(env_file=".env")
    
settings = Settings()