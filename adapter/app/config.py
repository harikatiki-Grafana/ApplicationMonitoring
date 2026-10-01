from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    teamcenter_base_url: str
    teamcenter_health_path: str = "/health"
    teamcenter_stats_path: str = "/monitoring/statistics"
    teamcenter_verify_tls: bool = True
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
settings = Settings()
