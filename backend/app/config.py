from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    supabase_url: str = ""
    supabase_key: str = ""
    google_maps_api_key: str = ""
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    # San Antonio city center (fallback when no user location)
    default_lat: float = 29.4241
    default_lng: float = -98.4936
    default_radius_miles: float = 5.0

    class Config:
        env_file = ".env"


settings = Settings()
