import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    bot_token: str = os.getenv("BOT_TOKEN", "")
    owner_id: int = int(os.getenv("OWNER_ID", "0"))
    main_channel: str = os.getenv("MAIN_CHANNEL", "")
    deals_channel: str = os.getenv("DEALS_CHANNEL", "")
    logs_channel: str = os.getenv("LOGS_CHANNEL", "")
    support_bot: str = os.getenv("SUPPORT_BOT", "")
    default_upi_id: str = os.getenv("DEFAULT_UPI_ID", "")
    default_upi_name: str = os.getenv("DEFAULT_UPI_NAME", "")
    database_url: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./vouchnexa.db")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
