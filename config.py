from dataclasses import dataclass
from typing import List
import os

@dataclass
class Config:
    """Configuration settings for the trading bot."""
    # API keys and credentials (loaded from environment variables for security)
    COINGECKO_API_KEY: str = os.getenv("COINGECKO_API_KEY", "your_coingecko_api_key")
    BINANCE_API_KEY: str = os.getenv("BINANCE_API_KEY", "your_binance_api_key")
    BINANCE_SECRET_KEY: str = os.getenv("BINANCE_SECRET_KEY", "your_binance_secret_key")
    TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_TOKEN", "your_telegram_bot_token")
    TELEGRAM_CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID", "your_chat_id")
    
    # Trading parameters
    ASSETS: List[str] = ["bitcoin", "ethereum", "litecoin"]
    VS_CURRENCY: str = "usd"
    INITIAL_CAPITAL: float = 10000.0
    TRADE_INTERVAL: int = 3600  # Seconds (1 hour)
    
    # Database and cloud settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///trading_bot.db")
    AWS_ACCESS_KEY: str = os.getenv("AWS_ACCESS_KEY", "your_aws_access_key")
    AWS_SECRET_KEY: str = os.getenv("AWS_SECRET_KEY", "your_aws_secret_key")
    S3_BUCKET: str = "trading-bot-data"