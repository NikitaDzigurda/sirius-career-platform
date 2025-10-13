"""
Конфигурация приложения
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Настройки приложения"""
    
    # Основные настройки
    app_name: str = "Sirius Career Platform"
    app_version: str = "0.1.0"
    debug: bool = False
    
    # Настройки сервера
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Настройки базы данных
    database_url: str = "mysql+pymysql://user:password@localhost:3306/sirius_career"
    database_echo: bool = False
    
    # Настройки безопасности
    # secret_key: str = "your-secret-key-change-in-production"
    # algorithm: str = "HS256"
    # access_token_expire_minutes: int = 30
    
    # Настройки OTP
    # otp_expire_minutes: int = 5
    # otp_length: int = 6
    
    # Настройки email (для будущего использования)
    # smtp_server: Optional[str] = None
    # smtp_port: Optional[int] = None
    # smtp_username: Optional[str] = None
    # smtp_password: Optional[str] = None

    # Настройки Redis (для будущего использования)
    # redis_url: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Глобальный экземпляр настроек
settings = Settings()
