from pydantic import BaseSettings, AnyHttpUrl

class Settings(BaseSettings):
    data_service_base_url: AnyHttpUrl = "http://localhost:8001"
    poll_interval_seconds: int = 60  # 1-minute bars

settings = Settings()